# Native ecosystem interoperability

In a bounded Windows synthetic experiment on 2026-09-08, one unchanged Agent Skill, one MCP filesystem server and one ordinary CLI participated without changing project memory or adding a MindOS package format. This is evidence for these selections, not universal compatibility. Native Skill client discovery remains NOT PROVEN. Human acceptance and external first-use are not established by this experiment.

## Observed matrix

| Native type / upstream | Exact selection | Observed result | MindOS adapter |
| --- | --- | --- | --- |
| Agent Skill: [Anthropic internal-comms](https://github.com/anthropics/skills/tree/41bbe19d1a1a7eaab5e7bb9050a417e5c6cffc8f/skills/internal-comms) | Commit `41bbe19d1a1a7eaab5e7bb9050a417e5c6cffc8f` | Six files installed unchanged; explicit agent-read 3P use PASS; native client discovery NOT PROVEN | None |
| MCP: [reference Filesystem server](https://github.com/modelcontextprotocol/servers/tree/a40bc270fb5ece62673f8a1196f57116d885c5eb/src/filesystem) | npm `@modelcontextprotocol/server-filesystem@2026.8.31`; source commit `a40bc270fb5ece62673f8a1196f57116d885c5eb` | Real stdio handshake, 14 tools listed, bounded list/read/write, two denied reads, clean process exit | None; disposable JSON-RPC client is test instrumentation |
| CLI: [lychee release](https://github.com/lycheeverse/lychee/releases/tag/lychee-v0.24.2) | `lychee 0.24.2`, Windows x86-64 MSVC release | Native offline JSON link check: missing target exit 2; fixture-only repair exit 0 | None |

The MCP handshake reports server version `0.2.0`; that is its protocol identity, not the npm package version. Preserve both instead of inferring provenance from the handshake alone.

## Installation, permissions and removal

All component installs and inputs were in a new temporary workspace containing only copies of public synthetic examples, Core and Default Workflow. Child processes received a fresh synthetic home/config/cache, an allowlisted environment and no credentials. No global Skill, production MCP configuration, service or startup registration was created.

- Skill: the existing Codex Skill installer downloaded the pinned GitHub revision into temporary project `.agents/skills/internal-comms`. Each file matched the upstream Git blob and recorded SHA-256. The agent read native `SKILL.md` and its selected 3P resource; only supplied synthetic facts were used. No account-backed source was queried. This manual resource consumption does not prove automatic client activation. The current client was not restarted into a potentially broader discovery scope.
- MCP: native npm install used an explicit temporary prefix/cache/config, an exact version, lockfile, `--ignore-scripts --no-audit --no-fund`; dependency resolutions were captured. Node `v24.18.0` ran the native entry with `--permission`, filesystem reads restricted to the synthetic workspace and writes to its project fixture. The server received exactly that project as its allowed-directory argument. The client advertised no Roots capability, so Roots could not replace that argument. A synthetic sibling sentinel and a `..` traversal to it were both denied by the server; the sentinel contents were not returned. An unadopted result was written only inside the fixture. The stdio process exited 0 after stdin closed.
- CLI: the upstream release archive digest matched the published SHA-256, and `--version` returned `lychee 0.24.2`. Invocation was `lychee --offline --format json --no-progress links.md` from a fresh synthetic link fixture. No remote links or preprocessors were supplied. The GREEN run changed only a missing test target, not project Current.

Public ingress was limited to upstream metadata, source and packages. Execution used local inputs and MCP stdio; lychee's offline mode blocks its network requests. This was not an OS-wide network capture, hostile-code sandbox audit or proof against every filesystem escape. Server arguments and Node permissions, not Roots declarations alone, provided the tested filesystem boundaries.

Recursive deletion was refused by the host approval policy. Components, dependency/cache trees and temporary configs were instead recoverably moved to a separate temporary quarantine. All seven original installation locations were absent and the experiment had no remaining server/CLI process. This is uninstall from the active fixture, not permanent erasure: recoverable copies remain outside it and are not published.

## Memory continuity and adoption

Each of three lanes retained all 22 original files: four Core, eleven Workflow and seven project files. Individual SHA-256 values matched before installation, while components were present and after uninstall. Plain-file recovery still found the same project identity, adopted limit 12, pending proposal 20 and historical limit 8. No external result changed Current automatically.

The original file-set digests below are identical across all three lanes and all three phases. Digest construction: SHA-256 of compact, sorted JSON mapping relative original file paths to their SHA-256 values; added result files are deliberately excluded.

| Original group | Before / after digest |
| --- | --- |
| Core (4 files) | `ceea8661f017cf5074d3bbffa28ae96f080c5712a04be5ef9c70ed427f49c60c` |
| Workflow (11 files) | `3b06985fa3c673d89e46a57ad466db919722adb0a19dce90ba03b0d84f3ae25e` |
| Project (7 files) | `2efcaa52c9f437d0e203dc9c54faee3c76227f8aba3099786da42cff278353a1` |

Use the [synthetic adoption example](../examples/interop/README.md) to inspect that seam without installing anything. The Workflow may review a result, reject it, keep it pending or explicitly adopt it with provenance. Capability availability is not permission to change memory. The Core contract and Default Workflow package themselves were not edited for interoperability.

## License and provenance friction

The Skill includes Apache-2.0 terms. The MCP npm archive's integrity matched registry metadata, but its declared LICENSE file was missing; its README still said MIT. The exact metadata `gitHead` [repository LICENSE](https://github.com/modelcontextprotocol/servers/blob/a40bc270fb5ece62673f8a1196f57116d885c5eb/LICENSE) describes an Apache-2.0 transition with non-relicensed MIT contributions retained and documentation under CC-BY-4.0. The experiment records this mismatch, not a blanket MIT conclusion. lychee supplies [MIT terms](https://github.com/lycheeverse/lychee/blob/lychee-v0.24.2/LICENSE-MIT). No third-party Skill body, implementation, binary or dependency is redistributed here; MindOS's own license is unchanged.

Native metadata plus a bounded experiment record supplied the needed identity, version, permissions and result provenance. No missing cross-format fact justified a new descriptor. The existing no-universal-manifest decision remains: no MindOS package registry, metadata mirror, mandatory wrapper or second package manager.

## OpenAI Plugin mapping — documentation only

Current [OpenAI plugin guidance](https://learn.chatgpt.com/docs/build-plugins) describes bundles of Skills, MCP servers or both. This supports the following conceptual mapping; it is not an installed-plugin test:

| MindOS concern | Packaging relationship |
| --- | --- |
| Default Workflow | Skill / workflow guidance; review and adoption policy |
| MCP, Apps, connectors | Optional external capability connection; separate permission surface |
| Local Memory Core | Independent files and continuity contract; not owned by capability packaging |

No plugin, app template or account connection was created. The [native Skill specification](https://agentskills.io/specification) remains the Skill format; MCP remains MCP; ordinary tools remain ordinary tools. Other agents, operating systems, servers, Skills and a second Workflow require their own evidence.
