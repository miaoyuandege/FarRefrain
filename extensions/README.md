# Optional extensions

Capabilities are not workflow policy. Extensions never independently promote content into Current Truth. Core and Default Workflow both work without them. Status describes this public distribution, not private operational readiness.

| Family | Module / seam | Public status |
| --- | --- | --- |
| Local Files | File-bridge read capability | INTERNAL_ONLY; no public package or write support |
| Transport | [Router](router/README.md) | SHIPPED; standalone local file transport |
| Runtime | Registered task/run facts | INTERNAL_ONLY; no database distributed |
| Observer | Git / system / runtime observation | INTERNAL_ONLY; no public integration acceptance claimed |
| Remote Entry | Bot or app access | INTERNAL_ONLY; no accounts/configuration bundled |
| Automation | Background orchestration / workflow engines | DEFERRED; not installed or enabled |

SHIPPED means code, configuration example, instructions and tests exist here; it is not a final-release certification. EXPERIMENTAL and PLANNED are reserved for actual candidate work, not promises of implementation. The existing [offline history distiller](../tools/history-distiller/README.md) remains an optional developer utility, not a shipped Observer service.

Prefer native Agent Skills for workflow, MCP/apps for capability seams, and established telemetry/automation ecosystems when a real integration is authorized. No universal manifest, registry, marketplace or custom tool protocol is introduced.
