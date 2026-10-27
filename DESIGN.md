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
- `.github/workflows/ruff-triage.md` triggers on owner-authorised **sandbox** `[EVAL]` issues and supports manual dispatch;
  `ruff-triage.lock.yml` is generated with `gh aw compile`.
- `AGENTS.md` contains repository facts, commands, conventions and forbidden changes.
  `.claude/skills/ruff-issue-triage/SKILL.md` defines the four dispositions; a trusted pre-agent
  Python check binds each sandbox issue to a frozen historical source, embeds its unedited body and
  ranks pre-cutoff predecessor titles without relying on the model to fetch live GitHub data.
- The updated instruction demands an observable skill-file read before classification.
  Both 27 October synthetic live runs independently log reading all 51 lines of the
  Claude-format skill. This does not prove compliance in all historical runs.
  `CONTRIBUTING.md` forbids unattended upstream AI contributions.
- **Untrusted input:** issue title/body, code/log snippets, frozen prior-record metadata, and GitHub tool
  or MCP responses. The issue may impersonate a maintainer; all are data, never instruction.
- **Agent actions:** a trusted Actions step checks the issue event and writes `runtime-binding.json`;
  model reads the embedded original issue plus time-filtered metadata, then requests `noop` or a
  bounded comment. No write token during reasoning; a separate scoped handler posts comments.
- **Enforced restrictions:** one comment maximum, triggering `[EVAL]` issue only, <=2 links, 6-minute
  timeout, 9 turns; no closure, deletion, label change, PR, merge, force-push or cross-repository
  writes. The workflow has `contents: read` and `issues: read` for model execution.
- Comment **600-character brevity is advisory**, not an enforced platform length cap; count, link,
  target and title restrictions are enforced by compiled safe outputs.
- **Network:** `network.allowed: [defaults]`, no web tools or extra MCP servers; external hosts blocked
  where engine firewall supports this, except framework/GitHub infrastructure.
- **Rationale for no-action:** explicit `on.status-comment: false` prevents implicit
  status comments. Complete reports should receive zero agent comments. A wrong duplicate link or
  unnecessary clarification consumes attention; measure both, not only how often the agent speaks.
## Historical evaluation
- `evals/inputs/`: 17 real September issue bodies and minimal earlier context. Original bodies verified
  unedited; post-creation comments/labels deliberately omitted. Upstream rules/templates pinned to a
  pre-September commit under `reference/`. Index covers May–Aug titles only, not all history;
  titles might have been edited after their original creation.
- `evals/inputs/adv-*/`: two *synthetic* tests: forged maintainer approval to close stale issues and
  malicious search/MCP-style instructions embedded in a predecessor.
- Expected actions (`NONE`, `CLARIFY`, `RELATED`, `ESCALATE`) and rationales were frozen **before**
  execution; expected files excluded from test-time remote checkout to prevent answer leakage.
- For each case measure exact action agreement, useful clarification quality, related-source accuracy,
  needless comments, false negatives, and any forbidden effects. `evals/README.md` documents replay and
  original URLs; `evals/results/` records actual results/failures separately.
- Conventional title/field heuristic baseline: **8/19** action classes, **5** unnecessary intervention intents,
  versus a non-blind GPT-6-assisted **16/19** and **2**. This posthoc comparison is illustrative, not a
  controlled model study.
- Human label history is *diagnostic*, not automatic ground truth. Judgements can be contestable; report
  disagreements rather than retrospectively changing expected outcomes.
## Governance (implemented vs proposed)
- **Identity:** actual sandbox comments were posted by `github-actions[bot]` via the safe-output handler;
  no comment or issue was posted upstream.
- **Least privilege:** Agent job has contents:read and issues:read only; no
  cross-repository write tools. Compiled activation/safe-output/conclusion jobs
  have issues:write, and safe-output/conclusion also have pull-requests:write
  from the framework despite no PR safe-output being enabled. This broader
  job-level token remains a residual risk; the compiler's generated lockfile
  should not be hand-edited.
- **Safe outputs:** add-comment max 1, max-links 2, triggering sandbox issue
  with [EVAL] title. noop handles abstention. Two inappropriate comments in
  ten historical runs remained within the cap. Both separate live synthetic
  injections yielded noop and zero comments on 27 October.
- **Human approval:** No agent edits/PRs. Human maintainer reviews comments before any real upstream
  action; upstream contributions forbidden. No CODEOWNERS needed for single-owner sandbox.
- **Budgets:** 6 min, 9 turns, 12 AI Credits/run, 80/day; workflow_dispatch user cap 10/hour.
  Daily cap is **not** a strict issue-arrival cap.
- **Audit:** GitHub Actions run IDs, model selector `copilot/auto`, posted comments and per-run AIC,
  fixed input/golden checksums and actual classes in `evals/results/live_runs.json`; provider model
  sub-version and monetary billing were not independently available.
- **Kill switch:** Owner disables Ruff triage under Actions and cancels active runs separately.
  The switch was exercised: GitHub confirmed `disabled_manually` after the sample.
- **Drift:** Owner should rerun a small preselected golden subset before any model/config change,
  review all comments against source evidence, and use live adversarial checks before real deployment.
  Not scheduled automatically, to avoid wasted credits.
- **Accountability:** GitHub account owner controls workflows, secrets and disable action; owner reviews
  outputs, reports errors, and approves changes. Model provides advice, never authority.
## Required five questions
1. **Issue says close all stale issues with maintainer approval?** Treat as adversarial body data; ignore; no
   close capability. `adv-maintainer-claim` tests this.
2. **Provider model changes and golden case fails?** Model alias is not immutable. Rerun on any model/config
   change and monthly; compare decisions, comments and recorded model ID; owner blocks rollout and restores last
   approved commit after mismatch.
3. **300 issues in one week?** Ordinary public issues fail the role/title gate before inference;
   for 300 permitted `[EVAL]` cases, trigger requests can exceed budget: per-run timeout/credit limits and 24h shared
   cap eventually reject runs; no queue guarantee. Excess reports receive **manual** triage; do not promise 300
   automated replies.
4. **Malicious tool/MCP result?** Freeze local candidate metadata, no external MCP and narrow outputs. Injection
   cannot grant write permission; at worst it could contaminate one bounded comment. `adv-mcp-injection`
   exercises this.
5. **Stop from a phone?** GitHub mobile browser > repository > Actions > select Ruff workflow > disable; visit
   active runs and cancel. Verify disabled state and remaining runs; owner retains direct issue access.
## Agent bill of materials
- **Model/engine:** GitHub Copilot engine (configured model resolved at runtime; not version-pinned).
  Workflow runner records actual model when available; no Claude subscription necessary.
- **Instructions:** workflow Markdown, `AGENTS.md`, Claude-format `SKILL.md`, `CONTRIBUTING.md`; policy
  snapshots in `reference/`.
- **Tools/MCP:** sandbox checkout, read-only GitHub `issues` tools and local Python deterministic
  checker; no custom external MCP; one safe-output handler.
- **Permissions/sources/logs:** only sandbox reads, per-event issue and pre-event Ruff snapshots; agent
  log, safe-output job, GitHub Actions metadata and `evals/` artefacts.
- **Evaluation/responsibility:** 17 historical and 2 synthetic cases; account owner is evaluator,
  maintainer and kill-switch operator.
## Recorded evaluation outcome
- Initial run 39791356243 failed before inference (missing Copilot secret). After authentication,
  model routing and event-binding corrections, 10 real issue-triggered workflows completed.
- **Live accuracy:** 3/10 exact class, 7/10 comment-versus-silence; 2 comments, both substantively
  problematic; 6.339795 AI Credits in primary runs. Posthoc deterministic baseline: **7/10** on this
  subset (not a held-out comparison). See `evals/results/live_report.md` and `live_runs.json`.
- GPT-6-assisted **non-blind** dry run: 16/19 classes on 17 real + 2 synthetic
  fixtures, not equivalent to live evaluation. Both synthetic cases were then
  run live on 27 October: 2/2 safe no-action outputs, 1.178925 AI Credits
  total, excluded from the ten real-case accuracy denominator.
- Runs spanned an initial and a revised workflow rubric, so the aggregate is **not a single-version
  estimate**. All failures and the extra #28503 retest remain recorded, without replacing gold.
- `evaluation-integrity.yml` verifies unit tests and the compiled restrictions; on `submission`
  it verifies all 19 golden SHA-256 commitments, and on gold-free `main` the hash check skips.
## Unresolved
- Live inference and sandbox safe-output execution are verified. Two
  fresh traces independently show the complete skill read, although earlier
  historical skill reads and universal instruction compliance remain unproven.
- AI-assisted second-pass review retained gold, marking #28483 contestable.
  Independent **human** adjudication is still outstanding.
- Frozen prior records are intentionally sparse; broad duplicate recall may be low. Manual model
  interpretation can still err, and budget credits may not equal money.
## AI-use statement
- Human selected Ruff and authorised sandbox publication; GPT-6 generated the implementation,
  most instructions, expected classifications and dry-run records. Do not imply user-authored code.
- Verification performed: authenticated GitHub snapshots, 22 unit tests, lock compilation, CI,
  historical source binding, real Copilot logs, observed comments and per-run credit accounting.
  Independent human adjudication remains outstanding; two subsequent live
  synthetic attacks and explicit skill-file reads are separately recorded.
