# Workspace architecture

Local Memory Core → Default / Custom Workflows → Optional Extensions. **Reference layout ≠ mandatory filesystem layout.** Preserve established project conventions and stable identity.

## Level 1 — One project / Minimal

The smallest useful setup is [files-only memory](../examples/kernel-only/README.md): root overview/current-stage, current-memory with core/general/planning, and history/provenance as needed. No Skill, Task, Runtime or Router is required. Planning is currently relevant intention, not adopted truth.

Recommended for explicit task handoffs: add [Default Workflow](../workflows/default/README.md), its thin native Skill and templates using [START_HERE](../START_HERE.md). Main AI → Research → Task → Execution → Verification → Report → Acceptance is workflow policy, not Core.

## Level 2 — Multiple long-running projects / Shared workspace

Share only genuinely reusable contracts, templates or distilled knowledge. Each project retains its own stable identity, boot map, current facts, pending intentions and history. A shared file must not silently override project authority or mix private contexts. No mandatory global directory or registry is needed.

## Level 3 — Optional integrations / Infrastructure

[Router](../extensions/router/README.md) is a shipped transport module. It delivers reviewed sources to configured inboxes, not current truth or execution queues. File bridge, Runtime, observers, remote entry and automation remain internal-only/deferred as documented in the [catalog](../extensions/README.md); they are not a public installation checklist.

Add only a capability whose permission/failure boundary is understood. Removing transport leaves boot/current/history intact, as the integration witness verifies. Core works with a custom workflow; no second concrete workflow is bundled or claimed as tested.
