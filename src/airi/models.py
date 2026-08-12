from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass(frozen=True)
class TaskContext:
    task: dict[str, Any]
    task_path: str
    prompt: str
    run_index: int
    run_id: str


@dataclass
class AdapterResult:
    output_text: str
    usage: dict[str, int | None] = field(default_factory=dict)
    provider_request_id: str | None = None
    provider_metadata: dict[str, Any] = field(default_factory=dict)
    error: str | None = None


@dataclass(frozen=True)
class EvaluationResult:
    success: bool
    score: float
    outcome: str
    checks: list[dict[str, Any]]
    severe_failures: list[str]
    notes: list[str]
