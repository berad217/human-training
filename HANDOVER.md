# Handover — human-training

**Session date:** 2026-07-20
**State:** Plugin at **1.15.1**, both manifests aligned. Working tree clean; latest commit
`dcb341e fix(start): glob-first doc location + role-based bridge (1.15.1)`. No skill graduated
this session — the change was a **fix to the `start` skill itself** (Track 2, `skills-source/start/`).
Prior ships (`antigravity-cli` 1.14.0, `codex-cli` 1.15.0) remain committed, pushed, tagged, and
released on GitHub.

---

## Recent work (most recent first)

1. **`start` skill hardened → 1.15.1** (`dcb341e`): reworked doc location to **glob-first**
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
releases, `skills-source/start/SKILL.md` (the 1.15.1 fix), `skills-drafts/README.md`, and
auto-memory.*
