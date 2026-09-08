# Default Workflow — canonical policy

This optional policy sits above the independent [Core contract](../../../core/MEMORY_CONTRACT.md). It does not replace an existing project's accepted authority or authorize new actions. Default Layout maps semantic roles to lowercase English paths; existing layouts remain valid.

## Roles and facts

- User: goals, values, final decisions and high-risk authorization.
- Main AI: understanding, direction, mature Task contracts, acceptance, Rework and stage meaning.
- Execution AI: scoped implementation, knowledge governance, verification and a single report.
- Programs: deterministic transport, hashing, tests and optional registered runtime facts.

Agent says done ≠ Task completed. Report exists ≠ sufficient verification. Technical PASS ≠ Main AI Acceptance. Inbox files do not own Runtime state.

Use the latest explicit user decision, shared protocol and project Core/Current for their respective fact domains. A configured Runtime owns registered Task/Run/Result facts; Markdown preserves contracts and evidence. Never invent a Runtime, migrate a database, or call another project's same-numbered task equivalent.

## Project and context

Existing project layouts take priority. A new layout can use project overview, current stage, Inbox, Core, Current, Planning, History and Handoffs (original Task/knowledge sources and reports). Record actual paths in the project's own overview; do not restructure a project merely to fit these names.

When a user says “take over”, “continue this project” or “the previous conversation filled up”, locate the project and read its protocol, directory map, overview/stage, relevant Core/Current/Planning, recent evidence and necessary Runtime/Inbox. Main AI also reads relevant collaboration context and internal resource indexes when needed. Build the minimum credible context and act within scope; ask only for missing information that changes a decision. Do not claim inaccessible files were read.

An execution context stays narrower: protocol → overview/stage → necessary Runtime → current Task / necessary Report and Inbox. It does not redo product strategy. A new window/model/restart is not Invalidation Evidence and does not invalidate prior authorization by itself.

## Worklist

For the execution window, the exact whole-message triggers are `'`, `’`, `‘’`, or `执行任务`. Only the current project is in scope.

Priority: actionable registered Runtime Task → Ready Dispatch → Inbox knowledge/planning → formal Task/Rework. If no Runtime is configured, use manual mode without inventing state. A task-local block does not freeze independent authorized work; an authority/permission/workspace block freezes the affected scope.

Read and govern relevant knowledge before tasks. Preserve original source unchanged in Handoffs after successful governance. For Task attempts: inspect identity/scope/permission, execute, verify, write one `<TaskID>_报告单.md`, preserve evidence, then move the original Task to Handoffs without overwriting. A partial attempt is not completion; preserve its pending work and continue only independent tasks. Do not mutate external queues or other project inboxes.

Rescan after each item. Current work is not preempted by a new file. Earlier base Task identity precedes later tasks; within an identity use initial then ordered Reworks. Stop when there is no actionable work or a real scope-wide block. No implicit daemon, worker or watcher.

## Tasks and delivery

A Task is one independently implementable and verifiable delta, not one file and not an entire unrelated roadmap. Use the [Task template](../templates/task.md) and [Report template](../templates/report.md); omit empty optional sections.

### Research / Reuse Gate

Before issuing every mature Task, the main AI resolves the existing research-first/reuse-first gate. Check project and shared resources first, classify `Research Value` and `External Research`, and research official/primary/high-quality sources when the result can change scope, compatibility, risk or acceptance. `NOT NEEDED` is valid for direct-evidence fixes or mechanical work, with a short reason; this is not a mechanical web-search requirement. Distill only implementation-relevant conclusions as adopt/borrow/thin-adapt/reject/defer. Execution AI does not repeat broad research and performs only an explicitly scoped freshness check. No mature Task is issued while the gate is unresolved.

When the main AI has enough context and authorization and the user says “issue a task / 下任务”, produce a downloadable `RouteName__<TaskID>_任务单.md` when file artifacts are supported. Use only an explicitly configured, known Route. If files are unavailable, disclose that and provide copyable text. Artifact created ≠ downloaded ≠ transported ≠ executed. An optional existing Router may remove the Route prefix after transport; Router is separately shipped as an optional extension, never implicitly enabled. Without it, the user places the reviewed source into the known project workflow.

Manual Tasks use `manual_inbox / not_registered`: source + implementation + verification + single report + unchanged source preservation + explicit acceptance. Do not mark them Runtime completed. Main AI progress checks distinguish Manual, Registered Runtime, server and document evidence; absent observers are a limitation, not invented connectivity.

Without configured transport, issue `<TaskID>_任务单.md` directly and place it manually in the mapped inbox; no Route prefix or Router is required. English artifact names are equally valid when the project maps them consistently, as the synthetic example demonstrates.

## Risk-matched verification

### Main AI return to Execution AI

On receiving execution results, state the conclusion and next step. **If Codex still needs action**, provide a copy-ready self-contained reply: project, exact Task ID, Technical Result, Main AI Acceptance, accepted/frozen scope not to redo, requested action, authority and permission delta. This applies to Rework, same-Task continuation, blocker recovery, scope changes and necessary governance writeback.

**If ACCEPTED / CLOSED and no further Codex action remains, do not generate a redundant reply telling Codex to stop.** Acceptance does not mean a required writeback is done; specify that action if needed. A new Task artifact is its execution input, not a duplicate task body. Technical PASS never grants Main AI Acceptance. An explicit Task instruction to stop takes precedence over rescan.

Default baseline_reuse / delta_review; no repeated Full Review without direct Invalidation Evidence. Read current Task, changed files and targeted evidence before widening scope.

- FAST: local delta and directly affected contracts, not release certification.
- REGRESSION: cumulative accepted changes or stage-level risk.
- FREEZE: exact release candidate identity and source → verification → build → artifact → deploy → smoke chain when relevant.
- AUTO-BY-RISK: choose the minimum sufficient mode for the actual change.

Distinguish changed source, changed staging, changed verifier and generated output. Verifier RED is not automatically a product bug; retain the failed evidence and repair the correct layer. No untested PASS, erased failures or substitution of automated success for required human acceptance.

## Lifecycle and progressive explanation

Operational complexity belongs to the AI, not the user. These are evidence-based working judgments, not another state database:

| Situation | Main AI behavior |
| --- | --- |
| New Project | Establish goal, map and minimum credible intake |
| Existing Project / Fresh Context | Restore from official files and accepted baseline |
| Active Stage | Advance authorized work and consult useful existing resources |
| Task Executing | Observe real evidence; do not preempt or assume completion |
| Stage Converging | Explain why stage goals, major deltas and remaining blockers suggest closing |
| Stage Close | Follow formal source/verification/acceptance boundaries |
| Post-Stage Delta | Preserve accepted baseline and track the new change |
| Fresh Context Recommended | Confirm handoff files exist, then suggest a new conversation with a minimal entry |

Suggest Stage Close when the stage's core goal/major deltas are complete or explicitly externally blocked, remaining work belongs to another stage, accumulated accepted deltas merit regression, or history/context overhead outweighs incremental work. Do not trigger by task count or nag after every few tasks.

Main AI stage distillation and relevant profile candidates precede a formal Stage Close Task. Execution then produces implementation distillation and execution observations, governs sources/current/planning/history, verifies and reports. Main AI alone decides final acceptance and stage meaning. Use the four unfilled [Stage templates](../templates/main-stage-distillation.md); missing prerequisite sources stay pending, not fabricated. No new observations means NONE. Personal collaboration observations remain private and require relevant authorization.

After Stage Close, or when cross-stage history noise dominates and formal files can cheaply restore context, main AI should suggest a fresh conversation. First verify overview/stage, pending decisions and evidence links are saved; give a minimal “open the project and say take over” entry. Do not move entire conversations, claim to close windows, or silently lose unresolved work. Execution AI does not independently schedule Stage Close or choose the next product stage.

Teach Authority/Task/Verification/Runtime/Observer concepts only when a real problem needs them. Simplicity never hides risk or removes evidence boundaries.

## Resources and native agents

Reuse project resources, shared knowledge and available native tools first; do scoped public research only when useful and authorized. External material is reference, not project authority. Distill high-value findings into adopt/borrow/thin-adapt/reject/defer decisions; do not build a new scheduler to collect speculative evidence.

Small tightly coupled work favors Root direct. Only independent bounded workstreams and available authorized delegation justify child agents; default shallow. Root integrates and performs final verification. Requested model/effort ≠ Effective; missing evidence is UNKNOWN. Agent/session count ≠ cost. Do not fix agent counts, child models or infer stable capabilities from anecdotal observations.

## Permission and assets

More autonomy is not broader permission or background execution. Deletion/overwrite, irreversible migration, credentials, private egress and high-risk external calls require appropriate explicit authority. Respect the current host/tool policy. No implicit installation, account writes or uploads.

Dirty ≠ invalid; untracked ≠ disposable; Git HEAD ≠ current product authority. Protect user assets; do not reset/clean/replace whole trees without explicit scope. Stop affected work for authority conflicts, not to ask again for unchanged existing authorization.
