# AAGU-009 refreshed preflight — 2026-08-31

> 历史观察，非当前就绪状态或恢复命令。2026-09-04 已将 009 收窄为软件修复，旧 repair-scope 已退役；下文保留当日记录，正式实验改由 [AAGU-027](../../AAGU-027/WORKITEM.md) 在 001 框架下重新定义和批准。

Observed at `2026-08-31T02:34:02.9974729+08:00`. This is execution-readiness evidence, not formal experiment evidence and not human acceptance.

## Local candidate

- Source branch: `codex/aagu-009-collateral-evidence`.
- Observed source `HEAD`: `2f5044f567368f7a02a1274daa0881521f6a400c`.
- Apply target: `codex/e7-two-surrogate-groups-20260805` at `77b629c77cb8372c73bcc776288f974782c9a644`.
- The source is four commits ahead of the Apply target and the tracked worktree was clean before and after verification.
- Focused regression command: `python -m pytest tests/test_aagu009_collateral_repair.py tests/test_attack_eval.py tests/test_collateral.py tests/test_dashboard_refresh.py -q`.
- Result: `44 passed in 5.76s`.
- `scripts/verify_if_writeback_patch.py` result: `ALL CHECKS PASSED`; GIF and IDEA resolved from the active checkout.

## Registered-config dry-run

Both canonical configs were invoked through `experiments/run.py --dry_run`; neither invocation used `--force` or wrote experiment artifacts.

| Config | Expanded identity | Result |
| --- | --- | --- |
| `phase_b_cora_gcn.yaml` | Cora / GCN / 6 methods / 6 strategies / 5 seeds = 180 cells | exit 0; `would_run: 180` |
| `phase_b_cora_gat.yaml` | Cora / GAT / 6 methods / 6 strategies / 5 seeds = 180 cells | exit 0; `would_run: 180` |

The two configs therefore still expand to the intended 360-cell Phase B surface. The AAGU-009 target subset is the 120 GIF/IDEA cells; the other 240 cells must be observed complete on the runner before quarantine. A local `would_run: 180` result does not prove the runner inventory and is not promoted to remote evidence.

## Git convergence gate

An explicit `git fetch origin --prune` produced these refs:

- local `main`: `fa5a3ecb190eba6a3d5694a041c0d839fc94d36b`;
- `origin/main`: `9d4a0475842d908a90e51fbc2d81c8878335c6c3`;
- Apply target: `77b629c77cb8372c73bcc776288f974782c9a644`, 23 commits ahead of and 2 commits behind local `main`.

The required single accepted full-SHA identity is not present. No push, Apply, merge to `main`, or remote checkout mutation was performed.

## Device and runner gate

- `.syncmate/device.yaml`: missing in the canonical checkout.
- Resolved SSH alias: `autodl-opengu`.
- Read-only SSH probe: failed with `Connection refused` before a remote command started.
- Formal interpreter, GPU visibility, canonical data, clean remote Git identity, 120 target leaves, 240 non-target leaves, and quarantine destination: `NOT OBSERVED`.
- Runtime claims outside this Block: AAGU-004 and AAGU-006 are both `awaiting_acceptance`.

## Decision

Fail closed before remote mutation. In particular, do not quarantine leaves, do not run with `--force`, do not fall back to CPU, and do not claim that the formal repair candidate exists. Resume at the Git/device/SSH gate recorded in `repair-scope.yaml` after the pending human decisions and runner availability are resolved.
