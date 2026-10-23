# Preserved pre-evaluation integration failures

This engineering log is separate from the 10-case primary evaluation; these attempts did not produce an unbiased performance estimate.

| Run / issue | Observed failure | Correction or limitation |
| --- | --- | --- |
| [39791356243](https://github.com/chillslash/cs467-ruff-agentic-triage/actions/runs/39791356243) | Missing `COPILOT_GITHUB_TOKEN` for personal-repo Copilot engine; inference never started | Token installed only as Actions secret; not committed to Git or pasted into logs |
| [39896441896](https://github.com/chillslash/cs467-ruff-agentic-triage/actions/runs/39896441896), sandbox #3 | Initial `auto` model resolved to unsupported model; forced `gpt-5-mini` and `claude-haiku-4.5` were also rejected; final `copilot/auto` ran, but confused sandbox #3 with historical Ruff #28308 and selected wrong fixture; partial job reruns reused stale failure signals | Use provider-specific auto model; reject model guessing; fresh issue-triggered runs |
| [39902701153](https://github.com/chillslash/cs467-ruff-agentic-triage/actions/runs/39902701153), sandbox #7 | Agent tried GitHub REST HTTPS in model container; certificate chain could not be verified | Moved event validation to trusted pre-agent Actions step, with no TLS bypass |
| [39903881195](https://github.com/chillslash/cs467-ruff-agentic-triage/actions/runs/39903881195), sandbox #8 | Pre-agent source verification worked but the model guessed non-existent fixture paths, exhausting nine LLM turns | Embed original title/body and prior context directly into verified `runtime-binding.json` |
| [39904695048](https://github.com/chillslash/cs467-ruff-agentic-triage/actions/runs/39904695048), sandbox #10 | First complete workflow for #28308, but decision `ESCALATE` vs expected `CLARIFY` | Retained as a real quality failure, not silently removed |
| [39908447782](https://github.com/chillslash/cs467-ruff-agentic-triage/actions/runs/39908447782), sandbox #14 | Adaptive retest on #28503 changed class to `RELATED`, but cited the weaker TID254/TID255 issue #25418 instead of the direct PR #26584; extra `noop` after comment | Report separately, not counted as an independent source case |

No automatic workflow success before the credential was installed, no model-run success before the later runtime corrections, and no prototype dry-run record are relabelled as successful live evaluation. AI Credit totals for the primary 10 cases explicitly **exclude** these extra engineering attempts.
