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

**Evaluation status (23 October 2026):** Ten genuine historical Ruff issues were processed by real GitHub Agentic Workflow/Copilot runs: **3/10 exact disposition agreement** and **7/10 correct comment-versus-no-comment choice** under the frozen rubric. Two sandbox comments were substantively problematic. The primary sample used **6.339795 AI Credits**. See the [live evaluation report](evals/results/live_report.md) and [case/run manifest](evals/results/live_runs.json). Earlier assistant-guided dry runs are **not** live inference.

Two further **synthetic live prompt-injection tests** on 27 October 2026 each yielded no action or comment, with an actual full skill-file read in the model trace. These are evaluated separately in [the adversarial report](evals/results/adversarial_live_report.md), not added to the ten historical cases. A [second-pass review](evals/results/golden_label_review.md) identifies a contestable golden classification without changing the frozen expected answers.

The model inference workflow is **disabled after evaluation** to avoid unplanned credit usage. The submission includes the compiled source, full historical and synthetic fixture set, adversarial assistant dry runs, and measured runtime failures. The live historical cases span an initial and a revised workflow version, so the aggregate is diagnostic rather than a held-out single-version performance claim.

## Repository branches
- `main`: runnable sandbox workflow with frozen input snapshots and scripts.
  It deliberately excludes the gold labels and reports from the default checkout.
- `submission`: assignment-complete record, including
  [golden expectations](https://github.com/chillslash/cs467-ruff-agentic-triage/tree/submission/evals/golden),
  [actual dry-run outputs](https://github.com/chillslash/cs467-ruff-agentic-triage/tree/submission/evals/results),
  all configuration and the compiled workflow. **Submit a link to a specific
  `submission` commit**, not the moving default branch.

The dry-run results are expressly **not** successful end-to-end agent runs.
