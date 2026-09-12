# Truth model v1

Plain files remain authority. Current is a maintained working projection from Evidence/History, not an append-only log. This contract adds optional explicit semantics to the [memory contract](MEMORY_CONTRACT.md); it does not require a workflow, model, service or migration.

## Status is separate from type

CAPTURED: a source/observation exists, without Current authority. PROPOSED: a relevant candidate, not truth. ADOPTED: relied-on truth within its stated scope. CONTESTED: unresolved real conflict; do not silently select a side. SUPERSEDED: previously current, now replaced; preserve history. OBSERVED: evidence-backed retrospective discovery, not implicit adoption.

Lifecycle: CAPTURED → PROPOSED → ADOPTED → CONTESTED or SUPERSEDED. OBSERVED may become PROPOSED; resolving CONTESTED into ADOPTED requires a new explicit decision. Types are FACT, DECISION, CONSTRAINT, GOTCHA, FAILURE. A historical failure does not authorize repeating a destructive operation.

Promotion requires existing evidence, clear scope, no unresolved equal/higher-authority conflict and the authorization required by the selected workflow/user. Automated capture/distillation cannot adopt. Replacing A with B preserves A as SUPERSEDED history and makes B ADOPTED with a reference to A where practical. Do not make history appear as though B always applied.

## Optional metadata

For example, at the start of an ordinary Markdown file:

```text
---
{"truth_status":"ADOPTED","knowledge_type":"CONSTRAINT","scope":["global"],"primary":true,"evidence":["../../history/decision.md"]}
---
# Current constraint
The scoped adopted statement goes here.
```

JSON front matter is used by the optional stdlib helper for inspectability without a YAML dependency. Evidence/supersedes references are relative to the record file. `primary` selects a small boot-relevant adopted record; it does not promote it. Metadata is optional: without it, explicitly mapped current/planning/history roles still mean adopted/proposed/historical. Missing or invalid explicit metadata fails closed; it never falls back into adoption. Unknown fields fail rather than being silently ignored.

Retrospective OBSERVED metadata needs evidence and remains labeled observed. A CONTESTED record retains competing claims and their provenance; projection does not resolve it. No bulk legacy migration is required. The optional helper accepts a caller's explicit file map; that map is not a new central registry or universal manifest. Human review still owns authority and decisions.
