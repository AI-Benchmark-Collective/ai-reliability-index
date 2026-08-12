from __future__ import annotations

import json
from pathlib import Path

from airi.adapters.mock import MockAdapter
from airi.evaluators import evaluate_evidence_brief
from airi.models import TaskContext
from airi.validation import load_and_validate_task

TASK_PATH = Path("benchmark/tasks/evidence-brief-001/task.yaml")


def test_mock_success_and_deterministic_failure() -> None:
    task = load_and_validate_task(TASK_PATH)
    success_output = MockAdapter().run(TaskContext(task, str(TASK_PATH), "", 0, "a"))
    failure_output = MockAdapter().run(TaskContext(task, str(TASK_PATH), "", 2, "b"))

    success = evaluate_evidence_brief(success_output.output_text, task, TASK_PATH)
    failure = evaluate_evidence_brief(failure_output.output_text, task, TASK_PATH)

    assert success.success is True
    assert success.score == 1.0
    assert failure.success is False
    assert failure.score == 0.7


def test_unsupported_number_loses_numeric_grounding() -> None:
    task = load_and_validate_task(TASK_PATH)
    payload = {
        "summary": "Unsupported projection of 99%.",
        "claims": [],
    }
    result = evaluate_evidence_brief(json.dumps(payload), task, TASK_PATH)
    check = next(item for item in result.checks if item["id"] == "numeric-claims-grounded")
    assert check["passed"] is False
