---
name: start
description: Explicit fresh-session opener for Claude Code (/human-training:start) or Codex ($human-training:start). Reads the project's temporal docs and in-repo memory index, sweeps ticked TASKS Active items to Done, checks unpushed commits and local Claude memory that may be stranded, then proposes the next move. Claude Code also checks marketplace freshness. Docs-only; the TASKS sweep is its one write. Use only when the user selects this skill at the top of a fresh session.
allowed-tools: [Read, Glob, Bash, Edit]
disable-model-invocation: true
---

# start — Fresh-session orient

One command that runs the orient sequence from `lifecycle-manager` §1, so a
fresh session never has to remember to type "read onboarding and the handover
and tell me where we are."

**Contract: docs-only, one write.** It reads, summarises, and proposes. It does
not run tests, build, push, or migrate. The one file it writes is `TASKS.md`,
and only for the sweep in §2: ticked items out of Active into Done as
one-liners. That write is mechanical and lossless (the why is in the DEVLOG,
the text in git), which is why it needs no approval; every other finding is
offered. The other commands it runs are reads (`git status -sb`,
`git diff --stat HEAD` when the tree is dirty, `git worktree list --porcelain`,
directory listings, the TASKS measurement).

**Invoke only when explicitly selected:** `/human-training:start` in Claude
Code or `$human-training:start` in Codex. Not on "let's get started" or "where
were we". Not in the plugin-factory repo itself; that repo has no sprint
workflow.

Use the active runtime to decide which host-specific checks apply. Do not
infer the host from an installed `claude` or `codex` command. Follow the
project's canonical instructions as loaded by that host; if the project uses
`CLAUDE.md`, keep it canonical in both hosts (Codex may be configured to use
it as an instruction fallback). Do not create a parallel `AGENTS.md`.

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
- **TASKS.md**: measure Active before opening it (the sweep, below), then the
  Active section only. Never surface Someday or Done.
- **memory/MEMORY.md**, if present: the shared, repo-tracked index in full;
  individual entries only when relevant. Use it in either host.

Not the spec, not source, not the full DEVLOG, unless a specific question needs
them.

### The TASKS sweep: measure, sweep, then read

Active is the one orient read with no natural ceiling. Items get ticked in
place mid-work and nothing moves them; findings get filed as items and grow
bodies. One project reached 264 KB / ~73K tokens of Active (139 open, 55
ticked), which a session reading Active whole would have paid for. `/start`
is the reader that pays, so it is the one that sweeps.

Before opening TASKS.md, measure Active (one command, `reference.md`): open
items, ticked items, bytes. Then:

- **Ticked items in Active → move them to Done now**, one line each:
  `- [x] ~~title~~ (date) - ids` — the title from the item's bold header, the
  date the item says it landed, the decision / finding / issue numbers it
  names, if any. Nothing else;
  the body's why is in the DEVLOG and its text in git. An unticked item whose
  header says it is superseded by a ticked one goes with it. Assert the item
  count before and after; report the number swept. If `git status` already
  shows TASKS.md modified, someone may be mid-edit: offer the sweep instead.
- **Still over ~10 open items or ~8 KB → read only each item's first line**,
  not the bodies, and offer to park all but the next few in Someday, verbatim.
  Which items are next is the user's call: propose the list, never park on
  your own.
- **An item over ~10 lines is a finding wearing a checkbox.** Say so once; its
  body belongs in the DEVLOG or the register, the item pointing at the number.
  Don't rewrite it here.
- Nothing ticked and under the bar: say nothing, same as the checks in §3.

## 3. Three checks: detect, report, offer, never act

Each one is silent when the state is resolved. A line that always appears
stops being read.

**Durability.** `git status -sb`, first line. `[ahead N]` means N commits exist
only on this disk: report and offer to push. No upstream, or in sync: say
nothing. If the rest of the output shows a dirty tree, run
`git diff --stat HEAD` (untracked names come from the status output) so each
changed file can be pinned to a thread in §4. File names and line counts only:
reading the diff itself is a move to offer, not to make.

**Stranded memory (either host).** Repo-tracked `memory/MEMORY.md` is the
shared source for private projects. Claude Code may also have useful notes at
`<Claude config dir>/projects/<slug>/memory/`; Codex can inspect those notes
read-only on the same machine. Use the bounded path discovery in
`reference.md`: current checkout plus Git-linked worktree roots, with
`CLAUDE_CONFIG_DIR` when set. Do not guess from other clones or fuzzy project
names. No credible local directory: say nothing unless availability matters.
Multiple plausible directories: show their paths and ask which project memory
to use. For exactly one credible directory, inspect its index and only relevant
entries, compare their facts with repo memory, and report potentially useful
facts missing from the repo. Offer a curated migration for a confirmed private
repo; never auto-copy, edit Claude's memory, or treat a matching slug alone as
proof of project identity. Migration is `workflow-orientation` §6's job. Keep
new durable facts in the repo memory for the rest of the session.

**Toolchain (Claude Code only).** Read
`~/.claude/plugins/known_marketplaces.json`. Each entry
carries `autoUpdate` and `lastUpdated`; those two fields are the whole check,
no network. `autoUpdate` absent or false: report it as the root cause, since
the catalog is not guaranteed to refresh and `claude plugin update` will keep
answering "already current" against the stale catalog. `autoUpdate` true but
`lastUpdated` months old: report that too. Fresh within a month, or no file:
nothing. The fix is in `reference.md`; offer it, never run it, never edit
`settings.json`.
In Codex, omit this check; Claude's marketplace registry does not describe
the active Codex plugin installation.

## 4. Surface the orientation, then propose

```markdown
**Where we are:** <one or two lines: current sprint/branch and its state>
**In flight:** <each thread + one tag, or "nothing — clean stop">
**Last chronicle entry:** <date + one line, from DEVLOG or its equivalent>
**Active tasks:** <top 1–3 from TASKS Active; omit the line if no TASKS.md>
**Tasks:** <swept N to Done; Active is M items / K KB — park the rest? omit when nothing swept and under the bar>
**Durability:** <N commits unpushed on <branch> — push? omit when in sync>
**Memory:** <local facts missing from repo, or ambiguous candidate paths — curate? omit when resolved or absent>
**Toolchain:** <marketplace <name>: autoUpdate off, last refreshed <date> — want the fix? omit when current>

**Next:** I'd suggest <X> because <Y>. 1) <X> (recommended). 2) <alt>. 3) Stop / set your own direction.
```

**Tag every thread** the handover calls in flight or unresolved, plus any work
git shows that the handover doesn't mention. Exactly one tag each:
`[shipped <sha|version>]`, `[committed, unpushed]`, `[uncommitted: <files>]`,
`[in flight <branch>]`, `[undecided]`, `[not started]`. A thread with no tag is
not done yet, so tag it. Tags come from git wherever git can see the state;
when it can't (a PR, a pending decision), suffix `per handover`. When the
handover and git disagree, tag what git shows and say so; that mismatch is
usually the most useful line in the orientation.

Keep it tight; the point is to remove inertia, not to produce a report. If the
handover, DEVLOG, or TASKS Active names a concrete unfinished task, that is the
recommended move; don't invent alternatives to fill the list. Verifying the
build or tests is a legitimate move to *offer*, especially on a fresh clone or
when the handover mentions lockfile drift, but never to run from here. A stale
plugin is never the recommended move on its own.
