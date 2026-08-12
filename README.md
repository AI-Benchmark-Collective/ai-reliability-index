# AI Reliability Index

An open, reproducible benchmark for measuring whether AI agents perform real-world
tasks **accurately, consistently, safely, and economically**.

> **Status:** `v0.1.0-alpha` is runnable infrastructure with one synthetic task and a
> deterministic demonstration adapter. No official model rankings have been published.

## Five-minute quickstart

```bash
git clone https://github.com/AI-Benchmark-Collective/ai-reliability-index
cd ai-reliability-index
python -m venv .venv
```

Activate the environment on macOS or Linux:

```bash
source .venv/bin/activate
```

Or on Windows PowerShell:

```powershell
.venv\Scripts\Activate.ps1
```

Then install and run the benchmark:

```bash
pip install -e .
airi validate --task evidence-brief-001
airi run --task evidence-brief-001 --adapter mock --runs 10 --output results/raw
```

Open `results/raw/report.html` after the run. The same directory contains one JSON
manifest and raw output per run plus a machine-readable `summary.json`.

The mock adapter is deliberately variable and completely offline. It demonstrates the
measurement pipeline; **its numbers are not AI-model results**.

## What the alpha measures

- task success rate;
- consistency across repeated runs;
- 95% Wilson intervals for binary success;
- severe-failure rate;
- human intervention;
- median and p95 latency;
- token usage and versioned cost estimates; and
- complete run-level manifests.

## Included task

`evidence-brief-001` gives the system five synthetic business documents, including an
authoritative record, irrelevant evidence, and a withdrawn conflicting draft. The
system must produce a JSON operating brief with correctly grounded citations.

The evaluator is narrow and deterministic. It checks the JSON contract, three required
facts, source correctness, use of withdrawn evidence, and unsupported numeric claims.

## Optional OpenAI Responses API adapter

The adapter uses the official Python SDK and reads the key from `OPENAI_API_KEY`.
Credentials are never accepted as CLI arguments or written to result files.

```bash
pip install -e ".[openai]"
export OPENAI_API_KEY="..."
airi run \
  --task evidence-brief-001 \
  --adapter openai \
  --model YOUR_PINNED_MODEL_VERSION \
  --runs 10 \
  --pricing-file pricing/your-versioned-price.json \
  --output results/raw/openai-run
```

Do not commit API keys or unreviewed paid results. Official comparisons require a
pinned model identifier, a contemporaneous pricing source, complete manifests, and
independent review.

## Commands

```text
airi validate --task TASK
airi run --task TASK --adapter {mock,openai} --runs N --output DIRECTORY
airi report --input RESULT_DIRECTORY --output report.html
```

`TASK` may be a task YAML path or a bundled task ID.

## Repository map

| Path | Purpose |
|---|---|
| `src/airi/` | CLI, adapters, runner, metrics, validation, and reporting |
| `src/airi/schemas/` | Versioned task and result JSON Schemas |
| `benchmark/tasks/` | Versioned task specifications and fixtures |
| `benchmark/scoring/` | Scoring documentation and evaluators |
| `results/` | Raw and independently verified outputs |
| `docs/methodology.md` | Evaluation and reporting protocol |
| `docs/governance.md` | Roles, decisions, membership, and conflicts |
| `docs/launch/` | Founding-contributor and release campaign assets |
| `CONTRIBUTING.md` | How to make an accepted contribution |

## Contribute

Useful first contributions include proposing or auditing a task, reproducing a result,
implementing an adapter, reviewing methodology, and improving deterministic evaluators.

Read [CONTRIBUTING.md](CONTRIBUTING.md), then choose an issue labeled
[`good first issue`](https://github.com/AI-Benchmark-Collective/ai-reliability-index/labels/good%20first%20issue)
or [`help wanted`](https://github.com/AI-Benchmark-Collective/ai-reliability-index/labels/help%20wanted).

## Methodological commitments

1. Reproducible configurations and versioned tasks
2. Deterministic scoring where feasible
3. Independent review of consequential scoring decisions
4. Complete cost and intervention reporting
5. Public limitations and correction history
6. No pay-to-rank placement
7. Disclosure of material conflicts of interest
8. No sensitive data or destructive live-system testing

See the full [methodology](docs/methodology.md).

## Membership and credit

Participation is open. Formal organization membership is earned through accepted,
attributable work and sustained adherence to the project’s standards. Membership is
never sold. See [governance](docs/governance.md) and the
[founding-contributor charter](FOUNDING_CONTRIBUTORS.md).

## Development

```bash
pip install -e ".[dev]"
ruff check src tests
pytest
```

Pull requests run the same checks on Python 3.11, 3.12, and 3.13.

## Citation and license

Citation metadata is provided in [CITATION.cff](CITATION.cff). Cite the exact release,
task-set commit, system version, configuration, and evaluation date.

Code is licensed under Apache-2.0. Individual task data may declare additional terms.

