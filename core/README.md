# Local Memory Core

Durable local memory for a project, usable with an editor and plain files alone.
The [memory contract](MEMORY_CONTRACT.md) defines semantics; the [default layout](layouts/default/README.md) is one replaceable mapping.

Start with a stable project identity, an overview that maps current knowledge, and a current-stage entry that distinguishes facts from intentions. Keep the evidence needed to explain an update and find superseded facts. A fresh reader should recover without the old conversation.

No Task artifact, AI role, Skill, Router, Runtime, database, daemon or MCP is required. Optional workflow policy is outside Core. See the [files-only example](../examples/kernel-only/README.md).
