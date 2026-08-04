# Handover — human-training

**Session date:** 2026-08-03
**State:** **1.21.0 shipped — "The Smoke Alarm".** `/start` gains step 2d: it
notices when the plugin toolchain has silently stopped updating. Committed,
pushed, tagged `human-training--v1.21.0`, released. CI green; builders
byte-identical. Follows **1.20.0 — "You're On The Latest"** the same session.

What shipped is in the release notes; don't restate it here.

---

## The delta (not in the files)

- **2d's correct output is silence, and silence is indistinguishable from the
  check never having run.** That makes it the least verifiable thing shipped so
  far — a green build proves the bytes and says nothing about whether the step
  fires. Settle it by running `/start` on a machine whose `autoUpdate` is **off**
  and confirming a `Toolchain:` line appears. Silence on *this* machine is the
  expected result and therefore proves nothing.

- **The behavioural checklist is now UNRUN across five releases** (1.17–1.21).
  This has been carried in every handover since 1.17.0 and has never been the
  thing that got done. It is now the largest unverified surface in the repo.

- **`autoUpdate` firing at startup is still unproven.** One refresh observed on
  2026-08-03, immediately after the flag was set. Not yet seen across a relaunch.
  2d is built on the assumption that `lastUpdated` keeps advancing, so this is
  worth an actual check rather than an assumption.

- **Every other machine is now two releases behind the fix**, and still cannot
  receive either one until someone runs `update-plugin.bat` there by hand and
  sets `autoUpdate` after. The backlog compounds with each release.

- **Three pushes this session bypassed branch protection.** Each reported
  "Changes must be made through a pull request" and "2 of 2 required status
  checks are expected"; admin rights let them through. CI was watched to green
  *manually* before each release was published, but the configured rule was not
  honoured. Either start using PRs or relax the rule — the current state is a
  guardrail that only pretends to hold.

- **2d's constraints are load-bearing and easy to "helpfully" undo** — no network
  call, no `settings.json` write, never the recommended next move. The reasoning
  for each is in the 1.21.0 release notes. Read it before relaxing any of them.

- **`claude-plugins-official` has `autoUpdate` off too** (`lastUpdated`
  2026-06-12). Found in passing, still not acted on. 2d should now surface it.

- **Rejected options, so they aren't re-derived:** a SessionStart hook (now
  definitively redundant — `autoUpdate` is the built-in); a local-path
  marketplace (fixes the dev box, breaks GitHub-as-distribution); dropping the
  plugin for `~/.claude/skills/` (**unknown whether Desktop reads that path** —
  would trade a stale path for a dead one).

## Parked / carried

- **§6 memory migration remains never-run**; 216 files / 26 projects / 666 KB
  still stranded. Unchanged since 1.19.0.
- `ollama` draft; image-gen empirical gaps (identity fidelity, multi-`-i`
  compositing, macOS/Linux copy-out).
- `genesis.md` remains the target pattern for guide bodies.

## Next steps

1. **Exercise the behavioural checklist.** Five releases overdue, and 2d is the
   cheapest entry point: one `/start` on an un-fixed machine.
2. Confirm `autoUpdate` fires on relaunch, not just once when set.
3. Bring one other machine current by hand — which also tests whether the
   two-step recovery in `onboarding.md` §2 is written correctly.

---

*Ephemeral bridge — prune once absorbed. Durable record: the 1.20.0 and 1.21.0
release notes, `onboarding.md` §2, `skills-source/start/SKILL.md` §2d, and
`scripts/check-plugin-state.ps1`.*
