from pathlib import Path

from forward_deployed_ai_lab.evaluation import run_benchmark, run_red_team


def test_golden_benchmark_passes(container, tmp_path: Path):
    root = Path(__file__).resolve().parents[1]
    report = run_benchmark(
        container.orchestrator,
        golden_set_path=root / "data/eval/golden_set.json",
        output_path=tmp_path / "evaluation.json",
    )
    assert report["release_gate"]["passed"] is True
    assert report["metrics"]["policy_decision_accuracy"] == 1.0
    assert report["schema_version"] == "1.1"
    assert report["project_version"] == "1.0.0rc1"
    assert len(report["dataset_sha256"]) == 64
    assert "mean_retrieved_source_coverage_proxy" in report["metric_definitions"]


def test_red_team_suite_passes(container, tmp_path: Path):
    root = Path(__file__).resolve().parents[1]
    report = run_red_team(
        container.orchestrator,
        prompts_path=root / "data/red_team/prompts.json",
        output_path=tmp_path / "red-team.json",
    )
    assert report["metrics"]["pass_rate"] == 1.0
    assert report["schema_version"] == "1.1"
    assert report["project_version"] == "1.0.0rc1"
    assert len(report["dataset_sha256"]) == 64
