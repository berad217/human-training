# Handover — human-training

**Session date:** 2026-09-12 (bookkeeping pass over the 2026-09-11 session)
**State:** **1.28.0 shipped** (`critic-loop`), tagged and released. **1.27.0 cut
retroactively** the same night — it had sat unreleased for 23 days because the
version-bump ritual never said to cut a GitHub release; the ritual now does.
Tree clean and in sync. Nothing in flight.

What shipped is in the release notes; don't restate it here.

---

## The queue is `TASKS.md`

Anything with a next action lives there. This file carries only what is
contested, unproven, or decided-but-not-obvious.

---

## Read this before probing anything

**The verification technique works and it will lie to you if you use it wrong.**
`claude -p --plugin-dir <repo> "<organic prompt>"` loads the working tree, so a
skill can be exercised before release without touching the installed plugin.
It found a real UTC bug and proved skill-to-skill chaining. It also produced a
false result that reached a release and deleted a working feature.

**Two rules, both non-optional:**

1. **Pass `--allowedTools Skill Read Glob Grep Bash`.** Without it the headless
   session's permission posture is variable, and `Skill` gets denied on some runs
   and not others. A denied `Skill` call means the skill never loaded and the
   agent hand-rolls the task instead — while sounding completely authoritative.
2. **Read outcomes, not requests.** A `tool_use` block is the model *asking*.
   What happened is in the paired `tool_result`, which is where
   `Permission to use Skill has been denied` sits.

Two further habits, learned the same way:

- **Run probes from a scratch directory, never from this repo.** `onboarding.md`
  tells agents not to invoke `human-training:*` skills here, which suppresses the
  trigger and yields a false negative.
- **Believe the subject.** Two runs stated in their own prose that Skill was
  blocked. That was overridden on the strength of a trace that had not been fully
  parsed. The subject was right.

**Negative results are weak; positive results are strong.** A found bug is a
found bug. "It didn't do X" from one run proves nothing.

## The delta (not in the files)

- **`critic-loop` lives in two places on purpose.** `skills-source/critic-loop/`
  is what ships. `skills-drafts/critic-loop/` stays because its `rounds/` are the
  evidence log (the two off-image rounds that gated graduation) and the draft
  README holds the n=4 observation below. Don't "tidy" the drafts copy away.

- **An observation, not a rule (n=4):** four times a critic marked an item *"not
  safe to take without review"* for a reason only the author could resolve, and
  each was taken as a logged deviation. Honest with a scrupulous author,
  rationalisation with a careless one, and the author can't tell which. It stays
  in the draft README until someone other than the author has watched it happen.

- **`/start` step 2d works. Do not delete it again.** 1.25.0 removed it on
  misread probe evidence and 1.26.0 put it back. The tell that you are about to
  repeat the mistake is a probe where 2d "silently didn't fire" — check for a
  denied `Skill` call before believing it.

- **The evidence ladder does not catch instrument failure.** It grades *how
  much* evidence stands behind a claim; both 2026-08-19 overclaims were a check
  that ran, produced output, and was misread. Unresolved.

- **Don't fold the ladder into the confidence score, and don't centralize it.**
  Confidence is how sure the agent feels; the rung is what was checked. Names
  and order shared, definitions local (settled 1.23.1).

- **`autoUpdate` absent does not mean "never refreshes".** 2d reports on the two
  fields, not on a theory of the mechanism.

- **The pstack rejections, so they aren't re-derived:** `poteto-mode`'s router,
  `swarm`, `arena`, `interrogate`, `architect`, `how`/`why`, `recall` (overlaps
  `/start`), `automate-me`. `unslop` would fight this repo's own prose — fork,
  don't adopt.

- **Branch protection is settled; don't reopen it.** "Bypassed rule violations"
  on push is the rule working. `enforce_admins` false, `berad217` the only write
  path.

## What is now actually verified

Watched running with a sound instrument: **`/start`** (globbing incl. uppercase
`HANDOVER.md`, TASKS Active only, unpushed-commit reporting, read-only contract,
step 2d) and **`leroy-jenkins` → `show-me-your-work`** chaining.
**`critic-loop`** was run on itself twice before shipping (that is the only
skill here judged by its own protocol).

Still assumed: `grill`, `tasks`, `handover-manager`, `project-checkup`,
`robustness-audit`, and everything in `skills-drafts/`.

## Toolchain data point

This machine is on **1.28.0** (installed 2026-09-11 22:13Z, three minutes
*before* the 1.28.0 release was cut — so it came from the tag or a manual update,
not the release loop). The `human-training` marketplace `lastUpdated` then
advanced to **2026-09-12 10:00Z** on its own. That is one data point toward
"`autoUpdate` keeps firing across relaunches" (still open in `TASKS.md`); it is
not yet proof the *plugin* follows the catalog. Other machines: unknown, and
they were seven releases behind at last check.

## Parked for the next session

`docs/the-new-rules-of-context-engineering-for-claude-5-generation.md` is the
Anthropic post on removing 80% of Claude Code's system prompt for Claude 5
models. Saved 2026-09-10, committed 2026-09-12, not yet read against
`skills-source/`. The open question is whether it becomes an audit lens on how
verbose these skill bodies are.

---

*Ephemeral bridge — prune once absorbed. Durable record: the release notes,
`TASKS.md` for the queue, and the skill bodies themselves.*
