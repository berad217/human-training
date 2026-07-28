# Handover — human-training

**Session date:** 2026-07-28
**State:** **1.17.0 shipped.** The session-durability change-set is implemented,
committed (`89f55e3`), pushed, tagged `human-training--v1.17.0`, and released as
*"v1.17.0 — Origin Story"*. CI green (`verify-bash` + `verify-powershell`).

**Durability:** clean. `main` in sync with `origin/main`, no `[ahead]` marker,
tag and release both on the remote. Nothing stranded.

**Next session: repo-wide skill refining.** Brad's stated plan — a pass across
all 16 skills rather than another single-skill change.

---

## What shipped

Root bug: `handover-manager` had no `Bash` in `allowed-tools`, so the one skill
responsible for closing a session safely *structurally could not* run
`git status`. Its guide also used "committed" in the prose sense, colliding with
git's verb. Together they let a handover assert "all work committed (SHA, SHA)"
about unpushed local tips.

Five changes: **Step 0 durability check** in `handover-manager` (+ `Bash` in both
builders), **step 2b** `git status -sb` in `start`, **"Make It Durable"** in
`lifecycle-manager`, **`[ahead N]`** surfaced in `project-checkup`, and a
generated **`skills/README.md`** redirect.

Full rationale + the incident narrative:
`docs/specs/2026-07-24-session-durability-design.md`. **Read its §9** — it records
six deviations from the spec as written, so the spec alone does not describe what
shipped.

## The delta (not in the files)

- **`skills/` is `rm -rf`'d on every build.** Anything added at `skills/` root
  must be *emitted by both builders* from a shared source file, or it vanishes on
  the next build. `skills/README.md` works this way
  (`workflow/templates/skills-readme.md` → both builders). This will matter
  immediately in a repo-wide refining pass.
- **Track 1 vs Track 2 determines where you edit.** Five skills
  (`handover-manager`, `lifecycle-manager`, `onboarding-creator`,
  `project-genesis`, `workflow-orientation`) are generated from
  `workflow/guides/` + frontmatter in **both** builders. The other eleven are
  copied from `skills-source/`. Editing `skills/` directly appears to work and is
  silently destroyed. Frontmatter changes must touch both builders or CI goes red.
- **Track 1 bodies ship to non-Claude agents**, so they must stay
  model-agnostic and shell-portable. That's why `| head -1` was dropped from the
  durability command — `head` doesn't exist under PowerShell.
- **Glob matching is case-sensitive even on NTFS.** `/start`'s handover glob
  missed this repo's own root `HANDOVER.md`. Fixed here, but worth checking
  whether other skills' globs have the same blind spot during the refining pass.

## Parked / carried

- **Behavioural checklist is UNRUN** (archived spec §6). The build passing proves
  bytes, not behaviour. Untested: handover in a deliberately-`ahead` repo; a
  no-remote repo; the multi-repo regression case (Blendy + Blocky is live and
  still available as the real test); that no agent pushes unasked. The `[behind N]`
  path is documented but never exercised.
- **Verify `handover-manager` actually has `Bash` at runtime** after
  `update-plugin.bat` + full relaunch. That is the entire fix — everything else is
  text.
- **Does tagging actually fix the stale Desktop/web copy?** That was the
  hypothesis last time. Unconfirmed for 1.17.0 — check Desktop shows 16 skills.
- **`ollama`** — live, low-priority draft.
- **image-gen empirical gaps** (from 1.16.0): real-photo identity fidelity,
  multi-`-i` compositing, macOS/Linux copy-out, adversarial triggering on
  "logo/icon/illustration" phrasings.

---

*Ephemeral bridge — prune once absorbed. Durable record: the four edited skills,
`docs/specs/2026-07-24-session-durability-design.md`, and the 1.17.0 release.*
