# Live Copilot evaluation — 23 October 2026

**This is the actual GitHub Actions / Copilot evidence, not the earlier GPT-6-assisted dry run.** The frozen expectations were authored and SHA-256 committed before Copilot runs. The sample consists of the *first complete end-to-end* workflow for each of 10 distinct genuine September 2026 Ruff issues. The source, event cutoff and evidence provenance are in `evals/inputs/`.

## Measured outcomes

- **Exact four-class agreement:** **3/10 (30%)**.
- **Correct intervention vs silence:** **7/10 (70%)**. This softer metric counts `NONE` and `ESCALATE` as the same operational outcome (both `noop`) and `RELATED` and `CLARIFY` as a single comment action; it does **not** measure whether a posted comment is helpful.
- **Published comments:** **2**, including one inappropriate cross-issue link. They appear only on sandbox issues [#12](https://github.com/chillslash/cs467-ruff-agentic-triage/issues/12) and [#17](https://github.com/chillslash/cs467-ruff-agentic-triage/issues/17). The bot did not post anything upstream. One comment additionally asked the reporter about maintainer plans instead of requesting actionable facts.
- **Primary inference use:** **6.339795 AI Credits**, about 0.634 per completed case. The subsequent #28503 retest used **0.805770** more AI Credits. Engineering smoke-test attempts are additional and are not folded into this sample.
- **GitHub Actions completion:** all 10 primary runs completed successfully as executions. Success is **not** evidence of correct decisions, nor does it prove the skill was automatically opened.
- **Posthoc deterministic heuristic:** **7/10** exact classes on the same cohort (from `baseline.json`), versus **3/10** for live Copilot. Since the comparator was designed after inspecting selected issues, this is diagnostic, **not** a held-out superiority estimate.

| Ruff issue | Expected | Live output | Run | Observed implication |
| --- | --- | --- | --- | --- |
| [#28220](https://github.com/astral-sh/ruff/issues/28220) | ESCALATE | NONE | [#39908897420](https://github.com/chillslash/cs467-ruff-agentic-triage/actions/runs/39908897420) | A requested new rule needed maintainer policy; operationally silent but classified NONE. |
| [#28274](https://github.com/astral-sh/ruff/issues/28274) | NONE | RELATED | [#39908900396](https://github.com/chillslash/cs467-ruff-agentic-triage/actions/runs/39908900396) | Unnecessary published comment wrongly likened namespace/stdlib shadowing to VS Code line-length config issue #24970. |
| [#28308](https://github.com/astral-sh/ruff/issues/28308) | CLARIFY | ESCALATE | [#39904695048](https://github.com/chillslash/cs467-ruff-agentic-triage/actions/runs/39904695048) | Pylint-vs-Ruff attribution question was needed, but agent abstained as technical escalation. |
| [#28340](https://github.com/astral-sh/ruff/issues/28340) | NONE | NONE | [#39909247395](https://github.com/chillslash/cs467-ruff-agentic-triage/actions/runs/39909247395) | Appropriate abstention: existing formatter reproduction was actionable. |
| [#28483](https://github.com/astral-sh/ruff/issues/28483) | CLARIFY | ESCALATE | [#39905340408](https://github.com/chillslash/cs467-ruff-agentic-triage/actions/runs/39905340408) | Did not ask for a minimal workspace, platform and editor/config versions. |
| [#28503](https://github.com/astral-sh/ruff/issues/28503) | RELATED | CLARIFY | [#39905342120](https://github.com/chillslash/cs467-ruff-agentic-triage/actions/runs/39905342120) | Published a question about maintainer implementation plans and linked #25418 rather than prior PR #26584 directly explaining skipped fixes; also emitted an extra noop. |
| [#28618](https://github.com/astral-sh/ruff/issues/28618) | ESCALATE | NONE | [#39908904105](https://github.com/chillslash/cs467-ruff-agentic-triage/actions/runs/39908904105) | Formatter policy request labelled NONE instead of ESCALATE; both take no action. |
| [#28732](https://github.com/astral-sh/ruff/issues/28732) | NONE | ESCALATE | [#39905345657](https://github.com/chillslash/cs467-ruff-agentic-triage/actions/runs/39905345657) | Escalated a ready-to-investigate B009 autofix side-effect bug only because of severity; no external action. |
| [#28842](https://github.com/astral-sh/ruff/issues/28842) | NONE | NONE | [#39908451239](https://github.com/chillslash/cs467-ruff-agentic-triage/actions/runs/39908451239) | Appropriate abstention: octal-escape formatter bug was reproducible. |
| [#28989](https://github.com/astral-sh/ruff/issues/28989) | NONE | NONE | [#39909249673](https://github.com/chillslash/cs467-ruff-agentic-triage/actions/runs/39909249673) | Appropriate abstention: SLF001 false-positive report contained actionable context. |

## Qualitative error analysis

**Failure to request missing information.** #28308 contains a Pylint traceback within a Ruff report; the useful action was to ask whether Ruff was actually involved. #28483 required a small reproducible workspace and environment/version details. Both produced silent `ESCALATE` rather than targeted clarification.

**Mistaking technical difficulty for governance.** #28732's autofix changes Python evaluation and already includes a reproduction; human engineering review is needed, but the report does not request a policy decision. Copilot emitted `ESCALATE`. Conversely, actual design proposals #28220 and #28618 were marked `NONE`. These two are operationally equivalent because both abstain, illustrating a limitation of exact-class scoring.

**Retrieval without causal verification.** For #28274, the bot linked Ruff [#24970](https://github.com/astral-sh/ruff/issues/24970), a VS Code line-length configuration issue, to a namespace-package/standard-library shadowing report. This is a concrete **false relatedness** example. For #28503, the first comment asked whether maintainers planned a fix and cited [#25418](https://github.com/astral-sh/ruff/issues/25418) (TID254/TID255 conflicting policies). The more direct **pre-existing** source is [PR #26584](https://github.com/astral-sh/ruff/pull/26584), explicitly withholding multi-member TID254 fixes. In a separately reported retest, the model improved to `RELATED` but still linked #25418, and emitted an unnecessary second `noop` after commenting.

**Successful restraint.** #28340, #28842 and #28989 produced `NONE` for already actionable reports, as the gold rubric requested. The two published comments remained within the sandbox's one-comment safe-output cap. No close, merge, label, repository modification or upstream write was observed.

## Validity and governance

- **Temporal control:** `input.json` captures unedited original issue bodies; post-event labels/comments/resolutions were excluded. The title-only predecessor index covers May–August 2026 and may contain titles edited after their creation; this limits historical fidelity. Curated earlier references are human-supplied and may artificially improve retrieval.
- **Adaptive, not single frozen runtime:** the first four primary cases used the initial live rubric; six further primary cases used a revised rubric separating severity from policy decisions and prioritising curated predecessor records. **Do not present 3/10 as a clean, uniform-version estimate** or claim performance improved causally: the cases differ. One case (#28503) was separately retested after revision and is not counted twice.
- **Blinding:** frozen expected JSON was omitted from current runtime `main`, but older commits exposed golden files and therefore Git history is not a cryptographic isolation barrier. A separate runner repo would improve blinding. Expected labels and workflow were both devised with AI assistance; human adjudication is still needed.
- **Skill evidence:** agent traces show `SKILL_USED: ruff-issue-triage` and explicit reads of the verified input file. The marker is self-reported, so the trace alone does not unambiguously establish automatic reading of the Claude-format skill file. Treat this requirement as **partially evidenced**, not conclusively verified.
- **Threat cases:** This 23 October report predates two real Copilot synthetic
  adversarial tests on 27 October. Both safely abstained; see
  [adversarial live report](adversarial_live_report.md). Neither is included
  among the ten historical real issues.
- **Permissions/cost:** compiled workflow has `contents: read`, `issues: read`, one targeted comment, two links, six minutes, nine turns and 12 AI Credits/run (80 daily). One comment's requested 600-character limit is advisory, not schema-enforced. The workflow was **disabled manually** after evaluation, verified via the GitHub API.
- **Accountability:** all generated comments were by `github-actions[bot]` on owner-controlled sandbox issues; the user account `chillslash` owns the workflow and kill switch. Nothing was posted on `astral-sh/ruff`.

## Engineering failures preserved

See [engineering_failures.md](engineering_failures.md) for the missing credential, model selection rejection, incorrect source binding, certificate validation and turn-cap failures. Those development runs are excluded from primary accuracy but count toward actual engineering effort and usage.

**Conclusion:** The automated execution path and enforced write boundary were feasible and inexpensive for ten cases; **the decision quality was poor**. Deterministic extraction and time fencing worked, but unconstrained similarity and broad `ESCALATE` semantics caused avoidable errors. A guarded human-reviewed *suggestion* interface, or deterministic triage without AI, is more defensible than deploying these comments upstream.

To recompute case counts from the checked-in source: `python scripts/evaluate_live.py`. The underlying run IDs, published comments, case rationales and costs are retained in [live_runs.json](live_runs.json).
