# Walkthrough: one long-running project

> **Illustrative walkthrough, not a measured case study.** The details below show the intended collaboration model; they are not a claim about speed, reliability, or a real user's results.

Imagine a developer building a product over several months. The repository already has code, tests, and agent instructions. FarRefrain adds a small project-state layer so new conversations can recover what matters without treating old chat as the source of truth.

## Day 1 — Establish the current project context

The developer and main AI identify the project's goal, current stage, important constraints, and existing verification commands. Stable decisions go into **Current**. Possible future directions and unresolved choices go into **Planning**. New notes or scoped task sources arrive in **Inbox**.

They do not copy the entire conversation into project files. Only information that the next session must trust or evaluate is preserved.

## Later — Start from a fresh chat

The developer opens the project in a new conversation:

> **User:** Take over this project.
>
> **AI:** Current stage: onboarding flow refinement. Accepted baseline: the existing sign-in flow and its focused tests. Open decision: recovery copy. Next action: inspect the new accessibility request in the Inbox.

The exact wording will vary. The important behavior is that the AI reads the project overview, current stage, relevant Current and Planning material, and any necessary task evidence before proposing work. If a required file is missing or unreadable, it says so rather than inventing context.

## A bug or change appears

Suppose keyboard focus is lost after a validation error. The main AI turns that need into one scoped task:

- reproduce the user-visible problem;
- change only the affected form behavior;
- keep the accepted sign-in contract intact;
- run the focused accessibility and form checks;
- require human confirmation only for the experience that automation cannot judge.

The task records scope, boundaries, and acceptance. It does not reopen unrelated roadmap questions or grant new permissions.

## Execution — Change, verify, report

In an execution context, the developer says:

> **User:** Execute the task.

The execution AI restores the minimum task context, implements the bounded change, and verifies the actual symptom. It writes one report that distinguishes observed technical results from anything still pending.

If the focused test passes but the experience still needs a person to try it, the report says **Technical PASS / human acceptance pending**. “The agent says it is done” is not the completion criterion.

## Human acceptance — Keep judgment human

The developer reviews the result and either accepts it, asks for one concentrated rework, or changes direction. Acceptance updates the project's current understanding; a failed attempt remains honest historical evidence instead of being rewritten as a clean pass.

## Handoff — Make the next session cheap

The original task source and report move to **Handoffs**. **Current** contains the accepted truth, while **Planning** keeps only decisions that remain open. The Inbox no longer holds completed work.

In the next fresh chat, the AI can recover the stage and next action from project files. It does not need the user to replay the previous conversation, and it does not need to load every historical report.

## What can vary

A small project may use only a few Markdown files. A larger workspace may add shared knowledge or optional observability. Some tasks are manual; others may have a task Runtime. The stable idea is the same: trusted current context, explicit scope, risk-matched verification, separate acceptance, and a preserved handoff.

Next: review the [workspace levels](WORKSPACE_ARCHITECTURE.md), the [principles](PRINCIPLES.md), or return to the [Quick Start](QUICK_START.md).
