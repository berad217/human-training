---
name: start
description: One-keystroke session opener. Orients to the current project by verifying the workflow docs exist and reading the temporal context (onboarding map, latest DEVLOG entry, current handover), then surfaces a concise orientation and proposes the next move. Docs-only and read-only — no tests run, no files written. Explicit invocation via /start at the top of a fresh session.
allowed-tools: [Read, Glob, Bash]
---

# /start — Fresh-session orient

A friction-killer for the first keystroke of a fresh session. You reset context
often; this removes the cost of remembering to type "read onboarding and the
handover and tell me where we are." One command runs the orient sequence.

This skill is **read-only and docs-only**. It does not run tests, build the
project, or write any file. It reads, summarizes, and proposes — nothing else.

## When to invoke

Explicit invocation via `/start`, typically as the first thing in a new session
on a project that uses this workflow. Do **not** auto-trigger on phrases like
"let's get started" or "where were we" — wait for the command.

## What it is (and what it delegates to)

This is `lifecycle-manager` §1 "Joining a Moving Train," extracted as a
one-keystroke trigger. It does not re-implement orientation logic — it runs the
read sequence and hands off when something is missing:

- **Docs missing or incomplete** → stop orienting and offer
  `human-training:workflow-orientation` (it owns doc auditing and creation).
- **Deep periodic re-entry** (returning after weeks, "what should I even do
  here?") → that's `human-training:project-checkup`, which is heavier and
  state-aware. `/start` is the fast everyday opener; project-checkup is the
  occasional deep audit. Mention it if the project looks dormant, but don't run
  it.

---

## The sequence

### 1. Locate the docs (read-only existence check)

Check each canonical doc at its candidate locations. First hit wins.

- **onboarding.md**: project root → `./docs/onboarding.md` → `./docs/.agents/onboarding.md`
- **CONTEXT.md**: project root → `./docs/CONTEXT.md`
- **DEVLOG.md**: project root → `./docs/devlog.md` → `./docs/DEVLOG.md`
- **Handover**: `./HANDOVER.md` → `./docs/.agents/current-handover.md` → `.agents/current-handover.md` → legacy `.claude/current-handover.md`

If a project has its own `onboarding.md`, trust its "Getting Oriented" section
as the map for where the other docs live — it overrides the defaults above
(this is what makes bridged / non-canonical layouts work).

**If onboarding.md is absent entirely:** the project likely isn't set up for
this workflow. Don't read blindly. Report what's missing and offer
`workflow-orientation`. Stop there.

### 2. Read the temporal context (and only that)

Apply lifecycle-manager's context hygiene — read what's *temporal*, not
everything:

- **onboarding.md** — read the "Getting Oriented" / map section to learn where
  things live. Skim, don't memorize the whole file.
- **CONTEXT.md, if present** — the project's glossary. Durable rather than
  temporal, but small and high-leverage: it's the shared language, so reading it
  keeps your naming aligned. Skip it silently if absent — not every project has
  one.
- **Latest DEVLOG entry only** — the most recent sprint entry. The recent
  technical baggage, not the full history.
- **Current handover, in full** — this is the ephemeral delta: what was
  in-flight, breaking, or being debated. Read all of it (it's short by design).

Don't read the spec, source files, or full DEVLOG unless a specific question
requires it. Reference files are for lookup, not required reading.

### 3. Surface the orientation + propose the next move

A concise summary, then the next move at the top of mind (Teflon Mode):

```markdown
**Where we are:** <one or two lines — current sprint/branch and what state it's in>
**In flight (from handover):** <what was mid-stream or unresolved, or "nothing — clean stop">
**Last DEVLOG entry:** <date + one-line summary>

**Next:** I'd suggest <X> because <Y>. 1) <X> (recommended). 2) <alt>. 3) Stop / set your own direction.
```

Keep it tight. The point is to remove inertia, not to produce a report. If the
handover or DEVLOG names a concrete unfinished task, that *is* the recommended
next move — don't invent alternatives just to fill the list.

Verifying the build/tests is a legitimate next move to *offer* here (it's
lifecycle's step 4), but `/start` never runs it unprompted — that's the
docs-only contract. Put it in the numbered options if the environment looks
untrusted (fresh clone, lockfile drift mentioned in handover).

---

## Anti-patterns

- **Re-implementing orientation.** This is a trigger for lifecycle §1, not a
  third copy of it. When docs are missing, delegate to `workflow-orientation`.
- **Reading everything.** Latest DEVLOG entry, not the whole log. Onboarding
  map, not the whole file. Temporal context only.
- **Running tests or writing files.** Docs-only, read-only. Verification is
  offered as a next move, never executed by this skill.
- **Burying the next move.** It's the lead, not a footnote. Propose, don't ask
  "what now?".
- **Firing in this repo's own workflow.** This skill ships to downstream hobby
  projects. The plugin-factory repo itself has no sprint workflow to orient to.
