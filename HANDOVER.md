# Handover — human-training

**Session date:** 2026-07-20
**State:** Plugin at **1.15.5**, both manifests aligned. Working tree clean. **CI is green** and
**`main` is now branch-protected** (see items 3–4). No skill graduated this session — content
refreshes only, to the `codex-cli`, `antigravity-cli`, and `start` skills (all Track 2,
`skills-source/`). Prior ships (`antigravity-cli` 1.14.0, `codex-cli` 1.15.0) remain committed,
pushed, tagged, and released on GitHub.

---

## Recent work (most recent first)

1. **`antigravity-cli` quiet-failure frame + version-drift check → 1.15.5** (`5f88720`, "Radio
   Silence"): ported the two transferable ideas from the codex field-notes pass, *adapted* not
   copied — a TL;DR "agy degrades quietly → assume-degraded-until-verified" meta-rule (cross-linked
   to codex-cli), and a version check *inverted* for agy's silent self-update (not "go update" but
   "re-test the version-pinned empty-stdout bug, it may have been silently fixed"). Finer field-notes
   items skipped — already present in agy-specific form.
2. **`codex-cli` field notes folded in → 1.15.4** (`8afd89c`, "Trust but Verify"): integrated items
   A–E from the (now-deleted) `codex-cli-field-notes.md` staging doc around one frame — Codex fails
   *quietly*. TL;DR meta-rule; §4 `-o`-not-always-pristine (read-only apology preamble) + one-`-o`-
   path-per-run + model-identity added to the unreliable-narrator lesson; §6 banner-as-model-of-record
   + effort-per-leg-class; four new §8 troubleshooting rows.
3. **Branch protection enabled on `main`** (2026-07-20): required checks (`verify-bash` +
   `verify-powershell`) + require-PR (0 approvals), but **`enforce_admins=false`** so admins push
   directly — because the `gh` token here **cannot create/merge PRs** (see delta + auto-memory
   [[gh-token-cannot-do-prs]]). Also dropped the PR paths filter so required checks always report.
4. **Fixed chronically-red CI** (`5215a06` + `5b4b2dd`): `verify-powershell` had failed on *every*
   push since ~1.14.0 while `verify-bash` passed — unnoticed on then-unprotected main. Cause: shipped
   `.py` assets under `* text=auto` checked out **CRLF** on the Windows runner vs the builders' **LF**.
   Fix: pin `.py/.txt/.js/.ts/.css/.html` to `eol=lf` in `.gitattributes` (index blobs already LF, no
   content change) + add `.gitattributes` to the workflow paths. Both jobs green.
5. **`codex-cli` GPT-5.6 refresh + version nudge → 1.15.2 / 1.15.3**: model-forward "Picking the
   model" section (**Sol/Terra/Luna → Opus/Sonnet/Haiku**, default Terra); `--ignore-user-config`
   discards the model default (pair with `-m`); reasoning enum `minimal|low|medium|high|xhigh` (+`max`
   for 5.6); a first-use version-mismatch nudge; local CLI bumped to **0.144.6**. **Excluded** the
   subscription-economics angle (personal-workflow, not a repo concern — Brad deciding where it lives).
6. Earlier this session: **`start` hardened → 1.15.1** (glob-first + role-based bridging); drafts
   residue-vs-genuine note (`6f417dc`). Prior: `codex-cli` 1.15.0 ("Exec Order"), `antigravity-cli`
   1.14.0 ("Defying Gravity").

## The delta (not in the files)

- **Codex CLI research is current as of 2026-07-20** (from OpenAI's `learn.chatgpt.com` docs):
  live frontier family is **GPT-5.6** (Sol/Terra/Luna, added CLI `0.143.0` on Jul 8). Brad's
  machine is now on **`0.144.6`** (upgraded this session from `0.144.1`); the non-fatal
  `models cache: missing field supports_reasoning_summaries` startup error was a stale cache from
  the old CLI and is **gone** after the upgrade + one refresh run. Codex usage is metered as
  **messages per rolling 5h window, weighted by model** — the honest shape behind the (excluded)
  economics angle.
- **Trigger evals can't use the real harness in this environment.** Nested `claude -p`
  **401s** here (confirmed by probe), so `run_trigger_eval_win.py` would report every query
  as a false negative. The working method is **blind subagent judges**: spawn N general-purpose
  agents, give each the unlabeled queries + a realistic skill menu (the skill under test +
  its real confusables + "none"), have them classify, then tally majority vote vs the gold
  labels yourself. 3 judges × 20 queries was fast and unanimous. (Reinforces auto-memory
  `project_skill-creator-optimizer-broken-on-windows`.)
- **`skills-drafts/` is now clean:** `ollama/` (live, low-priority draft — keep), plus
  residue from shipped skills (`antigravity-cli-workspace/` re-runnable eval harness,
  `gemini-api/research/`, `pdf-toc-splitter/test_pdf_splitter.py`), plus `README.md`.
- **`.gitignore` excludes `*.log`** (skill-dev run artifacts).

## Parked / carried

- **Confining `agy` to its cwd** — agy agents must not bash their way to places they should
  never be. No verified flag-based cwd jail yet (`--sandbox` + auto-approving `toolPermission`
  is the untested candidate); only **tool-free deprivation** (don't give agy file tools;
  inline content yourself — the consultant pattern) reliably scopes it today. Settle in a
  throwaway isolated dir.
- **`ollama`** — live but low priority; graduate when it earns it.
- Branch protection on `main` is **enabled** (2026-07-20): PRs required (0 approvals — solo
  self-merge), `verify-bash` + `verify-powershell` must be green, enforced for admins too. **Direct
  pushes to main are blocked** — work on a branch and open a PR (`gh pr create` → wait for CI →
  `gh pr merge`). To relax if the friction bites: set `enforce_admins=false` (admin override) or
  lift protection in repo settings. The verify workflow runs on *all* PRs to main (no paths filter)
  so required checks always report.

---

*Ephemeral bridge — prune once absorbed. Durable record: the shipped skills, the GitHub
releases, `skills-source/codex-cli/SKILL.md` (the 1.15.2 GPT-5.6 refresh),
`skills-source/start/SKILL.md` (the 1.15.1 fix), `skills-drafts/README.md`, and auto-memory.*
