# Default Workflow (optional, recommended)

One opinionated workflow layered on the [Core contract](../../core/MEMORY_CONTRACT.md): Main AI → Research / Reuse Gate → Task artifact → Execution AI → Verification → Report → Main AI Acceptance → focused Rework if needed → Stage Close when appropriate.

The single policy authority is [WORKFLOW.md](references/WORKFLOW.md). The native [SKILL.md](SKILL.md) is a thin execution entry; six [templates](templates/task.md) support Task, Report and four Stage Sources. Optional [main-AI instructions](references/main-ai.md) and [guardrails](references/guardrails.md) route back to it, not duplicate it.

Use manual file handoff; no Router, database or background component is needed. A custom workflow can use Core without adopting these roles or stages. No second workflow implementation is claimed.

For installation use [START_HERE](../../START_HERE.md). Copy this folder's SKILL.md, references and templates to `.agents/skills/default`, and the Core contract alone to `.agents/core/MEMORY_CONTRACT.md`; the same relative Core links resolve both in the repository and in the installation. Do not copy SKILL.md alone or overwrite an existing same-name Skill. Installation does not save ChatGPT account settings or prove client discovery.
