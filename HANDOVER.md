# Handover — human-training

**Session date:** 2026-09-19
**State:** **1.35.0, 1.36.0, 1.37.0 shipped** in one session — `leroy-jenkins`,
`handover-manager`, `workflow-orientation` through the trim, each probed live
before release. Tree clean and in sync. Nothing in flight.

What shipped is in the release notes; don't restate it here.

---

## The queue is `TASKS.md`

Anything with a next action lives there. This file carries only what is
contested, unproven, or decided-but-not-obvious.

---

## Read this before probing anything

**The verification technique works and it will lie to you if you use it wrong.**
`claude -p --plugin-dir <repo> "<prompt>"` loads the working tree's `skills/`
(the **build output**, so rebuild first or you probe the old body). Six clean
probes now, one false result that once reached a release.

**Rules, all non-optional:**

1. **Pass `--allowedTools Skill Read Glob Grep Bash`**, plus `Agent` for skills
   that dispatch and `Edit Write` for skills that write. Without it `Skill`
   gets denied on some runs and not others, and a denied `Skill` call means the
   agent hand-rolls the task while sounding authoritative.
2. **Read outcomes, not requests.** `tool_use` is the model asking; the paired
   `tool_result` is what happened, and that is where a denial sits.
3. **Count `Skill` calls in the stream — and know which trigger path you used.**
   A slash-command prompt (`/human-training:x ...`) inlines the body: **zero**
   `Skill` calls is correct there, not a denial. An organic prompt should show
   exactly one. More than one means a subagent re-triggered the skill.
4. **Run probes from a scratch or downstream directory, never from this repo.**
   `onboarding.md` suppresses `human-training:*` triggers here.
5. **Believe the subject.** When a run says in its own prose that a tool was
   blocked, it was. It will also tell you when it has spotted the fixture.

**Negative results are weak; positive results are strong.** The variance floor
is two audit runs disagreeing on the headline finding.

**Cost.** `/start`, `handover-manager`, `workflow-orientation` probes are
$0.50–1. `leroy-jenkins` with a stated goal is ~$1.15 without subagents.
`robustness-audit` is $6–15 because it dispatches.

**Fixture.** A 60-line Python CLI (`tempo/`: parse a workout log, weekly
totals; 3 pytest tests; `onboarding.md`, `docs/DEVLOG.md`, `TASKS.md` with three
Active items) is enough for every non-audit skill. Five minutes to rebuild.
Add a bare remote + one unpushed commit + one uncommitted red test for
handover; four commits past the last DEVLOG entry for orientation.

## The delta (not in the files)

- **The trim method is now 5 for 5** (`/start`, `robustness-audit`,
  `antigravity-cli`, `codex-cli`, `image-gen`, then today's three). Keep every
  rule that encodes a fact the model cannot see by looking. Fold anti-pattern
  sections into the step they guard. Move templates, lists, history and worked
  examples to a reference, pointed at from the step. Add a `Reply:` line. Probe
  after. Dense skills (five states + a procedure) cut ~40%, not ~55% — don't
  force it.

- **Track 1 has no `reference.md` slot.** Guides ship through `build_skill` with
  synthesized frontmatter; the only extra files are `assets/` copied from
  `workflow/templates/`. So a Track 1 reference lives at
  `workflow/templates/<skill>-reference.md` and is added to the assets list in
  **both** builders. Diff the two builders' output (`-OutputDir` on the ps1)
  before committing — CI does the same with `diff -r`.

- **The Bash tool's heredoc mangles `\\`.** Twice today a Python patch that
  should have written a backslash-newline continuation wrote a literal `\n`
  into `build-skills.sh`; the build then silently skipped an asset named `n`.
  The only tell is `WARNING: asset not found` in the build output. Grep the
  build output for `warn` every time, and use the Edit tool, not a heredoc,
  for builder edits.

- **`/start`'s docs-only contract is still contested.** Both `/start` probes
  read source diffs to explain a dirty tree, and it was the most useful line
  in the orientation. Undecided whether to permit `git diff --stat` on a dirty
  tree. Decided (1.34.0): the TASKS sweep is its one write.

- **No model ids in skill bodies** (Brad, 2026-09-12; in memory too).
  `gemini-api` is the last skill with ids in the body; it is on the queue.

- **Issue #6 was bot outreach**, closed without comment: identical title on
  216 repos from a 1,707-repo account funnelling into a 290-star/276-fork
  "awesome" list. The tell is the star:fork ratio. Ignore the genre.

- **`critic-loop` lives in two places on purpose.** `skills-source/` ships;
  `skills-drafts/critic-loop/rounds/` is the evidence log. Don't tidy it.

- **`/start` step 2d works. Do not delete it again** (1.25.0 removed it on a
  misread probe; 1.26.0 restored it). A probe where 2d "silently didn't fire"
  means a denied `Skill` call — check that first.

- **The evidence ladder does not catch instrument failure.** Both 2026-08-19
  overclaims were a check that ran and was misread. Unresolved.

- **The pstack rejections, so they aren't re-derived:** `poteto-mode`'s router,
  `swarm`, `arena`, `interrogate`, `architect`, `how`/`why`, `recall`,
  `automate-me`. `unslop` would fight this repo's prose; fork, don't adopt.

- **Branch protection is settled.** "Bypassed rule violations" on push is the
  rule working.

## What is now actually verified

Watched running with a sound instrument: **`/start`**, **`robustness-audit`**,
**`antigravity-cli`**, **`codex-cli`**, **`leroy-jenkins`** (stated goal,
unattended, floor respected), **`handover-manager`** (Step 0 first, `wip:`
commit, offered push without pushing), **`workflow-orientation`** (zero writes,
stopped at Discuss), **`critic-loop`** on itself. All under Claude Code only;
**nothing has been live-run under Codex** despite three releases now claiming
host-agnostic bodies.

Still assumed: `grill`, `tasks`, `project-checkup`, `onboarding-creator`,
`lifecycle-manager`, `project-genesis`, and everything in `skills-drafts/`.

## Toolchain data point

Installed plugin is **1.34.0** (sha `039c50a`); catalog `lastUpdated`
2026-09-16 20:57Z; repo is at **1.37.0**. Four releases unfetched. The
"does `autoUpdate` fire on relaunch" task now has the cleanest fixture it will
ever get — the relaunch was deferred today only because other sessions were
mid-job. Do it first thing next session, before anything else moves.

---

*Ephemeral bridge — prune once absorbed. Durable record: the release notes,
`TASKS.md` for the queue, and the skill bodies themselves.*
