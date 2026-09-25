# start — reference

Mechanics and history behind the TASKS sweep in `SKILL.md` §2 and the three
checks in §3. Open this when one fires and you need the detail, or when tempted
to remove one.

## The TASKS measurement

One read-only command, before TASKS.md is opened. Use the form for the active
shell; neither writes a scratch file:

```bash
LC_ALL=C awk '/^## Active/{a=1;next} /^## /{a=0} a {if ($0 ~ /^- \[ \]/) open++; if ($0 ~ /^- \[x\]/) ticked++; bytes += length($0)+1} END {printf "open %d  ticked %d  bytes %d\n", open, ticked, bytes}' TASKS.md
```

```powershell
$tasksText = Get-Content -Raw TASKS.md
$activeText = [regex]::Match($tasksText, '(?ms)^## Active[^\r\n]*\r?\n(.*?)(?=^## |\z)').Groups[1].Value
"open $([regex]::Matches($activeText, '(?m)^- \[ \]').Count)  ticked $([regex]::Matches($activeText, '(?m)^- \[x\]').Count)  bytes $([text.encoding]::UTF8.GetByteCount($activeText))"
```

## The Done one-liner

`- [x] ~~<title>~~ (<YYYY-MM-DD>) - <ids>`

- **title**: the item's bold header, cut at the first clause break (` - `, `: `,
  `. `) after ~25 characters; strip a leading date and any `DONE ...:` or
  `(superseded by ...)` prefix.
- **date**: the latest date in the item that follows a status word (LANDED,
  DONE, CLOSED, RULED, PRICED TO ZERO, SUPERSEDED, MOOT); else the item's own.
- **ids**: the decision / finding / issue numbers in the header (D57, F290,
  #123), first four; omit the dash when there are none.

Every Active item's first line must survive verbatim (kept or parked), as
exactly this one-liner (swept), or be a named drop (a superseded original whose
ticked twin carries its ids). Assert that before writing. A script beats hand
edits past a dozen items; a scratchpad Python with those asserts did 194 items
in one pass.

## Bounded local Claude memory discovery (either host)

Claude Code derives the per-project memory directory from its working directory
by replacing each of `:`, `\`, `/` and `_` with `-`:

```
P:\software_projects\Blendy_McBlendface  ->  ~/.claude/projects/P--software-projects-Blendy-McBlendface/memory/
```

Use the active process's `CLAUDE_CONFIG_DIR` when set; otherwise use
`~/.claude`. The override replaces that whole config directory, not its
`projects/` subdirectory. A Codex process may not inherit an override used
only to launch Claude. If the expected directory is unavailable, say so when
relevant and ask for the config path; do not search the machine for it.

1. Take the current working directory and `git rev-parse --show-toplevel` (if
   in Git), then the `worktree ` paths from `git worktree list --porcelain`.
   These are related checkout paths, not evidence of another machine's clone.
   Deduplicate identical path strings, but preserve case variants because they
   can produce different slugs. Inspect at most 20 linked worktree roots; if
   there are more, say the search was truncated. For each root, derive the
   exact slug above and test `<config>/projects/<slug>/memory/`.
2. The slug is case-sensitive to how the path was typed. Also list only the
   immediate child names of `<config>/projects/` (up to 500; disclose any
   truncation) and test case-insensitive equality with each derived slug. A
   case variant is another candidate, not an automatic replacement. Do not
   use prefix, substring, or project-name matches. A slug is lossy (`_` and
   path separators collide), so read the memory index or a relevant entry for
   project/path evidence before calling it credible. If identity remains
   unclear, show the candidate and ask rather than treating it as a match.
3. Deduplicate candidates resolving to the same directory. If none is credible,
   stay quiet or report unavailable. If several remain plausible (including
   two case variants or linked worktree memories), show the paths and ask which
   to use. Do not merge them or silently prefer the current worktree.
4. For one credible directory, read at most its `MEMORY.md` index (up to 16 KB)
   and three relevant entry files. Compare claims with the repo's
   `memory/MEMORY.md` and relevant entries. Name useful missing facts, with
   source paths, rather than counting files as missing facts. If identity or
   content is unclear or truncated, disclose that and offer review; never
   copy or edit from this skill. Offer curated migration only when the repo is
   known to be private.

## The toolchain fix, when asked for

Claude Code only:

```bash
claude plugin marketplace update <name>
claude plugin update <plugin>@<name>
```

The first line is the one everyone skips; without it the second consults the
same stale catalog and reports success. Then set `"autoUpdate": true` on that
marketplace in `~/.claude/settings.json`. Applying an update needs a full quit
and relaunch, not a new thread.

Observed 2026-08-19: a catalog refreshed with `autoUpdate` absent. The flag
removes the *guarantee* of refresh, not the possibility. Report on the two
fields, not on a theory of the mechanism.

## Why these checks exist

- **The TASKS sweep.** panel_reader's Active section was 264 KB — 139 open and
  55 ticked items, some 150–290 lines long — after two months of ticking in
  place. `/start` had read the first 60 lines and missed the rest; the `tasks`
  skill's Done verb fires only on `/tasks` or "mark X done", and the lifecycle
  loop never touches TASKS. The sweep sits in `/start` because it is the reader
  that pays for the bloat, and a session open is the one moment when culling
  doesn't pull attention off a task in hand (2026-09-16).
- **Uppercase `HANDOVER.md`.** A lowercase `*handover*` glob missed a root
  `HANDOVER.md` on a case-insensitive filesystem. The both-cases rule in §1 was
  written after that miss.
- **Toolchain.** A plugin install sat many versions behind for months with no
  error, because the marketplace catalog only refreshes when `autoUpdate` is
  set, and `claude plugin update` compares against the catalog. The check was
  removed in 1.25.0 on a misread probe (a denied `Skill` call looked like the
  check silently not firing) and restored in 1.26.0. Before deleting it again,
  confirm the probe actually loaded the skill.
- **`git diff --stat` on a dirty tree, and no further.** Both probes before
  1.41.0 broke the docs-only contract to read source diffs, and the result was
  the most useful line in their orientations: it tied a dirty tree to the
  thread that made it. `--stat` keeps that attribution at bounded cost and
  without reading source; the content diff stays an offered move (decided
  2026-09-25).
- **Status tags.** Adapted from pstack `recall`'s output contract (1.41.0),
  minus its PR tags, which need network `/start` doesn't use. The aim is
  preventive, not incident-earned: prose "In flight" lets a handover's word
  stand unchecked, and one tag per thread, taken from git where git can see,
  puts any handover-versus-git mismatch on the page. Unprobed at release.
- **Stranded memory.** Solo developer, desktop plus laptop: the global path
  fails silently, as an agent that has forgotten something the human is sure
  they said.
