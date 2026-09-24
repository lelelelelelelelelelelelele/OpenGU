# GIF/IDEA Profile：真实 gate 验证

Execution SHA: `6594debe4a7247d2274f65ffc435cb6ea4f27a4e`. Job: `aagu077-profile-gate-20260924`.

2026-09-24 21:01:31—21:03:27（北京时间），实际116秒。6/6格完成，13/13产物通过SyncMate SHA-256校验及本地复核。9月25日恢复监控并完成回传，没有重复提交实验。

| Dataset H64 | Method | scale | damp | mu=scale*damp | GU cache | Producer called | F1 before -> after |
|---|---|---:|---:|---:|---|---|---|
| Cora | GIF | 9791 | 0.20098238047209782 | 1967.818487202 | miss | True | 0.902214 -> 0.904059 |
| Cora | IDEA | 9791 | 0.20098238047209782 | 1967.818487202 | miss | True | 0.902214 -> 0.904059 |
| CiteSeer | GIF | 23004 | 0.20094722036615764 | 4622.589857303 | miss | True | 0.744745 -> 0.747748 |
| CiteSeer | IDEA | 23004 | 0.20094722036615764 | 4622.589857303 | miss | True | 0.744745 -> 0.747748 |
| PubMed | GIF | 173215 | 0.20037196190824003 | 34707.429381936 | miss | True | 0.885649 -> 0.883621 |
| PubMed | IDEA | 173215 | 0.20037196190823992 | 34707.429381936 | miss | True | 0.885649 -> 0.883621 |

## 参数与缓存核对

全部格：iteration=100（GU算法迭代参数）、训练seed42、PageRank、删除比例10%。Profile按数据集和模型宽度匹配，不按训练seed匹配。

按可信运行manifest中的六个output.artifact_id，只读获取SSH上对应的GU Prediction header。artifact_id、recipe_hash、content_hash逐格一致。解码实际Recipe中的target.parameters，与Profile加方法YAML逐字段比较，6/6完全一致。

使用项目ArtifactRecipe重新计算六个完整Recipe哈希，6/6与实际缓存记录一致。分别只改变scale或damp，12/12个哈希均变化。这是离线缓存身份检查，没有执行额外实验。本次未进行第二次相同参数运行来实测GU命中。

experiments/modular_gu.py使用同一instance.parameters构造target身份和方法args。六格GU均miss且producer_called=true；score、selection、method_checkpoint均为6格hit。因此复用了模型和选点，六格GU实际重新计算。

## Evidence

- [Per-cell parameters and cache hashes](profile-gate-20260924.json)
- [Verified run manifest](../../../../results/runs/gpu4090/aagu077-table02-gif-idea-gate/aagu077-profile-gate-20260924-v1/run.json)
- [Collection and verification receipt](../../../../.syncmate/deliveries/aagu077-profile-gate-20260924.json)
- [Read-only remote header snapshot](../../../../.syncmate/aagu077-gate-cache-headers.json)

## 结论与范围

Profile映射、真实方法调用、GU缓存身份及产物回传通过工程验证。用户于2026-09-25明确接受本次六格gate。范围为三个H64数据集共六格，不覆盖Cora H16、其他训练seed或414格完整补充表。Table02整体科学决定保持原状态，414格尚未启动。

旧controller快照停在running；恢复后以同一job的最终receipt及已校验delivery确认完成，未手工改写controller。
