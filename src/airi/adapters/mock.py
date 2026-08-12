from __future__ import annotations

import json

from airi.models import AdapterResult, TaskContext


class MockAdapter:
    """Offline adapter with deterministic outcome variation for demonstrations.

    It is not an AI model and its output must never appear in a model leaderboard.
    """

    name = "mock"
    model = "deterministic-demo-v1"

    def capabilities(self) -> dict[str, bool]:
        return {
            "network": False,
            "tool_use": False,
            "seed": True,
            "usage_reporting": True,
            "trace_export": True,
        }

    def run(self, context: TaskContext) -> AdapterResult:
        mode = context.run_index % 4
        claims = [
            {
                "claim": "Q3 revenue was $12.4 million.",
                "source_ids": ["DOC-01"],
            },
            {
                "claim": "Customer churn was 3.8% in Q3.",
                "source_ids": ["DOC-02"],
            },
            {
                "claim": "The enterprise export launch moved to November 18, 2026.",
                "source_ids": ["DOC-03"],
            },
        ]

        if mode == 2:
            # A deterministic citation failure demonstrates why repeated runs matter.
            claims[1]["source_ids"] = ["DOC-04"]

        payload = {
            "summary": (
                "Q3 growth remained positive, churn improved, and the enterprise export "
                "launch was delayed to address audit-log defects."
            ),
            "claims": claims,
        }
        return AdapterResult(
            output_text=json.dumps(payload, indent=2),
            usage={"input_tokens": 500, "cached_input_tokens": 0, "output_tokens": 120},
            provider_request_id=f"mock-{context.run_id}",
            provider_metadata={"synthetic": True, "mode": mode},
        )
