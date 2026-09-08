# Provenance / third-party audit

Current public attribution: **Copyright (c) 2026 miaoyuandege**. User-authorized license: [MIT](../LICENSE), decided 2026-09-04. Attribution gate = YES for this public pre-release only; no corporate ownership, registered trademark or exclusive copyright registration is asserted.

Scope: the exact paths in asset-manifest.json plus that manifest itself. This is a source-provenance review, not a legal opinion or a warranty of worldwide copyrightability.

| Assets | Inspected provenance | Distribution conclusion |
| --- | --- | --- |
| Core contract; workflows/default Skill, policy, guardrails and main-AI entry | Curated from project-controlled internal governance, with explicit transformations recorded in SOURCE_MAP and manifest | Candidate-authored/maintained content; no identified copied third-party prose; license and public attribution authorized by the user decision; no independent legal title warranty |
| LICENSE | Standard MIT text from [Choose a License](https://choosealicense.com/licenses/mit/); only year and fullname placeholders filled | Copyright (c) 2026 miaoyuandege; no extra restrictions |
| Six workflows/default/templates files | Unfilled internal generic templates, no user-completed content | No identified third-party notice obligation |
| Router and synthetic tests | Project-controlled accepted internal transport implementation, genericized fixtures and new bounded portability/config adapters; standard library only | No production configuration, routes, logs or third-party implementation copied; same MIT attribution |
| History distiller and tests | Project-controlled parser and synthetic fixtures; imports only argparse, collections, datetime, hashlib, json, pathlib, re and standard test modules | Python standard library is referenced, not bundled; no upstream source package or private verification module included |
| Preflight, local-discovery probe and candidate tests | New local tooling; standard library only; public API requests authored from documented contracts, not copied SDK code | No bundled SDK, client executable or third-party runtime; Codex remains separately installed |
| README/docs/security/contributing/presets/example/gitignore | New candidate prose and links; summaries of official sources, not full copied articles | No image, font, binary, model weight or external repository source imported |

Review method: per-file mapping plus imports, textual attribution/URL search, fixture inspection and accepted source-creation evidence. No external repository clone or automatic private-tree export was used. Synthetic test strings are not real accounts or histories. Absence of a notice in source alone is not proof of unrestricted ownership; externally sourced additions must be re-audited.

No redistributable third-party component requiring a separate THIRD_PARTY_NOTICES.md was identified, so no empty notice file is created. MIT/Apache compatibility has no known third-party conflict in this inventory; MIT and public attribution are now resolved by the explicit user decision. AI assistance does not by itself prove originality or legal title.
