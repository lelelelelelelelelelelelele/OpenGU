# 第三轮证据归档清单（准备，尚未复制）

拟归档 146 个实际文件，共 8205089 字节；目标为 paper_writing/review/2026-10-24-round3/evidence。本工具当前只写 ignored 清单，没有修改 tracked 目标。

科学 gate 固定为 not_met。A 五新 seed 确认失败必须完整保留；技术检查通过不改变该结论。B 第一层、图控制与 Ret 训练质量属于不同证据层。

所有文件按原字节复制，不改图、CSV、数值或报告文字。执行SHA从对应run/receipt及具名历史来源读取；分析代码当前版本不冒充实验执行版本。每个文件的原路径、SHA256、目标路径、底层执行版本见MANIFEST.json。

复制后保留报告目录及资源文件名，相对图片/同目录链接可继续解析。原报告含有生成时状态；当前结论以对应决定为准。归档同时保存PLAN_MANIFEST.json、PLAN_REPORT.md/html及独立ARCHIVE_RECEIPT.json；计划快照中的“尚未复制”不冒充最终状态。外部仓库证据路径仍为来源引用，这不是包含Cache/model等全部原始载荷的独立复现实验包。

未出现的图诊断full与Ret结果只列为待收录类别，不进入文件列表、不生成占位文件。完整14份scope-support CSV及方法语义限制一并保留，不能只抽有利条件。

移动后相对href/src与Markdown链接检查：passed，58条本地链接，问题0条；详见LINK_VALIDATION.json。正式复制会再次检查，存在断链就停止，不把断链HTML作为阅读入口。

准备命令：python promote_evidence.py；只读核验：python promote_evidence.py --verify；收到根代理明确执行指令后才运行 python promote_evidence.py --promote。默认不会复制。已存在目标必须与冻结源hash一致；冲突即停止，不覆盖、不清理。

| 类别 | 文件数 | 已记录执行SHA | 范围 |
| --- | --- | --- | --- |
| a_e84r1 | 6 | eb5e0d79950cf983bbe14b85c63961ce68ab7b0e | Exploratory ten seeds, separate from confirmation |
| a_audit_e84r1 | 2 | eb5e0d79950cf983bbe14b85c63961ce68ab7b0e | Validation-selected checkpoint identity and export audit; audit clock kept separate from execution |
| a_e84c1 | 13 | d4d70db2b0a599c0385dc398abf41b030332c816 | Independent five seeds: not_confirmed; do not pool, drop failures, replace primary endpoint, or promote writing gate |
| a_audit_e84c1 | 3 | d4d70db2b0a599c0385dc398abf41b030332c816 | Validation-selected checkpoint identity and export audit; audit clock kept separate from execution |
| b_first_layer | 13 | d4d70db2b0a599c0385dc398abf41b030332c816 | 36 GU diagnostics; preserve all 40 truth cells per endpoint; Original/GU/Ret raw values; observational only, no graph/C&S/Ret quality acceptance |
| b_first_layer_decomposition | 4 | d4d70db2b0a599c0385dc398abf41b030332c816 | Actual source e85r1, not e85gr1. CiteSeer published original graph; all per-seed request contrasts and budget interactions retained, including cancelling components. Count decomposition is an identity, not causal attribution. |
| b_figures | 11 | d4d70db2b0a599c0385dc398abf41b030332c816 | Reports copied unchanged, including preparation-time A pending wording; current A decision is a/e84c1. The archived preparatory A script is not evidence of an additional execution. |
| scope_support | 20 | 57c5f21c0403d9d6f34dc27b82051c624b62e161, 8fb8169475b015ac4cc6dd1a61c6d26ee5ff7670, 9d24b46ff14156685c62d8cdb59df1840d9e2c22, a217daf5c67b485afed63c393b5e8bb23820b237, bab1781e182254e0b02cbeb1de138d58f7f1cd50, e5a61494b63d0a403f1d88acff05184e6f446dd6 | All 14 CSVs retained. Old GNNDelete excluded; IDEA not independent; shard methods as-implemented only; historical 080 distinct. No reclassification as new A replication or method-fidelity certification. |
| b_graph_full | 13 | d4d70db2b0a599c0385dc398abf41b030332c816 | Full graph-control analysis only; Ret training-quality and overall writing gate remain separately adjudicated |
| b_graph_interpretation | 16 | d4d70db2b0a599c0385dc398abf41b030332c816 | Descriptive full-scope graph/C&S interpretation; retain matched-CS definitional-equality warning, three-seed uncertainty and separate Ret-quality/contribution gates. |
| b_graph_print_proof | 23 | d4d70db2b0a599c0385dc398abf41b030332c816 | Private layout copies only: final three ACM pages verified 8.5–10.5 pt; original scientific figures unchanged and retain 6.4–6.7 pt reduction risk. Preserve failed baseline PDF. No whole-paper pagination, grayscale or scientific acceptance claim. |
| ret_pilot | 14 | b3481f571880b0ee1a631f87277f6209501dad8b | Preserve scientific_gate=stop_unexplained_final_difference including stopped/blocked pilot. Best/final/old-final and all nine CSVs retained; pilot does not imply complete scope. |
| ret_pilot_audit | 3 | b3481f571880b0ee1a631f87277f6209501dad8b | Original remote read-only endpoint audit plus separate wall-clock receipt and stderr; no training, no cache mutation, not included in job execution time. |
| ret_pilot_interpretation | 3 | b3481f571880b0ee1a631f87277f6209501dad8b | Actual source e85rtg1 pilot when pilot scope; no causal claim about historical old-final training, no replacement of old-final by new-best, all failed evidence retained. |
| ret_pilot_diagnosis | 2 | b3481f571880b0ee1a631f87277f6209501dad8b | Cause undetermined; no extension to remaining six. The source consumer execution a217 is not asserted to be the old cached Output first-producer SHA. CPU invariance does not establish GPU invariance or a CUDA cause. |

待收录（无文件）：

- retrain_complete：Exact admitted nine-condition complete analysis, then --include-ret-complete; complete may never occur if pilot is blocked

## 完整文件清单

| 源路径 | 目标相对路径 | SHA256 |
| --- | --- | --- |
| self/research/experiments/drafts/round3-execution-prep/e84r1/DECISION.json | a/e84r1/DECISION.json | 505c8696bd3e6d664fee20018cab8bb4886103bef91d4eefeff2f7a153993b42 |
| self/research/experiments/drafts/round3-execution-prep/e84r1/endpoints.csv | a/e84r1/endpoints.csv | ad24427c6d224efa42ff519f19a1bc3bfb1b9ef2f7dbebb7bfdc5a6583e38887 |
| self/research/experiments/drafts/round3-execution-prep/e84r1/paired_contrasts.csv | a/e84r1/paired_contrasts.csv | b368055708379023df6b7df7241016a293bae95603baf969b2b2ee914adbbc65 |
| self/research/experiments/drafts/round3-execution-prep/e84r1/contrast_summary.csv | a/e84r1/contrast_summary.csv | 0ffe22f73629458be94c7079ffc3a82ddc3f08174553af79dfa6dd621a1d43ac |
| self/research/experiments/drafts/round3-execution-prep/e84r1/REPORT.md | a/e84r1/REPORT.md | 035eb5656a43b536cb138c0226da693cfab2be295f17bb75aca0030ddb4644b8 |
| self/research/experiments/drafts/round3-execution-prep/e84r1/REPORT.html | a/e84r1/REPORT.html | 21225121acfb43a59c8b61686f828570ca94a1c2e5f498bdfe49d3c6eba9e4f2 |
| self/research/experiments/drafts/round3-execution-prep/A_MAIN_CHECKPOINT_AUDIT.json | a/audits/A_MAIN_CHECKPOINT_AUDIT.json | 5b8f7d9e6c8f8071fe12cc8ec1b4d422030f199151372e0164607f5d3bd26b9b |
| self/research/experiments/drafts/round3-execution-prep/A_MAIN_RETURN_SUMMARY.json | a/audits/A_MAIN_RETURN_SUMMARY.json | 0aa32de0fcaaa6298c9e83cb54c94f5137db5cdd7f5db65c37abdd52cdf07a5d |
| self/research/experiments/drafts/round3-execution-prep/e84c1/DECISION.json | a/e84c1/DECISION.json | 62fa8795ccdd159791796fb1cf7f8eb21117a98e0c6908331e1409e73aab3dd7 |
| self/research/experiments/drafts/round3-execution-prep/e84c1/endpoints.csv | a/e84c1/endpoints.csv | 3093d97b508fe795bdc8e410cf2ec3391f123f0d45ab5ed20f4db33f346f0add |
| self/research/experiments/drafts/round3-execution-prep/e84c1/paired_contrasts.csv | a/e84c1/paired_contrasts.csv | ac0d7d30e73fbfa625cdd0296a2433d6c99fb1b76b2fa1385bf8f1cc8d2dfe5d |
| self/research/experiments/drafts/round3-execution-prep/e84c1/contrast_summary.csv | a/e84c1/contrast_summary.csv | e00779418f007b4b0dee60cde00616ee777f66449d13d634d3749dd84d3d7eb4 |
| self/research/experiments/drafts/round3-execution-prep/e84c1/REPORT.md | a/e84c1/REPORT.md | d3e03d6a675917e9b65963dd57b5c5e45db50d15588e57e0af260aa0586dc4c5 |
| self/research/experiments/drafts/round3-execution-prep/e84c1/REPORT.html | a/e84c1/REPORT.html | cc5d5c8c7985b93728a0b445f5461f3808953a09fbe2daac5151ed312e52ad2e |
| self/research/experiments/drafts/round3-execution-prep/e84c1/A_CONFIRMATION.png | a/e84c1/A_CONFIRMATION.png | c1a82c092bf49f3900bad7a1e7ba63583260ac2aaffdaa07975fdc3f574c7ac5 |
| self/research/experiments/drafts/round3-execution-prep/e84c1/A_CONFIRMATION.svg | a/e84c1/A_CONFIRMATION.svg | 638590707ba202151561087f94cb5afb68c5ec3791093ab55d902450fe33077a |
| self/research/experiments/drafts/round3-execution-prep/e84c1/A_CONFIRMATION.pdf | a/e84c1/A_CONFIRMATION.pdf | b0b0f0a1455b7e2c698c57d49db3ebfa89e29e11d0bab5b0226782211f8e65c8 |
| self/research/experiments/drafts/round3-execution-prep/e84c1/CONFIRMATION_PLOT_REPORT.md | a/e84c1/CONFIRMATION_PLOT_REPORT.md | 45885b5d7d0d3be9e6624a7a3c712f0c81bef475ca0ec355db4410d2aa4fd987 |
| self/research/experiments/drafts/round3-execution-prep/e84c1/CONFIRMATION_PLOT_REPORT.html | a/e84c1/CONFIRMATION_PLOT_REPORT.html | 44ade05a4703bb21fae0f3e14b24078e264ecbe70dd393c7a8a235c72066c447 |
| self/research/experiments/drafts/round3-execution-prep/e84c1/PLOT_EVIDENCE.json | a/e84c1/PLOT_EVIDENCE.json | 1ac276e057c0f50f780d41d2abb140b9ee49dcc5cf6855a7fdd2dc7fc880393a |
| self/research/experiments/drafts/round3-execution-prep/e84c1/PLOT_QA.json | a/e84c1/PLOT_QA.json | 233cc113e79b24a9dfa37965e08b0b51f0305befc2d29d41d1e314ecc7761729 |
| self/research/experiments/drafts/round3-execution-prep/A_CONFIRM_CHECKPOINT_AUDIT.json | a/audits/A_CONFIRM_CHECKPOINT_AUDIT.json | 8b96ff256272a4ba823cd7cd706abe742b92d00c571ed85ba7b40ff22b9c6c93 |
| self/research/experiments/drafts/round3-execution-prep/A_CONFIRM_CHECKPOINT_AUDIT_TIMING.json | a/audits/A_CONFIRM_CHECKPOINT_AUDIT_TIMING.json | 7e9a44b1e9d5bef5329b0328ec5e5c7475ab5c8dc99649a64b3fdc9e7fa85cc6 |
| self/research/experiments/drafts/round3-execution-prep/A_CONFIRM_RETURN_SUMMARY.json | a/audits/A_CONFIRM_RETURN_SUMMARY.json | 73d05a0d241e0e16f142088a3c1c53d7e24337ed54145cfc2dcf85bd0d53bec0 |
| self/research/experiments/drafts/round3-b-diagnostics/e85r1/checks.json | b/first_layer/e85r1/checks.json | 955edf08a0ff11eaf2d21227c6d764d18e698bee72fcfa59976135e37025e77e |
| self/research/experiments/drafts/round3-b-diagnostics/e85r1/endpoints.csv | b/first_layer/e85r1/endpoints.csv | 1ea053e68e1eafddbfbd92c6e295f6a64167732894297a5e21918c962b197a60 |
| self/research/experiments/drafts/round3-b-diagnostics/e85r1/truth_relations.csv | b/first_layer/e85r1/truth_relations.csv | 7c7165230377b99d0094d8968acf17c9435036cefd40e20dc5b5e9ed34d8b973 |
| self/research/experiments/drafts/round3-b-diagnostics/e85r1/request_composition.csv | b/first_layer/e85r1/request_composition.csv | 07c1cd3c1edbd9c901bd4ac8217418e3ec29577ff3e61f94f6b2dac405e2f56b |
| self/research/experiments/drafts/round3-b-diagnostics/e85r1/condition_summary.csv | b/first_layer/e85r1/condition_summary.csv | 1e1c5e7222836c8b151e3f80f1428bbba3f8d8e58fe99257a27e36ffdb39900f |
| self/research/experiments/drafts/round3-b-diagnostics/e85r1/paired_baseline_contrasts.csv | b/first_layer/e85r1/paired_baseline_contrasts.csv | caaba52c77e15d1a92ac54b1753a0fab9517ed39e1a82e3f2080a6013ae9cf23 |
| self/research/experiments/drafts/round3-b-diagnostics/e85r1/budget_change_decomposition.csv | b/first_layer/e85r1/budget_change_decomposition.csv | 1516cc8578a076ae7fc048715dd191c88b743bb3760941209d2ec73afe9cf54b |
| self/research/experiments/drafts/round3-b-diagnostics/e85r1/REPORT.md | b/first_layer/e85r1/REPORT.md | d8463d0be7948ca8a563e52b9cab05a75ed7884077a884ee0bf8a360506088d3 |
| self/research/experiments/drafts/round3-b-diagnostics/e85r1/REPORT.html | b/first_layer/e85r1/REPORT.html | 754b548d6d68027b32a6f47045f8ab13578067be41f6742f2990d4bfd99e74a9 |
| self/research/experiments/drafts/round3-b-diagnostics/e85r1/FRAMING.md | b/first_layer/e85r1/FRAMING.md | 4c769fbf582d503b14acf0f8ae263efc5a5eb854f506b8c9af0342cb79aa8e8f |
| self/research/experiments/drafts/round3-b-diagnostics/e85r1/FRAMING.html | b/first_layer/e85r1/FRAMING.html | f343403379639b76c97431d4b3b928f80f190907ab985ae613a2c9f7a4f270b8 |
| self/research/experiments/drafts/round3-b-diagnostics/e85r1/FRAMING_DATA.json | b/first_layer/e85r1/FRAMING_DATA.json | 7bf21041d5f01547eeb38285dcaf388595ebe58d0117db3250d9ec56fcfb1c00 |
| self/research/experiments/drafts/round3-b-diagnostics/e85r1/FRAMING_VALIDATION.json | b/first_layer/e85r1/FRAMING_VALIDATION.json | 0da1330808e22afcb43f922ddbfc37a4448e491de6dbcd703699b7f76fd31238 |
| self/research/experiments/drafts/round3-graph-analysis/FIRST_LAYER_DECOMPOSITION.csv | b/first_layer/decomposition/FIRST_LAYER_DECOMPOSITION.csv | 07453d2987e2ee2df93dd8f160b0397c3509125b639fd5aec10714936cf53646 |
| self/research/experiments/drafts/round3-graph-analysis/FIRST_LAYER_DECOMPOSITION.md | b/first_layer/decomposition/FIRST_LAYER_DECOMPOSITION.md | dfe43ba281b832cd7298f37d382f61cc09dd116b29d2467a08fa4deeb7e2acfc |
| self/research/experiments/drafts/round3-graph-analysis/FIRST_LAYER_DECOMPOSITION.html | b/first_layer/decomposition/FIRST_LAYER_DECOMPOSITION.html | dece4ebdd3379930325044902389cfd8d9ac04faa62a8e8d8e75493e541b9383 |
| self/research/experiments/drafts/round3-graph-analysis/FIRST_LAYER_DECOMPOSITION_CHECKS.json | b/first_layer/decomposition/FIRST_LAYER_DECOMPOSITION_CHECKS.json | d65f1e7a222ffc9bd8503319347412b725f021fb6a55661ca60368e392582ca2 |
| self/research/experiments/drafts/round3-figure-prep/B_FIGURE_INPUTS.json | b/figures/B_FIGURE_INPUTS.json | 62a0f5c0dc29e4e2715d0e1dfae6f1839ae308b0852e7f24ccb68a0a72b24c70 |
| self/research/experiments/drafts/round3-figure-prep/REPORT.md | b/figures/REPORT.md | 1c08b417cfb0bf491afb19916ec808e55ea126067e7537d3b4958416891bcf49 |
| self/research/experiments/drafts/round3-figure-prep/REPORT.html | b/figures/REPORT.html | d92dce671f7c1600e9f00f15357bc0d348a5834544d96c42e03ade0b7b05668f |
| self/research/experiments/drafts/round3-figure-prep/plot_b_response.py | b/figures/plot_b_response.py | d96ffcfc41dd6a2230a4afec06b68fd0627c65ed315ec8037c0276a9175c307d |
| self/research/experiments/drafts/round3-figure-prep/plot_a_confirmation.py | b/figures/plot_a_confirmation.py | 4bc96b72aa40aa36d43a0fb5c5069746466866531db9100cc7c80f78eebbf809 |
| self/research/experiments/drafts/round3-figure-prep/B_original_gu_retrain_accuracy.png | b/figures/B_original_gu_retrain_accuracy.png | b1a281b8d4bf32534b54877df3ab3e8d861f6e4aaac2fff01c40961ebea2a16d |
| self/research/experiments/drafts/round3-figure-prep/B_original_gu_retrain_accuracy.svg | b/figures/B_original_gu_retrain_accuracy.svg | afdedff0751ef58c8d4c7458aa9351049a0f36169e9f22c5c0f48d1cb1759bf0 |
| self/research/experiments/drafts/round3-figure-prep/B_original_gu_retrain_accuracy.pdf | b/figures/B_original_gu_retrain_accuracy.pdf | 236a6e9fcc3034ef76d6b950b2e49b566344a134a10ed5b8c3ad360e1007e39c |
| self/research/experiments/drafts/round3-figure-prep/B_truth_partition.png | b/figures/B_truth_partition.png | ae64543227d4fc4d707f58b403e3f5278d5de289d95427a79f35b1e7124bd9d1 |
| self/research/experiments/drafts/round3-figure-prep/B_truth_partition.svg | b/figures/B_truth_partition.svg | f9e09b3aa4c8b4f216299e9642032de722b9d83ef24a62ad77d75e5087ffddbd |
| self/research/experiments/drafts/round3-figure-prep/B_truth_partition.pdf | b/figures/B_truth_partition.pdf | 8a515fb9ee597b81d0563e1890d4724636ea9c0cc635a8b74091ba3492b37363 |
| self/research/experiments/drafts/round3-scope-support/budget_current_nonshard.csv | scope_support/budget_current_nonshard.csv | 943cd86919ee59c5db65048acdc72f36e7d5349aea1720ce32dadbc5e6223fab |
| self/research/experiments/drafts/round3-scope-support/budget_historical_shards.csv | scope_support/budget_historical_shards.csv | 612a646b1b0030aac164b3ee077b1379a2dc32a212694883faaf771b297a1d78 |
| self/research/experiments/drafts/round3-scope-support/budget_seven_point_curves.csv | scope_support/budget_seven_point_curves.csv | 0c9b6c0ad9ba95d648bce9df09817f93735578c6d32db8d26206cc0c0074ead5 |
| self/research/experiments/drafts/round3-scope-support/budget_shape_summary.csv | scope_support/budget_shape_summary.csv | 32050114f9ef484c459d2a27c3f2898488135349f0ccdf49410575a17fcc856f |
| self/research/experiments/drafts/round3-scope-support/build_scope.py | scope_support/build_scope.py | c4f5bdf532d66abd403df024b425dbd82115a70323f0b535adbddd4bc76ad37f |
| self/research/experiments/drafts/round3-scope-support/CLAIM_SOURCE_FIGURE_MAP.json | scope_support/CLAIM_SOURCE_FIGURE_MAP.json | 8960cb1fe3f57902b8ec29506b9b8f708b5928f129a88a2944f69497fde6287e |
| self/research/experiments/drafts/round3-scope-support/common_output_identity.csv | scope_support/common_output_identity.csv | 7106588859a3f9a887bf8e89eb1e9f45f0a5cf671f6bf4d213b2c3983bd17fb1 |
| self/research/experiments/drafts/round3-scope-support/fixed10_endpoints.csv | scope_support/fixed10_endpoints.csv | dfd96589d5e529c7d42f477186029d47837ddd633e5fd14dc941a5aba9dae0bb |
| self/research/experiments/drafts/round3-scope-support/fixed10_geometry.csv | scope_support/fixed10_geometry.csv | 4853352f8183b964d2b21a429a39583123da4271d1edbcb027752d34003cd7ee |
| self/research/experiments/drafts/round3-scope-support/fixed10_hops.csv | scope_support/fixed10_hops.csv | 6287cb0bf50df678d272e82a9efc3d74cba3b85a21668a033d643ac63e99f51a |
| self/research/experiments/drafts/round3-scope-support/fixed10_random_contrasts.csv | scope_support/fixed10_random_contrasts.csv | 8b791f513e6cc13696b7eb0836df5962d84450a3a73e13286360a5bdb126c3f6 |
| self/research/experiments/drafts/round3-scope-support/METHOD_SEMANTICS.json | scope_support/METHOD_SEMANTICS.json | db0149e8cd9a8b25433e365f857cb83541436e126a4d163501f2fc48930a7e9f |
| self/research/experiments/drafts/round3-scope-support/REPORT.html | scope_support/REPORT.html | 84a63e4d63d6ad90cede83732cb6a0a38fd286f50b1e27150633fb4bc0ff2d12 |
| self/research/experiments/drafts/round3-scope-support/REPORT.md | scope_support/REPORT.md | ec411f133e4de7f43641e1cefbc644d4b6c24e1c5c46778a6e837d1b00fe57b9 |
| self/research/experiments/drafts/round3-scope-support/selector_costs.csv | scope_support/selector_costs.csv | 6ee770d4422f474915badc86bb50fc0ad0c3bdbac708dc8ccdef80615fda2dd1 |
| self/research/experiments/drafts/round3-scope-support/source_direct_contrasts.csv | scope_support/source_direct_contrasts.csv | 732b36af848571088f4dabe0c26bed2e0e2cb2ef233abce0f311dfb56681aa05 |
| self/research/experiments/drafts/round3-scope-support/source_endpoints.csv | scope_support/source_endpoints.csv | 4726aa875b4214e8de21f4375d74691f2a2ae329e6b74bbec9f4c22a1587568c |
| self/research/experiments/drafts/round3-scope-support/source_random_contrasts.csv | scope_support/source_random_contrasts.csv | b09774c419e7f54df44d52a599951d701f9c9f93d39aa47f72e9e77a70132914 |
| self/research/experiments/drafts/round3-scope-support/source_scope.csv | scope_support/source_scope.csv | c06e1bbb798a667bd9e413c8653215bb76a07d400f43473bbc4bd7a2faa326a4 |
| self/research/experiments/drafts/round3-scope-support/VALIDATION.json | scope_support/VALIDATION.json | c8a9e8e6149ac5e4560eb7d355bc6a15e34faee7b3e8b611f174070324aff580 |
| self/research/experiments/drafts/round3-graph-analysis/e85gr1/checks.json | b/graph/e85gr1/checks.json | adb4fc8ac604c8816ba2e41edda7af772554804ffbec4cb02691872e833ba34a |
| self/research/experiments/drafts/round3-graph-analysis/e85gr1/REPORT.md | b/graph/e85gr1/REPORT.md | 7919bd4782cd67652cb9e6cf9a113e9dfe5412d0574483b79399a321d9708f57 |
| self/research/experiments/drafts/round3-graph-analysis/e85gr1/REPORT.html | b/graph/e85gr1/REPORT.html | add2f4415960328678c95569dcb53c469a651286f45dfdbf1581c0dd15bbef4f |
| self/research/experiments/drafts/round3-graph-analysis/e85gr1/endpoints.csv | b/graph/e85gr1/endpoints.csv | 102f7a9de1e81108744037eb52710b3fe8ca784a11d44aaa306e687b7d0e3c31 |
| self/research/experiments/drafts/round3-graph-analysis/e85gr1/truth_relations.csv | b/graph/e85gr1/truth_relations.csv | eaef50cb9df303305c5f93b85eaef7d9d90af0b12c99353a80809c0812882043 |
| self/research/experiments/drafts/round3-graph-analysis/e85gr1/request_composition.csv | b/graph/e85gr1/request_composition.csv | c4ac7649a4368b7c893b3bf74ffa67a06284f0622f13c1f4ea84ab0fafc65bbb |
| self/research/experiments/drafts/round3-graph-analysis/e85gr1/endpoint_identities.csv | b/graph/e85gr1/endpoint_identities.csv | f9941a90d6a2e3d170e2320d8a69555b7592f19a7bde7b9b29eec93196288383 |
| self/research/experiments/drafts/round3-graph-analysis/e85gr1/cs_effects.csv | b/graph/e85gr1/cs_effects.csv | 79ac9d65581203c5c39eda2d3153fd16aedf46114159bc6ca59d06a5a51bda29 |
| self/research/experiments/drafts/round3-graph-analysis/e85gr1/graph_changes.csv | b/graph/e85gr1/graph_changes.csv | 596d4f5a4f2b7f5f43a5c4f2487f4c2f699bfd81b3cfaa0e94a5cbeb0fa963e1 |
| self/research/experiments/drafts/round3-graph-analysis/e85gr1/condition_summary.csv | b/graph/e85gr1/condition_summary.csv | 86a9f8dbace7ad6fc44dc2bb16dfd402e4d4c0aeb2d2d05791d64003626b4f91 |
| self/research/experiments/drafts/round3-graph-analysis/e85gr1/paired_request_contrasts.csv | b/graph/e85gr1/paired_request_contrasts.csv | 0537c6c10d571127028a6ac35855c817e939fd091c7cf2d10f74a866ca2b0b1f |
| self/research/experiments/drafts/round3-graph-analysis/e85gr1/budget_contrast_changes.csv | b/graph/e85gr1/budget_contrast_changes.csv | 9f4ae5f9f6dd1f43c8ff773972aa804e4af829a98be507b05966a4ea75f542be |
| self/research/experiments/drafts/round3-graph-analysis/e85gr1/control_contrast_changes.csv | b/graph/e85gr1/control_contrast_changes.csv | b37f6c46c45f96751edb326719dd847cb18da58d50a59757fc74743f6baf20f2 |
| self/research/experiments/drafts/round3-graph-analysis/e85gr1/interpretation/budget_interaction_summary.csv | b/graph/e85gr1/interpretation/budget_interaction_summary.csv | 3f745a1a8cf1ede80fb17b34b50cfdb8ca067fb78972ed32f30a47a9faf22d7a |
| self/research/experiments/drafts/round3-graph-analysis/e85gr1/interpretation/cs_summary.csv | b/graph/e85gr1/interpretation/cs_summary.csv | 602e183a10881079c7682aba5504e31c68d9005679a658f1fb9d80c79ca45b7d |
| self/research/experiments/drafts/round3-graph-analysis/e85gr1/interpretation/endpoint_summary.csv | b/graph/e85gr1/interpretation/endpoint_summary.csv | e0015d9d5be5c341cd145eb203849cfb59ea03de76579d07ef540d309cd8eb08 |
| self/research/experiments/drafts/round3-graph-analysis/e85gr1/interpretation/graph_change_summary.csv | b/graph/e85gr1/interpretation/graph_change_summary.csv | a6b1258be65a25d64d8ae6a2e6c802cdcd68ad7dfff9d200cba2126fef93a08f |
| self/research/experiments/drafts/round3-graph-analysis/e85gr1/interpretation/KEY_FINDINGS.json | b/graph/e85gr1/interpretation/KEY_FINDINGS.json | b4fe9b0313802b6dc6c2f1ad10298f8198beff0819e2e9e8f7d0d893f881221e |
| self/research/experiments/drafts/round3-graph-analysis/e85gr1/interpretation/megu_cs_controls.pdf | b/graph/e85gr1/interpretation/megu_cs_controls.pdf | b78025813ef9f51a7f2e6376d50f2359feeaa4f1e0ea3171371ecd4004aa2508 |
| self/research/experiments/drafts/round3-graph-analysis/e85gr1/interpretation/megu_cs_controls.png | b/graph/e85gr1/interpretation/megu_cs_controls.png | a30fa19e4278e9758873638b611d41335f039f5a5124a7105edd73a3ebb0e343 |
| self/research/experiments/drafts/round3-graph-analysis/e85gr1/interpretation/REPORT.html | b/graph/e85gr1/interpretation/REPORT.html | 773677f61dffc62fad425333b6d3c5eb2ba8a546772e03cc9a25413d31eac469 |
| self/research/experiments/drafts/round3-graph-analysis/e85gr1/interpretation/REPORT.md | b/graph/e85gr1/interpretation/REPORT.md | 846d8e7e7fa9df7247707676574e43b8424ee81fd2c4ed6a1fd3256970894350 |
| self/research/experiments/drafts/round3-graph-analysis/e85gr1/interpretation/request_contrast_summary.csv | b/graph/e85gr1/interpretation/request_contrast_summary.csv | b29b516184cef2b5519a9781b352a6641bb5e5402d4d8dfb5f45a2c0a04f16d7 |
| self/research/experiments/drafts/round3-graph-analysis/e85gr1/interpretation/ret_only_truth.pdf | b/graph/e85gr1/interpretation/ret_only_truth.pdf | 6a05ced20b9ff4685e711102d44dd993b2f5f1fb6d0626a35c3965c339e1b4f9 |
| self/research/experiments/drafts/round3-graph-analysis/e85gr1/interpretation/ret_only_truth.png | b/graph/e85gr1/interpretation/ret_only_truth.png | db9d6e0b1d03006b114932b8c7a4d7235fef254e765d82da1ae1058eda6db31c |
| self/research/experiments/drafts/round3-graph-analysis/e85gr1/interpretation/strategy_graph_controls.pdf | b/graph/e85gr1/interpretation/strategy_graph_controls.pdf | 286bafaf7306e723c6614ad69a0ac3bb19a2b1e1edaa48f2651419f623c51061 |
| self/research/experiments/drafts/round3-graph-analysis/e85gr1/interpretation/strategy_graph_controls.png | b/graph/e85gr1/interpretation/strategy_graph_controls.png | de161cc63745d6ce41716393044644e90f64a0b523561c6939871481c2fa495d |
| self/research/experiments/drafts/round3-graph-analysis/e85gr1/interpretation/VALIDATION.json | b/graph/e85gr1/interpretation/VALIDATION.json | d53272996eee9197b281d5469b37fc89c88d442edac7e162b6b7011c87996eab |
| self/research/experiments/drafts/round3-graph-analysis/e85gr1/interpretation/ARTIFACT_QA.json | b/graph/e85gr1/interpretation/ARTIFACT_QA.json | cc451023362ae1337d4708f4eea0a7beaabbe65c62926f01b2b4a6c1e62fd277 |
| self/research/experiments/drafts/round3-figure-proof/b-full-controls/REPORT.md | b/graph/proof/REPORT.md | 07e292c0b2d7b5cdd950631d50fb9feba51c7ec1ac327631805a6ead6a36c1c5 |
| self/research/experiments/drafts/round3-figure-proof/b-full-controls/REPORT.html | b/graph/proof/REPORT.html | 319a904bcb91511b6fb4f232045ec0c0071c177d40e208f63c098fb3838cf705 |
| self/research/experiments/drafts/round3-figure-proof/b-full-controls/VALIDATION.json | b/graph/proof/VALIDATION.json | 507ba8409717ca044365e97d431861be0403a0a1b4fe71e55e98d45fa333e4ae |
| self/research/experiments/drafts/round3-figure-proof/b-full-controls/REFLOW_PROVENANCE.json | b/graph/proof/REFLOW_PROVENANCE.json | 1154e476adc468a3d73dfaa6547cc56fa1a65e4fa4bcdd893b901572970ef927 |
| self/research/experiments/drafts/round3-figure-proof/b-full-controls/main.tex | b/graph/proof/main.tex | cf0d42ad00659ae4108f40e2a80806b7f1bf177ab66be3cc9681c9419f41fb45 |
| self/research/experiments/drafts/round3-figure-proof/b-full-controls/build/main.pdf | b/graph/proof/build/main.pdf | c77353c376b2da02253e52c16f0fe161f82c97475ec9e9cb37cef7bb4c387064 |
| self/research/experiments/drafts/round3-figure-proof/b-full-controls/baseline/build/main.pdf | b/graph/proof/baseline/build/main.pdf | 1b0749dc18ebee9fcb6d8da6887c6b21bf01bc45cdc53739a884b2ddaa750820 |
| self/research/experiments/drafts/round3-figure-proof/b-full-controls/private_plot_function.py | b/graph/proof/private_plot_function.py | b941ea6411dbbfd1ea5c44df8ffd56c0d0d7d6793f5eb795d43562f59d908315 |
| self/research/experiments/drafts/round3-figure-proof/b-full-controls/original_plot_function.py | b/graph/proof/original_plot_function.py | ce9c8a7ac4e1ffbe6bf40257c4068d67d6d491a3a05455bf2938101f22676c97 |
| self/research/experiments/drafts/round3-figure-proof/b-full-controls/reflow_copies.py | b/graph/proof/reflow_copies.py | e3b050971061de3a1c45fca117baeade3a0d31528977038d1c13ea8072ea3547 |
| self/research/experiments/drafts/round3-figure-proof/b-full-controls/INPUTS.json | b/graph/proof/INPUTS.json | 5bce9567efe1d6d36c58133fa6f054116538590957793039a0aa67091c9b52dd |
| self/research/experiments/drafts/round3-figure-proof/b-full-controls/images/strategy_graph_controls.pdf | b/graph/proof/images/strategy_graph_controls.pdf | 313a7ddbfd1bf235862f224d5a070d2e75d074abdeeb0d5e7a6c11f37f8b8de1 |
| self/research/experiments/drafts/round3-figure-proof/b-full-controls/images/ret_only_truth.pdf | b/graph/proof/images/ret_only_truth.pdf | 30b6b3d3495569a0830c6de873fff4371ee6162977fa8b04155bcbf268d2f7f7 |
| self/research/experiments/drafts/round3-figure-proof/b-full-controls/images/megu_cs_controls.pdf | b/graph/proof/images/megu_cs_controls.pdf | 5c40861b4478e22944b43699dadc4e53a84bff927ae282e6816ddeacbe1dbcb6 |
| self/research/experiments/drafts/round3-figure-proof/b-full-controls/rendered/page-1.png | b/graph/proof/rendered/page-1.png | 795f695ddbf381886d9059eea040e2958daade398bfac1b43a5c83426c88d2d2 |
| self/research/experiments/drafts/round3-figure-proof/b-full-controls/rendered/page-2.png | b/graph/proof/rendered/page-2.png | f58f4730b0a6b961455129f6827e4ec769dbf8ef4743cc8c7c5265a141693fd9 |
| self/research/experiments/drafts/round3-figure-proof/b-full-controls/rendered/page-3.png | b/graph/proof/rendered/page-3.png | 218869521799a8238810b839b124a4b40cb7c718b0d7ff2e7d616701d1fae10b |
| self/research/experiments/drafts/round3-figure-proof/b-full-controls/baseline/rendered/page-1.png | b/graph/proof/baseline/rendered/page-1.png | 94722e66ea3f7ef17be0337b6084924419c2be093bb0d0dacdbe50228bd4c6e2 |
| self/research/experiments/drafts/round3-figure-proof/b-full-controls/baseline/rendered/page-2.png | b/graph/proof/baseline/rendered/page-2.png | 1cf3854af8f445955fc93fce07dad24b9fc4636f693418e699bd8d9bdd88b687 |
| self/research/experiments/drafts/round3-figure-proof/b-full-controls/baseline/rendered/page-3.png | b/graph/proof/baseline/rendered/page-3.png | 75ba68f50b7af31044e93929f18ac16179433210ea1e4d6a2cf3bdf8921c823f |
| self/research/experiments/drafts/round3-figure-proof/b-full-controls/FINAL_MANIFEST.initial.json | b/graph/proof/FINAL_MANIFEST.initial.json | e099d14aaf6f1bd3121bb45950f1380ed3c67063d202ca2718c5e087de337e1c |
| self/research/experiments/drafts/round3-figure-proof/b-full-controls/MANIFEST_EXPANSION_CHECK.json | b/graph/proof/MANIFEST_EXPANSION_CHECK.json | ab08bfcb6fadfad4aa25af636e84e934435570c3c2de34d5340b3fbf35c75351 |
| self/research/experiments/drafts/round3-figure-proof/b-full-controls/FINAL_MANIFEST.json | b/graph/proof/FINAL_MANIFEST.json | 97f689aefdfabfbb352b8ae0bd47818756c8aa616281c28de79bbba64d2c4144 |
| paper_writing/protocol/exp085/analysis/pilot/trajectories.csv | retrain/pilot/trajectories.csv | bc5c1097f857096dead6f4ea80bf0ed06fb90f720a51671f0440507a451097ca |
| paper_writing/protocol/exp085/analysis/pilot/endpoints.csv | retrain/pilot/endpoints.csv | 093098ef62e98bebf08397cc9ef35b88b53b84060b9c93c3a9130058cdbb8d48 |
| paper_writing/protocol/exp085/analysis/pilot/full_trace.csv | retrain/pilot/full_trace.csv | 23931ef298bc3c99a0a396364454d5a5fd85722b4a4002a8d5d2cd72ae3d207b |
| paper_writing/protocol/exp085/analysis/pilot/paired_request_contrasts.csv | retrain/pilot/paired_request_contrasts.csv | 42af60fd639364545a37b5195c1396362da6da639447226282f865be42567e5b |
| paper_writing/protocol/exp085/analysis/pilot/condition_summary.csv | retrain/pilot/condition_summary.csv | fca230a3401e9355d36be790b01f24cdd8566c17ecc8014cbfea47e716ac519c |
| paper_writing/protocol/exp085/analysis/pilot/gu_reference_pairs.csv | retrain/pilot/gu_reference_pairs.csv | f96533debc5e8df7d1720b2a0df4626ff234769045686e555afcd3d37ceab9a8 |
| paper_writing/protocol/exp085/analysis/pilot/gu_reference_classes.csv | retrain/pilot/gu_reference_classes.csv | 359bb6ea04cb26920f43616fcf6974bd04b4bfbe953e640dc8615efc150cce67 |
| paper_writing/protocol/exp085/analysis/pilot/gu_reference_correctness.csv | retrain/pilot/gu_reference_correctness.csv | e014163269ac4e1df791249d809bc7cbbc34ba0bf4fd1df4e358f522ee2c361c |
| paper_writing/protocol/exp085/analysis/pilot/gu_request_contrasts.csv | retrain/pilot/gu_request_contrasts.csv | b86662f3a523d13991ab1510bf67670f0b95af28c646bfe3e3d3a9b6e17d5ed7 |
| paper_writing/protocol/exp085/analysis/pilot/DECISION.json | retrain/pilot/DECISION.json | 6e5595d504f6f3d8d729135d11905ace86f5c5f3d19e766ad4ba71dc12f446f8 |
| paper_writing/protocol/exp085/analysis/pilot/REPORT.md | retrain/pilot/REPORT.md | 950f409df50c08a54f15992317e81239485cc6fbe99cb260d4c369829781294c |
| paper_writing/protocol/exp085/analysis/pilot/REPORT.html | retrain/pilot/REPORT.html | 6f080e8f43c20ef560c566f7681c24519c0af2724c2bd5037289cf35b4316ef5 |
| paper_writing/protocol/exp085/analysis/pilot/GU_reference/REPORT.md | retrain/pilot/GU_reference/REPORT.md | 3afb772efb8256d1cb3c3dde16780cb2b1091c8493064545da1cb54d5c1a7d8f |
| paper_writing/protocol/exp085/analysis/pilot/GU_reference/REPORT.html | retrain/pilot/GU_reference/REPORT.html | 93670736797a7c8fb8947715e39e78d2642069594cba164e42ad150e7132b6d4 |
| self/research/experiments/drafts/round3-retrain-prep/e85rtg1_ENDPOINT_AUDIT.json | retrain/pilot/audits/e85rtg1_ENDPOINT_AUDIT.json | 770481ccb58b52c873f24a34514c52675dcaf4978a17c02e8d5521b2a59e5e89 |
| self/research/experiments/drafts/round3-retrain-prep/e85rtg1_ENDPOINT_AUDIT_TIMING.json | retrain/pilot/audits/e85rtg1_ENDPOINT_AUDIT_TIMING.json | 4f6f2adfb11dc315936eb46386c6f9884ac544ddf042991e2567e9e80d9601df |
| self/research/experiments/drafts/round3-retrain-prep/e85rtg1_ENDPOINT_AUDIT.stderr.txt | retrain/pilot/audits/e85rtg1_ENDPOINT_AUDIT.stderr.txt | bdc36621c1ae03d6791190b49c81c70090d027c6efa041fec41166861dc3d375 |
| self/research/experiments/drafts/round3-ret-interpretation/pilot/REPORT.md | retrain/pilot/interpretation/REPORT.md | 3832e7fa1ea1e2ca14402c5694143d893b04e4eb94260894ae018fb20e91302f |
| self/research/experiments/drafts/round3-ret-interpretation/pilot/REPORT.html | retrain/pilot/interpretation/REPORT.html | 92d33df615e848e56bedb239bd913d01535b085ce76aca169842350dfcf5c09e |
| self/research/experiments/drafts/round3-ret-interpretation/pilot/VALIDATION.json | retrain/pilot/interpretation/VALIDATION.json | 47b4a9d459bffb9fa14f039fcff55414abc45e0e56dc5f0a5571dfae98179c4b |
| self/research/experiments/drafts/round3-ret-interpretation/DIAGNOSIS.md | retrain/pilot/diagnosis/DIAGNOSIS.md | 76ba317459195c08fbc0b1fe2b91fef73ccf9ba65e10e94a41f85ef1d65bbd3a |
| self/research/experiments/drafts/round3-ret-interpretation/DIAGNOSIS.html | retrain/pilot/diagnosis/DIAGNOSIS.html | 2d8d85cb1e8d4e73effc2a6fc235a1b6c3de04acc5a11e9875506727dd718077 |
