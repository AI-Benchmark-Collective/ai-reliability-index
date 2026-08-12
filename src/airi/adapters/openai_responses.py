from __future__ import annotations

import os
from typing import Any

from airi.models import AdapterResult, TaskContext


class OpenAIResponsesAdapter:
    """OpenAI Responses API adapter.

    The API key is read by the official SDK from OPENAI_API_KEY. It is never accepted
    as a CLI argument, written to a result manifest, or included in logs.
    """

    name = "openai-responses"

    def __init__(self, model: str) -> None:
        if not model:
            raise ValueError("--model is required for the OpenAI adapter")
        if not os.environ.get("OPENAI_API_KEY"):
            raise RuntimeError("OPENAI_API_KEY is not set")
        try:
            from openai import OpenAI
        except ImportError as exc:
            raise RuntimeError(
                "Install the OpenAI extra first: pip install -e '.[openai]'"
            ) from exc
        self.model = model
        self._client = OpenAI()

    def capabilities(self) -> dict[str, bool]:
        return {
            "network": True,
            "tool_use": False,
            "seed": False,
            "usage_reporting": True,
            "trace_export": True,
        }

    def run(self, context: TaskContext) -> AdapterResult:
        response = self._client.responses.create(
            model=self.model,
            instructions=(
                "Complete the benchmark task using only the supplied evidence. "
                "Return only valid JSON matching the requested output contract."
            ),
            input=context.prompt,
        )
        usage: dict[str, int | None] = {
            "input_tokens": _usage_value(response.usage, "input_tokens"),
            "cached_input_tokens": _nested_usage_value(
                response.usage, "input_tokens_details", "cached_tokens"
            ),
            "output_tokens": _usage_value(response.usage, "output_tokens"),
        }
        return AdapterResult(
            output_text=response.output_text,
            usage=usage,
            provider_request_id=getattr(response, "_request_id", None),
            provider_metadata={},
        )


def _usage_value(usage: Any, key: str) -> int | None:
    if usage is None:
        return None
    value = getattr(usage, key, None)
    return int(value) if value is not None else None


def _nested_usage_value(usage: Any, parent: str, key: str) -> int | None:
    if usage is None:
        return None
    details = getattr(usage, parent, None)
    if details is None:
        return None
    value = getattr(details, key, None)
    return int(value) if value is not None else None
