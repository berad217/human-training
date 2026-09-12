---
name: start
description: One-keystroke session opener. Reads the project's temporal docs (onboarding map, latest DEVLOG entry, current handover, TASKS Active, in-repo memory index), checks for unpushed commits, stranded memory and a stale plugin toolchain, then surfaces a short orientation and proposes the next move. Read-only, docs-only. Explicit invocation via /start at the top of a fresh session.
allowed-tools: [Read, Glob, Bash]
---

# /start — Fresh-session orient

One command that runs the orient sequence from `lifecycle-manager` §1, so a
fresh session never has to remember to type "read onboarding and the handover
and tell me where we are."

**Contract: read-only, docs-only.** It reads, summarises, and proposes. It does
not run tests, build, push, migrate, or write a file. The only commands it runs
are reads (`git status -sb`, a directory listing).

**Invoke only on `/start`.** Not on "let's get started" or "where were we".
Not in the plugin-factory repo itself; that repo has no sprint workflow.

**Hand off when:** onboarding is absent (`human-training:workflow-orientation`
owns doc auditing); the project looks dormant and the question is "what should
I even do here?" (mention `human-training:project-checkup`, don't run it).

## 1. Locate the docs

Glob by filename across the tree, and list the repo root. Do both every time,
including on a project you know: the miss this skill exists to prevent was
orienting from memory and skipping a doc that was there.

- `**/onboarding.md`, `**/CONTEXT.md`, `**/DEVLOG.md`, `**/TASKS.md`,
  `**/memory/MEMORY.md`
- `**/*handover*.md` **and** `**/*HANDOVER*.md`. Match the substring, because
  the file is also called `current-handover.md` or `latest_handover.md`, and run
  both cases, because glob matching is case-sensitive even on a case-insensitive
  filesystem. A lowercase pattern silently misses a root `HANDOVER.md`.

Multiple hits: prefer the project-root or `docs/` copy over an archived,
vendored, or `node_modules` one.

**Onboarding's map wins over these names.** Many projects keep the same three
roles under other names, often behind a pointer file: a *durable chronicle*
(DEVLOG role), an *ephemeral session delta* (handover role), and optionally a
*forward queue* (TASKS role). When the canonical names don't glob up but
onboarding exists, follow its "where everything lives" section, one hop through
any state pointer it names, and read those. That is not a missing-docs
condition.

**Onboarding absent:** the project isn't set up for this workflow. Don't read
blindly. Report what's missing, offer `workflow-orientation`, stop.

## 2. Read the temporal context, and only that

- **onboarding.md**: the orientation / map section. Skim.
- **CONTEXT.md**, if present: the glossary. Small; keeps naming aligned.
- **DEVLOG**: the latest entry only.
- **Handover**: in full. It is short by design.
- **TASKS.md**: the Active section only. Never surface Someday or Done.
- **memory/MEMORY.md**, if present: the index in full; individual entries only
  when relevant.

Not the spec, not source, not the full DEVLOG, unless a specific question needs
them.

## 3. Three checks: detect, report, offer, never act

Each one is silent when the state is resolved. A line that always appears
stops being read.

**Durability.** `git status -sb`, first line. `[ahead N]` means N commits exist
only on this disk: report and offer to push. No upstream, or in sync: say
nothing.

**Stranded memory.** Claude Code keeps per-project memory at
`~/.claude/projects/<slug>/memory/`, which does not travel between machines.
Derive the slug (see `reference.md`) and compare with the in-repo `memory/`:

| In-repo | Global | Say |
|---|---|---|
| yes | no | nothing |
| no | yes | "N entries stranded at the global path — want them moved in-repo?" |
| yes | yes | a probable fork; surface it and stop, don't guess which is canonical |
| no | no | nothing |

Migration is `workflow-orientation` §6's job. If memory is in-repo, write new
memory there for the rest of the session.

**Toolchain.** Read `~/.claude/plugins/known_marketplaces.json`. Each entry
carries `autoUpdate` and `lastUpdated`; those two fields are the whole check,
no network. `autoUpdate` absent or false: report it as the root cause, since
the catalog is not guaranteed to refresh and `claude plugin update` will keep
answering "already current" against the stale catalog. `autoUpdate` true but
`lastUpdated` months old: report that too. Fresh within a month, or no file:
nothing. The fix is in `reference.md`; offer it, never run it, never edit
`settings.json`.

## 4. Surface the orientation, then propose

```markdown
**Where we are:** <one or two lines: current sprint/branch and its state>
**In flight (from handover):** <mid-stream or unresolved, or "nothing — clean stop">
**Last chronicle entry:** <date + one line, from DEVLOG or its equivalent>
**Active tasks:** <top 1–3 from TASKS Active; omit the line if no TASKS.md>
**Durability:** <N commits unpushed on <branch> — push? omit when in sync>
**Memory:** <N entries stranded — move in-repo? omit when resolved or absent>
**Toolchain:** <marketplace <name>: autoUpdate off, last refreshed <date> — want the fix? omit when current>

**Next:** I'd suggest <X> because <Y>. 1) <X> (recommended). 2) <alt>. 3) Stop / set your own direction.
```

Keep it tight; the point is to remove inertia, not to produce a report. If the
handover, DEVLOG, or TASKS Active names a concrete unfinished task, that is the
recommended move; don't invent alternatives to fill the list. Verifying the
build or tests is a legitimate move to *offer*, especially on a fresh clone or
when the handover mentions lockfile drift, but never to run from here. A stale
plugin is never the recommended move on its own.
