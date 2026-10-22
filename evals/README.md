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
After runs, the frozen expected outcomes and agent transcripts are published.
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
