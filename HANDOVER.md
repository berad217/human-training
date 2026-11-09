# Handover — human-training

**Session date:** 2026-11-09. Shipped 1.46.0 "The Expensive One Consults"
(`91e819e`), CI green on main, release cut. Workflow: editing a Track 2 skill
(`coordinator`), then the version bump. Nothing is in flight; the tree was
clean after the release. Queue is `TASKS.md`; durable know-how is
`docs/maintainer-notes.md`.

## The delta

- **Two coordinator additions have never run.** "Which shape for a job" and
  the advisor (reference.md; evidence rows 44 and 45) came from the hosted
  platform's multi-agent docs and Brad's suggestion, not from a shift. The test
  is one shift with the coordinator on a cheaper model. Judge it by the consult
  log in the return brief, and by the usage meter against a normal night.
- **A consult has no cost figure.** The log line records trigger, question and
  result. No way was found for the coordinator to read one subagent's spend;
  the fallback is a usage reading before and after.
- **Pending test — claude.ai auto-sync.** Carried from 2026-10-30 and still
  unread across 1.44.0–1.46.0. Read "Synced commit" on the account marketplace
  *before* clicking Check for updates: already at `91e819e` means the September
  toggle fix worked.
- **`skills-drafts/night-shift/` is gone from this checkout.** The old question
  (move it out, or gitignore it) resolved as moved; `.gitignore` has no entry.
- **A stale Codex worktree:** `codex/start-self-ref-check`, under the Codex
  app's worktrees folder. The branch has nothing main lacks and the worktree is
  clean, so both can go. Brad's call; not removed.
- **`evidence.md` has two rows numbered 41** (the roster report, and Codex
  delegation). Left alone; a consolidation pass can renumber.

## Next

1. The auto-sync check above, then update each machine.
2. Run a shift on a cheaper coordinator with the advisor on.
3. Probe 1.40–1.44 (TASKS Active).
