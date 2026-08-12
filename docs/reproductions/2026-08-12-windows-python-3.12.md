# v0.1.0-alpha quickstart reproduction on Windows

This note records an independent reproduction of the offline mock
demonstration in the README. It does not report AI model performance.

## Environment

- Date: 2026-08-12
- Benchmark commit: `5fe4720c4665c07667ec1dae6a8f5b7861519c83`
- Operating system: Microsoft Windows NT 10.0.26200.0 (AMD64)
- Python: 3.12.13
- Install command duration: 10.39 seconds
- API keys or paid services: none

The reproduction started from a fresh clone. A fresh virtual environment was
created with the README command. Because the activation command in the README
was POSIX-specific, the remaining commands were invoked through the Windows
virtual-environment executables.

## Commands

```powershell
git clone https://github.com/AI-Benchmark-Collective/ai-reliability-index
cd ai-reliability-index
python -m venv .venv
.venv\Scripts\python.exe -m pip install -e .
.venv\Scripts\airi.exe validate --task evidence-brief-001
.venv\Scripts\airi.exe run --task evidence-brief-001 --adapter mock --runs 10 --output results/raw
```

Validation returned `valid: evidence-brief-001@0.1.0`.

## Results

The run produced:

- 10 `*.result.json` run manifests and 10 corresponding raw output files;
- `results/raw/summary.json`;
- `results/raw/report.html`;
- 10 eligible runs, of which 8 succeeded;
- a success rate of 0.8; and
- no severe failures.

The observed 80% synthetic success pattern matches the README expectation, so
there was no result discrepancy to investigate.

SHA-256 of `results/raw/summary.json`:

```text
721da9a4d7f40eec3245efbab6e1d48a1348aca51bf560331fd67a6e56e99a46
```

The generated result files are intentionally not committed: the digest and
environment metadata identify this mock reproduction without adding transient
run IDs and latency values to the repository.

## Ambiguity found

The README originally documented only `source .venv/bin/activate`, which does
not work in Windows PowerShell. This reproduction adds the equivalent
`.venv\Scripts\Activate.ps1` command while leaving the POSIX instruction
unchanged.
