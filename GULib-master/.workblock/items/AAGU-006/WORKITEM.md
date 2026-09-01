# AAGU-006 · FIX · 目标实验 Dataset/Split 权威修复

Block ID: `AAGU-006`

Item Version: 2.1

当前状态: `registered / not claimed`

> Apply target ref：`refs/heads/codex/e7-two-surrogate-groups-20260805`

Execution topology: `sequential`

Item Type: Block

## Human Surface

### 核心意图

让正式实验的数据划分成为可声明、可复用、可校验的独立数据状态，而不是由每次实验运行或随机种子临时重切。实验配置默认使用 `0.7 / 0.1 / 0.2` 和 split seed 2024，但允许注册任意总和为 1、满足对应实验目标语义的合法比例与非负 split seed。同一 dataset 与同一归一化 split contract 只生成一个持久化划分；不同合法合同拥有不同身份，从而同时保证复用和实验多样性。通用 OpenGU 可以保留零 validation 的合同；target-direct 因攻击目标取自 validation mask，只要求自己的注册比例提供非空 validation。

### 本次增量

复用 OpenGU 现有的“划分后保存 pickle、后续直接加载”基础设施，把 split mapping 设为唯一数据划分输入，并由 dataset family、归一化比例和 split seed 确定性派生 processed profile 与候选集合/数量。删除预算的 ratio 或固定 `k` 仍由实验注册独立拥有；若注册 ratio，运行时只把它投影到候选集合得到实际整数数量。`0.7`、`0.70` 等等价写法必须得到同一身份和同一 pickle 路径；首次 miss 生成 masks、pickle 与 manifest，后续命中直接复用。Cache V2 不建立 split-specific 根，但其 Recipe/Artifact 绑定实际 `split_hash` 和候选集身份；只有非法比例、不满足当前实验目标定义，或声明与持久化事实冲突时才 fail closed，不能因为比例不是默认值而拒绝。

### 核心验收

- 正式实验 YAML 显式声明 split mapping，当前 default 为 `0.7 / 0.1 / 0.2` 与 split seed 2024；另一组满足 target-direct 目标语义的合法比例能通过同一入口注册和运行准备，不被 default gate 拒绝。
- 同一 dataset + 等价 ratios + 同一 split seed 在多次运行和不同实验 seed 下得到同一 canonical profile、同一 pickle 路径与同一 `split_hash`；真实 cold/warm 测试证明只生成一次且不覆写。
- 不同合法 split contract 得到不同 profile 并可并存；非法比例、manifest、持久化 masks 或 Cache V2 输入身份冲突才明确拒绝。当前正式实验注册均能解析到显式 split mapping，且复用 OpenGU 持久化路径而非另建私有数据系统。

## Orchestration contract

- Class: `FIX`
- Priority: `P0 / first`
- Source anchor: legacy WORKPLAN target-direct dataset/split conflict.
- Outcome: active planning and executable configuration point to one verified dataset/split identity; obsolete split/budget wording is removed from the active view rather than retained as a parallel lane.
- Fact owner: `experiments/AGENTS.md` and the accepted executable recipe selected during execution.
- Blocks: experiment-definition and target-direct execution nodes until accepted.

## Acceptance route proposal

- Route: `formal`.
- Primary surface: `data / research contract`.
- Minimum evidence: authoritative split identity, consistent owner links and recipe, contract tests/dry-run, and dashboard drift validation.
- Confirmation: user delegated registration now; confirm or correct this contract only when the Block is claimed for real execution.
- Report size: decide at claim; registration creates no empty report.

## Boundaries

- No IF scientific decision, selector choice, formal GPU run, result reinterpretation, or historical evidence deletion.
- Registration only; later execution must claim this exact locator.

## Status history

- 2026-08-26: registered from the prominent WORKPLAN dataset/split repair Todo under delegated registration authority.
- 2026-08-31: upgraded the same stable WorkItem to protocol 2.0 with the current sequential topology and Apply target; no Claim, candidate, or acceptance fact changed.
- 2026-09-02: the user explicitly authorized upgrading this same AAGU-006 WorkItem to protocol 2.1 before acceptance; no implementation or acceptance fact changed in this protocol-only projection.
