# /start — reference

Mechanics and history behind the three checks in `SKILL.md` §3. Open this when
a check fires and you need the detail, or when tempted to remove one.

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
