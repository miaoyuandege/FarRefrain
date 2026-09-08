# Pre-v0.1 modular migration

This public pre-release is not a stable API or v0.1 final. Git history retains the old layout.

| Previous entry | Canonical home |
| --- | --- |
| core/MindOS.md | [Default Workflow policy](../workflows/default/references/WORKFLOW.md); old entry is a pointer |
| core/templates | [Workflow templates](../workflows/default/templates/task.md) |
| codex/skill | [Workflow Skill](../workflows/default/SKILL.md) |
| chatgpt/custom-instructions | [Main-AI instructions](../workflows/default/references/main-ai.md) |
| codex/profiles | [Guardrails](../workflows/default/references/guardrails.md) |
| presets | [Three adoption choices](../START_HERE.md) |

Core now has its own [contract](../core/MEMORY_CONTRACT.md) and [layout](../core/layouts/default/README.md). Router is a standalone [extension](../extensions/router/README.md). External-first-use fixtures remain synthetic legacy-layout examples, not a second default.

Inspect existing overview/customizations first. Preserve project identity/current/history; deliberately merge an installation with authorization. Do not overwrite same-name Skills or silently migrate projects. New installs preserve the Core/Workflow relative-link geometry in START_HERE. Old single-file Skill copying is no longer supported.
