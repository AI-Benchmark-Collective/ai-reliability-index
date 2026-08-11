# Scoring

Versioned deterministic evaluators and human-review rubrics live here.

Every evaluator must document:

- accepted inputs and emitted outputs;
- compatible task versions;
- deterministic and nondeterministic behavior;
- missing-data and infrastructure-failure handling;
- severe-failure detection;
- tests and expected edge cases; and
- known limitations.

A scoring implementation change that can alter results requires a new evaluator version.
