# AAGU-024 · 结构迁移与零变化审计

审计日期：2026-09-01
Git baseline：`be0dd0fad09458d6111ab2e422c8c8bdd3d90bfc`
协议来源：WB-228 exact candidate `bbb299034a58438c691a3f7a5380b005cfe80219`
当前 installed contract：WorkItem `2.1`，`block-workflow 2.1.0`，`acceptance-reporting 2.1.0`

本文件是 AAGU-024 的验证快照，不是 WORKPLAN、成员状态、依赖或优先级的新权威来源。

## 1. 迁移清单

| WorkItem | baseline 协议 | baseline 人类入口 | 迁移后 | 当前状态保持 | live WORKPLAN 快照 |
|---|---|---|---|---|---|
| AAGU-001 | 实际 1.0（无声明） | `Block human acceptance surface` | 2.1 + 唯一首个 Human Surface | `registered / not claimed` | P0；前置 AAGU-006、AAGU-015 |
| AAGU-002 | 实际 1.0（无声明） | `Block human acceptance surface` | 2.1 + 唯一首个 Human Surface | `registered / not claimed` | P0；前置 AAGU-001 |
| AAGU-003 | 实际 1.0（无声明） | `Block human acceptance surface` | 2.1 + 唯一首个 Human Surface | `registered / not claimed` | P2；前置 AAGU-001、002、007、008、010、011、012、013、014 |
| AAGU-005 | 实际 1.0（无声明） | `Block human acceptance surface` | 2.1 + 唯一首个 Human Surface | `registered / not claimed` | P3；前置 AAGU-001 |
| AAGU-007 | 实际 1.0（无声明） | 无 | 2.1 + 唯一首个 Human Surface | `registered / not claimed` | P0；前置 AAGU-002 |
| AAGU-008 | 实际 1.0（无声明） | 无 | 2.1 + 唯一首个 Human Surface | `registered / not claimed` | P1；前置 AAGU-007 |
| AAGU-010 | 2.0 | 无 | 2.1 + 唯一首个 Human Surface | `registered / not claimed` | P0；前置 AAGU-009 |
| AAGU-011 | 实际 1.0（无声明） | 无 | 2.1 + 唯一首个 Human Surface | `registered / not claimed` | P1；无前置 |
| AAGU-012 | 实际 1.0（无声明） | 无 | 2.1 + 唯一首个 Human Surface | `registered / not claimed` | P1；无前置 |
| AAGU-013 | 实际 1.0（无声明） | 无 | 2.1 + 唯一首个 Human Surface | `registered / not claimed` | P2；无前置 |
| AAGU-014 | 实际 1.0（无声明） | 无 | 2.1 + 唯一首个 Human Surface | `registered / not claimed` | P2；无前置 |
| AAGU-020 | 实际 1.0（无声明） | `Intent` | 2.1 + 唯一首个 Human Surface | `registered / not claimed` | P1；无前置 |
| AAGU-021 | 实际 1.0（无声明） | `Intent` | 2.1 + 唯一首个 Human Surface | `registered / ready after dependency` | P1；前置 AAGU-020 |
| AAGU-022 | 实际 1.0（无声明） | `Intent` | 2.1 + 唯一首个 Human Surface | `registered / ready after dependency` | P2；前置 AAGU-021 |

AAGU-010 的自身 Record 在 baseline 已写 `Priority: P1 after accepted collateral evidence`，而同一 baseline 的 live WORKPLAN 投影为 `P0 / AAGU-009`。本次迁移保留两边原文，不把这个既存差异解析成新的优先级决定；Human Surface 只陈述共同事实“等待 AAGU-009 的 collateral evidence 前置满足”。

## 2. Human Surface 结构验证

使用当前安装的确定性校验器逐项执行：

```powershell
python -B -X utf8 C:\Users\ADMIN\.codex\skills\acceptance-reporting\evals\check_human_surface.py --kind workitem <WORKITEM.md>
```

结果：`14/14 PASS`。每份文件均满足：

- 只有一条 `Item Version: 2.1`；
- 第一个二级标题是唯一 `## Human Surface`；
- `核心意图 / 本次增量 / 核心验收` 顺序正确且非空；
- 不再存在 `## Intent`、`## Acceptance Brief` 或 `## Block human acceptance surface` 并行权威标题。

校验器只证明结构可定位；简体中文内容另由逐项语义审计确认，没有把新实验结论、数据身份、formal evidence 或执行授权写入成员。

## 3. 非 Human Surface 逐字守恒

对 baseline 与迁移后 Record 使用同一归一化规则：删除 `Item Version` 行；删除 baseline 的旧人类入口区块或当前的 Human Surface 区块；忽略空行；其余行按顺序逐字比较。

结果：`14/14 NON_HUMAN_EXACT=True`。

这证明原 ID、当前状态、Item Type、Orchestration/Source/Scope/Non-goals、Acceptance contract、relations、priority 文本、运行与 SSH/GPU 边界、registration boundary 和 status history 均未被迁移改写。

## 4. 禁止修改对象与 Claim guard

相对 Git baseline，以下 tracked 路径全部 `UNCHANGED=True`：

- AAGU-004、006、009、018、019、015、016、017、023 的 `WORKITEM.md`；
- `self/dashboard/WORKPLAN.md`，baseline SHA-256 为 `58F29747989D6C400B5E3AAB941B1B490BD1E80EEFC02FB2FF718C2CD4BD799F`；
- 实验代码、Cache V2、results 与 DocMap 没有出现在 changed-path set。

既有 runtime Claims 的内容哈希保持：

| Claim | baseline/current SHA-256 | 结果 |
|---|---|---|
| AAGU-004 | `C33E94CB247AFF1C369B1178B7A0BAF3EA99405CA0112B8FAF344559B78B95DA` | unchanged |
| AAGU-006 | `D1252646BE178EB6E7FA6D06DC1A17CD7F54F025440CFED1574FE0F7FF5B6E79` | unchanged |
| AAGU-009 | `82C3FD936A6ECD39146BE4CBFE6264AA10EF05FF17561C6704C3BE565FBD5008` | unchanged |

14 个成员 Claim 数：`0`。AAGU-024 自身按 `block-workflow` 新建 Claim，当前为 `ongoing / revision 1`；它是 owner runtime 事实，不属于成员零变化 guard。

## 5. 内容哈希 before/after

| WorkItem | baseline SHA-256 | migration SHA-256 |
|---|---|---|
| AAGU-001 | `BCE57BCDDF73CE97C6D7799B33B674069E93FC60DFE280E1D7DEEFD7A530FE24` | `DF446AC5F3B3DE62F68BF2D8EAE92428E2DD06BD8CE6662F94A1795F18D4F7F4` |
| AAGU-002 | `6EE316EE70BA75DA74EE3611D637B3DA6AB9B21106608A5A25BCB837676751FE` | `4DB164D916C9EEEB8531E13329C5B7C34C781571B1884C6B263D1022DFB407D0` |
| AAGU-003 | `993B9E0F1ACF76BDB6B56930D314892557691B019D971FEFC6BC780EC2ADA2E7` | `EB6FDEF67EECE67D530B13AE35FD5ACFDC5DCE8C9A46EEBF06E36D49BF9CA3AD` |
| AAGU-005 | `156D458862331A262F398F0F92629D4FC93EF9A9B8C66E913D101B0156E15724` | `6E814F3EACFF7139C050C908A775F7BB2A03D9F5BE1FA2F69B49C046D815BF22` |
| AAGU-007 | `A365C971275DAB2A6268030CDE4FEE4EB607C0BFFBD5FC2683D9D28DE4EC21C0` | `0AA890C58714D0F1BCC2CD68B1B851E8608372002B6978DD37F1BF401FB8BB8B` |
| AAGU-008 | `F710C44860814208D889F264C05BF97C10B790F9A774ABB530FA31AD557CCC1C` | `1CC220B439CADD5DDC29C739816A2D1FA626445B21D6692A1260099FF115F160` |
| AAGU-010 | `D433F8F5F2CE10E2F131EE9BD4720A8972520088EB7E690AFCCF3FB0E869D917` | `6E79C9C97A9AF358577327F15ED2EC74CE59B11E8235EA93F352212831EC3F6E` |
| AAGU-011 | `7C4BAE05437FEE40AEAD8DF745861BA88043DD37A3A7B21A60618555C2DCC6D1` | `B376AC53FDB98EC98D39D241D5D5333B47DD4875917478C646D9592E6CE0D811` |
| AAGU-012 | `4A38AF0F0D2B0163484086E54F44782C881426679F30C1FE29A978913448FAC4` | `0676B3FB2EF930B8F3EC4558851855880728493D4312D7F26214175B128A9FBE` |
| AAGU-013 | `2CC8CC40EC184B92EE92217457ADA1D3036E5C7B958503547C7D359708887C39` | `CE54371B2091A494E8BFE895159C66DE19149D6A80027A449F67133FF0384507` |
| AAGU-014 | `B100709F8E4B77BCE8DD3BE90B156C8E4C64E417FBBA90F2772A4CF7216A3C67` | `472D43A5DDAAA233C470BA708AFB58156940A9D3DC7ABF25F969223C1EB004B1` |
| AAGU-020 | `5456DAE2F8DD8DF7B08CCFC2CE016EC36E33CE5511077692EEB13884576577EC` | `A115C62644D19D4D071ACCAB689069715DC11AA7237CE44C8FB406AD80FB85CB` |
| AAGU-021 | `D714758565D0E681064A91E443B04C80CA2F3C208B6C9B2F50C5DEFE3CB1F5F7` | `D1459365448B6ECCED89503E09A981619053C25B3F3D8E3C59396317A5B476F2` |
| AAGU-022 | `98C25A58B878756349F3A6ECF128603383DF713531589E8928D750A9353A7767` | `B8ADCC72878DAE3103618615211C82E8A8AE26F93C3BC80BC57874D00EB0324C` |

## 6. 尚未满足的 final evidence

主任务先提供 COMP-042 candidate `f6832b9dec0be903d9f8d83f50ba2bc2864dfbd7`。该 candidate 的受控 MIX fixture/native evidence 有效，但使用相同产品代码加载真实 AAGU 临时快照时，在形成 Campaign view 前遇到 Item Type parser stop；详情见 `companion-aagu-probe.md`。该 candidate 已作废。

COMP-042 随后在同一 Block 内修复并形成新 exact candidate `08be674abc60c9249982a1c3f341a080cd8b5121`。AAGU-024 从 fresh registry 重新加载同一 clean snapshot，得到 24 nodes、20 relations、Graph factVersion 5；1.0/2.0/2.1 版本分别为 5/4/15，14 个迁移成员全部 `Human Surface=available`，9 个代表性 legacy/2.0 records 全部 `Human Surface/Human Result=not_applicable`。真实 native Campaign/Graph 截图、精确字段与零写入验证见 `companion-aagu-acceptance.md`。没有使用 fallback 或伪造截图。

当前 installed `run_git.py finish` 对 nested project 的 owned-path 检查另有一个已复现 stop：`git status --porcelain=v2 -z` 返回 Git-root-relative `GULib-master/...`，而调用方合法的 project-relative owned paths 是 `.workblock/...`，因此 16 个实际 owned paths 被误报为 `unrelated-dirty-state`。该调用 metrics 为 1 个只读 status；index 和 HEAD 均未改变。主任务已确认不得手工绕过 finish，需等待已验证的 2.1 合法入口。

主任务之后以可逆 hotfix 更新当前 installed `block-workflow/scripts/run_git.py`：

- installed SHA-256：`BC2B64DD7EC8F2ABC68500D0598BC1D09009D25841F4DFD48AC81A876AB272C0`；
- 修复边界一：把 porcelain-v2 `-z` 的 Git-root-relative changed paths 归一为 project-relative，再执行 owned-path guard；
- 修复边界二：`read_head_oid` 从 nested project 向上定位真实 `.git`，root detector 跳过不含 `HEAD` 的空 `.git/` 目录；
- 主任务回归结论：含空 `.git/` 的 nested fixture finish 保持 3 个 Git commands，project 外 unrelated dirty state 仍 fail-closed；
- 可逆备份：`C:\Users\ADMIN\.codex\skill-backups\aagu-nested-finish-pre-hotfix-bbb2990\block-workflow`。

该 hotfix 没有进入 WB-228 exact Git candidate `bbb299034a58438c691a3f7a5380b005cfe80219`。AAGU-024 的最终候选若由此 installed hotfix 形成，Report 必须把它列为当前工具链前提，不能把 nested finish 修复归功于或投影回 `bbb2990...`。
