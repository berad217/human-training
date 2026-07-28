# Handover — human-training

**Session date:** 2026-07-28
**State:** **1.18.0 shipped.** Repo-wide skill alignment to the Claude 5
context-engineering guidance — committed (`ac1d8d0`), pushed, tagged
`human-training--v1.18.0`, CI green (`verify-bash` + `verify-powershell`),
plugin updated 1.17.0 → 1.18.0 at user scope. **Needs a full quit + relaunch
to load** — a new thread is not enough.

What shipped is in the commit message and the release notes; don't restate it
here.

---

## The delta (not in the files)

- **The behavioural checklist is still UNRUN, and the surface just grew.**
  Carried unexercised from 1.17.0. 1.18.0 adds two changes nobody has watched
  run: `robustness-audit` now reports-then-filters, so its **output volume
  changed by design** and the new shape is unseen; and five descriptions were
  trimmed 1321 → 1111 words with **triggering unmeasured** (skill-creator's
  optimizer is broken on Windows — blind subagent judges are the workaround).
  The build proves bytes. It proves nothing about behaviour.

- **Glob brittleness is a confirmed pattern now, not an anecdote.** Two
  instances, one per session: `**/*handover*.md` missed the root `HANDOVER.md`
  (case-sensitivity), and `{dir}/**/*.md` missed `dir/SKILL.md` (needs a
  subdirectory to match). Both fail the same way — **an empty result reads as
  "verified clean"** — which is the worst possible failure mode for an audit
  step. This currently exists only as prose in handovers that get pruned. It
  deserves to be a real line in a skill.

- **Full Opus 5 tuning on Track 1 was a deliberate call, not an oversight.**
  Brad chose it knowing the five model-agnostic guides also ship to Codex and
  Gemini agents. Don't revert it as a portability bug. Shell-portability is
  still a hard CI constraint and was preserved separately.

- **`genesis.md` is the target pattern.** Lean body plus `> read assets/...`
  pointers; it needed no changes this pass. The other guides are converging on
  it — that's the direction, if the refining continues.

## Parked / carried

- **First checkable after relaunch:** does `handover-manager` actually have
  `Bash` at runtime? Does Desktop show 16 skills (the tagging-fixes-stale-copy
  hypothesis, still unconfirmed since 1.17.0)?
- `ollama` — live, low-priority draft.
- image-gen empirical gaps (real-photo identity fidelity, multi-`-i`
  compositing, macOS/Linux copy-out).

## Next steps

1. Relaunch, then run the two post-relaunch checks above.
2. Exercise the behavioural checklist — it now spans two versions of
   unverified change.

---

*Ephemeral bridge — prune once absorbed. Durable record: commit `ac1d8d0`,
the 1.18.0 release, and `docs/specs/2026-07-24-session-durability-design.md`.*
