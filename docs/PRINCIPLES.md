# Principles

These principles describe the product's collaboration model. They summarize intent; the installed protocol remains the operational authority.

## 1. Put durable context in trusted project files

Do not make users replay chat history to restore a project. Preserve only the context that future work needs, in files the project can inspect and maintain.

## 2. Separate current truth from historical source

Current state should be easy to find. Original inputs, superseded ideas, failed attempts, and reports remain traceable without competing with what is true now.

## 3. Agent says done ≠ Task completed

An agent's completion claim is one signal, not the result. Scope, changed artifacts, verification, and remaining conditions determine the technical state.

## 4. Technical PASS ≠ human acceptance

Automation can prove technical contracts; people still own product judgment and final acceptance. Keep those states explicit instead of silently promoting one into the other.

## 5. Keep scope and authority explicit

Every change should have a known owner, boundary, and source of truth. A new request, file, or tool does not automatically grant broader access or redefine the product.

## 6. Match verification to risk

Use the smallest evidence that proves the affected contract, then expand when the change or direct invalidation evidence demands it. A focused documentation change should not pretend to be a release freeze.

## 7. Reuse before rebuilding

Restore accepted baselines and existing project knowledge before reopening settled work. Research or redesign only where it can materially change the decision.

## 8. Treat automation as optional

Files and normal tools are enough for the minimal workflow. Add services, routing, observability, or task infrastructure only when a repeated need justifies their permissions and failure modes.

## 9. Let AI absorb operational complexity

AI should locate context, follow the workflow, and surface meaningful gaps. Humans keep goals, judgment, acceptance, and high-risk decisions rather than learning internal machinery for its own sake.

## 10. Make fresh-chat recovery cheap

A new conversation should recover the current stage, accepted baseline, open decisions, and next action from concise project state. It should not require a transcript replay or a full historical review.

See [Why FarRefrain](WHY_FARREFRAIN.md) for the mechanism comparison, [Workspace architecture](WORKSPACE_ARCHITECTURE.md) for adoption levels, and the [walkthrough](WALKTHROUGH.md) for an end-to-end example.
