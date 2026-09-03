# AAGU-025 · 通用缓存原位接入 Cache V2

软件验收 · behavior / integration / data · 2026-09-03

## Human Result

### 实际增量

通用 Result、Selection、Score 现在默认共用 Cache V2，保留正常缓存能力；旧后端、Legacy 回退和自动建目录逻辑已移除。collateral、预热和相关执行入口同步接入，现有正式 Artifact 合同继续可读。

### 核心观察

在隔离 CPU 输入上，默认真实入口冷启动 MISS，第二次命中同一个 Evaluation Artifact，两次请求只执行一次训练/遗忘计算；Score 计算也完成冷/热复用。改变图、特征、标签、候选集、划分、模型或种子时，旧结果均未被复用。

干净代码检查点通过 293 项相关回归，通用矩阵 dry-run 展开 180 个 cell。三个真实 Legacy 根与现存 Cache V2 共 75 个文件，路径、大小及 SHA-256 全部保持一致；入口文件访问审计未发现 Legacy 读写或创建。

[完整验证记录](evidence/verification.json) · [场景与 Artifact 身份](evidence/junit.xml) · [缓存保护清单](evidence/cache-before.json)

### 当前决定

> 当前验收决定：`接受`

Agent 建议接受此次软件接入：已观察到默认缓存、精确复用、身份拒绝和数据保护。决定者为用户，当前决定以本区投影为准；软件验证与后续同步安装的事实分别见验证证据和 Closeout 记录。

## 行为与集成判断

| 场景 | 实际观察 | 判断 |
| --- | --- | --- |
| 默认冷/热执行 | 真实 AttackManager 与 demo CLI 冷启动写入 Selection/Evaluation；热请求复用同一 Artifact，计算次数为 1。 | PASS |
| Selection 单独命中 | 改变目标训练参数或 GU 方法后，Selection 可以精确复用，但 Evaluation 独立 MISS；原选点耗时从 V2 header 读取。 | PASS |
| Score 能力 | 真实 TracIn、IM、Hybrid 消费者完成写入与读取；warm Score 的 producer 被 fail-if-called 断言保护。实际权重或特征变化后精确 MISS。 | PASS |
| 开关语义 | 全局关闭时 Result、Selection、Score 的可选读写均被跳过且不建 store；只关闭 Score 时，Selection/Evaluation 仍可用；单次 use_cache 覆盖也生效。 | PASS |
| 身份与完整性 | 7 类输入变化均产生新结果身份；损坏 Selection 在计算前拒绝；同一 Score Recipe 的不同内容进入冲突隔离，原 payload 保留。 | PASS |
| Legacy 路径 | 文件 open/mkdir/listdir/scandir/remove/rename 审计覆盖默认入口和 CLI，访问违规数为 0；静态扫描仅作为补充。 | PASS |
| 正式入口 | 已验证 Artifact 经正式输入接口进入真实 pipeline；store 字节不变。既有 Cache V2、target-direct Recipe/manifest/split/stage 回归通过。 | PASS |
| AutoReport | 通用冷启动显示 MISS，热请求显示 HIT；V2 Selection/Evaluation 均绑定 Artifact/hash，标记 authoritative。 | PASS |

验证数据为 8 节点合成图和 2 类 CPU 线性模型；测试注入数据准备与具体 GU 方法，训练/重训各执行两步。AttackManager、CLI 参数链、策略、V2 store/resolver 和 AttackPipeline 的选点后执行编排为生产代码。这证明软件接入行为，不构成新数据集上的研究结果，也不代替真实 GPU 方法的科学验收。

## 精确冷/热证据

| 字段 | 观察 |
| --- | --- |
| 冷 Selection | sel_2cb7bc24_6e8ec0a8 |
| 冷 Evaluation | eval_e968fd88_bc640274 |
| 热 Evaluation | eval_e968fd88_bc640274 |
| Evaluation Recipe SHA-256 | e968fd88a3784f202a18553dd293b85bdce1f3818f8082c0a6cff94b7f60b43c |
| Evaluation Content SHA-256 | bc640274d63168cc0e123a9e2b355b7496c6376976a37cdd9de0c0da1e985e18 |
| 两次请求的计算次数 | 1 |
| Legacy 文件访问违规数 | 0 |

| 变化 | 此前 Artifact | 变化后 Artifact（MISS） |
| --- | --- | --- |
| features | eval_ace7ca1f_78cfc5ed | eval_386f0a8f_449bb184 |
| labels | eval_ace7ca1f_a411f3b1 | eval_b74bfcfe_33bceb90 |
| graph | eval_ace7ca1f_6a2bbecd | eval_cdee05a8_c4357b20 |
| candidates | eval_ace7ca1f_90637a98 | eval_aca7ef66_dadeb79c |
| split | eval_ace7ca1f_b05a66ef | eval_2cf2e398_85b638b8 |
| model | eval_ace7ca1f_5647f01f | eval_6cc37245_4d0cb0d1 |
| seed | eval_ace7ca1f_57118e0f | eval_165f70d7_9cef20f5 |

## 真实缓存保护

开工前只读记录每个文件的相对路径、大小与 SHA-256；干净候选 Verify 后重新枚举并逐项比对，相等而非仅数量相同。所有临时 Artifact store 均位于测试临时目录。

| 真实根目录 | 文件数 | 字节数 | 前后判断 |
| --- | --- | --- | --- |
| results/cache | 8 | 59952 | 完全相同 |
| results/selection_cache | 9 | 19696 | 完全相同 |
| results/score_cache | 26 | 697912 | 完全相同 |
| results/cache_v2 | 32 | 983515 | 完全相同 |

未发起 SSH 操作，未启动正式 GPU 实验，未移动、删除或改写真实旧 payload，也未改写既存 V2 Artifact。SSH payload 未逐文件复查，因此不声明完成远端数据核验。AAGU-023 inventory、ledger、报告与物理归档仍由原 Block 拥有。

[逐文件保护清单](evidence/cache-before.json) · [前后对比及 tree hash](evidence/verification.json)

## 实现边界与审阅记录

通用 GU 只返回聚合指标，不能伪造 Prediction。新增的 Selection-dependent Evaluation 载荷使用既有 FormalArtifactStore、索引、resolver、header 与依赖校验；已有 Prediction-dependent Evaluation 的合同及 Artifact 不变。Cache 层未加入数据加载或实验计算。

删除仅涉及过时的缓存转换/注入/读取源码及其失效测试；预热和监视能力已更新到 V2。不同 k 使用精确请求；此接入不沿用 Legacy 的目录扫描和隐式子集回退。

早期 demo 测试曾经走到 AutoReport 的默认输出位置，新建了 15 条测试事件。已通过创建时间、事件身份及全部临时 Artifact 路径确认归属，原字节移入本 Block 测试证据；测试随后显式隔离三个 AutoReport 输出路径，仓库投影由原 generator 重建，最终与原 tracked 内容一致。事件字节未改写。

[早期测试事件原字节](evidence/early-test-events.jsonl) · [接入说明](../../../docs/generic_cache_v2.md)

## 候选与验证范围

软件行为回归的精确已测检查点为 ab005b66a5a1c8e415a62f8e549629af480d6d51。报告候选及后续交付配置的实际差异、证据复用判断和精确 Git 身份见最终候选核验与 Closeout 记录。

用户于 2026-09-04 接受软件候选 0501316e1774985d3339e14ea3693fd5e3c022e3，并要求补齐 SSH 安装配置。最小 install 动作仅把已落地主线同步到唯一 SSH 活跃检出并核验完整文件身份；不安装环境、不启动实验、不处理真实 payload。此配置不改变以上缓存行为结论。

[交付配置与差异核验](../../runtime/aagu025-delivery-verify.json)

Apply target 为 refs/heads/main，基线 7a2c11fb06cff01363d7773c446370e1588ade4a。用户接受前不合并、不推送、不安装、不清理 Claim。

[权威 WorkItem](WORKITEM.md) · [最终 HEAD 与差异核验](../../runtime/aagu025-final-verify.json) · [pytest 输出](evidence/regression.txt) · [dry-run 输出](evidence/generic-dry-run.txt)

回归：293 passed，1 warning；退出码 0。覆盖通用消费者、CLI、AutoReport、缓存完整性与依赖、target-direct 和运行器。dry-run：180 would_run，退出码 0。新增/修改 Python 源码 AST 解析及 git diff --check 通过。

报告渲染检查：PASS。桌面与窄屏已实际查看，决定区和正文可读，无横向溢出或断图。

[渲染核验记录](evidence/render-qa.json)
