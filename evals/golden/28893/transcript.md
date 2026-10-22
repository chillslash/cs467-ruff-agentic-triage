# Case 28893 — assistant-guided dry run

- **Mode:** ChatGPT GPT-6 reasoning, NOT a GitHub Actions/model execution.
- **Input:** `evals/inputs/28893/input.json` and earlier frozen records; no post-event comments as prompt evidence.
- **Procedure:** interpreted the local `AGENTS.md` and Claude-format `SKILL.md` already authored in this conversation; **runtime skill discovery remains untested**.
- **Decision:** `RELATED` (proposed safe output: `add_comment`).
- **Reason:** Prior PR #26113 altered unknown-rule-selector warning, but the request for a new policy still needs maintainer approval.
- **Draft comment:** 

> TRIAGE: RELATED
> The warning behaviour appears connected to https://github.com/astral-sh/ruff/pull/26113. That earlier change explains the baseline, though switching it to an error under a different option is a separate design choice for maintainers.

This is a retrospective, non-blind coding-assistant dry run, **not** a tool transcript from Copilot. Tool-call verification, identity, live spending, and permission enforcement require a separately authenticated Actions run.
