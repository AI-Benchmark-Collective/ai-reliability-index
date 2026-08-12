# Show HN draft — do not post before release gates pass

## Title

Show HN: AI Reliability Index – repeated-run evaluation for AI agents

## First comment

We built this because a single successful trajectory can hide substantial run-to-run
variation. The project runs the same versioned task repeatedly, preserves every eligible
and infrastructure-failed attempt, and reports success, consistency, severe failures,
latency, intervention, cost, and uncertainty.

The repository includes a completely offline mock demonstration so the evaluation
pipeline can be tried without an API key. The public model comparison is separately
labeled and includes pinned configurations, raw traces, pricing sources, and limitations.

We would especially value criticism of the outcome-consistency definition, missing-run
treatment, and whether the task admission standard is strict enough.

Repository: https://github.com/AI-Benchmark-Collective/ai-reliability-index

