"""Regression tests for the dashboard config inventory semantics."""
from __future__ import annotations

import csv
from pathlib import Path

from scripts.dashboard import gen_config_inventory as gen


ROOT = Path(__file__).resolve().parents[1]
CSV_PATH = ROOT / "self" / "dashboard" / "config_inventory.csv"


def _rows_by_name():
    with CSV_PATH.open(encoding="utf-8-sig", newline="") as fh:
        return {row["name"]: row for row in csv.DictReader(fh)}


def test_inventory_csv_records_alpha0_a3_and_evidence_state_semantics():
    rows = _rows_by_name()

    a3 = rows["A3_cora_GCN_alpha0.00"]
    assert a3["done"] == "10"
    assert a3["valid"] == "10"
    assert "hybrid_alpha0.00" in a3["warning"]

    gcn = rows["phase_b_cora_gcn"]
    assert gcn["done"] == "180"
    assert gcn["valid"] == "100"
    assert gcn["accepted_remote"] == "20"
    assert gcn["rerun"] == "60"
    assert "GraphRevoker" in gcn["warning"]
    assert "remote E4" in gcn["warning"]
    assert "local evidence import" in gcn["warning"]
    assert "proper-TracIn" in gcn["warning"]

    gat = rows["phase_b_cora_gat"]
    assert gat["done"] == "180"
    assert gat["valid"] == "100"
    assert gat["accepted_remote"] == "20"
    assert gat["rerun"] == "60"

    a5 = rows["A5_ratio_0.01"]
    assert a5["done"] == "90"
    assert a5["valid"] == "50"
    assert a5["rerun"] == "40"
    assert "r0.01" in a5["warning"]
    assert "E4 only covered r0.05" in a5["warning"]
    assert "1 failed" in a5["warning"]

    arxiv_tracin = rows["phase_b_arxiv_tracin_smoke"]
    assert arxiv_tracin["done"] == "1"
    assert arxiv_tracin["valid"] == "0"
    assert arxiv_tracin["rerun"] == "1"
    assert "proper-TracIn" in arxiv_tracin["warning"]

    old_sanity = rows["sanity_graphrevoker_r05_full"]
    assert old_sanity["done"] == "6"
    assert old_sanity["valid"] == "0"
    assert old_sanity["rerun"] == "6"
    assert "legacy TracIn/Hybrid" in old_sanity["warning"]

    postfix_sanity = rows["sanity_graphrevoker_r05_notracin"]
    assert postfix_sanity["done"] == "4"
    assert postfix_sanity["valid"] == "0"
    assert postfix_sanity["rerun"] == "0"
    assert postfix_sanity["accepted_remote"] == "4"
    assert "local evidence import pending" in postfix_sanity["warning"]


def test_generator_exports_usable_warning_and_rerun_fields():
    row = {
        "file": "phase_b_cora_gcn.yaml",
        "name": "phase_b_cora_gcn",
        "cat": "main-matrix (cora)",
        "dataset": "cora",
        "model": "GCN",
        "ratio": "0.05",
        "hybrid_alpha": "",
        "n_methods": "6",
        "n_strategies": "6",
        "n_seeds": "5",
        "n_cells": "180",
        "done": "180",
        "valid": "100",
        "rerun": "60",
        "accepted_remote": "20",
        "src": "csv",
        "methods": "GIF|GNNDelete|MEGU|IDEA|GraphEraser|GraphRevoker",
        "strategies": "random|degree|pagerank|tracin|im|hybrid",
        "seeds": "42|212|722|1337|2024",
        "warning": "GraphRevoker four-strategy cells passed the remote E4 gate; local evidence import pending; proper-TracIn refresh pending.",
    }

    configs_js = gen.build_configs_array([row])

    assert "valid:100" in configs_js
    assert "acceptedRemote:20" in configs_js
    assert "rerun:60" in configs_js
    assert "warning:\"GraphRevoker four-strategy cells passed the remote E4 gate; local evidence import pending; proper-TracIn refresh pending.\"" in configs_js


def test_dashboard_template_labels_rerun_basis_beyond_graphrevoker_only():
    template = gen.TEMPLATE

    assert "rerun basis" in template
    assert "GraphRevoker post-fix rerun" in template
    assert "remote accepted/archive pending" in template
    assert "proper-TracIn refresh" in template


def test_story_metadata_connects_experiments_to_advisor_narrative():
    story_js = gen.build_story_meta_js()

    assert "Question" in story_js
    assert "Setup" in story_js
    assert "Why" in story_js
    assert "Current read" in story_js
    assert "Next decision" in story_js
    assert "proper-TracIn" in story_js
    assert "IF-concordance" in story_js
    assert "remote E4 gate" in story_js
    assert "local evidence import" in story_js
