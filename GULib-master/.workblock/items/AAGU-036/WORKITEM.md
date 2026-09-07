# AAGU-036 · 实验结果引用既有 Dataset/Split，消除重复存储

Block ID: `AAGU-036`
> Apply target ref：`refs/heads/main`
Item Version: 2.1
Item Type: `Block`
Block Type: `FIX`
当前状态: `registered / not claimed`
Stable locator: `.workblock/items/AAGU-036/WORKITEM.md`

## Human Surface

### 核心意图

YAML 已绑定且正式 processed 目录已持有的图、节点特征、标签和固定划分属于实验输入，不应重复嵌入每份实验结果。实验结果应精确引用该输入，只持有本次产生或确实变化的内容；在保证身份可核验和结果可复核的前提下，避免大数据集、多 cell 和缓存 HIT 导出造成按实验数重复复制输入。

### 本次增量

修复当前 build_output 将 x、y、edge_index、train/val/test_mask 嵌入每个 Output，以及 export_outputs 将完整缓存 payload 再写入每个 predictions.npz 的存储契约。贯通既有 Dataset/Split 引用、缓存解析、结果导出、SyncMate 校验/回传和离线评估/模型重建。复用配置绑定的正式输入，不重建或改变划分，不新增一套平行数据源。处理真正变化的训练图、监督集合和方法特有输出，保持其原有语义。

### 核心验收

1. 同一 Dataset/Split 的多个 cell、多个 run 和 warm HIT 均不向每份缓存/结果包复制完整 x、y、原图和固定 split masks；检查实际文件及 producer 调用，而非只看 HIT 字段。
2. 基于内容身份和校验值解析 YAML 所绑定的正式输入；同名异内容、错误划分、缺失或损坏依赖明确失败，不自动下载、重划分、改用同名文件或启动 producer。
3. 冷/热路径和收集后的独立读取均走真实公共入口，预测、指标、删除语义和模型恢复与同输入基线一致；读取端无需依赖每份结果内嵌原图。
4. 提供多 cell、多 run 的文件清单和实际新增字节表，区分共享输入、方法输出、缓存、导出及回传。固定输入的存储成本不随 cell 数重复增长；用小图及较大合成输入验证增长规律，不以压缩掩盖重复存储。
5. 回传目标已具有精确依赖时复用；缺失时沿正式收集链最多提供一份可核验共享依赖，并符合现有正式输入目录边界。离线读取缺失依赖时明确报错。
6. 用户通过 Markdown/HTML 报告判断容量收益、行为一致性和历史产物边界；测试通过不替代用户接受。

## Execution contract

- Execution topology: `sequential`
- Acceptance Route: `practical`
- Primary surface: `data / integration / contract`
- Decision owner: 用户
- Report: 配套 Markdown/HTML；给出直接入口、前后目录与容量表、实际冷/热及回传证据。
- Minimum real evidence: 公共入口的多 cell 冷/热执行、精确 producer/HIT 记录、真实导出与校验/收集后读取、预测和指标一致性、磁盘增量。
- Post-candidate decision: 完成验证后停在 awaiting acceptance，由用户接受同一候选。

## Source and scope

来源：2026-09-08 SSH 数据盘只读审计及用户明确要求创建 Block。当前观测的 AAGU-032 扩展结果每个数据集有 96 份 predictions.npz。Cora 单份 x 约 15.5MB，96 份约 1.49GB；Citeseer/PubMed 同样重复嵌入特征。抽查及全量 ZIP 目录扫描显示各数据集 x 的 CRC/大小一致。该观测证明重复存储，不证明重新随机划分。

源代码锚点：experiments/modular_run.py::read_dataset、experiments/unlearning_outputs.py::build_output/load_output/validate_embedded_data/restore_model、cache_v2/unlearning_output.py、experiments/modular_artifacts.py、scripts/syncmate 的 method output/收集消费者及对应测试。

正式共享输入以 YAML、manifest、内容哈希和 split identity 为准。SSH 已有 planetoid_70_10_20_seed2024 资产；不得用本地旧 0.8_0_0.2 文件替代。固定图/划分不是每次实验的新结果，体积小的标签与 masks 也不作为重复嵌入的例外。

现有自包含 payload 同时承担离线验证和模型恢复，修复必须覆盖这些消费者，不能只删导出数组或仅修改文件名。保持组件职责分离，移除被替代的旧运行路径，不增加兼容读取、fallback 或迁移层。具体引用实现以实施时最新契约为准。

## Boundaries

- 本次仅注册，不 Claim、实施、启动正式 GPU 实验或执行 SSH 部署。
- 实施验证以 CPU、小规模受控输入和正式收集链的隔离验证为主；不得顺带触发科学矩阵或改变科研结论。
- 现有 Cache V2 Artifact、run-bound 文件与历史报告不得就地改写、重打包、删除或清缓存；不能因契约变化自动重跑。候选报告说明新旧产物边界及历史占用，历史清理需独立明确授权。
- 不更改数据划分、选择策略、训练方法或指标定义；不把本次已清理的旧 FlowChunk 环境纳入本 Block。
- 不预声明 Claim owner、分支或 worktree 路径；后续执行读取最新仓库事实。

## Status history

- 2026-09-08：用户要求创建解决重复输入存储问题的 Block；registered / not claimed。
## Execution ordering · 2026-09-08

- Priority: `P0`；当前优先修复节点。
- Prerequisite: `AAGU-034` 已接受的公共执行入口。
- `AAGU-007 depends_on AAGU-036`：本修复接受并落地后，再执行 007 和由其门控的 031/033 等后续实际实验。
- 用户明确授权本次维护依赖图与看板；不构成 Claim、实施或实验运行授权。方案工作和本修复的受控软件验证可先行。
