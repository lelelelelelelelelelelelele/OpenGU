import json

import pytest

pytest.importorskip("matplotlib")

from scripts.evaluation.plotting.attack_charts import generate_attack_charts, load_attack_matrix


def test_attack_chart_schema_and_outputs(tmp_path):
    payload = {
        "methods": ["GIF", "GNNDelete", "GraphEraser", "GUIDE"],
        "strategies": ["random", "degree", "pagerank", "tracin", "im", "hybrid"],
        "values": {
            "GIF": {"random": 0.009, "degree": 0.019, "pagerank": 0.013, "tracin": 0.020, "im": 0.017, "hybrid": 0.028},
            "GNNDelete": {"random": 0.068, "degree": 0.054, "pagerank": 0.054, "tracin": 0.090, "im": 0.138, "hybrid": 0.089},
            "GraphEraser": {"random": -0.070, "degree": -0.044, "pagerank": -0.030, "tracin": -0.048, "im": -0.052, "hybrid": -0.063},
            "GUIDE": {"random": -0.046, "degree": -0.083, "pagerank": -0.052, "tracin": -0.052, "im": -0.087, "hybrid": -0.123},
        },
        "unit": "ratio",
    }

    input_json = tmp_path / "attack.json"
    input_json.write_text(json.dumps(payload), encoding="utf-8")

    loaded = load_attack_matrix(input_json)
    out_dir = tmp_path / "plots"
    outputs = generate_attack_charts(loaded, out_dir)

    assert len(outputs) == 3
    for output in outputs:
        assert output.exists()
