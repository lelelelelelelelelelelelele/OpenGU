# -*- coding: utf-8 -*-
"""Read-only source audit; outputs belong only to this inventory directory."""
from __future__ import annotations

import csv
import hashlib
import itertools
import json
from collections import Counter
from datetime import datetime, timezone, timedelta
from pathlib import Path

OUT = Path(__file__).resolve().parent
ROOT = OUT.parents[3]


def read(path):
    return json.loads((ROOT / path).read_text(encoding="utf-8"))


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def write_json(name, obj):
    (OUT / name).write_text(json.dumps(obj, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def references(obj):
    if isinstance(obj, dict):
        if isinstance(obj.get("path"), str):
            yield obj["path"]
        for value in obj.values():
            yield from references(value)
    elif isinstance(obj, list):
        for value in obj:
            yield from references(value)


USES = {
    "007": ("运行链路验证", "已接受4输出gate；只能支持链路有效，不是大规模科学样本。"),
    "008": ("定义/待核对", "无现行配置、运行或分析；不能称K5参照已完成。081的五节点与五个请求重复不同。"),
    "010": ("指标覆盖", "已复用011的207请求/1242配对；不能因独立analysis not_started写成Flip/Hop未计算，也不能重复计样本。"),
    "011": ("主实验", "e11r1的1449格完成且分析完成，新协议待科学接受；当前partial是新增ETR范围未执行，不能降级已有主表。"),
    "012": ("既有结果分析", "无需GPU；已有历史分解，Flip/Hop可消费010/011；analysis note等待010已漂移。"),
    "013": ("来源前驱", "756格/648配对完成；后续079十seed覆盖，不能再累计成独立重复；部分highlights仍说079未执行。"),
    "014": ("大图selector部分完成", "ogbn-arxiv Random/Degree与R-point已可信完成；IM运行中、D-full未提交；只能支持selector规模/成本，无大图GU效果。"),
    "015": ("设计/接口", "分阶段设计由031/032承接；配置存在不等于17方法大矩阵完成。"),
    "021": ("定义/待核对", "无现行配置、拟合或计时结论；已有014/056实测可回答部分成本问题，不能把本实验算完成。"),
    "022": ("定义/待核对", "无独立探针或外推结果；用014/056实测替代泛称大图无证据，但不能冒认完成022。"),
    "027": ("恢复待定", "无确认现行结果；历史120条件不能直接复用作当前collateral证据。"),
    "031": ("选点机制支撑", "历史72条件/252排名比较已接受；另有0920新72格run，不能继承0909接受；适于source/参数消融。"),
    "032": ("重训与近似支撑", "3000轮360格Retrain-only待审；可对比source/参数/曲率近似，不能替代GU攻击端点。"),
    "039": ("定义/待核对", "CP3/CP6仅登记，无当前独立运行/分析，不应写成已有trajectory机制证据。"),
    "051": ("请求抽样变异", "150格、10个独立Random请求、固定训练seed42、四GU+Retrain；已有分布，不能写项目无请求重复；历史协议不直接并入新011。"),
    "053": ("IM配置与旧下游", "36采样诊断+96下游分开；已接受限定用途。RR65536主表是配置选择，不是充分性/最优性证明。"),
    "056": ("大图selector完成", "ogbn-arxiv RR1024单次真实MISS、K5927、366.55s、内存采样7.59GiB，执行已接受；分析尚未登记，无大图GU。"),
    "058": ("定义/待核对", "无目标backbone泛化矩阵；079是换选点模型而不是换victim backbone。"),
    "059": ("数值失败与忠实性", "12格真实失败诊断保留，负曲率和尺度上界给后续移位校准依据；不是有效GU结果。当前REPORT已接受诊断交付而analysis仍pending。"),
    "061": ("基础模型有效性", "H16/H64权重训练/导出已接受；不能等同求解稳定或GU有效。"),
    "062": ("数值有效性协调", "四组PT校准+84格验证已接受；协调记录不新增独立样本。"),
    "065": ("数值校准", "Cora H16/H64校准已完成；冻结参数非按F1选取，依赖各自checkpoint。"),
    "066": ("数值与no-update对照", "Cora两宽度42格验证，3个新Random请求、T100/200/400；有同图Original/retained logits/flip对照，不能说完全无no-update证据。"),
    "067": ("数值与no-update对照", "CiteSeer H64 21格/115产物已验证；H16暂缓；同图no-update accuracy与非退化logits检查不是080战略预算机制校准。"),
    "068": ("数值与no-update对照", "PubMed H64 21格/115产物已验证；H16暂缓；仅支持固定PT、10%三Random请求。"),
    "078": ("baseline/训练有效性", "五组隔离轨迹与checkpoint来源诊断已完成；含validation选点、P0身份复评；并非都只是未采用checkpoint，亦非新多seed主结果。"),
    "079": ("主实验", "e79r6的2520格/2160配对十seed完成，分析完成待科学接受；当前partial仅ETR扩展未执行。"),
    "080": ("预算主实验", "2016格/1722配对已完成待科学接受，固定split三seed旧分片协议；非全部方法预算扩展的新版确认。"),
    "081": ("小请求诊断", "同一Random五节点、三训练seed已可信完成；不是K5五请求噪声参照，无Retrain，旧协议不能直接当新版稳定性验证。"),
    "082": ("分片训练/聚合有效性", "live记录滞后：除Cora CPU，引用报告已有CiteSeer/PubMed GPU12轨迹/384指标、四聚合臂；300轮选择已接受，单seed非全局最优。"),
    "083": ("新协议正式gate", "6格/13文件可信，四GU端点MISS；支撑新loss+300轮真实执行，非独立大矩阵科学验证。"),
}

records = []
for path in sorted((ROOT / "self/research/experiments").glob("EXP-*.json")):
    d = json.loads(path.read_text(encoding="utf-8"))
    ap = ROOT / "self/research/analyses" / path.name
    a = json.loads(ap.read_text(encoding="utf-8")) if ap.exists() else None
    n = d["id"].split("-")[1]
    category, use = USES[n]
    refs = sorted(set(references(d)) | set(references(a)))
    deliveries = []
    for ref in refs:
        if ref.startswith(".syncmate/deliveries/") and (ROOT / ref).is_file():
            receipt = read(ref)
            result = receipt.get("result", {})
            project = result.get("project_acceptance", {})
            deliveries.append({"path": ref, "receipt_sha256": digest(ROOT / ref), "status": result.get("status"), "project_passed": project.get("passed"), "accepted_cells": project.get("accepted_cells"), "scientific_acceptance": project.get("scientific_acceptance"), "verify_summary": result.get("verify", {}).get("summary")})
    records.append({
        "id": d["id"], "title": d["title"], "scope": d["scope"], "question": d["question"],
        "source": path.relative_to(ROOT).as_posix(), "source_sha256": digest(path),
        "analysis_source": ap.relative_to(ROOT).as_posix() if ap.exists() else None,
        "analysis_source_sha256": digest(ap) if ap.exists() else None,
        "preparation": d["preparation"], "execution": d["execution"],
        "analysis": a.get("analysis") if a else None, "decision": a.get("decision") if a else None,
        "category": category, "paper_use_judgment": use,
        "configuration_inventory": [{**c, "exists": (ROOT / c["path"]).exists()} for c in d.get("configs", [])],
        "attempts": [dict({k: v for k, v in at.items() if k not in ("runtime", "evidence")}, evidence=at.get("evidence", []), runtime={k: v for k, v in at.get("runtime", {}).items() if k in ("job_started", "actual_status", "actual_seconds", "actual_basis", "cache")}) for at in d["attempts"]],
        "delivery_evidence": deliveries,
        "referenced_existing_files": [ref for ref in refs if (ROOT / ref).is_file()],
        "referenced_absent_paths": [ref for ref in refs if not (ROOT / ref).exists()],
        "sources": d.get("sources", []),
    })

# Recompute the actual EXP-082 GPU factorial grid and 300-to-3000 changes.
base = ROOT / ".workblock/items/AAGU-104/evidence/ssh-gpu2"
rows = list(csv.DictReader((base / "all_curve_metrics.csv").open(encoding="utf-8")))
axes = {k: sorted({r[k] for r in rows}, key=lambda x: int(x) if k == "epoch" else x) for k in ("dataset", "method", "phase", "epoch", "aggregation_arm")}
keys = [tuple(r[k] for k in axes) for r in rows]
expected = list(itertools.product(*(axes[k] for k in axes)))
assert len(rows) == 384 and len(set(keys)) == 384 and set(keys) == set(expected)
look = {(r["dataset"], r["method"], r["phase"], r["epoch"], r["aggregation_arm"]): r for r in rows}
changes = []
for dataset, method, phase in itertools.product(axes["dataset"], axes["method"], axes["phase"]):
    first = look[dataset, method, phase, "300", "corrected"]
    last = look[dataset, method, phase, "3000", "corrected"]
    changes.append({"dataset": dataset, "method": method, "phase": phase,
                    "validation_accuracy_at_300_pct": float(first["validation_accuracy_pct"]),
                    "validation_accuracy_at_3000_pct": float(last["validation_accuracy_pct"]),
                    "validation_gain_3000_minus_300_pp": float(last["validation_accuracy_pct"]) - float(first["validation_accuracy_pct"])})
stored = list(csv.DictReader((base / "epoch_comparison.csv").open(encoding="utf-8")))
assert len(stored) == 12
for c in changes:
    match = next(s for s in stored if (s["Dataset"], s["Method"], s["Phase"]) == (c["dataset"], c["method"], c["phase"]))
    assert abs(c["validation_gain_3000_minus_300_pp"] - float(match["Val gain 3000-300 (pp)"])) < 1e-10
manifest = json.loads((base / "archive_manifest.json").read_text(encoding="utf-8"))
archive_checks = [{"path": str((base / name).relative_to(ROOT)).replace("\\", "/"), "expected_sha256": sha, "observed_sha256": digest(base / name), "matches": digest(base / name) == sha} for name, sha in manifest["files"].items() if (base / name).is_file()]
assert all(x["matches"] for x in archive_checks)
with (OUT / "EXP082_recomputed_validation_changes.csv").open("w", encoding="utf-8", newline="") as f:
    writer = csv.DictWriter(f, fieldnames=list(changes[0])); writer.writeheader(); writer.writerows(changes)
epoch_audit = {"rows": len(rows), "axes": axes, "complete_factorial_grid": True, "training_trajectory_count": 12,
               "interpretation": "384 = 2 datasets x 2 methods x 3 phases x 8 epochs x 4 aggregation arms; repeated measurements of 12 training trajectories, not 384 independent experiments.",
               "min_validation_gain_pp": min(c["validation_gain_3000_minus_300_pp"] for c in changes),
               "max_validation_gain_pp": max(c["validation_gain_3000_minus_300_pp"] for c in changes),
               "archive_hash_checks": archive_checks, "changes": changes,
               "live_record_drift": "EXP-082.json still says CiteSeer/PubMed SSH not started; explicitly referenced AAGU-104 current report and GPU archive establish completed and accepted 300-epoch schedule diagnostics. No live state was edited."}

# Hash-check only the already collected selector results; no datasets/caches are loaded.
selector_rows = []
for run, job_wall, job in [("exp014-selector-baselines/e14b1", 54.0, "exp014-20261024-e14b1"), ("exp014-selector-r-point/e14r3", 364.0, "exp014-20261024-e14r3")]:
    root = ROOT / "results/runs/gpu4090" / run
    d = json.loads((root / "run.json").read_text(encoding="utf-8"))
    delivery = read(f".syncmate/deliveries/{job}.json")["result"]
    for item in delivery["verify"]["verified"]:
        local = ROOT / "results/runs/gpu4090" / item["path"][len("results/runs/"):]
        assert digest(local) == item["sha256"]
    for cell in d["cells"]:
        p = root / cell["path"] / "selection.json"; s = json.loads(p.read_text(encoding="utf-8"))
        ns = s["selected_nodes"]
        assert len(ns) == len(set(ns)) == s["requested_k"] == 5927 and min(ns) >= 0 and max(ns) < 169343
        assert digest(p) == cell["files"]["selection.json"]["sha256"]
        timing = cell["timing"]
        selector_rows.append({"selector": cell["conditions"]["selector"], "node_count": 169343, "candidate_count_from_receipt": 118540,
                              "requested_k": s["requested_k"], "nodes_unique_and_in_id_range": True,
                              "candidate_membership": "project acceptance recorded PASS; this audit did not load the remote Dataset candidate mask",
                              "selection_id": s["selection_id"], "selection_file": p.relative_to(ROOT).as_posix(),
                              "selection_sha256": digest(p), "job_wall_seconds": job_wall, "job_wall_shared": len(d["cells"]) > 1,
                              "access_wall_seconds": timing["current_access"]["wall_seconds"],
                              "exclusive_phases": timing["current_access"]["phase_seconds_exclusive"],
                              "selection_seconds": timing["selection_seconds"], "score_access_seconds": timing["score_access_seconds"],
                              "cache": cell["cache"], "producer_called": cell["producer_called"],
                              "delivery_status": delivery["status"], "scientific_acceptance": delivery["project_acceptance"]["scientific_acceptance"]})

# Extract the overlooked no-update/numerical coverage without extrapolating its range.
calibration = []
for number, suffix in [(66, "h16"), (66, "h64"), (67, "h64"), (68, "h64")]:
    rel = f"self/research/analyses/EXP-{number:03d}/validation-{suffix}-20260924.json"; d = read(rel)
    calibration.append({"source": rel, "sha256": digest(ROOT / rel), "verified_artifacts": d.get("verified_artifacts"),
                        "cells": d.get("cells"), "gate": d.get("numerical_gate", d.get("observer_gate")),
                        "utility_fields": sorted({k for request in d.get("utility", {}).values() for method in request.values() if isinstance(method, dict) for k in method}),
                        "limitations": d.get("limitations", d.get("boundary")),
                        "raw_utility": d.get("utility")})

audit = {"generated_at": datetime.now(timezone(timedelta(hours=8))).isoformat(),
         "scope": "All top-level Work Plan experiment records and matching versioned analysis records; explicit evidence links only. No GPU, SSH, sync, commit, experiment-state or scientific-decision mutation.",
         "record_count": len(records), "matching_analysis_record_count": sum(r["analysis_source"] is not None for r in records),
         "record_counts_are_not_independent_experiment_counts": True,
         "outline_snapshot_sha256": digest(ROOT / "paper_writing/outline/OUTLINE.md"),
         "experiments": records, "exp082_cpu_reanalysis": epoch_audit,
         "exp014_collected_selector_audit": selector_rows, "fixed_pt_validation_coverage": calibration}
write_json("INVENTORY.json", audit)
write_json("EXP014_collected_selector_audit.json", selector_rows)
write_json("EXP082_validation_audit.json", epoch_audit)
write_json("validation.json", {"passed": True, "records": len(records), "analysis_records": audit["matching_analysis_record_count"],
                                "exp082_factorial_rows": len(rows), "exp082_archive_files_hash_verified": len(archive_checks),
                                "exp082_epoch_comparison_rows_recomputed": len(changes), "exp014_collected_cells_hash_verified": len(selector_rows),
                                "sources_not_modified": True})

header = """# 全实验库存与提纲遗漏审查

本报告以2026-10-24（Asia/Shanghai）本地证据快照为准。扫描全部31份顶层 `self/research/experiments/EXP-*.json` 与27份对应版本化分析记录；只沿明确引用追踪关键报告、回传回执与原始CSV。没有启动GPU、连接SSH、同步、提交，或修改实验/科学状态。此库存的HTML由父报告统一生成。

**关键修正：详细提纲正确保留了011/079/080三个主科学模块，但漏掉一层已经完成的实验有效性支撑。项目并非只有三个矩阵和若干待补实验。** 应将这些材料接入 Experimental Design 的实验有效性小节和实现附录，而不是一律新增主RQ。库存ID包括协调、前驱、复用指标与诊断，不可将31个ID或所有cell求和成独立科学样本。

## 最重要的六项修正

1. **分片300轮不是未经检验的任意选择。** `EXP-082.json`的live描述停在Cora CPU、CiteSeer/PubMed SSH未启动；它明确引用的 [AAGU-104报告](../../../../.workblock/items/AAGU-104/REPORT.md) 第21、48–53、65、86行已经记录三数据集诊断、GPU完成及2026-10-23用户接受300轮选择。当前CSV确有384行：2数据集×2方法×3阶段×8轮数×4聚合臂，来自12条训练轨迹，不是384个独立重复。本审查复算corrected臂12组300→3000验证变化，范围 **−0.900901～+0.900901 pp**，与归档epoch_comparison逐项一致；GPU归档逐文件哈希验证通过。Cora另有CPU曲线。它部分回应欠训练/轮数任意质疑；不能证明300轮对所有seed最优。live状态漂移在此记录，不自动改状态。

2. **GIF/IDEA已有求解、非退化与no-update有效性验证。** [062收口](../../../../self/research/analyses/EXP-062/closeout-20260924.md) 第3–16行明确四组条件（CoraH16/H64、CiteSeerH64、PubMedH64），共84格Validate；校准Random104245，验证独立请求104246/104247/104248，10%预算、T100/200/400。F1不选参；检查HVP、移位残差、更新非退化。066 H64保存original/retained同图no-update logits距离、预测翻转与accuracy；067/068保存两图no-update accuracy及非零logits检查。**不能说项目完全缺Original/no-update对照**；但该覆盖是固定PT、三Random请求，不是080战略大预算的GU/Original/Retrain距离与重训自然波动校准。正移位也改变方程，不能将稳定求解写成原论文精确遗忘保证。

3. **已有真实大图selector成本证据，且014新增结果已回传。** [056报告](../../../../.workblock/items/AAGU-056/REPORT.md) 第7–15行是ogbn-arxiv RR1024，K5927、实际MISS、Selector **366.55 s**、进程380.39 s、5秒采样内存峰值7.59GiB；执行已接受，可行性分析未登记。014当前已有Random/Degree合并基线与R-point可信结果，169,343节点、118,540候选、K5927；两作业wall **54 s / 364 s**。R-point cell访问324.512s，其中模型准备48.060s、selector_access276.452s；Random/Degree访问2.601/4.642s。三份Selection的文件哈希、5927个唯一合法节点ID均复核。candidate-mask成员资格以项目回执PASS为据，本审查不加载正式Dataset。IM-RR65536当前running，D-full尚无新attempt。**足以在成本/规模附录报告已观测可运行性；不足以声称大图GU效果或真实Web部署验证。** 不能用不同RR规模和执行版本直接推导加速比。

4. **Random请求分布不是空白。** [051报告](../../../../.workblock/items/AAGU-051/REPORT.md) 第9–31、39–53行记录三数据集×10个预定Random请求×四GU+Retrain=150输出/120配对，固定训练seed42，控制请求抽样变异。Cora GNNDelete after均值65.701%、SD4.444pp、范围62.177–74.908%；PubMed SD1.745pp、CiteSeer0.315pp。其3000轮前的历史协议不能并到新011；新版011本身也有每训练seed10个Random请求。可用现有逐请求数据解释“请求抽样 vs 训练seed”，无需将EXP-008/K5未完成泛化成完全没有噪声参照。051不校准同一固定请求的重复Retrain自然波动。

5. **基础模型质量及checkpoint选择已有独立诊断。** [078训练轨迹](../../../../self/research/experiments/drafts/AAGU-078-citeseer-training-diagnostic-20260923/README.md) 第13–42行：CiteSeerH64验证准确率峰值76.88%@24，末轮74.77%，末轮test74.62%，与正式053P0的74.47%相近；后续[验证集选点](../../../../self/research/experiments/drafts/AAGU-078-citeseer-h16-baseline-20260924/README.md) 取得H64 test77.33%，候选未替换正式模型。[终轮P0来源](../../../../self/research/experiments/drafts/AAGU-078-final-epoch-p0-20260924/README.md) 分清三图H16/H64和实际053H64 cache身份。Cora[完整轨迹](../../../../self/research/experiments/drafts/AAGU-078-cora-h16-best-checkpoint-20260924/README.md)显示patience5选点反而低3.14pp，full3000验证峰值候选高1.11pp；不能简单宣称早停总会提高。已有结果可回应低CiteSeer基线/模型是否误配；仍只是一split/一seed诊断，未证明GU响应对checkpoint选择不敏感。

6. **081/083是有价值的诊断，不是新科学规模。** [081完成摘要](../../../../.syncmate/citeseer-k5-20261019/completion/REPORT.md) 第21–31行：同一Random五节点的GraphRevoker GPA+optimal，seed42/212/2024 accuracy变化+0.369/−0.185/−3.506pp；无Retrain，且是旧协议。它反驳“一定小删就稳定”，不能当K5五请求分布或新版机制证据。083为新loss+300轮正式6格gate，13文件可信，四GU输出MISS、两个Retrain HIT；见gate-analysis.json。说明真实执行链成立，不可替代后续011/079完整结果。

## 完整库存：定义、运行、分析与科学决定分开

下表四段状态依次为准备/执行/分析/科学决定，均是记录原值；`accepted`不是整项所有新批次自动被接受，需读右列限定。`—`表示没有对应analysis记录。配置文件存在性、attempt与delivery回执状态详见INVENTORY.json。

| ID | 名称 | 四段状态 | 真实层次与论文用途 |
|---|---|---|---|
"""
lines = [header]
for record in records:
    state = "/".join([record["preparation"]["state"], record["execution"]["state"], (record["analysis"] or {}).get("state", "—"), (record["decision"] or {}).get("state", "—")])
    lines.append(f"| {record['id']} | {record['title']} | {state} | {record['paper_use_judgment']} |\n")
lines.append("""
## 对详细提纲的具体调整建议

- **保持主文Q1–Q3及011/079/080模块，不靠增加RQ制造完整性。** 在第5章增加紧凑的“实验有效性与实现核验”段/表，将059→062/065–068的失败保留与稳定校准、078的checkpoint来源、082→083的新分片协议依据接入；提纲当前第283行仅写“新分片损失、300轮”，没有给选择依据。
- **附录A应新增数值与训练有效性表。** 四行PT校准/验证范围、300/3000分片验证变化、baseline选择诊断。保留原生求解、移位、零噪声IDEA与GraphRevoker变体，既承认已做的控制，也明示仍缺什么。模型训练有效性不等同于攻击机制成立。
- **附录成本/规模可以由已完成的014/056支撑。** 提纲第115行不另设大图/效率RQ是合理的，但完全不呈现大图运行事实会丢掉可复核优势；用一小表分别写规模、请求量、selector配置、真实wall、缓存及scope，IM当前未完成单列，不把运行中的记录写成结果。
- **R0/T2机制支撑接回031/032真实全层次。** 031有完整排名、source/全参数/邻域近似对照及历史时序观测；032有360个当前Retrain端点。最近一次031新run与历史已接受run分开，较旧的计时不用于当前严格加速率。读现稿附录不足以代表完整库存。
- **请求抽样变异层面用051及新011已有重复。** 独立训练、独立请求、固定split各回答不同不确定性；多请求已存在，但未等于多个split或同一请求重复Retrain。051四方法不含GIF/IDEA，不将前驱013/079与指标复用010重复计数。
- **仍真实缺少的结论不能被新库存“补成”。** EXP-058无目标backbone泛化；079仅换selector模型。021/022无正式拟合/外推，039无独立CP3/CP6，027无可信当前恢复边界；完整方法特定同家族Retrain、战略预算Original距离和同请求自然重训变异、真实Web权限/用户所有权验证仍未被这些诊断闭合。

## 可信核验与本地新分析

本轮CPU增量仅为两项库存核验，不触碰父agent负责的011/079端点分析：

1. 从082原CSV复算12组corrected聚合下300→3000验证变化，核验384行完整笛卡尔结构及归档文件SHA；结果见 `EXP082_recomputed_validation_changes.csv`、`EXP082_validation_audit.json`。
2. 消费014已经完成的两份delivery和run/Selection，核验回执SHA与节点数/唯一性/ID范围，提取真实wall边界；结果见 `EXP014_collected_selector_audit.json`。没有任何GPU运行或补传。

所有31记录及27分析文件的读取时SHA、attempt范围、现存配置与缺失引用、delivery状态、科学决定原文均保留于 `INVENTORY.json`。它是可复核快照，不拥有live实验状态；读到的路径缺失不自动判定实验未执行，明确的state/report漂移也不在此静默修补。新011/079/080结果仍待科学审阅；082的接受只覆盖300轮选择及指定训练诊断。输出完整性检查见 `validation.json`。
""")
(OUT / "INVENTORY.md").write_text("".join(lines), encoding="utf-8")
print(json.dumps({"records": len(records), "analyses": audit["matching_analysis_record_count"], "exp082_rows": len(rows), "archive_hash_checks": len(archive_checks), "exp014_cells": len(selector_rows), "output": str(OUT)}, ensure_ascii=False))
