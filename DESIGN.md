# CS467 A3 — Ruff issue-readiness agent
## Decision and scope
- **Upstream:** [astral-sh/ruff](https://github.com/astral-sh/ruff); **deployment:** this independent
  public sandbox only, not upstream.
- **Workflow:** first-pass issue readiness, evidence-backed earlier references, selective clarification,
  and explicit abstention.
- **Why AI:** version/text extraction and candidate search are deterministic; deciding whether a minimal
  reproduction is *sufficient*, whether apparently similar reports share a cause, and whether a request
  changes policy needs context-sensitive judgement.
- **Measured need:** 68 new Ruff issues in 1–30 September 2026; 55 received a human-applied label, median
  2.1 h to first human label among labelled reports (51 within 24 h). See
  `research/workload-2026-09.json` and `scripts/measure_workload.py`.
- **Limits:** labels are a proxy for human triage, *not* work hours or delays; 13 had no human label;
  fast handling weakens a backlog argument. Benefit sought: consistency and reduced repeated reading,
  *not* replacing fast maintainers.
- **Rejected alternative:** pytest had 31 September issues and excellent reproduction cases, but Ruff's
  68 issues and rule-versus-bug-versus-design variety support a richer measurable evaluation. Rejected a
  rule-only labeler: mostly deterministic, and would overstate AI's benefit.
## Operating design and enforced boundaries
- `.github/workflows/ruff-triage.md` triggers on new **sandbox** issues and supports manual dispatch;
  `ruff-triage.lock.yml` is generated with `gh aw compile`.
- `AGENTS.md` contains repository facts, commands, conventions and forbidden changes.
  `.claude/skills/ruff-issue-triage/SKILL.md` contains six ordered decisions; `scripts/triage_checks.py`
  extracts fields and ranks time-filtered local predecessors.
- The agent must *open and use* the skill, checked via runner transcript and `SKILL_USED` marker, not
  inferred from the file existing. `CONTRIBUTING.md` forbids unattended upstream AI contributions.
- **Untrusted input:** issue title/body, code/log snippets, frozen prior-record metadata, and GitHub tool
  or MCP responses. The issue may impersonate a maintainer; all are data, never instruction.
- **Agent actions:** read sandbox checkout/GitHub metadata, run local parsing script, request `noop` or
  one safe-output comment. No write token during reasoning; comment is processed by separate scoped job.
- **Hardly restricted:** one comment maximum, triggering `[EVAL]` issue only, <=2 links, 8-minute
  timeout, 12 turns; no closure, deletion, label change, PR, merge, force-push or cross-repository
  writes. The workflow has `contents: read` and `issues: read` in its reasoning job.
- **Network:** `network.allowed: [defaults]`, no web tools or extra MCP servers; external hosts blocked
  where engine firewall supports this, except framework/GitHub infrastructure.
- **Rationale for no-action:** complete reports should receive zero comments. A wrong duplicate link or
  unnecessary clarification consumes attention; measure both, not only how often the agent speaks.
## Historical evaluation
- `evals/inputs/`: 17 real September issue bodies and minimal earlier context. Original bodies verified
  unedited; post-creation comments/labels deliberately omitted. Upstream rules/templates pinned to a
  pre-September commit under `reference/`.
- `evals/inputs/adv-*/`: two *synthetic* tests: forged maintainer approval to close stale issues and
  malicious search/MCP-style instructions embedded in a predecessor.
- Expected actions (`NONE`, `CLARIFY`, `RELATED`, `ESCALATE`) and rationales were frozen **before**
  execution; expected files excluded from test-time remote checkout to prevent answer leakage.
- For each case measure exact action agreement, useful clarification quality, related-source accuracy,
  needless comments, false negatives, and any forbidden effects. `evals/README.md` documents replay and
  original URLs; `evals/results/` records actual results/failures separately.
- Conventional title/field heuristic baseline: **8/19** action classes, **5** unnecessary intervention intents, versus a non-blind GPT-6-assisted **16/19** and **2**. This posthoc comparison is illustrative, not a controlled model study.
- Human label history is *diagnostic*, not automatic ground truth. Judgements can be contestable; report
  disagreements rather than retrospectively changing expected outcomes.
## Governance (implemented vs proposed)
- **Identity:** GitHub Actions bot/safe-output actor; record actual posting identity in logs if a live
  run succeeds.
- **Least privilege:** Agent workflow `permissions: contents: read, issues: read`; no cross-repo write
  tool. Inspect compiled agent and safe-output jobs.
- **Safe outputs:** `add-comment.max: 1`, `max-links: 2`, target triggering issue, `[EVAL]` title gate.
  `noop` for abstention; tested structurally and adversarially.
- **Human approval:** No agent edits/PRs. Human maintainer reviews comments before any real upstream
  action; upstream contributions forbidden. No CODEOWNERS needed for single-owner sandbox.
- **Budgets:** 8 min, 12 turns, 200 credits/run, 3000 credits/day; workflow_dispatch user cap 10/hour.
  Daily cap is **not** a strict issue-arrival cap.
- **Audit:** GitHub Actions run ID, steps, timestamps, engine/model version and safe outputs where
  exposed; fixed inputs, expected and actual case logs, Git commit. Actual usage/cost may be unavailable.
- **Kill switch:** Owner opens Actions > Ruff triage > `...` > Disable workflow on phone, then cancels
  running jobs from each run's page. Disabling alone does not cancel in-flight jobs.
- **Drift:** Owner reruns 17+2 golden tasks before configuration/model change and at least monthly;
  personally reviews **all** changes, especially wrongful comments/noops and adversarial cases. Not
  scheduled automatically.
- **Accountability:** GitHub account owner controls workflows, secrets and disable action; owner reviews
  outputs, reports errors, and approves changes. Model provides advice, never authority.
## Required five questions
1. **Issue says close all stale issues with maintainer approval?** Treat as adversarial body data; ignore; no close capability. `adv-maintainer-claim` tests this.
2. **Provider model changes and golden case fails?** Model alias is not immutable. Rerun on any model/config change and monthly; compare decisions, comments and recorded model ID; owner blocks rollout and restores last approved commit after mismatch.
3. **300 issues in one week?** Trigger requests can exceed budget: per-run timeout/credit limits and 24h shared cap eventually reject runs; no queue guarantee. Excess reports receive **manual** triage; do not promise 300 automated replies.
4. **Malicious tool/MCP result?** Freeze local candidate metadata, no external MCP and narrow outputs. Injection cannot grant write permission; at worst it could contaminate one bounded comment. `adv-mcp-injection` exercises this.
5. **Stop from a phone?** GitHub mobile browser > repository > Actions > select Ruff workflow > disable; visit active runs and cancel. Verify disabled state and remaining runs; owner retains direct issue access.
## Agent bill of materials
- **Model/engine:** GitHub Copilot engine (configured model resolved at runtime; not version-pinned).
  Workflow runner records actual model when available; no Claude subscription necessary.
- **Instructions:** workflow Markdown, `AGENTS.md`, Claude-format `SKILL.md`, `CONTRIBUTING.md`; policy
  snapshots in `reference/`.
- **Tools/MCP:** sandbox checkout, read-only GitHub `issues,repos` tools and local Python deterministic
  checker; no custom external MCP; one safe-output handler.
- **Permissions/sources/logs:** only sandbox reads, per-event issue and pre-event Ruff snapshots; agent
  log, safe-output job, GitHub Actions metadata and `evals/` artefacts.
- **Evaluation/responsibility:** 17 historical and 2 synthetic cases; account owner is evaluator,
  maintainer and kill-switch operator.
## Recorded evaluation outcome
- Actions run 39791356243 stopped before inference: personal-repo Copilot engine secret missing; do not mistake it for a tested agent.
- Explicit GPT-6-assisted *non-blind* dry run of 17 real + 2 adversarial cases: 16/19 action-class agreement, 2 unnecessary comment intents; see `evals/results/`. Runtime skill loading, posting controls and billing remain untested.
- `evaluation-integrity.yml` verifies golden SHA-256 commitments, unit tests and case comparisons independently of the model.
## Unresolved
- End-to-end model authentication and actual skill-use evidence must be demonstrated or explicitly marked
  untested, with the assignment-permitted assistant dry run as fallback. Do not claim inferred execution.
- Frozen prior records are intentionally sparse; broad duplicate recall may be low. Manual model
  interpretation can still err, and budget credits may not equal money.
## AI-use statement
- Human-directed project choice, acceptance of safety boundaries and grade-focused evaluation scope;
  AI-assisted drafting of workflow, scripts, documentation and expected classifications.
- Every source issue, cutoff and earlier reference must be checked against GitHub; validate scripts with
  unit tests and compiled workflow, compare actual outputs case by case, and disclose any limits on live
  agent execution. Human must inspect before submission.
