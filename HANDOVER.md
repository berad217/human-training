# Handover — human-training

**Session date:** 2026-07-20
**State:** Plugin at **1.15.3**, both manifests aligned. Working tree clean. **CI is green** —
see item 1: the `verify-powershell` job had been chronically red (since ~1.14.0) and is now fixed.
No skill graduated this session — content refreshes only, to the `codex-cli` and `start` skills
(both Track 2, `skills-source/`). Prior ships (`antigravity-cli` 1.14.0, `codex-cli` 1.15.0)
remain committed, pushed, tagged, and released on GitHub.

---

## Recent work (most recent first)

1. **Fixed chronically-red CI** (`5215a06` + `5b4b2dd`, no version bump): `verify-powershell` had
   failed on *every* push since ~1.14.0 while `verify-bash` passed — nobody noticed on unprotected
   main. Root cause: shipped `.py` assets fell under `* text=auto`, so the committed `skills/` tree
   checked out **CRLF** on the Windows runner while both builders emit **LF**, failing the parity
   diff on every line. Fix: pin `.py/.txt/.js/.ts/.css/.html` to `eol=lf` in `.gitattributes` (no
   plugin content change — index blobs were already LF), and add `.gitattributes` to the workflow's
   `paths:` filter so such changes re-run the check. **Both jobs now green.**
2. **`codex-cli` version-mismatch nudge → 1.15.3**: added a first-use check (`codex --version` vs
   `npm view @openai/codex version`) instructing the agent to surface a stale CLI to the user —
   the skill is often the *only* thing positioned to notice, so it doubles as an update prompt.
   Placed in the always-read honesty block, not the (skippable) install section. Bumped local CLI
   to **0.144.6** in the process; the pre-existing `models cache: missing field
   supports_reasoning_summaries` startup error was a **stale cache from the old CLI** and cleared
   after the upgrade + one refresh run (verified — a real instance of the footgun the nudge warns about).
2. **`codex-cli` refreshed for GPT-5.6 → 1.15.2** (`552b771`): made the skill model-forward —
   new "Picking the model" section mapping **Sol/Terra/Luna → Opus/Sonnet/Haiku** (default Terra,
   escalate to Sol, drop to Luna for mechanical work); documented that **`--ignore-user-config`
   discards the config.toml model default** so it must be paired with explicit `-m`; corrected the
   reasoning-effort enum to `minimal|low|medium|high|xhigh` (+ `max` for 5.6 per the 0.143.0
   changelog, not yet in config-reference); refreshed version/default to `0.144.1`/`gpt-5.6-sol`.
   Model string dogfood-verified via a Luna smoke test (exit 0). **Deliberately excluded** the
   subscription-economics / "near-free capacity" angle — that's a personal-workflow argument, not
   a repo concern; Brad is still deciding where (if anywhere) it lives.
2. **`start` skill hardened → 1.15.1** (`dcb341e`): reworked doc location to **glob-first**
   (never assume a hardcoded path — empty glob, *then* "missing") and added **role-based
   bridging** so it maps chronicle/handover/queue by role rather than filename, following
   onboarding's map (and one hop through any active-project pointer) on non-canonical layouts.
   Edited in `skills-source/start/SKILL.md`, rebuilt, version-bumped both manifests.
2. **Drafts residue-vs-genuine clarified** (`6f417dc`) in `skills-drafts/README.md`: a folder
   there is either a genuine draft or post-graduation residue; disambiguator is "does a matching
   `skills-source/<name>/` exist?".
3. Earlier: **graduated `codex-cli`** (headless `codex exec` driver) → v1.15.0, [release "Exec
   Order"]; verified 20/20 triggering via blind subagent judges. **Graduated `antigravity-cli`**
   (headless `agy` driver) → v1.14.0, [release "Defying Gravity"].

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
- Branch protection on `main` still deferred (solo direct-to-main).

---

*Ephemeral bridge — prune once absorbed. Durable record: the shipped skills, the GitHub
releases, `skills-source/codex-cli/SKILL.md` (the 1.15.2 GPT-5.6 refresh),
`skills-source/start/SKILL.md` (the 1.15.1 fix), `skills-drafts/README.md`, and auto-memory.*
