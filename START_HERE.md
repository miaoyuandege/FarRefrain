# Install with AI

MIT LICENSED public pre-release, not v0.1 final. Tell your AI: “Help me use this in my project.” Recommended: **Core + Default Workflow**. Supply a goal and allowed location; no protocol homework is required.

## A. Inspect

Install FarRefrain as a project continuity layer. Read [Core](core/README.md), [Workflow](workflows/default/README.md) and the existing project's overview/stage. Confirm target, permissions and layout. Preserve unrelated files. Check for same-name `default` or old `mindos` Skills before copying. Do not assume client/login/account or Runtime.

## B. Install — three choices

1. **Core only:** copy the [files-only example](examples/kernel-only/README.md) into a new authorized directory or map its semantics onto existing files. Read the [contract](core/MEMORY_CONTRACT.md). No Skill, Python, Task or Router is needed. Replace synthetic identity/facts with user-confirmed ones for a real project.
2. **Recommended: Core + Default Workflow:** place `core/MEMORY_CONTRACT.md` at `<project>/.agents/core/MEMORY_CONTRACT.md`; copy `SKILL.md`, `references/` and `templates/` from `workflows/default` into `<project>/.agents/skills/default`. Keep references/templates together; never copy SKILL.md alone. The package README is repository navigation, not an installed Skill resource. If either target exists, stop and review/merge deliberately. This placement preserves the Skill's `../../core` link. Link the installed contract and workflow from the overview.
3. **Optional Router:** after choice 2 works, follow [Router setup](extensions/router/README.md) with a new generic config and reviewed targets. No automatic service or background installation. Removing Router does not remove memory.

These are local copy instructions, not authorization for network/account changes. Review cloning/downloading separately. Confirm `default` points to the project installation in your client's Skill listing; file existence is not discovery. See [platform evidence](docs/PLATFORM.md).

## C. Place your first input

Files only: read overview/current, make one authorized factual update, preserve its predecessor in history with provenance, and recover in fresh context.

Default Workflow: say “接管这个项目” / “Take over this project”, then choose a scoped change with the Main AI. It resolves the Research / Reuse Gate and creates a [Task](workflows/default/templates/task.md). Place it manually in the mapped inbox, select `$default` in the execution client and say “执行任务”. The [synthetic lifecycle](examples/default-workflow/README.md) shows artifact roles, not a completed human test.

## D. Verify

Check copied Core/Workflow hashes and relative links, stable project identity and current/planning distinction. Inspect actual client discovery. For Workflow inspect changed files, real verification, one report and unchanged Source preservation. Main AI Acceptance remains independent. [Automated smoke](docs/VERIFY.md) is not authenticated end-to-end or external human first-use.

## E. Tell the user

Report installed paths, checks and missing client/permission/acceptance evidence. Never claim account settings were saved; [main-AI instructions](workflows/default/references/main-ai.md) are optional and saved separately by the user. With no further action after acceptance, omit redundant “tell Codex to stop” replies; when action remains give one self-contained instruction.
