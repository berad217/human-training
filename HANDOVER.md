# Handover — human-training

**Session date:** 2026-06-16
**State:** All work committed AND pushed. Plugin **1.12.0**, both manifests
aligned, sh-build `diff -r` parity clean, working tree clean. Latest substantive
commit `2cc4ef3` (leroy → 1.12.0); this handover refresh sits on top. **This
machine has NOT yet restarted onto 1.12.0** — user is about to run
`update-plugin.bat`. Nothing in flight.

---

## What this session did

Made the **`leroy-jenkins`** skill less prescriptive at launch and shipped it as
1.12.0.

| Commit | What |
|--------|------|
| `2cc4ef3` | **leroy-jenkins: stated goals first-class + unattended mode.** (1) A goal you state at invocation is now a first-class work surface, co-equal with the canned Full Treatment / Audit Blitz modes — those become the *no-goal fallback*, so no more railroad into project-checkup/robustness-audit. (2) New "Unattended / long-haul runs" section for "do as much as you can, I'm going to bed" runs — plan + checkpoint to DEVLOG, delegate chunks to subagents to stay context-lean, and a reversible-or-park policy for LOW-confidence forks when no one's there to ask. (3) Dropped `allowed-tools` so Leroy inherits the Agent tool (needed for the subagent delegation). → 1.12.0 |

**Detour worth knowing:** this clone was **7 commits behind origin** at session
start (and carried stale uncommitted leroy edits). The first bump went to 1.11.0
— which origin had already shipped for the `tasks` skill — so it collided and
forced a rebase onto origin's tip. leroy's SKILL.md had zero conflict; only the
manifest version line clashed. Lesson saved to auto-memory: **`git fetch` and
check `HEAD..origin/main` before bumping versions in this repo.**

## Untested — the calibration to run next

The new Leroy behavior is **shipped but not yet exercised live.** Cleanest test is
the user's own Unreal-learning project:
`/leroy-jenkins run with the curriculum, pick sensible next features, document
choices, playtest when there's time` — confirm it treats the stated goal as the
work instead of showing the two-option audit menu. The unattended/subagent path
wants a separate "I'm going to bed" run to confirm it delegates and checkpoints.

## Matt-skills adoption roadmap (the delta that only lives here)

- **DONE:** `grill`, `CONTEXT.md`, `tasks` (tasks not from Matt — lifted from
  Anthropic's productivity plugin, stripped for a solo hobbyist).
- **NEXT (still recommended):** `diagnose` — disciplined live-bug loop (reproduce
  → hypothesise → instrument → fix → regression-test), the *dynamic* counterpart
  to `robustness-audit`. Scrub Matt's CONTEXT/ADR cross-refs → DEVLOG on the way in.
- **Behind it:** `improve-codebase-architecture` (heavier); `tdd` (better folded
  into `lifecycle-manager` than shipped standalone).
- **SKIP (decided):** issue-tracker-paradigm skills, `handoff` (handover-manager
  is better), `write-a-skill` (have skill-creator), misc.

## Open / next (carried forward)

- **Other machines** need `update-plugin.bat` + restart to reach 1.12.0.
- **CI not visually confirmed** — repo is private and `gh` isn't installed
  locally, so the invariant was run by hand (sh-build `diff -r` clean + manifests
  aligned) and is expected green; glance at the Actions tab to be sure.
- **`start`↔`tasks` still untested** in a real downstream project.
- **README cheek** — user hasn't nitpicked the voice; tweakable. (This session
  made one small in-voice tweak to the leroy row's "when to reach for it" cell.)
- Still open from before: branch protection on `main` (deferred — fights solo
  direct-to-main).

---

*Ephemeral bridge — prune once the next session absorbs it. The durable record is
the commits, onboarding, README, and auto-memory.*
