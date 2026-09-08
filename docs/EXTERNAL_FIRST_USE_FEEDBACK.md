# 外部首次使用反馈（短表）

先把仓库 URL 给自己的 AI，只说：“帮我安装 FarRefrain，并告诉我安装完成后怎么开始使用。” 不预先学习 Skill 路径。请保留第一次遇到的困难，即使后来自己解决，也不要把它从反馈里删掉。

- AI 能否找到并阅读 START_HERE？YES / NO
- 能否下载仓库？YES / NO
- Skill 安装与实际发现是否成功？YES / NO
- “接管这个项目”后是否自行恢复 Context？YES / NO
- 是否必须手动解释 FarRefrain 术语？YES / NO
- 是否执行小 Task、Verification 并生成 Report？YES / NO
- 原任务单是否归档且未改写？YES / NO
- 最卡的一步 / 首个错误是什么？
- 最看不懂的一句话是什么？
- 你愿意继续用吗？为什么？

结果：PASS / PARTIAL / BLOCKED。PASS 需要下载→安装发现→接管→执行→验证→真实报告全流程成立，且无越权。完成但文案/路径有明显摩擦记 PARTIAL；关键步骤无法继续记 BLOCKED。准备者的本机 smoke 不是这份真人反馈。

最低环境：OS 版本；Codex/客户端版本；公开 commit SHA（或下载包中的 asset-manifest hash）；Python/PowerShell版本只在实际用到时填。无需设备序列号、用户名或账号信息。

可选：脱敏错误提示、以项目相对路径表示的错误位置、必要截图。截图先裁掉账号、私人窗口、用户目录及地址栏中的敏感参数。

不要发送 API key、token、Cookie、私人 repo、完整 Codex session/history、prompt历史、私人代码、个人目录、账号凭据。不要为了测试开启遥测。反馈由测试者审阅后自行交给邀请者；此模板不会自动发送任何信息。

朋友结果回来后由主理 AI 判断：PASS 补证据；PARTIAL 只修真实摩擦；BLOCKED 针对 first divergence 返工。不自动宣称整个 Release Readiness 或正式发布已通过。
