# Handover — human-training

**Session date:** 2026-06-19
**State:** All work committed AND pushed. `main` at `7f07bfb`, tree clean. Plugin
**1.12.0** now has its **first tagged release** (`human-training--v1.12.0`), so the
skills reach the desktop/web/phone apps, not just the CLI. Nothing in flight.

---

## This session (short version — detail lives elsewhere)

Solved the "newer human-training skills are missing in the desktop/web app" mystery
and shipped the fix. Full root cause + diagnostic playbook are in **auto-memory**
(`desktop-prefers-stale-remote-human-training`); the cross-device publish step is now
in the **README** ("…and to your phone, web, and the desktop app"); the tag + release
are on GitHub. One line: a stale **claude.ai-account (remote)** copy was being
preferred over the current **local CLI** install, and the cure was cutting a
**versioned release** so the remote had something newer to resolve to.

## The delta (not yet in any file)

- **Fuzzy bit, on purpose:** it works on web + desktop, but we never isolated whether
  the account marketplace actively *re-pulled* the release or whether the **full
  desktop restart** alone cleared a cache. Brad's call: "whether it pulled the remote
  or not, it works." Don't re-investigate unless it regresses — memory has the tells.
- **New publish discipline:** cross-device changes now need `claude plugin tag --push`
  (+ optional `gh release create`) on top of build → bump → push. `update-plugin.bat`
  still only covers local CLI machines.

## Deferred by choice (not blocked)

- **Leroy 1.12.0 live test** — the stated-goals-first-class + unattended-mode behavior
  is shipped but never exercised live. Brad is parking it until he has *inference to
  burn* and a real goal (the Unreal-learning project). Confidence is fine: even the old
  prescriptive style stayed steerable with a little prompting.

## Carried forward (durable, unchanged)

- **Matt-skills roadmap — NEXT = `diagnose`** (disciplined live-bug loop; the dynamic
  counterpart to `robustness-audit`). Behind it: `improve-codebase-architecture`, `tdd`.
- Branch protection on `main` still deferred (solo direct-to-main).

---

*Ephemeral bridge — prune once absorbed. The durable record is the commits, README,
and auto-memory.*
