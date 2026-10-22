# CS467 Assignment 3 â€” Ruff issue-triage agent

Independent public **sandbox**, not affiliated with Ruff maintainers.
Source: https://github.com/astral-sh/ruff. No upstream deployment.

## Workflow
GitHub Agentic Workflow source: [`.github/workflows/ruff-triage.md`](.github/workflows/ruff-triage.md);
compiled Actions lock file: [`ruff-triage.lock.yml`](.github/workflows/ruff-triage.lock.yml).
The agent performs first-pass reasoning on historical Ruff issue reports; it may
ask for specific missing information or link an earlier known record, or abstain.
No closing, merging, changing labels, code edits, or upstream communication.

## Evaluation and reproducibility
See [`evals/README.md`](evals/README.md) for origin, timestamp boundaries,
golden answers, actual outputs, logs, comparison metrics, and replay commands.
Run `python -m unittest discover -s tests -v`, then
`python scripts/validate_evals.py` and `gh aw compile ruff-triage`.
`DESIGN.md` explains controls, risks, trade-offs, and AI disclosure.

Do not confuse **compiler success**, **historical script checking**, or
**an end-to-end workflow success** with decision accuracy. Each is tested separately.

