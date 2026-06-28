# Handover — human-training

**Session date:** 2026-06-28
**State:** New skill **`antigravity-cli`** graduated to `skills-source/`, built, and
verified. Plugin bumped to **1.14.0**. **Committed locally — NOT yet pushed**, and
**not yet installed on any machine** (`/plugin update` pending).

---

## This session (short version)

Triaged last session's uncommitted tree, then **graduated `antigravity-cli`** (the
headless `agy` driver, eval-green 20/20 + 6/6 regression) from `skills-drafts/` to
`skills-source/`. Followed the `gemini-api` precedent: SKILL.md + `evals/trigger-eval.json`
ship; dev docs (draft README, eval-queries.md) dropped; the Windows trigger-eval harness
stayed behind in `skills-drafts/antigravity-cli-workspace/`. Build parity (`diff -r`),
manifest validity, and version alignment all green. Bundled the triage cleanups into the
same commit.

## The delta (not in the files)

- **Committed, not pushed.** One commit on `main`:
  `feat(skills): graduate antigravity-cli — headless agy driver (1.14.0)`. To go live:
  `git push`, then per machine `claude plugin marketplace update human-training` +
  `claude plugin update human-training@human-training` (or `update-plugin.bat`), then
  fully relaunch. Codex installs need a reinstall/cache-refresh + new thread.
- **`.gitignore` now excludes `*.log`** — skill-dev run artifacts (e.g. the eval
  `run_loop.log`) no longer show as untracked.
- **Eval harness retained.** `skills-drafts/antigravity-cli-workspace/`
  (`run_trigger_eval_win.py` + `trigger-eval.json`) is the re-runnable Windows trigger
  eval — the optimizer is broken on Windows, so this hand-rolled runner is the way to
  re-measure triggering. Not shipped (skills-drafts isn't built).
- **Writey incident — closed.** The stray-file recovery folder was deleted this session
  (you confirmed it was safe). writey_claude owned/owns all Writey recovery; this repo is
  clean of it. The footgun stays captured in the `antigravity-cli` skill (§6 + provenance).

## Parked / untested (carried)

- Whether `agy --sandbox` + an auto-approving `toolPermission` can HARD-confine `agy` to
  cwd the way Codex's sandbox does. No verified flag-based cwd confinement yet — only
  tool-free deprivation reliably scopes it. Worth settling in a throwaway isolated dir.
- Matt-skills roadmap — **NEXT = `diagnose`**; behind it `improve-codebase-architecture`, `tdd`.
- **Leroy** live test still never exercised.
- Branch protection on `main` still deferred (solo direct-to-main).

---

*Ephemeral bridge — prune once absorbed. Durable record: the shipped `antigravity-cli`
skill, the codex-cli/antigravity-cli §4 notes, and auto-memory.*
