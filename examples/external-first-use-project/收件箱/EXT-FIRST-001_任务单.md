# EXT-FIRST-001

Required Skill: $default
Execution Mode: manual_inbox / not_registered
Verification: FAST / text-only

## Goal

让首次使用的说明清晰准确。只把 `欢迎说明.md` 中的一整行 `等待补充。` 改成 `这个示例不需要额外安装。`，其余字节内容保持不变。

## Scope / Permission

仅允许修改欢迎说明、创建 `任务交接记录/EXT-FIRST-001_报告单.md`，以及报告完成后把本原任务单原字节移入任务交接记录（不得覆盖）。读取项目总览、阶段、当前有效、相关协议与本 Task；不要修改分发仓库、Skill、协议、其他项目或后台组件。

无需网络、账号、程序安装、Runtime、Agent委派、删除或新任务。只有测试者选择本项目并明确说“执行任务”后才执行本例。

## Acceptance

1. 精确替换指定一行；标题和安全提示不变。
2. 实际读取修改后的文件核对，不仅声称成功。保存原任务单 SHA256，归档后核对相同。
3. 单报告说明修改、检查结果、Scope和原 Source hash；Technical Result 依实际验证填写，Main AI Acceptance 保持 PENDING。
4. 原 Source 原字节归档，收件箱不再保留本任务；不因归档就声称真人验收通过。
5. 完成后停止，无其他 actionable Source 时不自行加活。
