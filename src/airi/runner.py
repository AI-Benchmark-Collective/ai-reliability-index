from __future__ import annotations

import hashlib
import json
import time
import uuid
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

from airi.adapters.base import AgentAdapter
from airi.evaluators import evaluate_evidence_brief
from airi.models import EvaluationResult, TaskContext
from airi.pricing import estimate_cost
from airi.reporting import write_html_report, write_summary
from airi.validation import validate_result


def build_prompt(task: dict[str, Any], task_path: Path) -> str:
    parts = ["USER REQUEST\n" + task["objective"]["user_request"].strip()]
    fixtures = task["environment"].get("fixtures", [])
    if fixtures:
        parts.append("EVIDENCE DOCUMENTS")
    for relative in fixtures:
        fixture_path = task_path.parent / relative
        parts.append(f"--- {relative} ---\n{fixture_path.read_text(encoding='utf-8').strip()}")
    return "\n\n".join(parts) + "\n"


def run_benchmark(
    task: dict[str, Any],
    task_path: Path,
    adapter: AgentAdapter,
    runs: int,
    output_dir: Path,
    pricing: dict[str, Any] | None = None,
) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    if runs < 1:
        raise ValueError("runs must be at least 1")
    output_dir.mkdir(parents=True, exist_ok=True)
    prompt = build_prompt(task, task_path)
    task_digest = hashlib.sha256(task_path.read_bytes()).hexdigest()
    manifests: list[dict[str, Any]] = []

    for run_index in range(runs):
        run_id = str(uuid.uuid4())
        started = datetime.now(UTC)
        monotonic_start = time.perf_counter()
        context = TaskContext(
            task=task,
            task_path=str(task_path),
            prompt=prompt,
            run_index=run_index,
            run_id=run_id,
        )
        try:
            adapter_result = adapter.run(context)
            evaluation = _evaluate(adapter_result.output_text, task, task_path)
            output_text = adapter_result.output_text
        except Exception as exc:  # noqa: BLE001 - external adapter failures must be recorded.
            from airi.models import AdapterResult

            adapter_result = AdapterResult(output_text="", error=f"{type(exc).__name__}: {exc}")
            evaluation = EvaluationResult(
                success=False,
                score=0.0,
                outcome="infrastructure_failure",
                checks=[],
                severe_failures=[],
                notes=[adapter_result.error],
            )
            output_text = ""

        duration = time.perf_counter() - monotonic_start
        completed = datetime.now(UTC)
        output_file = output_dir / f"{run_index + 1:03d}-{run_id}.output.txt"
        output_file.write_text(output_text, encoding="utf-8")
        manifest = {
            "schema_version": "0.1",
            "run_id": run_id,
            "task": {
                "id": task["task"]["id"],
                "version": task["task"]["version"],
                "source_path": str(task_path),
                "source_sha256": task_digest,
            },
            "system": {
                "adapter": adapter.name,
                "model": adapter.model,
                "capabilities": adapter.capabilities(),
                "provider_request_id": adapter_result.provider_request_id,
            },
            "configuration": {
                "run_index": run_index,
                "fresh_context": True,
                "retry_count": 0,
            },
            "timing": {
                "started_at": started.isoformat(),
                "completed_at": completed.isoformat(),
                "duration_seconds": round(duration, 6),
            },
            "usage": adapter_result.usage,
            "cost": estimate_cost(adapter_result.usage, pricing),
            "intervention": {"count": 0, "events": []},
            "outcome": {
                "category": evaluation.outcome,
                "success": evaluation.success,
                "score": evaluation.score,
                "checks": evaluation.checks,
                "severe_failures": evaluation.severe_failures,
                "notes": evaluation.notes,
            },
            "artifacts": {"output_file": output_file.name},
        }
        validate_result(manifest, source=run_id)
        manifest_path = output_dir / f"{run_index + 1:03d}-{run_id}.result.json"
        manifest_path.write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
        manifests.append(manifest)

    summary = write_summary(manifests, output_dir / "summary.json")
    write_html_report(summary, output_dir / "report.html")
    return manifests, summary


def _evaluate(output_text: str, task: dict[str, Any], task_path: Path) -> EvaluationResult:
    evaluator_type = task["evaluation"].get("type")
    if evaluator_type == "evidence_brief":
        return evaluate_evidence_brief(output_text, task, task_path)
    raise ValueError(f"unsupported evaluator type: {evaluator_type!r}")
