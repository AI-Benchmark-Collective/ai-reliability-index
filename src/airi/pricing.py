from __future__ import annotations

import json
from pathlib import Path
from typing import Any


def load_pricing(path: Path | None, model: str) -> dict[str, Any] | None:
    if path is None:
        return None
    data = json.loads(path.read_text(encoding="utf-8"))
    if data.get("model") != model:
        raise ValueError(f"pricing file is for {data.get('model')!r}, not {model!r}")
    for field in ("effective_date", "source", "input_per_million", "output_per_million"):
        if field not in data:
            raise ValueError(f"pricing file missing {field}")
    return data


def estimate_cost(usage: dict[str, int | None], pricing: dict[str, Any] | None) -> dict[str, Any]:
    if pricing is None:
        return {"estimated_usd": None, "pricing_source": None, "pricing_effective_date": None}
    input_tokens = usage.get("input_tokens")
    output_tokens = usage.get("output_tokens")
    if input_tokens is None or output_tokens is None:
        estimated = None
    else:
        cached = usage.get("cached_input_tokens") or 0
        uncached = max(0, input_tokens - cached)
        cached_rate = pricing.get("cached_input_per_million", pricing["input_per_million"])
        estimated = (
            uncached * float(pricing["input_per_million"])
            + cached * float(cached_rate)
            + output_tokens * float(pricing["output_per_million"])
        ) / 1_000_000
        estimated = round(estimated, 8)
    return {
        "estimated_usd": estimated,
        "pricing_source": pricing["source"],
        "pricing_effective_date": pricing["effective_date"],
    }
