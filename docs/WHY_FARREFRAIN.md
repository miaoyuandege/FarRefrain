# Why FarRefrain?

FarRefrain is for projects that need to stay understandable across many conversations, changes, and handoffs. It complements agent instructions and memory; it does not replace them.

## Agent instructions solve a different layer

Several useful mechanisms already help an AI work well. They answer different questions:

| Existing mechanism | Main question |
| --- | --- |
| `AGENTS.md` / repository instructions | How should the agent work in this repository? |
| Account or custom instructions | How should the assistant generally work with me? |
| Model or chat memory | What prior context may be remembered? |
| FarRefrain | What is the trusted current state of this long-running project, what is planned, what is executing, what is verified, and how does the next session continue? |

Repository instructions can define coding conventions, commands, and local constraints. Custom instructions can carry durable collaboration preferences. Memory can make continuity more convenient. FarRefrain works alongside all three by giving project state an explicit home.

## What long-running projects still lose

As work stretches across fresh chats, people, and tools, important facts can become hard to recover:

- the current direction gets mixed with superseded ideas;
- an unfinished task looks similar to a verified result;
- a report is mistaken for human acceptance;
- the next session has to reconstruct decisions from chat history;
- a new request accidentally expands scope or reopens an accepted baseline.

The problem is not that other mechanisms failed. The project needs a small, inspectable state layer of its own.

## What FarRefrain adds

FarRefrain keeps a few kinds of project truth separate:

- **Current** records what is true now.
- **Planning** records options, open decisions, and intended work.
- **Inbox** receives new sources and scoped tasks; it is not proof that work is active or complete.
- **Handoffs** preserve completed inputs, reports, and evidence without turning history into current truth.
- **Verification and acceptance** remain explicit, so technical success is not silently promoted into a human decision.

This structure lets an AI restore the current stage, reuse an accepted baseline, execute a bounded change, verify it, and leave the next session a trustworthy handoff.

## What FarRefrain does not replace

FarRefrain does not replace `AGENTS.md`, repository documentation, issue trackers, version control, tests, model memory, or human judgment. Use those mechanisms for what they already do well. FarRefrain connects them around long-running project continuity and scoped execution.

It is also not an autonomous operating system, background worker, or requirement to run a database, server, bot, Router, or multi-agent setup.

## When FarRefrain is worth using

FarRefrain becomes useful when a project spans multiple sessions, carries decisions that must remain auditable, has several workstreams, or needs a clear distinction between proposed, executed, verified, and accepted work.

It is especially helpful when “take over this project” should produce a reliable current-state summary instead of a replay of old conversations.

## When it is overkill

If a project is small, short-lived, or easy to reconstruct, FarRefrain may be unnecessary. Start with normal repository instructions and documentation, then adopt only the FarRefrain pieces that solve a real continuity problem.

Next: see the [reference workspace](WORKSPACE_ARCHITECTURE.md), follow an [illustrative walkthrough](WALKTHROUGH.md), or review the [design principles](PRINCIPLES.md).
