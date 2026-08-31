# AAGU-024 · 真实 AAGU mixed-version Companion 验收

验收日期：2026-09-01  
COMP-042 exact candidate：`08be674abc60c9249982a1c3f341a080cd8b5121`  
COMP branch：`refs/heads/codex/comp-042-mixed-version-campaign`  
AAGU snapshot HEAD：`bcbe688fde20e55af68cadda64fed93f13bcd196`

## 场景与隔离

人需要判断真实 AAGU WorkItems 在 mixed-version Campaign/Graph 中是否可读，而不是只看 COMP 自带的 MIX fixture。为此，canonical A 当前 `.workblock` 被复制到独立临时 Git snapshot；Companion registry 也位于独立 temp runtime。Windows native product 保留正常的 Graph 写能力，但本次动作只有加载、选择节点和截图，所有写目标都与 live AAGU 物理隔离。

首次 candidate `f6832b9dec0be903d9f8d83f50ba2bc2864dfbd7` 因真实 AAGU 的 unquoted `Item Type: Block` 在 `getCompanionView()` 前 fail closed；没有修改 AAGU 或篡改 fixture。COMP-042 同一 Block 修复后，新 candidate `08be674...` 从 fresh registry 重新注册相同 clean snapshot，并成功形成真实 AAGU view。

## 产品读回

`aagu-companion-view.json` 的确定性读回结果：

- `24` nodes、`20` relations、`graphFactVersion: 5`；
- WorkItem versions：1.0 × 5、2.0 × 4、2.1 × 15；
- 本次 14 个迁移成员全部 `human.surface.status=available`；
- AAGU-004、006、009、015、016、017、018、019、023 全部 `human.surface/result.status=not_applicable` 且 `fields=null`；
- AAGU-020 的三段字段与 snapshot 中 `## Human Surface` 逐字相同；
- view 形成前后 snapshot 中 33 个受检 `.workblock` 文件哈希完全一致，Git status 仍 clean。

## 真实 Windows native 截图

### Mixed-version Campaign / Graph

![真实 AAGU Campaign 同时显示 v1.0、v2.0、v2.1](aagu-mixed-version-campaign.png)

在 `WorkBlock Companion` 原生窗口中，项目标题、24 Blocks、20 Relations、Graph version 5 同时可见；节点卡片真实显示 v1.0、v2.0、v2.1 和各自 lifecycle。**PASS**。这张图证明混合版本项目成功加载；单独一张全图不证明抽屉内容来源。

### 2.1 canonical Human Surface

![AAGU-020 显示三段 canonical Human Surface](aagu-2-1-human-surface.png)

打开 AAGU-020 后，抽屉标识 `HUMAN SURFACE`、`v2.1 / declared`，并显示 `核心意图 / 本次增量 / 核心验收` 三段。文本与 WorkItem 逐字读回一致，未从旧 `Intent` 或标题猜造。**PASS**。

### Legacy 无 fallback

![AAGU-004 旧协议只显示真实机器事实](aagu-legacy-no-fallback.png)

打开隐式 1.0 的 AAGU-004 后，抽屉标识 `WORKITEM DETAILS` 与 `v1.0 / implicit-legacy`，只显示 lifecycle、blocked-by/next 和 confirmed upstream/downstream；完全没有 Human Surface / Human Result 标题、卡片、占位文案或来源区。**PASS**。

## 验证记录

| 判断 | 结果 | 实际证据 |
|---|---|---|
| 真实 AAGU parser / projection | PASS | fresh registry 成功加载 24/24 nodes、20 relations；`aagu-companion-view.json`。 |
| 迁移成员 Human Surface | PASS | 14/14 为 available；AAGU-020 三段逐字匹配。 |
| 旧版无新协议 fallback | PASS | 1.0/2.0 代表集合 9/9 为 not_applicable + null fields；AAGU-004 native 抽屉无标题/卡片。 |
| COMP targeted regressions | PASS | `project-source-adapter.test.js` + `mixed-version-campaign.test.js`：18/18 PASS。 |
| Native capture | PASS | 3 次 capture 均读回 `WorkBlock Companion`、24 nodes、1 project；PNG 为 1792×1196。 |
| AAGU / fixture 零写入 | PASS | live initial guard 只有 owner AAGU-024 的授权记录更新；其余 24 个 graph/WorkItem guard 零变化；fixture status clean。 |

## 证据身份

| 文件 | SHA-256 |
|---|---|
| `aagu-mixed-version-campaign.png` | `D7F4A6B5F206C02BD2F1411524F531FDA68A4550778DD01BFA6A69426202CCCF` |
| `aagu-2-1-human-surface.png` | `F15BE6FD3631A5059183BF715194C3CE9DDFF2C7E376C4FD9D56345F5B571F5F` |
| `aagu-legacy-no-fallback.png` | `90673798A953075B8DEA33226E9B53CAA9E39543DFA31CFB038CBB6BDD317E4F` |
| `aagu-companion-view.json` | `F43D842669CBF8A4A47EF7B778DF98A77F6BB5548A19D004CA1D5C3A05CC725B` |

三个 JSON capture manifests 保存各自临时 origin、selected node、human-surface flag、node count 和窗口尺寸。manifest 如实记录 native runtime 本身 `workItemsReadOnly=false / graphWritable=true`；安全性来自 registry/fixture 的物理隔离和前后 clean/hash guard，不把产品能力误写成只读模式。

## 工具链边界

AAGU 候选的最终 `run_git.py finish` 使用当前 installed 可逆 hotfix，SHA-256 为 `BC2B64DD7EC8F2ABC68500D0598BC1D09009D25841F4DFD48AC81A876AB272C0`。它修复 nested project 的 status path 归一化和 `.git` 向上定位，并跳过不含 `HEAD` 的空 `.git/` 目录；主任务用含该空目录的 nested fixture 验证 finish 仍为 3 Git commands 且 project 外 dirt fail-closed。该 hotfix 尚未进入 WB-228 Git candidate `bbb299034a58438c691a3f7a5380b005cfe80219`，本证据不声称 WB-228 candidate 已包含这项修复。
