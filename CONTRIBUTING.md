# Contributing to the AI Reliability Index

Thank you for helping build a benchmark that can be inspected, reproduced, and corrected.

## Ways to contribute

### Propose a task

Use the **Benchmark task proposal** issue form. A task must have a real decision or deliverable, a defined environment, an auditable success condition, known sources of ambiguity, and no confidential or personal data.

### Audit a task

Check whether instructions are unambiguous, evidence is sufficient, scoring matches the stated objective, and the task can be reproduced without privileged access.

### Reproduce a result

Use the same task-set commit and declared system configuration. Submit complete logs, timestamps, cost information, intervention records, and any deviations.

### Improve the implementation

Choose an issue with a defined acceptance test. Before significant work, comment on the issue so maintainers can confirm that the approach fits the release.

## Contribution workflow

1. Read the methodology and code of conduct.
2. Select an open issue or submit a structured proposal.
3. Fork the repository and create a focused branch.
4. Add or update tests and documentation with the change.
5. Open a pull request using the repository template.
6. Respond to methodological and technical review.
7. A maintainer merges the contribution after its acceptance criteria are met.

Please keep unrelated changes in separate pull requests.

## Acceptance standards

An accepted contribution must be:

- attributable and appropriately licensed;
- reproducible from the submitted materials;
- scoped to a documented problem;
- accompanied by an acceptance test or review rubric;
- transparent about limitations and conflicts;
- free of secrets, personal data, and proprietary benchmark answers; and
- consistent with the current methodology.

A contribution may be correct yet deferred if it falls outside the current release scope.

## Task requirements

Every task specification must include:

- stable task ID and version;
- domain and risk level;
- user objective;
- allowed and prohibited tools;
- starting state and required artifacts;
- time and cost limits;
- deterministic checks where possible;
- human-review rubric where necessary;
- severe-failure conditions;
- provenance and redistribution rights; and
- contamination considerations.

Start from `benchmark/tasks/example-task.yaml`.

## Result requirements

Every result submission must identify:

- benchmark commit SHA;
- system, model, and agent-framework versions;
- prompts and policies that materially affect behavior;
- temperature, seed, tool configuration, and retry policy;
- run count and timestamps;
- token usage, external costs, latency, and intervention;
- raw traces or an explicit reason they cannot be released; and
- submitter conflicts of interest.

## Credit and membership

Merged work is credited in the relevant release. Formal organization membership recognizes sustained responsibility; it is not automatically granted for opening an issue or making a cosmetic change.

A contributor becomes eligible for member review after either two accepted substantive contributions or one major contribution such as leading a benchmark track, evaluator, reproduction audit, or release section.

Existing maintainers review nominations using contribution quality, review behavior, reliability, and adherence to the code of conduct.

## Review expectations

Review the work, not the person. Identify the exact methodological or technical concern, explain why it matters, and suggest a testable resolution whenever possible.

## Questions

Use GitHub Discussions for design questions. Use issues for defined work and defects. Do not disclose vulnerabilities or private information in a public issue.
