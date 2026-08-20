# Handover — human-training

**Session date:** 2026-08-19
**State:** **Seven releases shipped: 1.22.0 → 1.26.0.** All committed, pushed,
tagged, released; CI green on each; builders byte-identical; tree clean and in
sync. Nothing in flight.

The session began as an audit of [pstack](https://github.com/cursor/plugins/tree/main/pstack)
(MIT) and ended in a retraction. What shipped is in the release notes; don't
restate it here.

---

## The queue is `TASKS.md`

Anything with a next action lives there. This file carries only what is
contested, unproven, or decided-but-not-obvious.

---

## Read this before probing anything

**The verification technique works and it will lie to you if you use it wrong.**
`claude -p --plugin-dir <repo> "<organic prompt>"` loads the working tree, so a
skill can be exercised before release and without touching the installed plugin.
It found a real UTC bug and it proved skill-to-skill chaining. It also produced a
false result that reached a release and deleted a working feature.

**Two rules, both non-optional:**

1. **Pass `--allowedTools Skill Read Glob Grep Bash`.** Without it the headless
   session's permission posture is variable, and `Skill` gets denied on some runs
   and not others. A denied `Skill` call means the skill never loaded and the
   agent hand-rolls the task instead — while sounding completely authoritative.
2. **Read outcomes, not requests.** A `tool_use` block in the stream is the model
   *asking*. What happened is in the paired `tool_result`, which is where
   `Permission to use Skill has been denied` sits. Parsing `tool_use` alone is
   how three probe runs looked like a skill choosing not to act when the skill
   had never run at all.

Two further habits, learned the same way:

- **Run probes from a scratch directory, never from this repo.** `onboarding.md`
  tells agents not to invoke `human-training:*` skills here, which suppresses the
  trigger and yields a false negative.
- **Believe the subject.** Two runs stated in their own prose that Skill was
  blocked. That was overridden on the strength of a trace that had not been fully
  parsed. The subject was right.

**Negative results are weak; positive results are strong.** A found bug is a
found bug. "It didn't do X" from one run proves nothing — run-to-run variance is
real, and one run leaked a DEVLOG entry two others correctly withheld.

## The delta (not in the files)

- **`/start` step 2d works. Do not delete it again.** 1.25.0 removed it on the
  evidence above and 1.26.0 put it back. Verified with `Skill` permitted: the
  skill loads, reads `known_marketplaces.json`, and emits a correct `Toolchain:`
  line. The tell that you are about to repeat the mistake is a probe where 2d
  "silently didn't fire" — check for a denied `Skill` call before believing it.

- **The evidence ladder does not catch instrument failure, and that is a real
  gap.** It grades *how much* evidence stands behind a claim. Both overclaims
  this session were a different shape: the check ran, produced output, and the
  output was misread. A rung-4 "I ran a script" is worthless if the script
  measured the wrong thing. Unresolved; worth thinking about before the ladder is
  cited as though it covers this.

- **Don't fold the ladder into the confidence score.** The obvious tidy-up and
  wrong. Confidence is how sure the agent feels; the rung is what was checked.
  The finding worth catching is the one that is 95-confident at rung 2.

- **Don't centralize the ladder either.** Settled 1.23.1 after measuring: ~14 of
  32 lines are portable, and rung 3 means genuinely different things in
  `robustness-audit` and `blast-radius`. Names and order shared, definitions
  local. A data format earns an owner; a vocabulary does not.

- **`leroy-jenkins` commits its trail; `show-me-your-work` does not by default.**
  Deliberate. Most trails are working artifacts; Leroy's case is the unusual one.

- **`autoUpdate` absent does not mean "never refreshes".** A catalog was observed
  refreshing on 2026-08-19 with the flag absent. 2d's wording was corrected to
  say the flag removes the *guarantee*; report on the two fields, not on a theory
  of the mechanism.

- **The pstack rejections, so they aren't re-derived.** Roughly two-thirds does
  not transfer: it assumes a team, Graphite stacks, MCP-backed observability, and
  subagents on named cross-vendor models the Agent tool cannot address. Rejected:
  `poteto-mode`'s router, `swarm`, `arena`, `interrogate`, `architect`,
  `how`/`why`, `recall` (overlaps `/start`), `automate-me` (this plugin *is* the
  mode skill).

- **`unslop` would fight this repo's own prose.** It bans em dashes,
  mid-sentence colons, and "surface"/"scaffolding" as metaphors; every skill body
  here uses all three deliberately. `TASKS.md` says fork it, not adopt it.

- **Branch protection is settled; don't reopen it.** Every push this session
  printed "Bypassed rule violations" — the rule working, not failing.
  `enforce_admins` false, required reviews 0, `berad217` the only write path.

## What is now actually verified

First time anything in this plugin has been *watched running* rather than
reviewed. Verified with a sound instrument: **`/start`** (doc globbing including
uppercase `HANDOVER.md`, newest-DEVLOG-entry-only, TASKS Active without leaking
Someday, unpushed-commit reporting, read-only contract, and step 2d), and
**`leroy-jenkins` → `show-me-your-work`** chaining with every alternative path
blocked.

Everything else is still assumed, including all of `grill`, `tasks`,
`handover-manager`, `project-checkup`, and `robustness-audit`.

## Stale, not merely queued

1. **Every other machine is seven releases behind** (1.22–1.26) and cannot receive
   any of them until someone runs `update-plugin.bat` there and sets `autoUpdate`.
   **This machine is too** — still on 1.21.1.
2. **`autoUpdate` firing across a relaunch remains unproven.**

---

*Ephemeral bridge — prune once absorbed. Durable record: the 1.22.0–1.26.0
release notes, `TASKS.md` for the queue, and the skill bodies themselves.*
