# Methodology — Draft v0.1

This document defines the minimum protocol for results published as part of the AI Reliability Index. It is a draft and will change through public review.

## 1. Evaluation unit

The primary evaluation unit is one **system–task run**: a declared agent system attempting a versioned task from a clean starting state under a recorded configuration.

A system includes the model, agent framework, system instructions, tools, policies, retry logic, and retrieval or memory components. Changing one produces a different evaluated configuration.

## 2. Repetition protocol

For v0.1, each system–task pair should receive at least 10 independent runs unless a task specification justifies another number.

Each run must:

1. begin from the task's declared clean state;
2. use the same disclosed configuration;
3. use a fresh conversation and isolated task environment;
4. record randomness controls when exposed;
5. record every human intervention and retry; and
6. preserve sufficient evidence for scoring review.

Unsupported transient infrastructure failures are reported separately; they are never silently removed.

## 3. Primary measures

Results are reported per task and in aggregate with denominators.

### Task success rate

`successful runs / eligible runs`

Success is determined by the versioned task evaluator. Partial credit may be reported separately but must not be relabeled as success.

### Outcome consistency

For tasks with categorical terminal outcomes:

`count of the most frequent terminal outcome / eligible runs`

The outcome taxonomy must be defined before reviewing model identities. Consistency is not correctness: a system may fail consistently.

### Severe-failure rate

`runs triggering at least one predeclared severe-failure condition / eligible runs`

Examples include unauthorized external actions, irreversible corruption, disclosure of protected information, fabricated evidence used in a decision, or violation of an explicit safety boundary. Each task defines applicable conditions in advance.

### Unsupported-claim rate

Report the number of externally verifiable material claims and the proportion unsupported or contradicted by permitted evidence. Claims must be sampled or reviewed under a published rubric.

### Human intervention

Report both the proportion of runs receiving intervention and the median number of interventions. Any intervention beyond standard initialization must be logged.

### Latency and cost

Report median and 95th-percentile wall-clock time, mean direct API/tool cost, token usage where available, and excluded infrastructure costs. Promotional credits do not make a run zero-cost.

## 4. Uncertainty

Binary proportions should include 95% Wilson confidence intervals. Small samples must be labeled exploratory. Aggregate results must not conceal task-level denominators or missing runs.

v0.1 will not publish a single composite reliability score until weighting choices have been publicly justified and sensitivity-tested.

## 5. Scoring

Prefer deterministic state or artifact checks. When human judgment is unavoidable:

- use a written rubric created before model identities are revealed;
- obtain two independent reviews for consequential or disputed cases;
- measure and report agreement;
- adjudicate disagreements with a third reviewer; and
- retain original scores and the adjudication rationale.

LLM judges may assist analysis but cannot be the sole undisclosed authority for an official result.

## 6. Comparability

A leaderboard row is comparable only when it uses the same task version and environment, allowed tools and limits, intervention and retry policy, scoring implementation, and reporting protocol. Material deviations receive a separate row and explanatory label.

## 7. Task admission

A task is eligible when it has:

- a meaningful real-world objective;
- redistribution rights for all included materials;
- a reproducible starting state;
- auditable success and failure criteria;
- documented ambiguity and contamination risks;
- no unnecessary sensitive data; and
- an independent review from someone other than its author.

## 8. Transparency and corrections

Official releases publish task specifications, evaluator versions, aggregate and task-level results, configuration manifests, known limitations, funding, and material conflicts.

Corrections preserve the previous release, explain the error, identify affected results, and publish a versioned replacement. Results may be withdrawn when their evidence cannot be verified.

## 9. Safety and privacy

Tasks must use synthetic, licensed, or appropriately public data. Do not test destructive actions against live third-party systems. Do not submit credentials, personal information, protected health information, confidential records, malware, or instructions intended to facilitate unauthorized access.

Security-sensitive work requires a documented sandbox and responsible-disclosure plan before execution.

## 10. Independence

Funding or technical access from an evaluated vendor must be disclosed. Sponsors receive no control over task selection, scoring, corrections, or ranking. Reviewers recuse themselves from decisions where they have a material conflict.

## 11. Required result manifest

Every official submission records the benchmark version and commit, evaluator version, system/model/framework versions, material prompts and tools, generation settings, timestamps, cost, latency, token use, retries, intervention, environment identifier, trace location or nondisclosure reason, and relevant conflicts.
