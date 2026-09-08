# Pre-v0.1 modular migration

## Public brand continuity

FarRefrain was previously published as MindOS. This is a brand rename, not a project reset, architecture change or v0.1 final release. Git history and historical Task/Report/Evidence names remain truthful.

The canonical repository is [miaoyuandege/FarRefrain](https://github.com/miaoyuandege/FarRefrain). GitHub repository rename redirects the [old repository URL](https://github.com/miaoyuandege/MindOS); do not recreate a repository at the old name. Existing clones should update origin to the new canonical URL. Hosted Actions and project Pages need separate review when present; neither was configured for this rename.

Current visuals use `farrefrain-*`; [Why FarRefrain](WHY_FARREFRAIN.md) is canonical and the old Why page is a thin compatibility pointer. `core/MindOS.md` remains a pointer, not a new brand-named authority. The native Workflow identity stays `default`.

Legacy machine identifiers are deliberately retained: `mindos-public-assets@1` (asset manifest schema), `mindos_inbox_router` (logger), `mindos_local_probe` (diagnostic client identity) and `MINDOS-...` (historical Task ID grammar). They are not public branding; consumers must not infer a new schema or new Task history from a brand change. Existing internal `project_key = mindos`, Route `MindOS`, authority filenames and physical roots also remain unchanged; adopters keep their own stable project identities.

Rollback is a reviewed revert commit plus an authorized rename of the same repository and origin update, not deletion/recreation or history rewriting. It requires checking namespace availability and redirect consequences again.

## Earlier modular layout migration

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
