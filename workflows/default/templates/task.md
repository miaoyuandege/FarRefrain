# 正式任务单

> 文件名：`<TaskID>_任务单.md`
> Rework：`<TaskID>_Rework-<NN>_任务单.md`
> 下载到发件箱：`<RouteName>__<上述文件名>`

**Required Skill: `$default`**

## Task ID

`<TaskID>`

## Goal

描述一个可独立施工、独立报告、独立验收的完整 Delta。

## Scope

### 可修改
-

### 不修改
-

## Baseline / Review Level

Baseline：`<只引用本 Task 真正需要的可信 Baseline>`

Review Level：`baseline_reuse` / `delta_review` / `full_review`

Verification Mode：`FAST` / `REGRESSION` / `FREEZE` / `AUTO-BY-RISK`

默认使用 `AUTO-BY-RISK`，不要求普通 Task 手动填写复杂验证矩阵。如明确指定 `FREEZE`，必须写清 Candidate identity 与 invalidation boundary。

## Research / Reuse Gate

Research Value：`HIGH` / `MEDIUM` / `LOW` / `NONE`

External Research：`DONE` / `NOT NEEDED` / `EXECUTION FRESHNESS REQUIRED`

Internal resources checked：
-

Decision：
- Adopt：
- Borrow：
- Thin Adapt：
- Reject：
- Defer：

Execution AI：不重复 broad research；只做本 Task 明示的定向 freshness check。

简单 Task 可把本节压缩为 `Research Value = NONE`、`External Research = NOT NEEDED` 与一句理由；不要为形式复制完整搜索记录。

## Delta

只写本次相对 Baseline 的变化。

## Acceptance

- 
- 

---

以下栏目**只有有实际内容时才保留**：

## Permission / Egress Exceptions

## Semantic Invariants

## Special Escalation

## 自动执行 Contract

只有 production Task Runner 已通过真实门禁且本 Task 确实自动进入 Runtime 时才保留。
