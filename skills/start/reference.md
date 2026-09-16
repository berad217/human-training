# /start — reference

Mechanics and history behind the TASKS sweep in `SKILL.md` §2 and the three
checks in §3. Open this when one fires and you need the detail, or when tempted
to remove one.

## The TASKS measurement

One command, before TASKS.md is opened:

```bash
awk '/^## Active/{a=1;next} /^## /{a=0} a' TASKS.md > /tmp/active.md
echo "open $(grep -c '^- \[ \]' /tmp/active.md)  ticked $(grep -c '^- \[x\]' /tmp/active.md)  bytes $(wc -c < /tmp/active.md)"
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

## The memory slug

Claude Code derives the per-project memory directory from the working directory
by replacing each of `:`, `\`, `/` and `_` with `-`:

```
P:\software_projects\Blendy_McBlendface  ->  ~/.claude/projects/P--software-projects-Blendy-McBlendface/memory/
```

The slug is case-sensitive to how the path was typed. A session launched from
`p:\...` rather than `P:\...` gets a different directory, so if the derived slug
finds nothing, list `~/.claude/projects/` and match case-insensitively before
concluding. Two case-variants both present is a fork.

## The toolchain fix, when asked for

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
- **Stranded memory.** Solo developer, desktop plus laptop: the global path
  fails silently, as an agent that has forgotten something the human is sure
  they said.
