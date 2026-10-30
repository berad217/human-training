# Handover — human-training

**Session date:** 2026-10-30. Landed the coordinator worker role (PR #7) and
shipped 1.44.0 "Workers Read One Page", CI green on the PR and on main. Queue
is `TASKS.md`; durable know-how is `docs/maintainer-notes.md`.

## The delta

- **Pending test — claude.ai auto-sync, now live.** 1.44.0 was released
  16:04Z. Read "Synced commit" on the account marketplace *before* clicking
  Check for updates: already at the 1.44.0 commit = the September toggle fix
  worked.
- **`skills-drafts/night-shift/` is untracked and must stay out of git.** It
  is the coordinator's pre-scrub draft: it names people, machines and a
  project. Undecided (Brad): move it out of the repo, or gitignore it.
- **Merged branch still checked out** in `../ht-coordinator-worker`
  (`coordinator-worker-role`, local and remote). Safe to remove once nothing
  is running there.

## Next

1. The auto-sync check above.
2. Probe 1.40–1.44 (TASKS Active).
