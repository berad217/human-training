# Handover — human-training

**Session date:** 2026-08-02
**State:** **1.19.0 shipped — "The Other Laptop".** Project memory moves in-repo
for private repos; `workflow-orientation` §6 owns the policy and migration,
`/start` gains a detect-and-offer at 2c. Committed, pushed, tagged
`human-training--v1.19.0`, released. Both builders byte-identical, manifests
aligned.

What shipped is in the release notes; don't restate it here. **Needs a full quit
+ relaunch to load** — a new thread is not enough.

---

## The delta (not in the files)

- **The migration procedure has never been run.** It was written this session
  against a real, measured problem and executed against nothing. §6 is
  documentation, not tested behaviour — **the first real run is the test**, and
  it should be one project end to end before the other twenty-five.

- **The inventory that motivated it, which is recorded nowhere durable:** 216
  memory files across 26 projects, 666 KB, all stranded at the harness's global
  path on one machine. `Writey-McWriteFace` alone holds 89. That is the backlog
  §6 exists to clear, and it evaporates with this handover if nobody acts on it.

- **The behavioural checklist is still UNRUN, now across three releases.** 1.19.0
  adds `/start` 2c and two changed descriptions; nobody has watched any of it
  run, and triggering is still unmeasured. The build proves bytes and never
  behaviour.

- **Full Opus 5 tuning on Track 1 was a deliberate call, not an oversight.** Brad
  chose it knowing the five model-agnostic guides also ship to Codex and Gemini
  agents. Don't revert it as a portability bug; shell-portability is a separate,
  still-enforced CI constraint.

- **`genesis.md` remains the target pattern** — lean body plus `> read
  assets/...` pointers. The other guides are converging on it.

## Parked / carried

- **First checkable after relaunch:** does `handover-manager` actually have
  `Bash` at runtime? Does Desktop show the full skill count (the
  tagging-fixes-stale-copy hypothesis, unconfirmed since 1.17.0)?
- `ollama` — live, low-priority draft.
- image-gen empirical gaps (real-photo identity fidelity, multi-`-i`
  compositing, macOS/Linux copy-out).

## Next steps

1. Relaunch, then run the two post-relaunch checks above.
2. Migrate one project's memory end to end — that exercises §6 for the first
   time and is worth more than reading it again.
3. Exercise the behavioural checklist; it now spans three versions of unverified
   change.

---

*Ephemeral bridge — prune once absorbed. Durable record: the 1.19.0 release
notes and `workflow-orientation` §6.*
