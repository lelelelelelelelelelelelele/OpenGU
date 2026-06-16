---
tags: [progress/moc, status/active]
type: MOC
created: 2026-06-15
updated: 2026-06-15
---

# 🏠 Progress Vault — Home

> 这是一个 **活的 Obsidian 式进展库**：按粒度分区记录"项目干了什么 / 现在在哪 / 接下来做什么"。
> **vault 根 = `report/progress/`**。库内笔记用 `[[wikilink]]` 互引；指向库外文件（`self/`、`report/daily-log/`）用相对 markdown 链接并标「外部」。
> 在 Obsidian 里把 `report/progress/` 作为 vault 打开即可（graph view 看 `#progress/*` tag 分层）。

## 🔴 现在 / Now（每次先看这里）

- **全面诊断（先读这个）** → [[2026-06_resume-diagnosis]]：原贡献证伪 + 5 类硬伤（C1-C6）+ 诚实版 paper 长啥样 + 路线
- **当前状态 + TODO + 大方向决策** → [PROGRESS（外部·操作中枢）](../../self/dashboard/PROGRESS.md)
- 一句话：cora 满矩阵数据回流，但 **C1 证伪原贡献**（degree 打败 IF selector）→ 需 reframe；环境待重建；大方向（rebuttal vs 重投）**待定**。详见 [[Findings-and-Decisions]]。

## 🗺️ 按粒度分区（区分开）

| 粒度 | 笔记 | 管什么 |
|---|---|---|
| **当前状态** | [PROGRESS（外部）](../../self/dashboard/PROGRESS.md) | 现在在哪、待办、决策（操作中枢，会动） |
| **宏观时间线** | [[Macro-Timeline]] | 项目启动→5.7 一页纸主线（冻结） |
| **阶段汇报** | [[2026-05_NeurIPS-Push]] | 单段冲刺的详细汇报（5/3-7） |
| **里程碑/检查点** | [[Milestones]] | 02-19 / 02-22 checkpoint、0417 课程报告、daily-log 索引 |
| **发现与决策** | [[Findings-and-Decisions]] | C1-C4、limitations L1-L8、研究路径、idea（会动） |
| **每日日志** | [daily-log（外部）](../daily-log/) | /daily-log 生成的逐日记录（原地不动） |
| **历史档案** | [EXPERIMENT_DASHBOARD（外部·FROZEN）](../../self/dashboard/EXPERIMENT_DASHBOARD.md) | 详细覆盖矩阵 + bug 档案 |

## 🟢 活的：怎么往里加东西

- **加一段新阶段汇报**：复制 [[Phase-Report]] 模板 → 存到 `phases/YYYY-MM_主题.md`，填 frontmatter（`status: active`），在本表加一行。
- **加每日日志**：照常 `/daily-log`（仍写到 `report/daily-log/`），重大日子在 [[Milestones]] 里补一行索引。
- **加发现/决策**：写进 [[Findings-and-Decisions]]，并在对应权威文档（`self/limitations.md` / 研究路径）落正文，这里只放索引+一句话。
- **大方向定了**：更新外部 PROGRESS.md §4 + 本页「现在/Now」。
- **bug 修了 / 数据重跑了**：更新 PROGRESS.md 的勾选；阶段笔记冻结不改（标 `status: frozen`），新进展开新笔记。

## 📐 约定

- 一条笔记一个粒度，**不复制**别处内容——只放摘要 + 链接（继承项目 no-duplication 铁律）。
- frontmatter 必带 `tags` + `status`（`active` / `frozen`）+ `created`。
- 冻结的笔记（已发生、不再改）标 `status: frozen`；会动的（状态/发现/决策）标 `status: active`。

## 🔖 标签速查

`#progress/moc` `#progress/timeline` `#progress/phase` `#progress/milestone` `#progress/findings` · `#status/active` `#status/frozen`
