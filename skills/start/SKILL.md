---
name: start
description: One-keystroke session opener. Orients to the current project by verifying the workflow docs exist and reading the temporal context (onboarding map, latest DEVLOG entry, current handover, in-repo memory index), then surfaces a concise orientation and proposes the next move. Also flags unpushed commits, project memory stranded outside the repo, and a plugin toolchain that has silently stopped updating — offering each without acting. Docs-only and read-only — no tests run, no files written. Explicit invocation via /start at the top of a fresh session.
allowed-tools: [Read, Glob, Bash]
---

# /start — Fresh-session orient

A friction-killer for the first keystroke of a fresh session. You reset context
often; this removes the cost of remembering to type "read onboarding and the
handover and tell me where we are." One command runs the orient sequence.

This skill is **read-only and docs-only**. It does not run tests, build the
project, or write any file. It reads, summarizes, and proposes — nothing else.

The one command it runs is `git status -sb`, which is strictly a read. The
docs-only contract exists to prevent *writes and side effects*; inspecting git
state has neither. See step 2b.

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

### 1. Locate the docs (glob first — never assume a path)

**Glob for each doc by filename across the tree *before* you conclude anything
is absent.** A hardcoded path list silently misses a doc that moved or lives in
a non-standard spot — it returns "not found" with no error, which reads as
"missing" when the doc is right there. A glob doesn't have that failure mode.
Run these (cheap, read-only):

- `**/onboarding.md`
- `**/CONTEXT.md`
- `**/DEVLOG.md` (and `**/devlog.md` on case-sensitive trees)
- `**/*handover*.md` **and** `**/*HANDOVER*.md` — **match the substring, and run
  both cases.** The handover role shows up as `HANDOVER.md`, `current-handover.md`,
  *or* `latest_handover.md`, and is often a small **pointer** to the real
  per-project copy. A `**/HANDOVER.md` glob misses `latest_handover.md` — same
  list-brittleness one level down. And **glob matching is case-sensitive even on
  case-insensitive filesystems**: a lowercase `*handover*` pattern silently misses
  a root `HANDOVER.md`. That is not hypothetical — it is the exact miss this
  bullet was written after.
- `**/TASKS.md`
- `**/memory/MEMORY.md` — the project's own memory index, if it keeps one
  in-repo. See 2c for why this matters more than its size suggests.

**Belt and braces: list the project root.** One directory listing of the repo
root cannot miss on case, and the root is where `HANDOVER.md`, `DEVLOG.md`, and
`TASKS.md` most often live. Run it alongside the globs, not instead of them —
the globs reach into `docs/` and `.agents/` where a listing won't.

These globs are a **fast net for the common names, not a guarantee.** A project's
chronicle can be a state doc (`writing-state.md`) and its queue can be absent
entirely — names you can't enumerate up front. When a role's file doesn't match
any glob, that's not "missing"; it's the bridge note below doing the real work.

**Run the glob even when you think you already know this project.** "I know
where things live here" is exactly the shortcut that makes `/start` whiff on a
doc that exists — you skip the check, orient from memory, and miss what moved or
what you never knew was there. Orient from what the tree *actually contains*, not
from priors. **Only after a glob returns empty may you treat that doc as missing.**

The candidate locations below are a **disambiguation hint** for when a glob
returns more than one hit (prefer the project-root / `docs/` copy over an
archived, vendored, or `node_modules`-buried one) — they are not the search:

- **onboarding.md**: project root → `./docs/onboarding.md` → `./docs/.agents/onboarding.md`
- **CONTEXT.md**: project root → `./docs/CONTEXT.md`
- **DEVLOG.md**: project root → `./docs/devlog.md` → `./docs/DEVLOG.md`
- **Handover**: `./HANDOVER.md` → `./docs/.agents/current-handover.md` → `.agents/current-handover.md` → legacy `.claude/current-handover.md`
- **TASKS.md**: project root → `./docs/TASKS.md`
- **Memory index**: `./memory/MEMORY.md` → `./docs/memory/MEMORY.md`

**Non-canonical layouts — follow onboarding's map; don't force the schema.**
When `onboarding.md` exists, its "Getting Oriented" / "Where everything lives"
section is the authority for where this project keeps its state — it overrides
the candidate paths above. Many projects don't use `DEVLOG.md` / `HANDOVER.md` /
`TASKS.md` *at all*; they keep the same **information** under different names,
often reached through a **pointer file** rather than a fixed path. So map by
**role**, not filename — every project that uses this workflow has, in some
form:

- a **durable chronicle** (where-we-are + decision history) — the DEVLOG role,
- an **ephemeral session delta** (what was in-flight) — the handover role,
- optionally a **forward queue** — the TASKS role.

When the canonical-named docs don't glob up but onboarding exists, that is **not**
a "docs missing" condition. Read onboarding's map and follow it — **including one
hop through any active-project / state pointer it names** — to whatever this
project actually uses for those three roles, then read *those* in step 2.

**If onboarding.md is absent entirely** (the glob returns nothing): the project
likely isn't set up for this workflow. Don't read blindly. Report what's missing
and offer `workflow-orientation`. Stop there.

### 2. Read the temporal context (and only that)

Apply lifecycle-manager's context hygiene — read what's *temporal*, not
everything. The doc names below are the **canonical** layout; on a bridged
project, read whatever onboarding's map pointed you to for each **role**
(durable chronicle = DEVLOG, session delta = handover, forward queue = TASKS),
even when the file is named something else and lives behind a pointer:

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
- **TASKS.md — Active section only, if present** — the forward queue. Read the
  **Active** items (not Someday, the parking lot; not Done). Skip silently if
  there's no TASKS.md.
- **`memory/MEMORY.md` in full, if present** — durable behaviour corrections the
  project has accumulated. It is an index of one-line pointers and costs almost
  nothing. Read the individual entries only when one is relevant to the work in
  hand. Skip silently if absent.

Don't read the spec, source files, or full DEVLOG unless a specific question
requires it. Reference files are for lookup, not required reading.

### 2b. Check durability (one command)

```bash
git status -sb
```

Read the **first line** — specifically the `[ahead N]` marker. `ahead N` means N
commits exist only on this disk: a previous session's work that was committed,
believed safe, and never pushed. Surfacing it at orient costs one command and
catches the drift a whole session earlier than the next handover would.

- `[ahead N]` → report it and **offer** to push.
- No upstream / not a git repo → say nothing. Not every project has a remote,
  and a missing remote is not news at orient.
- Clean and in sync → **say nothing.** Silence is the signal.

**Never push here.** `/start` reports; the user decides. Offering is in contract,
acting is not.

### 2c. Check whether memory is stranded outside the repo

Same shape as 2b, and the same discipline: **detect, report, offer, never act.**

Some harnesses keep per-project memory in a home-directory path derived from the
cwd — Claude Code uses `~/.claude/projects/<slug>/memory/`, where `<slug>` is the
working directory with `:`, `\`, `/` and `_` each replaced by `-`. So
`P:\software_projects\Blendy_McBlendface` →
`P--software-projects-Blendy-McBlendface`.

That location **does not travel between machines.** For a solo developer with a
desktop and a laptop it fails silently — no error, just an agent that has
forgotten something the human is sure they said.

Check for it. Then:

- **In-repo `memory/` exists and no global directory does** → say nothing. This
  is the resolved state.
- **A global directory exists for this cwd** → report the entry count and
  **offer** to migrate, which is `human-training:workflow-orientation` §6's job,
  not this skill's. One line is enough: *"N memory entries are stranded at the
  global path for this project — want them moved into the repo?"*
- **Both exist** → that is a duplicate canonical and a probable fork. Surface it
  and stop; do not guess which is authoritative.
- **Neither exists** → say nothing. Not every project keeps memory.
- **Derived slug finds nothing** → list `~/.claude/projects/` and match
  case-insensitively before concluding. **The slug is case-sensitive to how the
  path was typed**, so a session launched from `p:\...` rather than `P:\...`
  gets a different directory. Two case-variants both present is a fork.

**Never migrate from `/start`.** Copying files, rewriting an index and planting a
`CLAUDE.md` pointer are all writes, and this skill writes nothing. Hand off.

### 2d. Check whether the toolchain itself has stopped updating

Same shape again — **detect, report, offer, never act.** Unlike 2b and 2c, this
one is not about the project. It is about *your own tooling*: a plugin that
quietly stopped updating months ago changes what you are able to do here, and
nothing in the project's files can tell you.

Claude Code installs plugins through a local marketplace catalog. Refresh is
guaranteed only when the marketplace has `autoUpdate: true` — a per-marketplace
opt-in nested inside the marketplace entry, **not set for you when a marketplace
is added**.

While it is absent the catalog *may* still refresh, but nothing keeps it current,
and in practice it can sit untouched for months. Meanwhile `claude plugin update`
keeps answering "you're already current." That answer is *correct*: it compares
against the catalog, which has not moved. The install can sit many versions
behind without a single error.

**Report on the fields, not on a theory of the mechanism.** A stale `lastUpdated`
is the finding whether or not you can explain why it stalled. An absent
`autoUpdate` is worth flagging because it removes the guarantee — a catalog was
observed refreshing on 2026-08-19 with the flag still absent, so "absent means
never" is too strong to put in front of the user.

Read `~/.claude/plugins/known_marketplaces.json` — one entry per marketplace,
each carrying `autoUpdate` and `lastUpdated`. **Those two fields are the whole
check.** Do not reach for the network: a fresh session is the wrong place to
wait on `git ls-remote`, and the local fields already identify the failure.

- **`autoUpdate: true` and `lastUpdated` within the last month** → say nothing.
  Resolved state.
- **`autoUpdate` absent or `false`** → report it. This is the root cause rather
  than a symptom — the catalog will never refresh on its own. One line is
  enough: *"the `<name>` marketplace has autoUpdate off, so its plugins haven't
  updated since `<date>` — want the fix?"*
- **`autoUpdate: true` but `lastUpdated` is months old** → report it too. The
  flag is set and the refresh still isn't happening, which is a different
  failure and worth knowing about.
- **File absent, or no marketplaces registered** → say nothing. Plenty of
  environments run no plugins at all.

The fix, *when asked for*, is two commands and a setting — **offer, don't run**:

```bash
claude plugin marketplace update <name>
claude plugin update <plugin>@<name>
```

The first line is the one everyone skips, and without it the second consults the
same stale catalog and reports success. Then set `"autoUpdate": true` on that
marketplace in `~/.claude/settings.json` so it stops recurring. Applying an
update needs a **full quit and relaunch** — a new thread is not enough.

**Never edit `settings.json` here**, and never run the update. Both are writes,
and one of them is a write to the user's harness configuration. Report, hand
over the change, and let them make it.

### 3. Surface the orientation + propose the next move

A concise summary, then the next move at the top of mind (Teflon Mode):

```markdown
**Where we are:** <one or two lines — current sprint/branch and what state it's in>
**In flight (from handover):** <what was mid-stream or unresolved, or "nothing — clean stop">
**Last chronicle entry:** <date + one-line summary — from DEVLOG or the project's equivalent>
**Active tasks:** <top 1–3 from TASKS.md Active — omit this line entirely if there's no TASKS.md>
**Durability:** <N commits unpushed on <branch> — want me to push? — omit this line entirely when in sync>
**Memory:** <N entries stranded at the global path — want them moved in-repo? — omit this line entirely when resolved or absent>
**Toolchain:** <marketplace <name> has autoUpdate off; plugins last refreshed <date> — want the fix? — omit this line entirely when current>

**Next:** I'd suggest <X> because <Y>. 1) <X> (recommended). 2) <alt>. 3) Stop / set your own direction.
```

Keep it tight. The point is to remove inertia, not to produce a report. If the
handover, DEVLOG, or TASKS Active names a concrete unfinished task, that *is* the
recommended next move — don't invent alternatives just to fill the list.

Verifying the build/tests is a legitimate next move to *offer* here (it's
lifecycle's step 4), but `/start` never runs it unprompted — that's the
docs-only contract. Put it in the numbered options if the environment looks
untrusted (fresh clone, lockfile drift mentioned in handover).

---

## Anti-patterns

- **Skipping the glob because you "know" the project.** The single failure this
  skill exists to prevent: orienting from priors instead of from the tree, and
  reporting (or silently skipping) a doc that is actually present. Run step 1's
  glob every time, even on a project you've worked for months.
- **Asserting a doc is absent without globbing for it.** "Not at the path I
  expected" ≠ "missing." Empty glob first, *then* missing.
- **Forcing the canonical schema onto a bridged project.** If onboarding maps
  the chronicle / session-delta / queue to differently-named files (or behind a
  pointer), follow that map. Don't announce "no DEVLOG / no handover / no TASKS"
  when the project keeps the same information under its own names.
- **Re-implementing orientation.** This is a trigger for lifecycle §1, not a
  third copy of it. When docs are missing, delegate to `workflow-orientation`.
- **Reading everything.** Latest DEVLOG entry, not the whole log. Onboarding
  map, not the whole file. From TASKS, the **Active** section only — never
  surface Someday or Done at orient. Temporal context only.
- **Running tests or writing files.** Docs-only, read-only. Verification is
  offered as a next move, never executed by this skill. (Reading git state via
  `git status -sb` is not running the project — it writes nothing. See 2b.)
- **Pushing, or nagging about a clean repo.** `/start` reports unpushed work and
  offers; it never pushes. And when everything is in sync it says *nothing* about
  durability — a line that always appears stops being read.
- **Migrating memory, or nagging about a resolved one.** 2c reports and offers;
  `workflow-orientation` §6 does the moving. And when memory is already in-repo,
  say *nothing* — same rule as durability.
- **Nagging about the toolchain, or fixing it.** 2d reports and offers; it never
  edits `settings.json` and never runs an update. When `autoUpdate` is on and the
  catalog is fresh, say *nothing* — same rule as durability and memory. And a
  stale plugin is never the recommended next move on its own: mention it, then
  get on with the project's actual work.
- **Writing new memory to the global path because it is the harness default.**
  If the project keeps `memory/` in-repo, that is where memory goes for the rest
  of the session, not just at orient.
- **Burying the next move.** It's the lead, not a footnote. Propose, don't ask
  "what now?".
- **Firing in this repo's own workflow.** This skill ships to downstream hobby
  projects. The plugin-factory repo itself has no sprint workflow to orient to.
