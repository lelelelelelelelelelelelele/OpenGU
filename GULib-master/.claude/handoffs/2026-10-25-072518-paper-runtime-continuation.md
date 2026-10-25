# Handoff: paper review completed locally, dual-node implementation in progress

## Current State Summary

Continue the user's full paper goal in the same active turn: rigorous reviewer audit, repair/experiments, original V/C/E/I/P and three independent >=WA gate, then English v1 and actual LaTeX/visual checks. **Do not end merely because this milestone is saved.** Current writing_gate=not_met. Three fresh reviews all Weak Reject; no English v1 written. User does not authorize inventing scores/findings. There is substantial completed local work and a running internal implementation worker.

Continues from [prior reentry handoff](2026-10-25-062327-paper-session-restart.md), but this file supersedes its run/ownership status. Read the canonical WorkItem and live worker response before mutation.

## Important Context

Latest direct human answers in this original session:

1. “由本会话恢复原Claim继续” for AAGU-121 after another session could not attach its tree. Root successfully resumed the original Claim; do not ask again or create a new Claim.
2. “接受并授权转达本地合并请求” for SM027 candidate d8e451564bc4ad9ea562e09893810cd1c569cb72/Core0.6.0/445PASS. Root sent one explicitly authorized message to thread 01a17005-d86a-7e50-964a-8d701c2eff55, title「SM-027 · 共享检出多节点队列开发」. It has now locally merged and canonical WorkItem is accepted. **No push/publication/install/remote/GPU authorization came with that decision.** Do not send new cross-session messages without authorization.

AAGU-121's current contract still only permits local rework/tests/candidate; no merge/push/install/deploy/remote update/OpenGU real experiment, including smoke/gate. Once exact local candidate is verified, present concrete acceptance/installation/runtime decision; don't resurrect older broad permissions superseded by this contract. Public OpenGU push remains explicitly refused.

## Critical Files

- R canonical: E:/project/OpenGU/GULib-master (Git root parent OpenGU). Main was c555e63a6a2d0cb224d07d24f55ee9adad9827ee; unrelated reentry README/report/handoff dirty files belong to the other author-preparation session and were preserved.
- W paper: C:/Users/ADMIN/.codex/worktrees/paper-reentry-v1/OpenGU/GULib-master; branch codex/paper-reentry-v1. Commits 8f8fe8aa then b9936aa055ff2d11c612642c12a89840901b1d1d, last observed clean. No merge/push. Five new figures PDF/SVG/PNG plus all49 frozen inputs are committed (PDFs needed explicit add because global ignore).
- W/paper_writing/review/2026-10-25-reentry/POST_REVIEW.md/html is main review disposition; OUTLINE.v10.1.md/html and RESULTS_ARGUMENTS.md/html contain updated per-paragraph outline and Chinese result arguments. REPORT/CORE/OUTLINE.v10 are first frozen generation.
- Same directory REVIEW_INPUTS.json frozen manifest sha ade595b8711f276f4eb5c0b28715e722d95b46e21ec71c4b23dfb79ef2c7d3be. Its49 inputs were independently verified and then all verified from committed Git blobs. Never overwrite inputs/ or pretend later fixes were in first reviewer input.
- THEORY_REVIEW, EXPERIMENT_REVIEW, ANALYSIS_REVIEW MD/HTML: fresh independent reviews, each Weak Reject. They evaluated original Q1/Q2/Q3 and overall separately from B, corrected prior omissions, and did not penalize lack of English body before gate.
- D AAGU121: C:/Users/ADMIN/.codex/worktrees/dual-ssh-runners/OpenGU/GULib-master; codex/aagu-121-dual-ssh. Original9 WIP saved by standard run_git.finish as 7b859fe635d80fb1cf5cc213a8d07f616820db62 (superseded draft, not verified delivery). Standard resume then succeeded: claimId ca497160-d88a-4ed6-b422-418b7d2e1fc8, revision2, ongoing, ownerroot, session论文攻坚 -- XLX, timestamp07:14:36+08. Baselinefa8f6c75177d8053df3b7ff98b9d324bf21602f0 unchanged. New owned code changes are IN PROGRESS in D: do not commit until worker finishes.
- Canonical .workblock/items/AAGU-121/WORKITEM.md, design/consensus.md, REPORT.md/html and .workblock/runtime/AAGU-121/rework.md updated by root. Previous recovery-failure report preserved in evidence/recovery-before-original-session.md. Claim owner conflict is resolved, not a current blocker.
- SM027 canonical: E:/project/SyncMate/.workblock/items/SM-027/WORKITEM.md accepted. Main integration799b1dccb9aebfec9bc81b07fd1bb8df1605c1d2, accepted/build source d8e451564bc4ad9ea562e09893810cd1c569cb72, trees identical/combinationPASS. Version0.6.0 wheel SHA722a8e024cfb2050338a1b2c0f323f54f56aa8a2c84161d0317354ec9459fc75 at evidence/dist. Use accepted canonical interface.md and verification; original SM linked tree is being cleaned, do not depend on it. Local-only merge, no install/push.
- C config candidate: C:/Users/ADMIN/.codex/worktrees/round4-integration/OpenGU/GULib-master, commit117687cbc4a80e3dde700c854cc3378d7337ecdf over d0c9238bc47b684929876a7d5bacc7516e52fde8. EXP089111 config/Recipe files + P60GU50 files, last known unlanded; 20 obsolete untracked EXP087 files must remain excluded. Verify before using.

## Work In Progress / Agents

Internal /root/novelty_reading is running again as AAGU121 worker, not a separate user-visible Block owner. It owns D scripts/syncmate integration/install/policy/dependency, necessary experiment entry node argv/receipt/logging, removal of global Score startup scans, relevant tests and existing docs including experiments/AGENTS.md and R/self/research/RUNBOOK.md (in D copy only). Root owns canonical records and paper branch; don't touch worker files concurrently. No worker code commit yet. Ask its status/results or wait; do not spawn duplicate implementation.

Worker has: shared path corrected, no OpenGU-2/initialize compatibility, explicit node via ProjectExtension.resolve_recipe execution argv, run/train entry parsing and receipt/log node, global preflight scans removed while per-entry cache lock/HIT recheck/transactions remain. It is implementing all-registered-peer shared installation: each peer environment/status checked, anybusy/unknownblocks; coordinator maintenance.installation(node_ids=all) updates shared code once; original idle worker restart occurs in each respective SSH container, not all on coordinator. Per-peer receipts bind their own environment/Core/project/SHA.

Dependency pin now being fixed to accepted main799b plus build_sourced8 and wheel file hashes. Wheel was only extracted to R runtime for isolated PYTHONPATH tests, no pip install. First fixture test failure reason was a temporary root without Git identity -> Core accurately unknown. Worker preserved failed logs, added real independent Git checkout, retained idle assertion; nine focused tests then PASS. It must still complete genuine shared installer busy/unknown/one-update/per-peer restart+receipt tests and affected integration checks. Root requested failure details preserved, not removing meaningful checks to pass.

Important first-install seam: actual nodes may have Core0.5.1 or no Core. New v2 queue idle does not prove old global jobs/workers stopped. New code should fail closed unless explicit0.6 + initialized node queues; no migration/fallback/autoinstall. After concrete authorization, root must first establish old jobs done/old workers safely idle and all nodes confirmable, privately upgrade Core per container and initialize explicit queues via existing API, then normal shared-code installer. Do not fake readiness or remove old locks/queues.

## Scientific Results Added This Turn

analyze_existing.py reads admitted GIF160/Ret400 and e79r6 only; no producer/forward/GPU/SSH. Complete GIF primary arithmetic projection (NOT full320 admission/contract closure), unchanged sealed statistics hash0066b7d8...f8c21, n10/df9/Bonf7 critical3.461591:

- S−U budget interaction9.194 [6.001,12.388]pp
- M−U interaction4.139 [2.377,5.902]
- S−M5% .085 [−.923,1.093] (within predeclared±2)
- S−M33%5.140 [3.461,6.819] (outside)
- S−M interaction5.055 [3.225,6.885] (outside)
- K S−U44 interaction .090 [−1.925,2.105]
- D11−D10 S−U44 interaction−.691 [−2.705,1.324]

200 selected triangles reconstructed from40 integer truth cells,400 final/original Ret exact coverage. Independent reviewers recomputed, max discrepancy8.9e−16pp. Low-budget agreement doesn't satisfy all-three reproduction criterion. K/R10 broad intervals not zero/equivalent. Class0 saturation remains98.32%/5of10wholeclass; Ret difficulty plus conservativeG remains direct alternative explanation. Original Q1–Q3 must remain the spine; no requirement that each be independent innovation or that empirical work discover a new causal mechanism.

New eligible Q3 uses GIF/GE/GR, excluding oldGNNDelete/MEGU and IDEA duplicate. 900 seed profiles,144 direct pointwise contrasts,6 full source margins. Centered per-coordinate CV squared-distance margins /pp² (jackknife95): utility Cora.0568[−.281,.395],CiteSeer.00614[−.046,.058],PubMed.0874[.058,.117]; D Cora.874[.085,1.664],CiteSeer.526[.219,.832],PubMed.0326[−.013,.078]. Outcome-disclosed exploratory coordinate sensitivity. Fixed target architecture/config only, across-source actual Original-state equality NOT OBSERVED; this limits strict source-only causal/transfer claims, not all observed condition means.

Figures committed and visually inspected: F4 valid3GU+Ret two-row five-selector seven-budget curve, allSD visible (old GR42.69 cropped at45% nowfixed), redblue; F5 complete7forest; F3 e79r5 exact raw task-metric PubMed valid3GU sharedscale and ownbefore; F5B O/G/R+truth+paired finite channel; F6 full144means redblue heatmaps, colorbar clipping fixed and re-viewed. These are new adoption candidates, not proof author accepted final removal choices; preserve original sixGU archives. Captions/provenance in POST_REVIEW. F6 is appendix-priority, not automatic extra main figure.

Current C remains not_met, not merely a missing CI. Reviewers agree V/reading/traceability improved, but GIF newOriginal numerical applicability and important contribution still need actual science. EXP089 tests reliability/fairness, not a requirement to forceGIFtowardRet or destroy a genuine vulnerability. New mechanism confirmation is conditional on an important falsifiable finding, not the only acceptable paper route.

## LaTeX / Format

Existing build-paper.ps1 actually built environment template and baseline Overleaf copy using E:/Programs/texlive/2026/bin/windows. Baseline PDF W/paper_writing/latex/build/overleaf-validation/main.pdf is14pages, refsstart9,4TODO,7overfull hboxes; no undefined refs/citations. Root rendered/viewed pages7/8, oldGNNDelete table stillthere, largefig/captions and cropvisible. FORMAT_QA.md/html/json records exact PDF SHA8bf06a6c...10c4. This is not v1 or submission acceptance. OfficialWWW2027 primary source freshly checked: English sigconf anonymous review, main8 selfcontained /total12; firstpage explicit Web/track challenge. Need actual full-pageQA after scientific gate.

## Execution State / Next Steps

- Original Ret400, GIF160 + final twoGraph / R10 diagnostics complete trusted; Psource60/Ret60 complete, P GU60 notrun. EXP089 none run. Original MEGU h01,h02,h03 each native16 PASS =48of160; h04..10 unsubmitted. Do not rerun known batches.
- Root corrected stale EXP087 h01/h02 attempts from registered/not_submitted to collected_accepted/trusted_and_native_admitted, bound original receipts/admissions. h01 elapsed167s queue5; h02 elapsed173s queue6, returnunknown; cache h01method14MISS2HIT, h02MISS16. Exact evidence in B/method-admission-after119/EARLY_BATCH_STATE_RECONCILIATION.json. h03 unchanged. No scientific acceptance changed.
- Work Plan rebuild succeeded42pages/SVG,2399refs. gnnPython3.8 failsremovesuffix; bundled modernPython lacksPyYaml. Successful runner imported existing pure yaml from gnn site-packages then removed that sys.path, ran generator via runpy under modernPython. No dependency installed or code compatibility patched.
- Wait for AAGU121 worker final local implementation/check results; form standard run_git.finish candidate with exact owned paths; Verify/acceptance report and Claim awaiting_acceptance. Do not silently install from old blanket permissions.
- Need user acceptance of concrete AAGU121 and exact privateCore/OpenGUinstallation + real tests/frozen experiments authorization when candidate ready. Only ask after necessary local work reviewable. Initial old-core queue/worker transition must be explicit/safe; no active checkout update while any node busy/unknown.
- Remaining MEGU engineering driver originally hardbindscdb T3. After new actual installed SHA, retain scientific params/seed/method closure and save reviewed source equivalence/updated engineering execution handoff for never-submitted h04..10; don't rewrite old runs to newSHA. NewCore nodebinding/statusv2 doesn't migrate old handoffs or queues.
- C config commits111+50 need reviewed integration with currentmain, formal preflight, privateinstallreceipt. No future SHA invented. G1/G2 only generated after real A hessian observations. Original full320+P consumer/stats contracts stayunchanged.
- Once complete controlled scope/numerical validity and important finding, freeze newscientificreviewpackage, threefreshrole reviews≥WA plusroot V/C/E/I/P; then English v1,8/12pages, actual compile/render. Do not manufactureWA to satisfyuser goal.

## Decisions Made / Potential Gotchas

No public pushes, no test-label checkpoint rehabilitation, no pooling A10+failedA5, no seed fishing/endpoint switching, no fake GNNDelete/MEGU. The receive-only旁观 message from thread01a17001... was user-authorized to this session but does not authorize root messaging it back. Its priority matches ongoing work: existingdata prose/figures first; Q1–Q3overall separateB; numericalapplicability not forcedfidelity.

Memory used in this turn: MEMORY.md88–94, rollout01a16a78-76f1-7d83-966d-7769f38c8bec. Final userreply, whenever task actually concludes, must end with exactlyone memorycitationblock citing actualusedfiles. No memorywrite authorized.

## Immediate Next Steps

1. Check worker /root/novelty_reading progress and accepted SM027 source; keep its D edits untouched.
2. Continue local AAGU121verification/candidate before requesting concrete acceptance/install/run permission.
3. Preserve paper branch checkpointb9936aa, no premature Englishbody or WA claim. Continue original fulltask acrosscompaction.


## Later active checkpoint: before candidate finish

- W paper latest now1c6d20fa (afterb9936aa): added CHANNEL_PRECISION.md/html and ALL672 exploratory Ret-effect intervals (384 own +288 relative). Post-outcome label, pointwise and exploratoryBonf672 both saved; no newprimaryfamily. Critical edge-after-supervision S−U44 mean+.856 point95[−.067,1.779], so mean buffering is not established stablepositive. Sup−4.369[−6.202,−2.537],joint−3.514[−5.375,−1.652]; fullBonf672 for these arewide/cross0. POST_REVIEW/RESULTS_ARGUMENTS link this. Initial49 frozeninputsunmodified.
- Worker shared installer/nativeCLI suite55PASS; realGit+Core fixture validated allnodebusy/unknown gate, singleGitupdate, per-container idleworker restart/receipts, actual corruptCore bytes before/afterupdate refusedcredentials. Initialfailures preserved and repaired (CRLF fixturehash; context.use lifetime bug inCLI).
- Worker discovered ScoreBundleStore per-entry lock wrongly uses host-localPID liveness: experiments/c_target_v1/score_store.py338–366. Root approved minimal removal of immediateorphan branch, keepingO_EXCL/30sbound/HITrecheck/transaction/failurelockpreservation. Two bounded tests requested. Not cacheidentityschema change. Current native producer doesn't fingerprint thisStore file, but historical run_cora_gcn.py does fingerprint wholefile: itsRecipe fingerprint legitimatelychanges, no compatibility/identityrewrite. Workerdoingactual baseline/current identitycomparison; don't claim allhistoricalkeys unchanged.
- GUI consumer seam: CoreController.submit invokesexecution_readiness BEFORE SSHself, butcallback receives(rawpeer,definition), notnodeid/context. Rootapproved complete rawpeer uniquely matching currentexplicit registeredpeerkey; 0/multiplematchesreject, then samepolicy/receipt. Must actualController.submit testswrongnodereceipt/wrongalias/duplicatepeer stopsbeforetransport/dispatch; correctpathsameexistingCore.
- IMPORTANT INCIDENT: one CPUtest missed transportisolation and attempted one readonlySSHself. Existinglogscannotestablishwhetherconnectionoccurred. Nojob/dispatch/GPU. Root informeduserplainly and updatedcurrentcanonicalReport. Workerpreservesargv/logs, mustdefaultdenyrealssh/scp/sftp/Popen/runnetwork andmapallowednativeidentityquerytolocalrealfixture, includingtestthatunisolatedtransportisblocked BEFORE launching. Do notwrite'noSSH'/noConnectionclaimforentireBlock. Do notretryrealSSH.
- LatestlocalshortEXP014 e14r5/e14c1 showed done/complete nonstale last06:09:10/06:40:20. This is historicallastobservation, NOTcurrentallnodeidleproof. NoSSHusedbyrootforstatus.
- Current .workblock/policy.json = local-only/install. .workblock/actions/install.json STILL OLD singlehost/apply+receipt without--node/oldreceiptpath. Rootownsrecordactionupdates, workerdoesnot. Needs reviewedtwo-peer install/readBackregistration. project-installer explicitlyrequiresenvironmentupgrade asSEPARATEbootstrapaction (notroutineinstall). Beforelateruserapproval, prepareconcreteregistrationproposal; do notsilentlyexpandcurrentlyauthorizednetwork.
- Core0.6wheelmetadata Requires-Python>=3.8,PyYAML>=6; localgnn3.8supported. Actualsecondnode readinesssnapshot: bothcontainersPython3.10.8,torch2.1.2+cu118,PyG2.6.1; packageversionssameandoldCore0.5.1verified, oldshareddevice_idgpu4090 explainsneedexplicitnode. snapshotstale; formalchecksneededafterauthority. BothpeersinR/.syncmate/device.yaml now sharedcanonicalproject,/root/miniconda3/bin/python. Do notuseoldOpenGU-2path.
- Bootstrapdesignmustuseexplicitapprovedone-timeoldCoremaintenanceleaseafteroldjobscomplete/allcontainersconfirmable, installONLYacceptedCorewheel --no-index --no-deps (noCUDA/Python/dependencyrepair), preserveoldqueues/locks, initializeexplicit0.6nodequeueswithoutstartingnewworkers, thennormalsharedOpenGUinstall. Noautomaticmigration/fallbackintheproduct. Old0.5.1maintenance.installation() usesglobalgate,cooperativelypausesidleworker,doesnotitselfrestart; returnsrestartstate. Itcanholdlegacyadmissionduringapprovedpackageupgrade. Need exactsafeprocedureandregisteredwrite/networktargetsforlocalgnnplusbothprivatePythonenvs; notyetimplemented/authorized. Ifunexpectedlegacylock/state,stopwithfacts,notdeleteorautoretry. Probe mustverifyapprovedtargetpin ratherthanoldremotecheckout's0.5pin beforecodeupdate; inspectworkerimplementationforupgradeseam.
- UserlatestauthorityisONLYresumeAAGUlocalwork + acceptedSMlocalmerge. CurrentAAGUcandidateNOTformed, Nodeinstall/bootstrap/GPUSTILLNOTauthorized. Onceworkerfinishes, rootreviewexactdiff/ownedpaths, standardfinish+Verify, properacceptance-reportingModeBpair+Claimawaiting, THENaskconcreteacceptance/localmerge/privatebootstrap/install/minimalrealvalidation/frozenexperimentsdecision. Noearlypermissionforthinplan.


## 2026-10-25 08:29 - Final candidate and pending human decision

AAGU-121 final standard-finish candidate: ce1b726f4bdf1cad1cb26299cca5a4e9537852ed. All 30 committed sources verified; clean source worktree. Reuse 89 passing tests; six targeted P2 PID-label checks pass. Root reviewed the exact final P2 diff. Permanent evidence: .workblock/items/AAGU-121/evidence/local-candidate-20261025. Current REPORT.md/html passes structure validation. Browser file-protocol preview was policy-blocked; visual QA remains NOT OBSERVED, no workaround attempted.

Same Claim is awaiting_acceptance, revision3, updatedAt 2026-10-25T08:28:42+08:00. No unresolved local implementation rework; rework.md was normally removed. The OpenGU candidate has NOT been accepted by the human. No merge, installation, remote update or real OpenGU experiment is authorized yet.

SM-027 WAS accepted by the human and locally merged as 799b1dcc; Core0.6.0 accepted wheel remains in canonical SyncMate item/evidence/dist. No environment has been upgraded.

A single bundled question for exact candidate acceptance, local paper checkpoint, private Core/bootstrap/install and frozen scientific continuation is pending. Review BOOTSTRAP_PLAN.md/html and action-proposals under the same Item evidence. Both action proposals validate in agent mode; canonical actions remain unchanged. PAPER_CHECKPOINT_PROPOSAL.json lists the 13 canonical paper-navigation/review/handoff paths to preserve separately before combination merge. Recheck live ownership and dirt before staging; no stash/reset/clean.

After explicit approval: use standard same-Block closeout and actual combination verification; register separate approved bootstrap/install actions. Recheck BOTH live containers, old global queue, all old jobs and verified returns before mutation. Unknown/busy stops. Preserve history and locks. Existing maintenance controls the idle legacy worker; install only the exact private Core wheel into the three existing environments; initialize explicit queues; update shared code once; verify each node receipt and restore/start only its own worker. New empty queues, accepted dependency or fixture PASS do not prove remote readiness. No automatic retry, rollback, lock deletion or public push.

Then resume the seven missing MEGU16 batches, P60 GU, EXP089 and planned diagnostics. Preserve the 48 admitted MEGU, GIF160 and Ret400. Remote compute may be concurrent; collection stays serial in one controller. Scientific writing gate remains not_met, all three reviews Weak Reject. No English v1 or WA claim before actual new evidence and the original gate. Paper W latest 1c6d20fa; statistics, outline, red/blue figures and actual 14-page baseline TeX QA are saved there.
