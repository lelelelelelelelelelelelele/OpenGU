# AAGU-008 · EXP · K5 Noise Anchor

Block ID: `AAGU-008`

Item Version: 2.1

当前状态: `registered / not claimed`

Item Type: Block

## Human Surface

### 核心意图

在进一步扩展实验或引用到论文之前，先形成一份可独立接纳的 K5 noise anchor，让后续比较有一个身份明确、证据完整的噪声基线。

### 本次增量

在 AAGU-007 的 Target-Direct gate 满足后，按最终批准的实验配方运行 K5 anchor，保存固定、可核对的实验配方、代码 SHA、数据身份、完整产物和解释边界。本 Block 不假设不同随机种子（seed）之间科学等价，登记本身也不授权 GPU 执行。

### 核心验收

- K5 anchor 绑定已接受的前置 gate 与唯一可追溯的实验配方、SHA 和数据身份，证据包内容完整。
- 报告清楚说明该 anchor 可以支持什么比较、不能支持什么解释，不用跨 seed 假设补足缺失证据。
- 用户能基于真实产物和解释边界明确接受、返工或拒绝该独立 anchor。

## Orchestration contract

- Class: `EXP`
- Priority: `P1` on the single experiment timeline.
- Source anchor: legacy K5 noise-anchor Todo.
- Outcome: produce one independently acceptable K5 anchor package before any expansion or paper use.
- Fact owner: OpenGU DocMap experiment framework; executable identity remains in the final registered recipe.

## Acceptance route proposal

- Route: `formal`.
- Primary surface: `research evidence`.
- Minimum evidence: accepted gate, pinned recipe/SHA/data identity, complete artifacts, and explicit interpretation boundary.
- Confirmation: deferred until claim/real execution.
- Report size: decide at claim.

## Boundaries

- No cross-seed scientific equivalence assumption and no GPU execution by registration.

## Status history

- 2026-08-26: registered from the prominent K5 experiment Todo.
