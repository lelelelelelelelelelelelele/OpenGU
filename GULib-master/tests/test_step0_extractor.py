from pathlib import Path

from scripts.evaluation.metrics import extractor


def test_extract_metrics_from_log(tmp_path):
    log = tmp_path / "GIF_GCN_cora_r0.005.log"
    log.write_text(
        """
Performance Metrics:
Poison F1 Score: 0.9000
Unlearn F1 Score: 0.8708
Average AUC Score: 0.7401
Average Training Time: 10.2
Average Unlearning Time: 1.3

Epoch: 99 | F1 Score: 0.9123 | Loss
Original F1 Score: 0.9123
""",
        encoding="utf-8",
    )

    metrics = extractor.extract_metrics_from_log(log)
    assert metrics["f1_after"] == 0.8708
    assert metrics["auc"] == 0.7401
    assert metrics["f1_before"] == 0.9123


def test_generate_metrics_summary_and_save(tmp_path):
    logs_dir = tmp_path / "logs"
    logs_dir.mkdir(parents=True)
    (logs_dir / "GNNDelete_GCN_cora_r0.02.log").write_text(
        """
Performance Metrics:
Unlearn F1 Score: 0.8000
Average Unlearning Time: 3.5

Loss: 0.123, Accuracy: 0.800, Recall: 0.790, F1: 0.805
best: 0.890
""",
        encoding="utf-8",
    )

    out_json = tmp_path / "out.json"
    all_metrics, availability, output_path = extractor.run_extraction(logs_dir, out_json, print_table=False)

    assert "GNNDelete" in all_metrics
    assert "0.02" in all_metrics["GNNDelete"]
    assert availability["GNNDelete"]["f1"] is True
    assert output_path.exists()
