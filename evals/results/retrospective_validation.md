# Retrospective validation against Ruff maintainer records (30 October 2026)

This is a **post-evaluation, non-blind, AI-assisted external-evidence cross-check** of the ten frozen decisions. It uses Ruff issue labels and maintainer comments visible on 30 October **only after** the historical runs. These post-event observations were never provided to the agent or used to set the original expectations. A label is not an exact four-class ground truth; independent human adjudication of the evaluation rubric is still outstanding.

| Original Ruff issue | Frozen class | External observation (post-event; not agent input) | Assessment of original label |
| --- | --- | --- | --- |
| [#28220](https://github.com/astral-sh/ruff/issues/28220) | ESCALATE | Ruff later applied `rule` and `needs-decision`. | Consistent: asks whether a new rule should exist; no reporter fact is missing. |
| [#28274](https://github.com/astral-sh/ruff/issues/28274) | NONE | Later labelled `bug`, `analyze`. Reporter supplied versions, a runnable minimal example and already mentioned possible predecessor #21817. | Consistent with no *additional* bot comment. These labels do not establish an exact-class answer. |
| [#28308](https://github.com/astral-sh/ruff/issues/28308) | CLARIFY | Ruff later labelled it `question`; a human comment reproduced attachment text showing a **Pylint/Astroid** crash. | Supports asking which tool actually failed rather than treating it as a Ruff bug. |
| [#28340](https://github.com/astral-sh/ruff/issues/28340) | NONE | Later received `needs-decision` alongside formatter/style labels. The issue already includes before/after formatter output. | **Ambiguous class:** human style judgement may be required, but no additional bot comment was needed. NONE and ESCALATE have identical `noop` behaviour. |
| [#28483](https://github.com/astral-sh/ruff/issues/28483) | CLARIFY | A Ruff maintainer specifically requested a **small reproduction** and Windows/platform investigation; it received `needs-mre`. The reporter later traced the symptoms to the Pylint VS Code extension. | **Strongly corroborated** need for concrete missing details at report time. Final root cause must not be fed backward into the historical test. |
| [#28503](https://github.com/astral-sh/ruff/issues/28503) | RELATED | Ruff maintainer explicitly linked prior [PR #26584](https://github.com/astral-sh/ruff/pull/26584) and explained why the multi-import fix was intentionally omitted. | **Strongly corroborated** value of a specific pre-existing explanatory link. The live agent linked a weaker report. |
| [#28618](https://github.com/astral-sh/ruff/issues/28618) | ESCALATE | Ruff later labelled the opt-out request `needs-decision` and `style`. | Consistent with a maintainer policy choice rather than an information request. |
| [#28732](https://github.com/astral-sh/ruff/issues/28732) | NONE | Later labelled `bug`. Original report contained commands, Python/Ruff versions and observable side effects. | Consistent with a technically actionable bug needing investigation, not an escalation comment. |
| [#28842](https://github.com/astral-sh/ruff/issues/28842) | NONE | Later labelled `bug`, `formatter`. Original report included a minimal before/after semantic change. | Consistent with no redundant clarification. |
| [#28989](https://github.com/astral-sh/ruff/issues/28989) | NONE | Later labelled `bug`; original report gave a runnable SLF001 example and command. | Consistent with actionable input; does not prove correctness of Ruff's diagnosis. |

## Conclusions and limitations

- **Do not change the gold or score.** The original 3/10 exact class and 7/10 intervention/silence figures remain unchanged; later maintainer evidence is not available at prediction time.
- The strongest external checks are the maintainer's specific clarification request on #28483 and explicit predecessor explanation on #28503. The #28308 Pylint traceback provides another concrete tool-identification check.
- **#28340 is a real ambiguity**: an issue can be complete enough for the bot to remain silent and still need a human style/policy decision. This reveals overlap between `NONE` and `ESCALATE`, which both map to `noop`.
- The retrospective review is *not* an independent blinded human annotation, nor a validation of accuracy across Ruff issues. Human judgement by upstream maintainers is used as corroborating context, not automatically as the four-way label.
- The original frozen labels, their SHA-256 commitments and all model runs remain intact.
