# CS467 Assignment 3 — Ruff issue-triage agent

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

**Execution status (22 Oct 2026):** The compiled workflow started but Copilot activation failed for missing credential. A documented, non-blind GPT-6-assisted dry run is published at [submission evaluation results](https://github.com/chillslash/cs467-ruff-agentic-triage/tree/submission/evals/results); it is not evidence of a real agent run. See [DESIGN.md](DESIGN.md) for the controls still untested.

## Repository branches
- `main`: runnable sandbox workflow with frozen input snapshots and scripts.
  It deliberately excludes the gold labels and reports from the default checkout.
- `submission`: assignment-complete record, including
  [golden expectations](https://github.com/chillslash/cs467-ruff-agentic-triage/tree/submission/evals/golden),
  [actual dry-run outputs](https://github.com/chillslash/cs467-ruff-agentic-triage/tree/submission/evals/results),
  all configuration and the compiled workflow. **Submit a link to a specific
  `submission` commit**, not the moving default branch.

The dry-run results are expressly **not** successful end-to-end agent runs.
