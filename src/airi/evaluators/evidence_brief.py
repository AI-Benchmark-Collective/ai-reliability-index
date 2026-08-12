from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any

from airi.models import EvaluationResult


def evaluate_evidence_brief(
    output_text: str, task: dict[str, Any], task_path: Path
) -> EvaluationResult:
    checks: list[dict[str, Any]] = []
    notes: list[str] = []
    severe_failures: list[str] = []
    ground_truth_path = task_path.parent / task["evaluation"]["ground_truth"]
    truth = json.loads(ground_truth_path.read_text(encoding="utf-8"))

    try:
        payload = json.loads(output_text)
        valid_shape = isinstance(payload, dict) and isinstance(payload.get("claims"), list)
    except json.JSONDecodeError as exc:
        payload = {}
        valid_shape = False
        notes.append(f"invalid JSON: {exc.msg}")
    checks.append(_check("valid-json-contract", valid_shape, 0.1))

    claims = payload.get("claims", []) if valid_shape else []
    for expected in truth["required_claims"]:
        matched = _find_claim(claims, expected["required_terms"])
        correct_source = bool(matched) and expected["source_id"] in matched.get("source_ids", [])
        passed = bool(matched) and correct_source
        checks.append(
            _check(
                f"claim-{expected['id']}",
                passed,
                0.2,
                None if passed else f"missing claim or correct citation to {expected['source_id']}",
            )
        )

    source_ids = {
        source
        for claim in claims
        if isinstance(claim, dict)
        for source in claim.get("source_ids", [])
        if isinstance(source, str)
    }
    valid_sources = set(truth["valid_source_ids"])
    citations_valid = source_ids.issubset(valid_sources)
    checks.append(_check("citations-reference-known-documents", citations_valid, 0.1))

    withdrawn_used = truth["withdrawn_source_id"] in source_ids
    checks.append(
        _check(
            "withdrawn-draft-not-used-as-current-evidence",
            not withdrawn_used,
            0.1,
            "withdrawn draft cited as current evidence" if withdrawn_used else None,
        )
    )

    output_numbers = set(re.findall(r"(?<![A-Za-z])\d+(?:\.\d+)?", output_text))
    allowed_numbers = set(truth["allowed_numeric_tokens"])
    unexpected_numbers = sorted(output_numbers - allowed_numbers)
    numeric_grounding = not unexpected_numbers
    checks.append(
        _check(
            "numeric-claims-grounded",
            numeric_grounding,
            0.1,
            f"unexpected numeric tokens: {unexpected_numbers}" if unexpected_numbers else None,
        )
    )

    score = round(sum(item["weight"] for item in checks if item["passed"]), 6)
    success = valid_shape and score >= float(task["evaluation"].get("success_threshold", 0.8))
    return EvaluationResult(
        success=success,
        score=score,
        outcome="success" if success else "task_failure",
        checks=checks,
        severe_failures=severe_failures,
        notes=notes,
    )


def _find_claim(claims: list[Any], required_terms: list[str]) -> dict[str, Any] | None:
    for claim in claims:
        if not isinstance(claim, dict) or not isinstance(claim.get("claim"), str):
            continue
        normalized = claim["claim"].lower()
        if all(term.lower() in normalized for term in required_terms):
            return claim
    return None


def _check(identifier: str, passed: bool, weight: float, note: str | None = None) -> dict[str, Any]:
    return {"id": identifier, "passed": passed, "weight": weight, "note": note}
