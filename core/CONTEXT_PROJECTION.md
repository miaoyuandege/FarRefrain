# Bounded context projection v1

Read authoritative files through explicit role/scope links. Projection changes selection, never adoption. The [truth model](TRUTH_MODEL.md) is independent of the selected workflow. No agent entry, service, embedding index or manifest is required.

| Tier | Purpose / required authority | Default target | Fallback |
|---|---|---|---|
| 0 Boot | Identity, stage, real gate, role/escalation links plus a small primary ADOPTED Current record | 5 files / 6,000 chars / estimated 1,500 tokens | Identify missing primary truth; follow its explicit link. Never substitute Planning or silently truncate authority. |
| 1 Active Current | Boot plus broadly relevant adopted facts/decisions/constraints and explicitly unresolved Current conflicts | 8 files / 12,000 chars / estimated 3,000 tokens | Use a smaller maintained Current/index or report budget excess; History remains on demand. |
| 2 Task | Tier 1 plus explicit scope/component/topic links to relevant adopted constraints/gotchas/failures and labeled contested/observed records | 12 files / 18,000 chars / estimated 4,500 tokens | Ask for the missing scope/authority or follow named evidence. Unrelated failures are not injected. Planning only on explicit request and stays non-adopted. |
| 3 Evidence | Named why/when/change sources, history and provenance as needed | 16 files / 30,000 chars / estimated 7,500 tokens | Read named additional evidence in a bounded continuation; report excess rather than hide missing evidence. |

These are initial targets, not universal hard caps. A project may declare different targets with a reason. Small extra cost is justified only by useful recovered authority. Files, Unicode characters, raw bytes, per-file ceil(characters/4), and sequential hops must be reported; estimates are not a native tokenizer. Budget overflow is visible, not a reason to drop current truth or unresolved conflict. Native model/scaffolding costs are separate.

The optional [selection helper](../tools/context_projection.py) consumes an explicit caller-provided map of plain-file records. `choose` returns paths, not an authoritative generated memory store. Boot records must include links to Current/Planning and an escalation path; the reader follows the selected primary current source instead of loading the full Current tree. Invalid/conflicting metadata, missing evidence, or missing primary Current is a stop condition for the affected projection.

Metadata discovery and materialized-file construction have costs too: account for them separately, and never claim a full scan is a cheap boot read. For repeated use maintain small explicit indexes containing links and scope, not copied competing truth. If any index embeds statements, its provenance and freshness must be checked against sources before reliance. The reference helper performs no caching, writes, promotion or background scanning. Different reading workflows can use the same files and rules.
