# Handover — human-training

**Session date:** 2026-09-19 (second session)
**State:** **1.38.0 and 1.39.0 shipped** — `onboarding-creator` and `gemini-api`
through the trim, both probed live before release, CI green on both. Tree
clean and in sync. Nothing in flight.

What shipped is in the release notes; don't restate it here.

---

## The queue is `TASKS.md`

Anything with a next action lives there. This file carries only what is
contested, unproven, or decided-but-not-obvious.

---

## Read this before probing anything

**The verification technique works and it will lie to you if you use it wrong.**
`claude -p --plugin-dir <repo> "<prompt>"` loads the working tree's `skills/`
(the **build output**, so rebuild first or you probe the old body). Eight clean
probes now, one false result that once reached a release.

**Rules, all non-optional:**

1. **Pass `--allowedTools Skill Read Glob Grep Bash`**, plus `Agent` for skills
   that dispatch, `Edit Write` for skills that write, `WebFetch` for
   `gemini-api`. Without it `Skill` gets denied on some runs and not others,
   and a denied `Skill` call means the agent hand-rolls the task while
   sounding authoritative.
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
6. **Print the final reply with `PYTHONIOENCODING=utf-8`.** The summarizer
   script died on a `→` in the subject's last message under cp1252 and the
   most important paragraph of the probe (what it could not verify) was
   nearly missed.

**Negative results are weak; positive results are strong.** The variance floor
is two audit runs disagreeing on the headline finding.

**Cost.** `/start`, `handover-manager`, `workflow-orientation`,
`onboarding-creator` probes are $0.50–1. `gemini-api` on a review-and-fix
prompt is ~$0.85. `leroy-jenkins` with a stated goal is ~$1.15 without
subagents. `robustness-audit` is $6–15 because it dispatches.

**Fixtures.** A 60-line Python CLI (`tempo/`: parse a workout log, weekly
totals; 3 pytest tests; `onboarding.md`, `docs/DEVLOG.md`, `TASKS.md` with three
Active items) is enough for every non-audit skill; drop `onboarding.md` to
probe `onboarding-creator`. Five minutes to rebuild. Add a bare remote + one
unpushed commit + one uncommitted red test for handover; four commits past the
last DEVLOG entry for orientation. For `gemini-api`: a captioner on the
deprecated SDK with a retired id, `temperature`, `sleep(0.2)` and no error
handling, README saying "600 images, free tier", **no `GEMINI_API_KEY`** —
the missing key is the point (below).

## The delta (not in the files)

- **The trim method is 10 for 11.** Only `critic-loop` remains (4.6k, already
  has a reference, lowest expected gain — it may not be worth a release).
  The classifier held on every skill: keep what the model cannot observe by
  looking; fold anti-patterns into the step they guard; examples, templates,
  lists and history go to a reference pointed at from the step; add `Reply:`.
  Cuts ran 38% (`gemini-api`, dense with footguns) to 59% (`onboarding-creator`,
  which carried each section three times).

- **`/reload-plugins` does not refresh the marketplace catalog.** Verified
  this session: after the reload the catalog clone was still at `15f698f`
  (1.34.1), `lastUpdated` unchanged. Only a full app quit/relaunch runs the
  autoUpdate fetch — exactly what `/start` 2d and `onboarding.md` §2 say, now
  with evidence. Worth one line in `start`'s reference if it is not there.
  Further proof of lag: **this session's `handover-manager` invocation loaded
  the pre-1.36.0 body** (the old anti-patterns section, no `Reply:` line) —
  the desktop app is serving the stale plugin while the repo is at 1.39.0.

- **`autoUpdate` does fire on relaunch** — the catalog advanced 09-16 → 09-18
  22:03 EDT and the install moved 1.34.0 → 1.34.1. It lags three-plus
  releases only because that refresh ran 19 minutes before 1.35.0 landed. One
  relaunch now should land 1.39.0 and close the TASKS item; not done yet
  because Brad had other sessions mid-job both times.

- **"No key → snapshot id + startup guard + say so" is the contract working.**
  The `gemini-api` probe could not run `models.list()` (no key in the
  environment), so it took an id from the do-not-copy snapshot, added a guard
  that fails fast if the id is not live on the caller's key, and said in its
  reply that the id and the limit numbers were unverified. Do not read a
  hardcoded id in that situation as a miss; read a hardcoded id *without* the
  guard and the disclosure as one.

- **`onboarding-creator` ships two templates on purpose.** `assets/onboarding.md`
  is minimal and defers to a local `docs/.agents/lifecycle.md`; the
  self-contained skeleton in `assets/onboarding-reference.md` inlines the rules
  for projects that carry no lifecycle guide. Collapsing them changes what the
  asset assumes downstream — Brad's call, not a trim's. Undecided.

- **Track 1 has no `reference.md` slot.** Guides ship through `build_skill` with
  synthesized frontmatter; the only extra files are `assets/` copied from
  `workflow/templates/`. A Track 1 reference lives at
  `workflow/templates/<skill>-reference.md`, added to the assets list in
  **both** builders. Diff the two builders' output (`-OutputDir` on the ps1)
  before committing — CI does the same with `diff -r`.

- **The Bash tool's heredoc mangles `\\`.** A Python patch that should write a
  backslash-newline continuation writes a literal `\n` into `build-skills.sh`;
  the build then silently skips an asset named `n`. The only tell is
  `WARNING: asset not found` in the build output. Grep the build output for
  `warn` every time, and use the Edit tool, not a heredoc, for builder edits.

- **`Reply:` contracts now on 7 of 12 shipped skills** (`blast-radius`,
  `gemini-api`, `handover-manager`, `leroy-jenkins`, `onboarding-creator`,
  `show-me-your-work`, `workflow-orientation`). The TASKS item "add to every
  skill" is half done as a side effect of trimming; the untrimmed ones
  (`grill`, `tasks`, `project-checkup`, `lifecycle-manager`, `project-genesis`)
  are where it is missing.


- **Issue #6 was bot outreach**, closed without comment. The tell is the
  star:fork ratio. Ignore the genre.

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
**`antigravity-cli`**, **`codex-cli`**, **`leroy-jenkins`**, **`handover-manager`**,
**`workflow-orientation`**, **`critic-loop`** on itself, **`onboarding-creator`**
(one trigger, reference opened only where the body points, `skip:` line for
the inapplicable section, 115-line output with no padding), **`gemini-api`**
(one trigger after the provider grep, SDK swapped, sampling params dropped
with the Gemma caveat stated, introspected the installed SDK for timeout
units instead of guessing). All under Claude Code only; **nothing has been
live-run under Codex** despite five releases now claiming host-agnostic bodies.

Still assumed: `grill`, `tasks`, `project-checkup`, `lifecycle-manager`,
`project-genesis`, and everything in `skills-drafts/`.

## Toolchain data point (2026-09-25)

CLI install reached 1.39.0 after a relaunch (TASKS item closed). The
**desktop/web** copy is a separate claude.ai-account copy and had been stuck
at 1.21.1 for seven weeks with auto-sync on; "Check for updates" under Manage
marketplaces moved it to 1.40.0. That is now a manual release step (README,
onboarding). Whether auto-sync ever resumes on its own is unknown.

---

*Ephemeral bridge — prune once absorbed. Durable record: the release notes,
`TASKS.md` for the queue, and the skill bodies themselves.*
