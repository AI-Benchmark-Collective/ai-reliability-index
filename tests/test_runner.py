from __future__ import annotations

import json
from pathlib import Path

from airi.adapters.mock import MockAdapter
from airi.runner import run_benchmark
from airi.validation import load_and_validate_task, validate_result

TASK_PATH = Path("benchmark/tasks/evidence-brief-001/task.yaml")


def test_mock_run_writes_manifests_summary_and_report(tmp_path: Path) -> None:
    task = load_and_validate_task(TASK_PATH)
    manifests, summary = run_benchmark(task, TASK_PATH, MockAdapter(), 4, tmp_path)

    assert len(manifests) == 4
    assert summary["synthetic"] is True
    assert summary["metrics"]["success_rate"] == 0.75
    assert summary["metrics"]["outcome_consistency"] == 0.75
    assert (tmp_path / "summary.json").exists()
    assert (tmp_path / "report.html").exists()
    assert len(list(tmp_path.glob("*.result.json"))) == 4
    validate_result(json.loads(next(tmp_path.glob("*.result.json")).read_text()))
