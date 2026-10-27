# Second-pass review of the ten historical golden decisions

**Scope:** Analytic reassessment of frozen pre-event issue bodies, prior-record metadata, and dated Ruff artefacts on 27 October 2026. This is an **AI-assisted, non-blind review**, not independent human adjudication: the reviewer had access to previous results. The original gold labels and SHA-256 commitments remain unchanged.

| Ruff issue | Frozen gold | Second-pass judgement | Rationale |
| --- | --- | --- | --- |
| [#28220](https://github.com/astral-sh/ruff/issues/28220) | ESCALATE | Retain (high confidence) | Explicit proposal for a new style-enforcement rule. This needs a policy/design choice, not reproduction information. |
| [#28274](https://github.com/astral-sh/ruff/issues/28274) | NONE | Retain (high) | Complete namespace-package reproducer and version comparison. Bot's [#24970](https://github.com/astral-sh/ruff/issues/24970) VS Code line-length link is causally unrelated. |
| [#28308](https://github.com/astral-sh/ruff/issues/28308) | CLARIFY | Retain (medium-high) | A crash attachment is named Pylint, not Ruff; the reporter should identify the failing tool/command. Attachment contents were not independently executed. |
| [#28340](https://github.com/astral-sh/ruff/issues/28340) | NONE | Retain (high) | Original formatter code and its transformed output are already actionable. |
| [#28483](https://github.com/astral-sh/ruff/issues/28483) | CLARIFY | **Contestable; retain frozen gold** (medium-low) | A minimal workspace and extension/platform versions would help, but the issue already provides config, command-line comparison, symptoms and a log. A maintainer could reasonably choose NONE. |
| [#28503](https://github.com/astral-sh/ruff/issues/28503) | RELATED | Retain (high) | Earlier merged [PR #26584](https://github.com/astral-sh/ruff/pull/26584) explicitly withholds multi-member TID254 fixes. The bot's [#25418](https://github.com/astral-sh/ruff/issues/25418) describes another conflicting-policy mechanism. |
| [#28618](https://github.com/astral-sh/ruff/issues/28618) | ESCALATE | Retain (high) | Requests an opt-out from formatter policy. Both ESCALATE and NONE deliberately cause no bot comment. |
| [#28732](https://github.com/astral-sh/ruff/issues/28732) | NONE | Retain (high) | Exact commands, versions, platform and before/after side effects make it ready for investigation. Severity alone does not justify escalation. |
| [#28842](https://github.com/astral-sh/ruff/issues/28842) | NONE | Retain (high) | Complete reproducer shows changed byte values after formatting; further generic clarification would waste reporter attention. |
| [#28989](https://github.com/astral-sh/ruff/issues/28989) | NONE | Retain (medium) | Reproducible SLF001 report. Earlier [PR #16149](https://github.com/astral-sh/ruff/pull/16149) handles instance-like access patterns but does not conclusively cover this object-construction mechanism. Speculative linking would be unsafe. |

## Implications

Nine labels remain reasonable on the available record; **#28483 is materially judgement-dependent**. In a ten-case sample, a single disputed classification changes the headline by ten percentage points. Also, NONE and ESCALATE both mean silence, so exact agreement cannot stand alone; the published report separately measures comment/silence and substantively inspects the two actual comments.

This is not a held-out sample or an independent human reliability estimate. Workflow versions changed across cases, and both the golden decisions and this review were AI-assisted. If a human reviews the cases, document that judgement separately; do not retroactively edit the frozen labels to improve reported accuracy.
