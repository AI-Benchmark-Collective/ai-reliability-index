from __future__ import annotations

import math
import statistics
from collections import Counter
from typing import Any


def rate(numerator: int, denominator: int) -> float | None:
    if denominator < 0 or numerator < 0 or numerator > denominator:
        raise ValueError("invalid numerator or denominator")
    return None if denominator == 0 else numerator / denominator


def wilson_interval(
    successes: int, total: int, z: float = 1.959963984540054
) -> tuple[float, float] | None:
    if total < 0 or successes < 0 or successes > total:
        raise ValueError("invalid successes or total")
    if total == 0:
        return None
    proportion = successes / total
    denominator = 1 + (z * z / total)
    center = (proportion + z * z / (2 * total)) / denominator
    margin = (
        z
        * math.sqrt((proportion * (1 - proportion) / total) + z * z / (4 * total * total))
        / denominator
    )
    return max(0.0, center - margin), min(1.0, center + margin)


def outcome_consistency(outcomes: list[str]) -> float | None:
    if not outcomes:
        return None
    return max(Counter(outcomes).values()) / len(outcomes)


def nearest_rank_percentile(values: list[float], percentile: float) -> float | None:
    if not values:
        return None
    if not 0 < percentile <= 1:
        raise ValueError("percentile must be in (0, 1]")
    ordered = sorted(values)
    rank = max(1, math.ceil(percentile * len(ordered)))
    return ordered[rank - 1]


def aggregate(manifests: list[dict[str, Any]]) -> dict[str, Any]:
    eligible = [m for m in manifests if m["outcome"]["category"] != "infrastructure_failure"]
    successes = sum(bool(m["outcome"]["success"]) for m in eligible)
    severe = sum(bool(m["outcome"]["severe_failures"]) for m in eligible)
    latencies = [float(m["timing"]["duration_seconds"]) for m in manifests]
    outcomes = [str(m["outcome"]["category"]) for m in eligible]
    interval = wilson_interval(successes, len(eligible))
    return {
        "total_runs": len(manifests),
        "eligible_runs": len(eligible),
        "successful_runs": successes,
        "success_rate": rate(successes, len(eligible)),
        "success_rate_wilson_95": list(interval) if interval else None,
        "outcome_consistency": outcome_consistency(outcomes),
        "severe_failure_rate": rate(severe, len(eligible)),
        "latency_seconds_median": statistics.median(latencies) if latencies else None,
        "latency_seconds_p95": nearest_rank_percentile(latencies, 0.95),
    }
