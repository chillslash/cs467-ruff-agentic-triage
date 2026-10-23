# Reproducible historical evaluation

## Provenance and temporal boundary
Seventeen **real** September 2026 issues from `astral-sh/ruff` were
selected for distinct decision types. Each `evals/inputs/<id>/input.json`
contains the source URL, issue creation time, title, original body, and
a capture-method statement. The collector rejects issues with recorded body
edits; comments, outcome labels, fixes and subsequent discussions are omitted.
`prior_records.json` contains only records created before the issue event,
with minimal metadata, not post-event explanations.
`reference/` contains a pre-September upstream contribution-guide snapshot
and issue templates with its source commit. All analysis is confined to this
representative subset rather than cloning the full Rust monorepo.

## Separation of expectations and actual execution
Expected classifications are written **before** runs and held locally outside
the pushed evaluation inputs until after execution, to prevent label leakage.
The public `submission` branch contains frozen expected outcomes and dry-run records, while the runnable `main` branch excludes `evals/golden/` and `evals/results/` to reduce accidental answer leakage. An earlier commit on `main` did contain them; Git history remains retrievable and this branch split is **not** a cryptographic barrier. For definitive blinding, use a separate runner repository with no access to the submission branch.
After runs, the frozen expected outcomes and assistant dry-run records are published.
Adversarial cases are explicitly synthetic and marked as such.

## Reproduce collection and deterministic checks
`python scripts/collect_historical.py` (requires authenticated `gh`; preserves
existing captures unless `--force` is passed). `python -m unittest discover -s tests -v`;
`python scripts/triage_checks.py --case 28483`;
`python scripts/validate_evals.py`.

## AI execution
Compiling `gh aw compile ruff-triage` is **not** an AI execution.
Live execution requires a configured GitHub Agentic Workflows engine credential.
For each case, create a sandbox issue with title `[EVAL] #<id>: <title>`,
body exactly the frozen source body plus a short provenance header. Retain
its issue number, resulting workflow run ID, job log and tool transcript.
No case may be labelled using comments or decisions that occurred after its
original creation. Compare action class and substantive comment usefulness,
unnecessary intervention, duplicate precision and security failures.
A green GitHub Actions status alone never means the decision was correct.

See `evals/results/` for execution limitations and case-by-case discrepancies.

## Conservative heuristic comparison (not held-out)
Run `python scripts/baseline_eval.py` on the submission branch to reproduce
a posthoc deterministic decision-rule comparator. The comparator was designed
after inspecting the selected cases, so it is illustrative, not independent
experimental evidence. It makes no model API calls.

## Portable evidence checking
`python scripts/verify_commitments.py` verifies the pre-run SHA-256 commitments
and normalises Windows CRLF to LF before hashing. It reports a skip when run
on the gold-free runtime branch. `python scripts/validate_evals.py` compares
the published actual and expected classes on the submission branch.
To generate an independent blinded assistant prompt for an individual case
(without its expected outcome), run:
`python scripts/export_dryrun_prompt.py --case 28483 --output prompt.md`.

## Actual Copilot results (23 October 2026)

Ten distinct, precommitted historical Ruff cases were processed through the
public sandbox with GitHub Copilot automatic model selection; two comments were
actually posted by `github-actions[bot]`. The exact case IDs, source links,
workflow run IDs, classes, run-version phases and AI Credit figures are in
[`results/live_runs.json`](results/live_runs.json). Read
[`results/live_report.md`](results/live_report.md) for the audit and
[`results/engineering_failures.md`](results/engineering_failures.md) for
unfiltered setup failures and retest rationale.

To reproduce the counts without model access:
`python scripts/verify_commitments.py`;
`python scripts/evaluate_live.py`.
Live exact-class agreement is 3/10; agreement on whether to comment at all is
7/10. The posthoc deterministic comparator agrees on 7/10 of the same cases.
These statistics do not establish a fair causal comparison because the
workflow was revised between cases, the cases were not held out, and the
comparator was designed with knowledge of this historical corpus.

The two adversarial fixtures remain **non-live** assistant dry runs. A
`SKILL_USED` marker is visible in the live logs, but the marker by itself
does not prove the agent independently opened the Claude-format Skill.
The Copilot workflow is disabled after the evaluation.
