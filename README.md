# AI Reliability Index

An open, reproducible benchmark for measuring whether AI agents perform real-world tasks **accurately, consistently, safely, and economically**.

> **Status:** v0.1 methodology and task set are under active development. No official model rankings have been published yet.

## Why this exists

A single successful run does not make an AI agent reliable. The AI Reliability Index evaluates repeated executions and reports the distribution of outcomes—not only a headline average.

We measure:

- task success rate;
- consistency across repeated runs;
- severe-failure rate;
- unsupported-claim rate;
- human intervention required;
- completion time; and
- estimated execution cost.

## v0.1 scope

The first release will contain a small, auditable set of professional tasks. Each system–task pair will be run repeatedly under a documented configuration. Raw traces, scoring decisions, costs, limitations, and conflicts of interest will be disclosed wherever licensing and privacy permit.

We prioritize evaluation quality over task volume.

## Repository map

| Path | Purpose |
|---|---|
| `benchmark/tasks/` | Versioned task specifications |
| `benchmark/scoring/` | Scoring rubrics and evaluators |
| `results/` | Raw and independently verified outputs |
| `docs/methodology.md` | Evaluation and reporting protocol |
| `docs/governance.md` | Roles, decisions, membership, and conflicts |
| `CONTRIBUTING.md` | How to make an accepted contribution |

## Contribute

Useful first contributions include:

- proposing or auditing a benchmark task;
- reproducing a published result;
- implementing an agent or model adapter;
- improving a deterministic evaluator;
- reviewing the statistical methodology;
- documenting a failure case; and
- creating an accessible result visualization.

Read [CONTRIBUTING.md](CONTRIBUTING.md), then open a structured task proposal or choose an issue labeled `good first issue`.

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

## Membership

Participation is open. Formal organization membership is earned through accepted, attributable work and sustained adherence to the project’s standards. Membership is never sold and does not imply endorsement of a contributor’s unrelated work.

See [governance and membership](docs/governance.md).

## Roadmap

- [x] Publish initial project charter
- [x] Publish v0.1 methodology draft
- [x] Define a task specification template
- [ ] Approve the first 10 benchmark tasks
- [ ] Implement the reference runner and evaluators
- [ ] Add at least three system adapters
- [ ] Complete an independent scoring audit
- [ ] Publish AI Reliability Index v0.1
- [ ] Open nominations for benchmark-track leads

## Citation

Citation metadata is provided in [CITATION.cff](CITATION.cff). Results must cite the exact benchmark version, task-set commit, system version, configuration, and evaluation date.

## License

Code is intended to be released under the Apache License 2.0. Task data and written material may carry separate licenses where indicated. Do not contribute material you are not authorized to redistribute.
