# Maintainer notes — human-training

Durable knowledge about working *on* this repo that lived in `HANDOVER.md`
across sessions until 2026-09-25, when it was moved here: it is Record, not
Delta. The handover now carries only what is live. Read the probing section
before probing anything.

---

## Probing a skill

**The verification technique works and it will lie to you if you use it wrong.**
`claude -p --plugin-dir <repo> "<prompt>"` loads the working tree's `skills/`
(the **build output**, so rebuild first or you probe the old body). Eight clean
probes as of 2026-09-19, one false result that once reached a release.

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
is two audit runs disagreeing on the headline finding. **The evidence ladder
does not catch instrument failure:** both 2026-08-19 overclaims were a check
that ran and was misread.

**Cost.** `/start`, `handover-manager`, `workflow-orientation`,
`onboarding-creator` probes are $0.50–1. `gemini-api` on a review-and-fix
prompt is ~$0.85. `leroy-jenkins` with a stated goal is ~$1.15 without
subagents. `robustness-audit` is $6–15 because it dispatches. (Opus 5 era
figures; unchecked on Opus 5.5.)

**Fixtures.** A 60-line Python CLI (`tempo/`: parse a workout log, weekly
totals; 3 pytest tests; `onboarding.md`, `docs/DEVLOG.md`, `TASKS.md` with three
Active items) is enough for every non-audit skill; drop `onboarding.md` to
probe `onboarding-creator`. Five minutes to rebuild. Add a bare remote + one
unpushed commit + one uncommitted red test for handover; four commits past the
last DEVLOG entry for orientation. For `gemini-api`: a captioner on the
deprecated SDK with a retired id, `temperature`, `sleep(0.2)` and no error
handling, README saying "600 images, free tier", **no `GEMINI_API_KEY`** —
the missing key is the point: "no key → snapshot id + startup guard + say so"
is the contract working. Read a hardcoded id *without* the guard and the
disclosure as the miss.

**Which host loaded what.** The desktop app serves the claude.ai-account copy
of the plugin, not the local install, and a session's skill bodies can be many
releases stale (see README, "...and to your phone, web, and the desktop app").
Check the version in the loaded skill's path before trusting what it did.

## What has been watched running

With a sound instrument, under Claude Code only: `/start`, `robustness-audit`,
`antigravity-cli`, `codex-cli`, `leroy-jenkins`, `handover-manager`,
`workflow-orientation`, `critic-loop` (on itself), `onboarding-creator`,
`gemini-api`. **Nothing has been live-run under Codex.**

Never probed: `grill`, `tasks`, `project-checkup`, `lifecycle-manager`,
`project-genesis`, everything in `skills-drafts/`, and the 1.40–1.42 changes
(the `Reply:` lines, `/start` status tags and `diff --stat`, Leroy's no-stop
line).

## Building and editing

- **The trim classifier** (10 of 11 skills trimmed by 2026-09-19): keep what
  the model cannot observe by looking; fold anti-patterns into the step they
  guard; examples, templates, lists and history go to a reference pointed at
  from the step; add `Reply:`. Cuts ran 38% (`gemini-api`) to 59%
  (`onboarding-creator`). `critic-loop` (4.6k, already has a reference) is the
  one left, lowest expected gain.
- **Track 1 has no `reference.md` slot.** Guides ship through `build_skill`
  with synthesized frontmatter; the only extra files are `assets/` copied from
  `workflow/templates/`. A Track 1 reference lives at
  `workflow/templates/<skill>-reference.md`, added to the assets list in
  **both** builders. Diff the two builders' output (`-OutputDir` on the ps1)
  before committing — CI does the same with `diff -r`.
- **The Bash tool's heredoc mangles `\\`.** A Python patch that should write a
  backslash-newline continuation writes a literal `\n` into `build-skills.sh`;
  the build then silently skips an asset named `n`. The only tell is
  `WARNING: asset not found`. Grep the build output for `warn` every time, and
  use the Edit tool, not a heredoc, for builder edits.
- **`critic-loop` lives in two places on purpose.** `skills-source/` ships;
  `skills-drafts/critic-loop/rounds/` is the evidence log. Don't tidy it.
- **`/start`'s toolchain check works. Do not delete it again** (1.25.0 removed
  it on a misread probe; 1.26.0 restored it). A probe where it "silently
  didn't fire" means a denied `Skill` call — check that first.
- **`/reload-plugins` does not refresh the marketplace catalog.** Only a full
  app quit/relaunch runs the autoUpdate fetch (verified 2026-09-19).

## Settled, so nobody re-derives them

- **pstack rejections:** `poteto-mode`'s router, `swarm`, `arena`,
  `interrogate`, `architect`, `how`/`why`, `recall` (its status-tag contract
  was adopted into `/start` in 1.41.0; the skill itself was not),
  `automate-me`. `unslop` would fight this repo's prose; fork, don't adopt.
- **Branch protection:** "Bypassed rule violations" on push is the rule working.
- **Issue #6 was bot outreach**, closed without comment. The tell is the
  star:fork ratio. Ignore the genre.
