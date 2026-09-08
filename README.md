![FarRefrain — durable context for AI collaboration](assets/farrefrain-hero.svg)

# FarRefrain

A project continuity substrate for AI-native work.

Your agents can change. Your workflows can change. Your tools can change. Keep one recoverable project continuity layer: a Local Memory Core, replaceable workflows and optional native capabilities.

*The singer changes. The refrain continues.*

**You can start with files only.** New chats lose context; local boot entries, current knowledge and provenance make it recoverable. Move context out of the chat. Keep thinking in the conversation.

```text
Local Memory Core
        ↓
Default / Custom Workflows
        ↓
Optional Extensions
```

PUBLIC PRE-RELEASE TEST · MIT LICENSED · NOT v0.1 FINAL. See [LICENSE](LICENSE). External Human First-use = NOT RUN. Synthetic tests do not establish user acceptance.

## Install with AI

Give your AI this repository and [Install with AI](START_HERE.md). Recommended: **Core + Default Workflow**. It should inspect your existing project, preserve its conventions, install only what you choose and verify the links.

| Choice | Start here | Included |
| --- | --- | --- |
| A. Core only | [Files-only example](examples/kernel-only/README.md) | Identity, boot/current/history and authorized updates |
| B. Core + Default Workflow (recommended) | [Default Workflow](workflows/default/README.md) | Native Skill, research, Task/Report, verification and acceptance |
| C. B + Router | [Router extension](extensions/router/README.md) | Optional local transport, no automatic execution |

## A 30-second example

Before: “The old chat knew why this limit exists.”

With FarRefrain: read the overview, adopted limit and decision reference, see the pending alternative separately, then continue authorized work. This is an illustration, not a measured speed or success guarantee.

## Understand the model

[Why FarRefrain](docs/WHY_FARREFRAIN.md) · [Workspace architecture](docs/WORKSPACE_ARCHITECTURE.md) · [Walkthrough](docs/WALKTHROUGH.md) · [Principles](docs/PRINCIPLES.md)

## Start small

Core is the [memory contract](core/MEMORY_CONTRACT.md), not the author's full workflow. The [default layout](core/layouts/default/README.md) maps it to plain files. Planning means currently relevant intention, not adopted truth.

The retained artwork below illustrates the optional **Default Workflow**, not a Core requirement:

![Default Workflow collaboration loop](assets/farrefrain-workflow.svg)

Try the [synthetic lifecycle](examples/default-workflow/README.md). Replace its workflow while keeping identity/discoverability/provenance intact. No second workflow implementation is claimed. The [catalog](extensions/README.md) distinguishes shipped Router code from internal-only/deferred integrations. The [history distiller](tools/history-distiller/README.md) remains an optional offline utility, not an Observer service.

## Compatibility and evidence

One unchanged Skill (explicit use; native discovery not proven), a reference MCP server and an ordinary CLI have been exercised with removable synthetic installs. See [native ecosystem evidence and limits](docs/ECOSYSTEM_INTEROP.md).

Pre-v0.1 restructuring moved protocol, templates and client entries under `workflows/default`. Old entries are thin pointers, not parallel authorities. See [migration notes](docs/MIGRATION.md).

[Verification](docs/VERIFY.md) · [Release readiness](docs/RELEASE_READINESS.md) · [Platform](docs/PLATFORM.md) · [Inventory](docs/INVENTORY.md) · [Provenance](docs/SOURCE_MAP.md) · [Security](SECURITY.md) · [Contributing](CONTRIBUTING.md)
