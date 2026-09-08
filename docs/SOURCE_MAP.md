# Source map and synchronization

This public tree is an explicit allowlist, not an export of a private workspace. The [asset manifest](asset-manifest.json) records every file's hash, origin and transformation, excluding only itself to avoid recursive hashing.

| Public module | Origin and transformation | Verification |
| --- | --- | --- |
| core/ | New public contract/layout based on accepted minimal-memory architecture; former combined protocol replaced by pointer | Files-only update/recovery and identity/provenance witness |
| workflows/default/references/WORKFLOW.md | Former public core/MindOS.md, originally curated project-controlled protocol; moved with full workflow retained and action-only handoff delta | Role/research/acceptance review, links, synthetic lifecycle |
| workflows/default/SKILL.md | New thin native entry, informed by former public execution Skill | Native schema validation, installed-resource hash/link smoke |
| workflows/default/templates/ | Six existing unfilled public templates, moved; Skill reference updated | Template count, source preservation, policy consistency |
| workflows/default/references/main-ai.md and guardrails.md | Existing public account/native guidance reclassified; action-only return rule | One canonical policy, no account save claim |
| extensions/router/router.py | Project-controlled accepted local transport source; no production config copied; config-relative paths and exclusive portable move added | Standalone synthetic tests and real temporary CLI transport |
| extensions/router/tests/ | Accepted transport regressions genericized; production config lookup removed; portability/config tests added | Canonical/alias/collision/stability/event and six synthetic route checks |
| extensions/router/config.example.json and README.md | New generic example and platform/failure/privacy contract | Config resolution test; exact private-path scan |
| examples/kernel-only and default-workflow | New synthetic fixtures, no real project or human evidence | Disk recovery, manual lifecycle, add/remove Router independence |
| tools/history-distiller | Existing project-controlled parser and synthetic fixtures; private-history verifier not distributed | Ten offline stdlib tests |
| assets/ | Existing original vector artwork and deterministic social-preview render | Preserved dimensions/hashes; workflow graphic scoped to optional Workflow |
| Other docs/tests/tools/compatibility entries | Public-authored material, maintained for modular paths and boundaries | Links, privacy, installation smoke and exact inventory |

Runtime, file bridge, bots, observers and background integration remain internal-only or deferred; see [catalog](../extensions/README.md). No database, real session, production route target, credential, user profile, private log or live report is distributed. Existing compatibility entries are pointers only, never a second authority.

For future sync, inspect the exact source delta, reapply the named transformation, review every output, update its manifest hash and run exact staged verification. No automatic private-tree synchronization exists. Public file hashes describe a mutable pre-release, not v0.1 final certification.
