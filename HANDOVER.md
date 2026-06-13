# Handover — human-training

**Session date:** 2026-06-13
**State:** All work committed AND pushed. `origin/main` == local @ `ae50c84`,
plugin **1.11.1**, both manifests aligned, working tree clean. This machine has
been restarted onto 1.11.1 (`grill` / `start` / `tasks` now load). Nothing in
flight.

---

## What this session did

Two threads: (1) chased down why the plugin never auto-updated and shipped a
fix; (2) built the `tasks` skill end-to-end and gave the README a personality.

| Commit | What |
|--------|------|
| `65b7f13` | **`update-plugin.bat`** — one-click `marketplace update` + `plugin update` onramp. |
| `eeccead` | Bumped to 1.10.1; documented the onramp in README + onboarding. |
| `c00d9f6` / `a687953` | Design spec + implementation plan for the tasks skill (brainstorming → writing-plans). |
| `c883308` | **`tasks` skill** (per-project `TASKS.md`: Active/Someday/Done + a notices-&-offers mission-creep guardrail) + **`/start` now surfaces Active tasks** at orient; shipped 1.11.0; rewrote README in the markdown_reticulator cheeky voice. |
| `ae50c84` | **Durable Matt Pocock attribution** for `grill` (skill footer + README Credits) + a "two ways to use this repo" audience framing; 1.11.1. |

## The plugin-update root cause (the real find)

`autoUpdate: true` only refreshes the marketplace *catalog* at Claude Code
**startup**, and on these machines it wasn't firing — the catalog froze (stuck
at 1.5.0 for weeks). It is NOT network/auth/divergence: a manual `git fetch`
worked instantly and history is linear. Reliable fix = `update-plugin.bat`
(force `marketplace update` → `plugin update` → full restart). **`plugin update`
keys off the version string, not content** — so every skills change MUST bump
`version`, or the onramp silently no-ops. Now documented in README + onboarding.

Decided **against** the `--plugin-dir` live-from-repo model (user found it
confusing) — staying on marketplace + `update-plugin.bat`.

## Matt-skills adoption roadmap (the delta that only lives here)

- **DONE:** `grill`, `CONTEXT.md` — both now durably credited to Matt Pocock
  (mattpocock/skills, MIT, © 2026 Matt Pocock) in `grill`'s SKILL.md + README
  Credits, no longer just in this file.
- **`tasks`** shipped this session — NOT from Matt; lifted the TASKS.md idea from
  Anthropic's `productivity` plugin and stripped it to fit a solo hobbyist (no
  dashboard, no tracker sync, no shorthand-decoding).
- **NEXT (still recommended):** `diagnose` — disciplined live-bug loop
  (reproduce → hypothesise → instrument → fix → regression-test), the *dynamic*
  counterpart to `robustness-audit`. Scrub Matt's CONTEXT/ADR cross-refs → DEVLOG
  on the way in.
- **Behind it:** `improve-codebase-architecture` (heavier); `tdd` (better folded
  into `lifecycle-manager` than shipped standalone).
- **SKIP (decided):** `to-issues`/`to-prd`/`triage`/`setup-matt-pocock-skills`
  (issue-tracker paradigm), `handoff` (handover-manager is better),
  `write-a-skill` (have skill-creator), misc.

## Decisions made in conversation (not obvious from the diff)

- **`tasks` is per-project, Track 2, authored straight in `skills-source/`**
  (skipped the skills-drafts dance — nothing to retain there); the `TASKS.md`
  template is **inlined in SKILL.md**, not a separate asset.
- **TASKS vs DEVLOG boundary:** TASKS is the forward queue (next / parked / done,
  lightweight); DEVLOG is backward-looking decisions + rationale. Done entries
  are checkbox + date, never a changelog.
- **README voice = markdown_reticulator cheeky-but-useful** (saved to auto-memory
  as `readme-voice-preference`).

## Open / next

- **Other machines** still need `update-plugin.bat` + restart to reach 1.11.1.
- **CI not visually confirmed** — repo is private and `gh` isn't installed
  locally, so CI's exact invariant was run by hand (sh-build `diff -r` clean +
  manifests aligned) and is expected green; glance at the Actions tab to be sure.
- **`start`↔`tasks` is live but untested in a real downstream project** — worth
  calibrating: open a downstream project, run `/start`, see if Active surfaces well.
- **README cheek** — user hasn't nitpicked the voice yet; tweakable if a line
  doesn't land.
- Still open from before: branch protection on `main` (deferred — fights solo
  direct-to-main).

---

*Ephemeral bridge — prune once the next session absorbs it. The durable record is
the commits, onboarding, README, and auto-memory.*
