# AAGU-015 · EXP · IF 科学定义与 Selector 决策

Todo ID: `AAGU-015`

Item Version: 2.1

当前状态: `todo candidate`

Item Type: Todo

## Human Surface

### 核心意图

在 AAGU-001 实验框图、参数合同与注册规范被接受后，明确当前一轮 IF 科学定义、Selector 范围、研究主张和实验关联，避免先运行后补定义。

### 本次增量

保留同一科学定义 Todo，明确继承 001 的公共规范及 006 的数据/划分权威。后续 Promote 时形成一个可独立接受的科学决定；本次不替用户选择具体 IF 方案，也不批准或启动实验。

### 核心验收

- 当前只核对意图及顺序被正确记录：`AAGU-001 → AAGU-015`，保留 `AAGU-006` 的已接受输入约束。
- Promote 时需说明本轮科研问题、定义、Selector 配置与比较、指标及后续实验关联；实施证据和决定路线届时形成。
- 正式运行必须消费 001 规范下已登记并批准的本轮实验合同，不能由 Todo 登记、科学讨论或软件回归代替批准。

## Todo contract

- Class: `EXP`
- Priority: `P0` after the accepted AAGU-001 experiment framework and AAGU-006 dataset/split contract.
- Source anchor: unresolved IF scientific-definition and selector-choice boundary.
- Desired outcome: the user and a dedicated scientific task choose the IF definition, selector scope, claims, and experiment linkage.
- Fact owner: [OpenGU DocMap IF target-level experiment plan](../../../../../OpenGU-DocMap/10_实验矩阵/20_IF目标层级对比实验计划.md) for the scientific definition; executable data/split/budget identity must inherit the accepted AAGU-006 contract and cannot be overridden here.
- Promote condition: one independently acceptable scientific decision can be stated without starting formal GPU work.
- Confirmed relations: `AAGU-015 depends_on AAGU-001` and `AAGU-015 depends_on AAGU-006`; this makes the existing WORKPLAN/Graph relation explicit in the same Record.

## Boundaries

- This registration does not choose IF, edit formal recipes, claim evidence, or run experiments.
- Promotion inherits the accepted dataset/split/budget identity from AAGU-006; it must not reopen historical public-split, fixed-small-k, or 80/20 execution lanes.
- AAGU-001 is the common experiment-framework prerequisite. Software unit/regression tests do not constitute an experiment; real training/evaluation/timing work cannot bypass that ordering by being called a fix or dry-run.

## Status history

- 2026-08-26: registered as a numbered Todo candidate; promotion and acceptance contract are deferred to the scientific-definition task.
- 2026-09-04: 用户重申实验运行必须在 001 实验框图之后，015 同样遵守；将已有 001 前置关系写入同一 Todo，补齐 2.1 Human Surface。保留 todo candidate、未 Promote、未 Claim、未实施或接受。
