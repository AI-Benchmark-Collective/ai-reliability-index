from __future__ import annotations

import html
import json
from pathlib import Path
from typing import Any

from airi.metrics import aggregate


def load_manifests(directory: Path) -> list[dict[str, Any]]:
    manifests: list[dict[str, Any]] = []
    for path in sorted(directory.glob("*.result.json")):
        manifests.append(json.loads(path.read_text(encoding="utf-8")))
    return manifests


def write_summary(manifests: list[dict[str, Any]], path: Path) -> dict[str, Any]:
    if not manifests:
        raise ValueError("no result manifests found")
    first = manifests[0]
    summary = {
        "schema_version": "0.1",
        "task": first["task"],
        "system": {
            "adapter": first["system"]["adapter"],
            "model": first["system"]["model"],
        },
        "synthetic": first["system"]["adapter"] == "mock",
        "metrics": aggregate(manifests),
        "run_ids": [manifest["run_id"] for manifest in manifests],
    }
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(summary, indent=2) + "\n", encoding="utf-8")
    return summary


def write_html_report(summary: dict[str, Any], path: Path) -> None:
    metrics = summary["metrics"]
    success = _percent(metrics["success_rate"])
    consistency = _percent(metrics["outcome_consistency"])
    severe = _percent(metrics["severe_failure_rate"])
    synthetic_notice = (
        '<div class="notice"><strong>Demonstration only.</strong> The mock adapter is not an AI '
        "system, and these numbers must not be represented as model evaluation results.</div>"
        if summary.get("synthetic")
        else ""
    )
    serialized = html.escape(json.dumps(summary, indent=2))
    document = f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>AI Reliability Index report</title>
  <style>
    :root {{ color-scheme: dark; font-family: Inter, ui-sans-serif, system-ui, sans-serif; }}
    body {{ margin: 0; background: #07111f; color: #e8f0ff; }}
    main {{ max-width: 1050px; margin: auto; padding: 56px 24px 80px; }}
    .eyebrow {{ color: #78dce8; text-transform: uppercase; letter-spacing: .15em; font-weight: 700; }}
    h1 {{ font-size: clamp(2.2rem, 6vw, 4.8rem); line-height: .96; margin: 14px 0 18px; }}
    .sub {{ color: #a9b8d0; font-size: 1.1rem; max-width: 700px; }}
    .notice {{ margin: 28px 0; border: 1px solid #f5bd63; background: #2a2113; padding: 16px; border-radius: 12px; }}
    .grid {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(190px, 1fr)); gap: 14px; margin: 36px 0; }}
    .card {{ background: #101d2f; border: 1px solid #223653; border-radius: 16px; padding: 22px; }}
    .value {{ font-size: 2.2rem; font-weight: 760; margin-top: 8px; }}
    .label {{ color: #a9b8d0; }}
    pre {{ overflow: auto; background: #050b13; border: 1px solid #223653; padding: 18px; border-radius: 14px; }}
    a {{ color: #78dce8; }}
  </style>
</head>
<body><main>
  <div class="eyebrow">AI Benchmark Collective</div>
  <h1>AI Reliability Index</h1>
  <p class="sub">Task <strong>{html.escape(summary["task"]["id"])}</strong> evaluated with
  <strong>{html.escape(summary["system"]["adapter"])}</strong> / {html.escape(summary["system"]["model"])}.</p>
  {synthetic_notice}
  <section class="grid">
    <div class="card"><div class="label">Success rate</div><div class="value">{success}</div></div>
    <div class="card"><div class="label">Outcome consistency</div><div class="value">{consistency}</div></div>
    <div class="card"><div class="label">Severe-failure rate</div><div class="value">{severe}</div></div>
    <div class="card"><div class="label">Eligible runs</div><div class="value">{metrics["eligible_runs"]}</div></div>
  </section>
  <h2>Machine-readable summary</h2>
  <pre>{serialized}</pre>
  <p><a href="https://github.com/AI-Benchmark-Collective/ai-reliability-index">Methodology and source</a></p>
</main></body></html>
"""
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(document, encoding="utf-8")


def _percent(value: float | None) -> str:
    return "N/A" if value is None else f"{value * 100:.1f}%"
