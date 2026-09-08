# Platform and dependency contract

Validated environment: Windows, native Codex CLI 0.149.1 (installed executable; not bundled), Python 3.12, PowerShell 7 for the documented copy commands. Python 3.10+ is the declared minimum for the standard-library tools; only 3.12 was exercised here. No pip dependency is needed. Protocol and Skill use do not require Python; it is for verification and the optional distiller/probe.

Local Skill authoring/discovery uses the project's `.agents/skills/default/SKILL.md`, with the protocol accessible through the project overview. [Official Codex Skill documentation](https://learn.chatgpt.com/docs/build-skills) documents project/user discovery and recommends plugins for wider reusable distribution. This candidate offers manual repo-local setup, not a plugin marketplace installer. Avoid duplicate same-name personal Skills; Codex does not merge their definitions.

The native discovery probe found the project Skill but also outside-workspace Skill metadata despite an empty child home/config environment. No account authentication was copied, no model request was made and no AI-generated first-task report was produced. This is **local installation evidence, not clean end-to-end onboarding PASS**. A genuinely clean user profile/client with user-controlled authentication must complete the remaining first-use Gate before release readiness can pass.

macOS, Linux, WSL, other Codex versions, Claude Code, Gemini CLI and other clients are not yet verified. No cross-platform guarantee is made. A failed or unavailable native executable is an environment/setup limitation, not evidence that the Task ran.

Optional: generic ChatGPT instructions (user saves them), offline history distiller, workflow preset descriptions. Observability/full are design-only. Router is now independently shipped and optional, with relative config paths and a no-overwrite portable branch; only Windows / Python 3.12 has been exercised. Runtime, File Bridge, bot, background runner and scheduler remain unshipped. Earlier discovery results above describe the pre-modular Skill, not discovery of this new package.
