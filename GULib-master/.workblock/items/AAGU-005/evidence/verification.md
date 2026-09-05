# AAGU-005 整理验证 · 2026-09-06

本轮产品检查点为 `c9e094c55b42b2833fb24fcef5fe08f057605f68`。整理分支只新增本 item 的报告、核对脚本与证据，并更新 WORKPLAN 及其生成投影；实验、Core 接入实现、测试和配置不变。提交后的精确 HEAD 与差异读回记录在该工作区 `.workblock/runtime/aagu005-report-qa/candidate-verify.md`。

| 问题 | 实际观察 | 判断 |
|---|---|---|
| 既有原子配方与当前消费位置是否一致 | 使用实际注册配方、配置摘要、Core 执行合同及 OpenGU 输出路径枚举，6/6 一致 | PASS，仅覆盖这些原子配方 |
| 原子入口与 F1 读回检查是否通过 | 项目 Python 运行 13 项既有针对性检查，0 failure / error；原始结果为 `targeted-checks.xml` | PASS，未扩大为正式 GU 端到端 |
| 正式 GU 接入是否已全部对齐 | 20/20 配方产物集合不一致；真实 Adapter 预检抛出 WindowsPath 转 float 异常；接受检查仍使用旧 collateral | FAIL，保持进行中 |
| 新 Core 协议是否在 GPU 上重新联调 | 本轮未提交或执行新任务；旧实测均明确其版本 | NOT OBSERVED，遵循本轮只查代码的约束 |
| 本地与 SSH 依赖是否可消费 | 两端 Core 0.4.0 的 60 文件校验通过；SSH clean c9e094c5 | PASS |
| 报告能否正常阅读并找到证据 | Markdown/HTML 结构检查通过；所有 HTML 证据链接均存在；无脚本错误、页面横向溢出或断图 | PASS |
| 桌面首屏是否给出判断 | 实际查看 Chromium 1440×1000 截图及全页图：标题、事实、建议与唯一待决定投影清楚，决定区位于 y=601 | PASS |
| 窄屏是否可阅读 | 实际查看 390×844 截图：文字正常换行，无横向溢出；决定区在首屏下缘，需轻微滚动 | PASS，可阅读；不声称窄屏完整首屏覆盖 |
| 看板是否由权威事实重建 | `refresh.py --check` 通过；`tests.test_dashboard_refresh` 7 项通过；当前线指向本次 AAGU-005，已接受 028 不再占用当前线 | PASS |

原始渲染截图与测量保存在本工作区 `.workblock/runtime/aagu005-report-qa/`，包括 `desktop.png`、`desktop-full.png`、`mobile.png`、`mobile-full.png` 和 `render-check.json`。截图是生成证据，不入 Git。

上述检查支持本次整理包的真实性和可读性。AAGU-005 的完整接入判断仍为 FAIL，用户决定保持待决定；没有以报告验证通过替代接入通过。
