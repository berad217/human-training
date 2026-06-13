# Handover — human-training

**Session date:** 2026-06-08
**State:** All work committed, pushed, CI green (`origin/main` @ `35e8c04`).
Working tree clean except this file. Nothing in-flight. **The user is about to
fully restart Claude Code** to apply plugin **1.10.0** (just updated from a
stale 1.5.0). After restart, `/grill` exists for the first time.

---

## What this session did

Picked up two things from Matt Pocock's skills repo (`P:\software_projects\matt_skills`,
MIT) and fixed a plugin-distribution bug.

| Commit | What |
|--------|------|
| `5175628` | **New `/grill` skill** (Workflow #1, Track 2). Adversarial pre-build alignment — merged Matt's `grill-me` + `grill-with-docs` into one docs-aware skill. → 1.9.0 |
| `cbf61ea` | **Wired CONTEXT.md** (a domain glossary) across the doc family: seed (onboarding-creator + new `workflow/templates/CONTEXT.md` asset), read (start + lifecycle), flush (handover). → 1.10.0 |
| `35e8c04` | **Fixed the plugin-update docs** (onboarding.md + README) — machine-independent, added the missing `marketplace update` step. Docs-only. |

Plus: diagnosed why the user was stuck on 1.5.0 for 2 weeks and ran the update.

## The Matt-skills adoption roadmap (the real delta — only lives here)

- **DONE:** `grill`, `CONTEXT.md`.
- **NEXT (recommended):** `diagnose` — disciplined live-bug loop (reproduce →
  hypothesise → instrument → fix → regression-test). The *dynamic* counterpart
  to `robustness-audit` (which is static). Cleanest standalone adoption; scrub
  Matt's CONTEXT/ADR cross-refs → DEVLOG on the way in.
- **Behind it:** `improve-codebase-architecture` (deep-module refactoring;
  heavier — HTML report + asset files, leans on the CONTEXT.md substrate),
  `tdd` (better folded into `lifecycle-manager` than shipped standalone).
- **SKIP (decided):** `to-issues`/`to-prd`/`triage`/`setup-matt-pocock-skills`
  (issue-tracker paradigm — fights solo direct-to-main), `handoff`
  (handover-manager is better), `write-a-skill` (have skill-creator),
  `caveman`/`zoom-out`/`prototype`/misc (off-axis or niche).

## Decisions made in conversation (not obvious from the diff)

- **`grill` named for the method, not the outcome** (`align`/`crystallize`
  rejected) — the name protects the adversarial tone.
- **ADRs → DEVLOG, not separate `docs/adr/` files** — user keeps one decision
  log (he's not a SWE; solo hobby projects). Captured in auto-memory.
- **CONTEXT.md kept a strict glossary**; seeding is **lazy** (no empty-file
  litter) — `/grill` creates it when a term is worth pinning.
- **Plugin distribution gotcha (now in onboarding.md + README):** `autoUpdate`
  only refreshes the marketplace *catalog* at startup and never auto-installs.
  Each machine needs `claude plugin marketplace update human-training` →
  `claude plugin update human-training@human-training` → **full restart**.

## Invariant checks — all passing

`diff -r skills` byte-identical (PS == sh) · manifests valid + aligned at
1.10.0 · CI green on `cbf61ea` (the last build-affecting commit).

## Open / next

- **Restart**, then **try `/grill` live** on a real downstream project to
  calibrate the grilling voice before building on it.
- Then **`diagnose`** if continuing the adoption.
- Minor loose thread: grill's `CONTEXT-FORMAT.md` (discipline guide) and
  `workflow/templates/CONTEXT.md` (skeleton) overlap slightly — acceptable,
  consolidation optional.
- Still open from before: branch protection on `main` (deferred — fights solo
  direct-to-main).

---

*Ephemeral bridge — once the next session absorbs it, prune it. Durable record
is the commits, onboarding, README, and auto-memory.*
