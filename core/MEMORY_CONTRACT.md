# Local memory contract

This is the canonical Core semantic contract. It is independent of any agent or workflow.

1. **Identity.** Choose a stable project key and record it in the boot entry. A folder move or display-name change does not create a new project. Conflicting identities require a decision, not a guessed merge.
2. **Boot discovery.** A reader starts at the project overview and current-stage entry. The overview maps the actual current, planning and historical locations. Other names or layouts are valid if this discovery chain remains unambiguous.
3. **Durability and read.** Store enough human-readable local knowledge to restore project purpose, constraints, current facts and unresolved questions without access to an old conversation. Read linked evidence only when needed.
4. **Current and history.** Current contains adopted facts and constraints. Planning contains currently relevant intentions and unresolved decisions, not adopted truth. Historical sources retain their original time and context; age or location alone never promotes them to current truth.
5. **Authorized update.** Change only the memory the user has put in scope. Preserve unrelated edits. Before replacing current knowledge, preserve the previous fact when it matters for recovery, then repair the discovery links. Missing authority or contradictory facts stop the affected update.
6. **Minimum provenance.** An important change records its date, origin or decision reference, what changed and whether it is adopted, proposed or superseded. A short adjacent note or history link is sufficient; a registry is not required.
7. **Recoverability.** A fresh reader can identify the same project, locate current facts, distinguish pending intentions, and trace a replaced fact to its source. A plain-files-only witness is sufficient.

No workflow, task lifecycle, role hierarchy, scheduler, transport, account or service is mandated by this contract. Extensions may provide capabilities; they do not independently promote content into adopted truth.
