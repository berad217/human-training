# leroy-jenkins — reference

Lookup material for [SKILL.md](SKILL.md). Nothing here is required reading;
each section is pointed at from the step that needs it.

## Composition with Teflon Mode

Teflon is the *initiative* axis (who proposes the next move). Leroy is the
*autonomy* axis (who decides without asking). They compose orthogonally:

| Teflon | Leroy | Net behavior                                                    |
|--------|-------|-----------------------------------------------------------------|
| Off    | Off   | User directs, agent executes, confirms on moderate calls        |
| On     | Off   | Agent proposes, user approves each move                         |
| Off    | On    | User directs, agent executes without pausing on moderate calls  |
| On     | On    | Agent proposes AND executes, logs decisions, batch-review at end|

Teflon defaults on in the user's global instructions; Leroy is opt-in per
invocation.

## Time-aware aggressiveness (canned modes only)

| Time available | Suggested mode | Notes                                                   |
|----------------|----------------|---------------------------------------------------------|
| 90+ min        | Full Treatment | full sequence, take your time                           |
| 30–90 min      | Full Treatment | trim to active components per project-checkup's pulse   |
| 15–30 min      | Audit Blitz    | pick one surface set, ship the report                   |
| < 15 min       | Decline        | not worth the setup overhead — say so                   |

A stated goal is scoped to the window instead of declined.

## DEVLOG closing entry

```markdown
## Leroy run YYYY-MM-DD (HH:MM)

**Mode:** <stated goal | Full Treatment | Audit Blitz>
**Duration:** <minutes> · **Branch:** <branch> · **Trail:** `<path to .tsv>`

- **Shipped:** <one line per outcome>
- **Deferred / open questions:** <the LOW-confidence forks that were skipped>
- **Where to look if you disagree:** the trail, sorted by `ts`.
```

Wrong turns stay cheap because the trail says *why* — `git revert` on the
Leroy branch undoes them selectively.

## Resume note (`<run-id>-resume.md`)

Written beside the trail at pause. Contents:

- what you were doing when you stopped
- what is **verified** versus merely **written**
- current state of the tree (clean / broken, and how)
- the next concrete action
- any gotcha the next session would otherwise rediscover

Point at the trail for decision history rather than restating it.

## Host mechanics

- **Subagents.** Claude Code: the `Agent` tool. Codex: its subagent/spawn
  facility where enabled; otherwise inline with more frequent trail
  checkpoints. Subagent launches are asynchronous in current hosts, so
  "dispatch all in one block" is moot — one per turn overlaps anyway. The
  instruction was removed from the body on 2026-09-19 for that reason.
- **Confidence bar.** Defined in the user's global instructions
  (`~/.claude/CLAUDE.md` for Claude Code; Codex may be configured to read the
  same file as a fallback). Leroy shifts it; it does not define it.

## History

- Prose breadcrumbs in the DEVLOG were the original trail. They made the
  DEVLOG unreadable; the TSV trail and `show-me-your-work` replaced them.
- Body trimmed 2,283 → ~1,150 words on 2026-09-19 following the `/start`
  method: anti-patterns folded into the step they guard, templates and tables
  moved here, host-specific tool names generalised so the skill runs under
  Codex without floundering.
