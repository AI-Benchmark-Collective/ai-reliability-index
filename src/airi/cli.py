from __future__ import annotations

import argparse
import json
from collections.abc import Sequence
from pathlib import Path

from airi.adapters.mock import MockAdapter
from airi.pricing import load_pricing
from airi.reporting import load_manifests, write_html_report, write_summary
from airi.runner import run_benchmark
from airi.validation import ValidationFailure, load_and_validate_task


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="airi", description="AI Reliability Index CLI")
    subparsers = parser.add_subparsers(dest="command", required=True)

    validate = subparsers.add_parser("validate", help="validate a task specification")
    validate.add_argument("--task", required=True)

    run = subparsers.add_parser("run", help="run a repeated evaluation")
    run.add_argument("--task", required=True)
    run.add_argument("--adapter", choices=["mock", "openai"], default="mock")
    run.add_argument("--model")
    run.add_argument("--runs", type=int, default=10)
    run.add_argument("--output", type=Path, default=Path("results/raw"))
    run.add_argument("--pricing-file", type=Path)

    report = subparsers.add_parser("report", help="rebuild reports from result manifests")
    report.add_argument("--input", type=Path, required=True)
    report.add_argument("--output", type=Path, required=True)

    return parser


def main(argv: Sequence[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    try:
        if args.command == "validate":
            task_path = resolve_task(args.task)
            task = load_and_validate_task(task_path)
            print(f"valid: {task['task']['id']}@{task['task']['version']}")
            return 0
        if args.command == "run":
            task_path = resolve_task(args.task)
            task = load_and_validate_task(task_path)
            adapter = make_adapter(args.adapter, args.model)
            pricing = load_pricing(args.pricing_file, adapter.model)
            _, summary = run_benchmark(
                task=task,
                task_path=task_path,
                adapter=adapter,
                runs=args.runs,
                output_dir=args.output,
                pricing=pricing,
            )
            print(json.dumps(summary, indent=2))
            return 0
        if args.command == "report":
            manifests = load_manifests(args.input)
            summary_path = args.input / "summary.json"
            summary = write_summary(manifests, summary_path)
            write_html_report(summary, args.output)
            print(f"wrote {args.output}")
            return 0
    except (ValidationFailure, ValueError, RuntimeError, OSError) as exc:
        parser.exit(2, f"error: {exc}\n")
    return 1


def resolve_task(value: str) -> Path:
    candidate = Path(value)
    if candidate.is_file():
        return candidate.resolve()
    named = Path("benchmark") / "tasks" / value / "task.yaml"
    if named.is_file():
        return named.resolve()
    raise ValueError(f"task not found: {value}")


def make_adapter(name: str, model: str | None):
    if name == "mock":
        return MockAdapter()
    if name == "openai":
        from airi.adapters.openai_responses import OpenAIResponsesAdapter

        return OpenAIResponsesAdapter(model or "")
    raise ValueError(f"unknown adapter: {name}")


if __name__ == "__main__":
    raise SystemExit(main())
