# AAGU-009 local baseline — 2026-08-26

> 历史观察，非当前执行入口。2026-09-04 已将 009 收窄为软件修复，旧 repair-scope 已退役；下文保留当日记录，正式实验改由 [AAGU-027](../../AAGU-027/WORKITEM.md) 在 001 框架下重新定义和批准。

This is a read-only inventory of the collected local evidence. It is not formal acceptance evidence and does not authorize a remote run.

## Scope identity

- Exact affected matrix: `cora` × `GCN/GAT` × `GIF/IDEA` × six strategies × five seeds = 120 leaves.
- All 120 target leaf directories were present below the collected `results/runs/4090` view.
- All 120 included `attack.json`, `collateral.json`, and `_meta.json`; the local SyncMate view did not include `predictions.npz`.
- All 120 `_meta.json` files identified Git SHA `78872fc85dc86fc42f0abd3e6b2fb0b7536df95a`.

## Contamination indicators

- The affected SHA already contains the source commit `d674f629a4e4598816e75903c5d2ba6c0b260002`; ancestry alone therefore cannot prove that the fixed code was loaded at runtime.
- For all 60 same-coordinate `GIF`/`IDEA` pairs, `selected_nodes` matched.
- Their `hop_decay` payload was bit-identical in 33 of 60 pairs. This is a contamination indicator, not a replacement for the formal rerun.
- All 120 old collateral files were parseable and exposed the required hop fields. Completeness does not restore validity because runtime-loaded source identity was not proven.

## Live preflight result

- Local `main` matched `origin/main` at `9d4a0475842d908a90e51fbc2d81c8878335c6c3`.
- The AAGU-009 Apply target was `6be95c74f230cbfcb6a99d0166ba8b1d143e5416`, 20 commits ahead of `main`.
- `.syncmate/device.yaml` was absent in the primary checkout.
- The configured OpenGU SSH aliases tested for the active checkout refused the connection.
- AAGU-004 and AAGU-006 remained active outside this Block.

The formal repair therefore fails closed before any remote artifact mutation. The executable contract is `repair-scope.yaml`.
