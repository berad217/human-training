# Handover — human-training

**Session date:** 2026-09-25. Shipped 1.40.0–1.42.0, all CI green; what
shipped is in the release notes. Queue is `TASKS.md`; durable know-how moved
to `docs/maintainer-notes.md`.

## The delta

- **Pending test — claude.ai auto-sync.** Brad toggled "Sync automatically"
  off/on (~18:15Z) after proving it dead. On the next release, read "Synced
  commit" *before* clicking Check for updates: already moved = fixed.
- **Relaunch pending.** The desktop app still serves a cached old copy (this
  session's `/start` and `handover-manager` loaded pre-1.29 bodies). Full
  quit/relaunch before trusting any desktop-invoked skill.
- **Brad's global CLAUDE.md changed** (Teflon scope: no mid-task stops unless
  blocked or destructive; long-run report order Blocked on me / Changed /
  Found / Next). Live from the next session; watch whether stops drop.
- **1.40–1.42 are unprobed.** Riskiest: `/start` status tags.
- **Undecided (Brad):** `onboarding-creator`'s two templates — collapse or
  keep.

## Next

1. Probe `/start` tags on `tempo/` with a handover that overclaims.
2. Probe `leroy-jenkins` no-stop line.
