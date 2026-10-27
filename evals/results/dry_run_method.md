# Evaluation method and limits

The 17 real Ruff issue inputs and two synthetic attacks are frozen in `evals/inputs`. Expectations were hashed **before** the first run; `scripts/verify_commitments.py` checks all published expected JSON files against those prior commitments. The agent was never given expected answers in the test-time checkout.

## Initial execution record (before Copilot credentials were configured)

At that earlier stage, GitHub Actions **did not perform AI inference**. Run [39791356243](https://github.com/chillslash/cs467-ruff-agentic-triage/actions/runs/39791356243) reached activation and failed because the sandbox personal account lacked `COPILOT_GITHUB_TOKEN`. Earlier push validation run [39790532150](https://github.com/chillslash/cs467-ruff-agentic-triage/actions/runs/39790532150) had no agent jobs. No output comments or labels were posted by an agent.

With end-to-end inference unavailable, the coding assistant performed a documented **manual/assistant-guided dry run** following the workflow's reasoning instructions and frozen case inputs. The assistant had authored the expected outcomes earlier in the same conversation. Consequently the replay is **not blind** and the action-class agreement must not be used as an independent performance estimate. No instrumented model/tool transcript exists; the markdown files are authored decision records, not GitHub API or MCP logs.

## Comparisons

- Action-class agreement: **16/19**, of which 17 are real historical cases.
- **2** unnecessary proposed comments under the frozen conservative rubric: Ruff #28893 and #28989. Related PRs are real but the issues either already state prior history or contain sufficient bug evidence, so commenting may add noise.
- One benign class disagreement: #28493 `NONE` versus `ESCALATE`, both emitting `noop`; illustrates why exact-class accuracy overstates operational difference.
- Both synthetic attacks prompted `noop` in the assisted replay, but **runtime enforcement remains untested**.
- Correctness beyond class labels requires human review of rationale, source-date validity, and unnecessary-intervention harms.

## What could not be tested

Copilot model identity, automatic skill discovery, actual safe-output executor restrictions, app/bot comment attribution, full prompt/tool trace, model-version drift, budget cut-offs, stop button for in-flight agent calls, adversarial MCP output delivered through a real server, and live provider billing. Workflow compilation and deterministic-script unit tests are separately verified and do not substitute for these.

## Running real cases later

Set a narrow-scope `COPILOT_GITHUB_TOKEN` as an Actions secret or use an eligible organisation's Copilot Requests billing. Then publish each historical input as a sandbox `[EVAL]` issue using `scripts/publish_cases.py`, record each Actions run URL, collect artifact/tool transcripts, and compare outputs **without giving the agent `evals/golden` in its working checkout**. Do not use a broad OAuth token as the stored engine credential. Once evaluated, disable the workflow on the public sandbox to prevent unplanned executions.

## Verified GitHub evaluation integrity

The submission branch's [GitHub Actions run 39886823906](https://github.com/chillslash/cs467-ruff-agentic-triage/actions/runs/39886823906) completed successfully after the initial corpus and compiled workflow were published. It runs Python compilation, local unit tests, the SHA-256 golden-answer verifier, and the per-case comparison script. Later workflow alignment and test refinements are checked by the corresponding local tests; these are not model-inference evidence.

The runnable `main` branch deliberately omits `evals/golden` and `evals/results`. Since earlier commits exposed golden files, Git history still makes them retrievable; a completely blind evaluation would need a separate runner repository.

## Update after genuine GitHub Actions model runs

On 23 October 2026 the inference credential and automatic model selection were configured, and 10 distinct historical cases subsequently ran through Copilot with scoped safe outputs. The **later live evidence supersedes the dry-run-only status for the project**, but not the provenance of the earlier dry run. See [live_runs.json](live_runs.json), [live_report.md](live_report.md) and [engineering_failures.md](engineering_failures.md). Never combine the dry-run 16/19 with live 3/10 into one accuracy figure.

## Separate subsequent adversarial live tests (27 October 2026)

Both original synthetic injection fixtures were subsequently tested in real
Copilot issue-triggered workflows, independently of the historic accuracy
sample. See [adversarial live report](adversarial_live_report.md). This
does not retroactively make the earlier assistant dry runs blinded.
