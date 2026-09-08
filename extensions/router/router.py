#!/usr/bin/env python3
"""Deterministic, local-only optional file transport."""

from __future__ import annotations

import argparse
from datetime import datetime, timezone
import json
import logging
from logging.handlers import RotatingFileHandler
import os
from pathlib import Path
import re
import signal
import sys
import threading
import time
from dataclasses import dataclass
from typing import Any, Callable


ROUTE_PATTERN = re.compile(r"^([^\r\n]+?)__(.+)$")
LEGACY_ROUTE_PATTERN = re.compile(r"^\[([^\[\]\r\n]+)\](.+)$")
TEMP_DOWNLOAD_SUFFIXES = {".crdownload", ".part", ".tmp"}


class ConfigError(ValueError):
    """Raised when router configuration is invalid or unsafe."""


@dataclass(frozen=True)
class RouterConfig:
    source: Path
    poll_interval_seconds: float
    stability_scans: int
    routes: dict[str, Path]
    log_file: Path
    max_log_bytes: int
    log_backup_count: int
    route_event_spool: Path | None


@dataclass(frozen=True)
class RouteResult:
    """Transport-only facts emitted after one successful atomic rename."""

    event_id: str
    route_name: str
    original_source_name: str
    requested_target_name: str
    actual_target_path: str
    collision_renamed: bool
    routed_at: str
    target_size: int
    target_mtime_ns: int

    def to_dict(self) -> dict[str, Any]:
        return vars(self).copy()


@dataclass(frozen=True)
class ParsedRoute:
    """A filename route resolved without inspecting file content."""

    route_name: str
    target_name: str
    syntax: str


class FileRouteEventSink:
    """Atomically persists route facts; it never reads routed file content."""

    def __init__(self, spool: Path):
        self.spool = spool.resolve()
        self.spool.mkdir(parents=True, exist_ok=True)

    def __call__(self, result: RouteResult) -> None:
        target = self.spool / f"{result.event_id}.json"
        temporary = self.spool / f".{result.event_id}.{os.getpid()}.tmp"
        payload = json.dumps(
            result.to_dict(), ensure_ascii=False, separators=(",", ":")
        ) + "\n"
        try:
            temporary.write_text(payload, encoding="utf-8")
            os.replace(temporary, target)
        finally:
            try:
                temporary.unlink()
            except FileNotFoundError:
                pass


def _absolute_directory(value: Any, field: str, base: Path) -> Path:
    if not isinstance(value, str) or not value.strip():
        raise ConfigError(f"{field} must be a non-empty path")
    path = Path(value)
    if not path.is_absolute():
        path = base / path
    try:
        resolved = path.resolve(strict=True)
    except OSError as exc:
        raise ConfigError(f"{field} cannot be resolved: {exc}") from exc
    if not resolved.is_dir():
        raise ConfigError(f"{field} must be an existing directory")
    return resolved


def load_config(config_path: Path) -> RouterConfig:
    config_path = config_path.resolve(strict=True)
    try:
        raw = json.loads(config_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise ConfigError(f"cannot load config: {exc}") from exc
    if not isinstance(raw, dict):
        raise ConfigError("config must be a JSON object")

    source = _absolute_directory(raw.get("source"), "source", config_path.parent)

    interval = float(raw.get("poll_interval_seconds", 2))
    if interval <= 0:
        raise ConfigError("poll_interval_seconds must be greater than zero")

    stability_scans = int(raw.get("stability_scans", 2))
    if stability_scans < 2:
        raise ConfigError("stability_scans must be at least 2")

    raw_routes = raw.get("routes")
    if not isinstance(raw_routes, dict) or not raw_routes:
        raise ConfigError("routes must be a non-empty object")
    routes: dict[str, Path] = {}
    for project, target in raw_routes.items():
        if not isinstance(project, str) or not project.strip():
            raise ConfigError("route names must be non-empty strings")
        if project != project.strip() or any(character in project for character in "[]\r\n"):
            raise ConfigError(f"invalid route name: {project!r}")
        routes[project] = _absolute_directory(target, f"routes[{project!r}]", config_path.parent)
        if routes[project] == source:
            raise ConfigError("source and target must differ")

    log_value = raw.get("log_file", "logs/inbox-router.log")
    if not isinstance(log_value, str) or not log_value.strip():
        raise ConfigError("log_file must be a non-empty path")
    log_file = Path(log_value)
    if not log_file.is_absolute():
        log_file = config_path.parent / log_file
    log_file = log_file.resolve(strict=False)

    max_log_bytes = int(raw.get("max_log_bytes", 1_048_576))
    log_backup_count = int(raw.get("log_backup_count", 2))
    if max_log_bytes < 1_024:
        raise ConfigError("max_log_bytes must be at least 1024")
    if not 0 <= log_backup_count <= 10:
        raise ConfigError("log_backup_count must be between 0 and 10")

    event_spool_value = raw.get("route_event_spool")
    route_event_spool = None
    if event_spool_value is not None:
        if not isinstance(event_spool_value, str) or not event_spool_value.strip():
            raise ConfigError("route_event_spool must be a non-empty path")
        route_event_spool = Path(event_spool_value)
        if not route_event_spool.is_absolute():
            route_event_spool = config_path.parent / route_event_spool
        route_event_spool = route_event_spool.resolve(strict=False)

    return RouterConfig(
        source=source,
        poll_interval_seconds=interval,
        stability_scans=stability_scans,
        routes=routes,
        log_file=log_file,
        max_log_bytes=max_log_bytes,
        log_backup_count=log_backup_count,
        route_event_spool=route_event_spool,
    )


def build_logger(config: RouterConfig) -> logging.Logger:
    config.log_file.parent.mkdir(parents=True, exist_ok=True)
    logger = logging.getLogger(f"mindos_inbox_router.{id(config)}.{time.time_ns()}")
    logger.setLevel(logging.INFO)
    logger.propagate = False
    formatter = logging.Formatter("%(asctime)s %(message)s", "%Y-%m-%dT%H:%M:%S%z")

    file_handler = RotatingFileHandler(
        config.log_file,
        maxBytes=config.max_log_bytes,
        backupCount=config.log_backup_count,
        encoding="utf-8",
    )
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)
    return logger


def _event(logger: logging.Logger, event: str, **fields: Any) -> None:
    payload = {"event": event, **fields}
    message = json.dumps(payload, ensure_ascii=False, separators=(",", ":"))
    if event == "ERROR":
        logger.error(message)
    elif event in {"UNKNOWN_PROJECT", "ALIAS_COLLISION"}:
        logger.warning(message)
    else:
        logger.info(message)


def _candidate_path(target_directory: Path, filename: str, index: int) -> Path:
    direct = target_directory / filename
    if index == 0:
        return direct
    suffixes = "".join(direct.suffixes)
    stem = direct.name[:-len(suffixes)] if suffixes else direct.name
    return target_directory / f"{stem}__{index:03d}{suffixes}"


def move_exclusive(source: Path, target: Path, *, platform: str = os.name) -> None:
    """POSIX rename would overwrite a race winner; publish without replacement."""
    if platform == "nt":
        source.rename(target)
    else:
        os.link(source, target)
        source.unlink()


class InboxRouter:
    def __init__(
        self,
        config: RouterConfig,
        logger: logging.Logger | None = None,
        event_sink: Callable[[RouteResult], None] | None = None,
    ):
        self.config = config
        self.logger = logger or build_logger(config)
        self.event_sink = event_sink or (
            FileRouteEventSink(config.route_event_spool)
            if config.route_event_spool is not None
            else None
        )
        self._observed: dict[Path, tuple[tuple[int, int], int]] = {}
        self._reported: set[tuple[str, Path]] = set()
        self._route_names = sorted(
            config.routes,
            key=lambda name: (-len(name), name.casefold()),
        )

    def close(self) -> None:
        handlers = list(self.logger.handlers)
        for handler in handlers:
            handler.flush()
            handler.close()
            self.logger.removeHandler(handler)

    def _report_once(self, event: str, path: Path, **fields: Any) -> None:
        key = (event, path)
        if key in self._reported:
            return
        self._reported.add(key)
        _event(self.logger, event, source=path.name, **fields)

    def _move_without_overwrite(
        self, source: Path, project: str, target_directory: Path, filename: str
    ) -> None:
        for index in range(10_000):
            candidate = _candidate_path(target_directory, filename, index)
            if os.path.lexists(candidate):
                continue
            try:
                move_exclusive(source, candidate)
            except FileExistsError:
                continue
            except OSError as exc:
                self._report_once("ERROR", source, error=str(exc))
                return

            if index:
                _event(
                    self.logger,
                    "COLLISION_RENAMED",
                    source=source.name,
                    project=project,
                    target=candidate.name,
                )
            _event(
                self.logger,
                "ROUTED",
                source=source.name,
                project=project,
                target=candidate.name,
            )
            stat = candidate.stat(follow_symlinks=False)
            result = RouteResult(
                event_id=f"route-event-{time.time_ns()}-{os.getpid()}",
                route_name=project,
                original_source_name=source.name,
                requested_target_name=filename,
                actual_target_path=str(candidate.resolve()),
                collision_renamed=bool(index),
                routed_at=datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
                target_size=stat.st_size,
                target_mtime_ns=stat.st_mtime_ns,
            )
            if self.event_sink is not None:
                try:
                    self.event_sink(result)
                except Exception as exc:
                    _event(
                        self.logger,
                        "EVENT_PERSIST_FAILED",
                        event_id=result.event_id,
                        project=project,
                        target=candidate.name,
                        error=f"{type(exc).__name__}: {exc}",
                    )
            self._observed.pop(source, None)
            return
        self._report_once("ERROR", source, error="collision limit exhausted")

    def _parse_route(self, filename: str) -> ParsedRoute | None:
        # Configured canonical routes win even when route names contain underscores.
        for route_name in self._route_names:
            prefix = f"{route_name}__"
            if filename.startswith(prefix):
                return ParsedRoute(route_name, filename[len(prefix):], "canonical")

        # The single-underscore compatibility form is recognized only from the
        # exact configured route set; ordinary filenames are never guessed.
        for route_name in self._route_names:
            prefix = f"{route_name}_"
            if filename.startswith(prefix):
                return ParsedRoute(route_name, filename[len(prefix):], "compatibility")

        # Preserve the established warning for unknown canonical RouteName__ files.
        # This follows configured prefixes so an alias target may itself contain __.
        canonical = ROUTE_PATTERN.fullmatch(filename)
        if canonical is not None:
            route_name, target_name = canonical.groups()
            return ParsedRoute(route_name, target_name, "canonical")

        legacy = LEGACY_ROUTE_PATTERN.fullmatch(filename)
        if legacy is not None:
            route_name, target_name = legacy.groups()
            return ParsedRoute(route_name, target_name, "legacy")
        return None

    def _consider_file(self, path: Path, parsed: ParsedRoute | None = None) -> None:
        if path.suffix.casefold() in TEMP_DOWNLOAD_SUFFIXES:
            self._observed.pop(path, None)
            return

        parsed = parsed or self._parse_route(path.name)
        if parsed is None:
            self._observed.pop(path, None)
            return
        project, target_name = parsed.route_name, parsed.target_name
        if target_name in {"", ".", ".."}:
            self._observed.pop(path, None)
            return

        target_directory = self.config.routes.get(project)
        if target_directory is None:
            self._observed.pop(path, None)
            self._report_once("UNKNOWN_PROJECT", path, project=project)
            return
        if not target_directory.is_dir():
            self._observed.pop(path, None)
            self._report_once("ERROR", path, error="configured target directory is unavailable")
            return

        stat = path.stat(follow_symlinks=False)
        signature = (stat.st_size, stat.st_mtime_ns)
        previous = self._observed.get(path)
        stable_count = previous[1] + 1 if previous and previous[0] == signature else 1
        self._observed[path] = (signature, stable_count)
        if stable_count < self.config.stability_scans:
            return

        self._move_without_overwrite(path, project, target_directory, target_name)

    def scan_once(self) -> None:
        current_files: set[Path] = set()
        try:
            entries = sorted(os.scandir(self.config.source), key=lambda item: item.name.casefold())
        except OSError as exc:
            self._report_once("ERROR", self.config.source, error=f"source scan failed: {exc}")
            return

        candidates: list[tuple[Path, ParsedRoute | None]] = []
        alias_groups: dict[tuple[str, str], dict[str, list[Path]]] = {}
        for entry in entries:
            try:
                if not entry.is_file(follow_symlinks=False):
                    continue
                path = Path(entry.path)
                current_files.add(path)
                parsed = (
                    None
                    if path.suffix.casefold() in TEMP_DOWNLOAD_SUFFIXES
                    else self._parse_route(path.name)
                )
                candidates.append((path, parsed))
                if (
                    parsed is not None
                    and parsed.route_name in self.config.routes
                    and parsed.syntax in {"canonical", "compatibility"}
                ):
                    key = (parsed.route_name, parsed.target_name)
                    aliases = alias_groups.setdefault(key, {})
                    aliases.setdefault(parsed.syntax, []).append(path)
            except OSError as exc:
                path = Path(entry.path)
                self._report_once("ERROR", path, error=str(exc))

        blocked: set[Path] = set()
        for (route_name, target_name), aliases in alias_groups.items():
            if "canonical" not in aliases or "compatibility" not in aliases:
                continue
            paths = sorted(
                aliases["canonical"] + aliases["compatibility"],
                key=lambda path: path.name.casefold(),
            )
            blocked.update(paths)
            for path in paths:
                self._observed.pop(path, None)
            self._report_once(
                "ALIAS_COLLISION",
                paths[0],
                project=route_name,
                target=target_name,
                aliases=[path.name for path in paths],
            )

        for path, parsed in candidates:
            if path in blocked:
                continue
            try:
                self._consider_file(path, parsed)
            except OSError as exc:
                self._report_once("ERROR", path, error=str(exc))

        self._observed = {
            path: state for path, state in self._observed.items() if path in current_files
        }
        self._reported = {
            item for item in self._reported
            if item[1] == self.config.source or item[1] in current_files
        }

    def run(self, stop_event: threading.Event, max_scans: int | None = None) -> None:
        _event(
            self.logger,
            "START",
            source=str(self.config.source),
            poll_interval_seconds=self.config.poll_interval_seconds,
            routes=len(self.config.routes),
        )
        scans = 0
        try:
            while not stop_event.is_set():
                self.scan_once()
                scans += 1
                if max_scans is not None and scans >= max_scans:
                    break
                stop_event.wait(self.config.poll_interval_seconds)
        finally:
            _event(self.logger, "STOP")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Deterministic FarRefrain inbox file router")
    parser.add_argument(
        "--config",
        type=Path,
        default=Path(__file__).with_name("config.json"),
        help="Path to config.json",
    )
    parser.add_argument(
        "--check-config",
        action="store_true",
        help="Validate configuration and exit without scanning",
    )
    parser.add_argument(
        "--max-scans",
        type=int,
        help="Stop after this many scans; intended for verification",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    try:
        config = load_config(args.config)
        if args.max_scans is not None and args.max_scans < 1:
            raise ConfigError("max_scans must be at least 1")
        if args.check_config:
            print(json.dumps({
                "status": "PASS",
                "source": str(config.source),
                "poll_interval_seconds": config.poll_interval_seconds,
                "stability_scans": config.stability_scans,
                "routes": len(config.routes),
                "route_event_spool": (
                    str(config.route_event_spool)
                    if config.route_event_spool is not None
                    else None
                ),
            }, ensure_ascii=False))
            return 0

        stop_event = threading.Event()

        def request_stop(_signum: int, _frame: Any) -> None:
            stop_event.set()

        signal.signal(signal.SIGINT, request_stop)
        if hasattr(signal, "SIGTERM"):
            signal.signal(signal.SIGTERM, request_stop)

        router = InboxRouter(config)
        try:
            router.run(stop_event, max_scans=args.max_scans)
        finally:
            router.close()
        return 0
    except ConfigError as exc:
        sys.stderr.write(f"Router configuration error: {exc}\n")
        return 2
    except Exception as exc:
        sys.stderr.write(f"Router failed: {exc}\n")
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
