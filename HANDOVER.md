# Handover — human-training

**Session date:** 2026-06-28
**State:** Two skills graduated and shipped this session — **`antigravity-cli`** (v1.14.0)
and **`codex-cli`** (v1.15.0). Both **committed, pushed, tagged, and released** on GitHub.
Plugin at **1.15.0**. Working tree clean. **Not yet installed on this machine** (`/plugin
update` / `update-plugin.bat` pending).

---

## This session (short version)

1. Triaged last session's uncommitted tree and **graduated `antigravity-cli`** (headless
   `agy` driver) → v1.14.0, [release "Defying Gravity"].
2. Pruned a stale "Matt-skills roadmap" from the handover (the Matt Pocock adaptation is
   closed — orthogonal skills adopted + credited, clone deleted; `diagnose` etc. were never
   real backlog).
3. **Graduated `codex-cli`** (headless `codex exec` driver) → v1.15.0, [release "Exec
   Order"]. It had been used by hand for ages but was never a formal skill. Authored its
   `evals/trigger-eval.json` from the existing `eval-queries.md` candidates and verified
   **20/20** triggering via blind subagent judges (see method note below). Draft folder
   deleted entirely — no residue.
4. **Documented the drafts confusion** in `skills-drafts/README.md`: a folder there is
   either a genuine draft or post-graduation residue; the disambiguator is "does a matching
   `skills-source/<name>/` exist?".

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

*Ephemeral bridge — prune once absorbed. Durable record: the shipped skills, the two GitHub
releases, `skills-drafts/README.md`, and auto-memory.*
