# Default memory layout

Use this mapping for a new project, or preserve a project's established mapping.

```text
project-overview.md              stable identity, purpose, path map
project-current-stage.md         current position and unresolved decisions
current-memory/core/            adopted durable constraints
current-memory/general/         current working facts
current-memory/planning/        currently relevant intentions, not adopted truth
inbox/                         unprocessed sources, not authoritative state
handoffs/                      processed sources and their provenance
history/                       superseded knowledge
```

Create directories when there is content to store, not as empty scaffolding. Root boot entries remain small; map each role to its real location. See the [kernel-only example](../../../examples/kernel-only/README.md) for populated files and [contract](../../MEMORY_CONTRACT.md) for semantics. No particular language or directory name is mandatory; legacy layouts remain valid when their overview maps these roles.
