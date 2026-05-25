---
name: leroy-jenkins
description: Autonomy-biased operating mode for converting otherwise-wasted token quota (near 5-hour or weekly window resets) into useful work. Delegates work to robustness-audit or project-checkup, runs with a relaxed confidence bar, and logs decisions to DEVLOG instead of pausing for moderate-confidence calls. Explicit invocation via /leroy-jenkins.
allowed-tools: [Read, Write, Edit, Grep, Glob, Bash]
---

# Leroy Jenkins Mode

Autonomy-biased operating posture for spending tokens that would otherwise reset unused. The signature is not *what* work gets done — that's delegated to other skills — but *how* it gets done: aggressive parallelism, relaxed confidence bar, decision breadcrumbs instead of pauses for confirmation.

The actual work is performed by `human-training:robustness-audit` or `human-training:project-checkup`. Leroy is the overlay that changes their cadence.

## When to invoke

Direct, explicit invocation via `/leroy-jenkins`. Optionally accepts an estimated minutes-until-reset.

Do **not** auto-invoke on conversational phrases like "I have tokens to spare", "let's run wild", or "burn the quota". The user named those as exactly the kind of accidental trigger to avoid. Explicit slash-command only.

## Composition with Teflon Mode

Teflon is the *initiative* axis (who proposes the next move). Leroy is the *autonomy* axis (who decides without asking). They compose orthogonally:

| Teflon | Leroy | Net behavior                                                    |
|--------|-------|-----------------------------------------------------------------|
| Off    | Off   | User directs, I execute, I confirm on moderate calls            |
| On     | Off   | I propose, user approves each move                              |
| Off    | On    | User directs, I execute without pausing for moderate decisions  |
| On     | On    | I propose AND execute, log decisions, batch-approve at the end  |

Teflon defaults on for Brad (see `~/.claude/CLAUDE.md`). Leroy is opt-in per invocation.

## Modes

When invoked without a mode specified, present the choice with a recommendation. Numbered options, recommendation first:

> Pick a Leroy mode:
> 1) **Full Treatment** (recommended) — invokes project-checkup in force-all mode.
> 2) **Audit Blitz** — wider parallel fan-out of robustness-audit.

### Full Treatment

Invokes `human-training:project-checkup` in *force-all mode*: every component runs (workflow-orientation + robustness-audit + friction audit + next-move inventory), no skipping based on pulse state.

Best for: dormant or abandoned hobby projects, returning to a project cold, wanting comprehensive re-entry support.

### Audit Blitz

Wide parallel fan-out of `human-training:robustness-audit`. Differences from the default invocation:

- 7-10 surfaces instead of 3-5
- All agents run in parallel in a single dispatch
- Don't pause after synthesis to ask the user for triage — present the full color-coded report with action menu in one shot

Best for: projects with substantial code, user wants to find latent bugs as fast as possible.

## The autonomy-bias overlay

For decisions encountered during a Leroy run, the confidence bar shifts:

| Standard bar (from CLAUDE.md)           | Leroy-modified bar                                          |
|-----------------------------------------|-------------------------------------------------------------|
| HIGH — just do it                       | HIGH — just do it                                           |
| MODERATE — do it + flag in DEVLOG       | **MODERATE — do it, drop a breadcrumb, move on**            |
| LOW — STOP and ask                      | LOW — STOP and ask (unchanged)                              |

So moderate-confidence decisions no longer pause. They get logged for batch review at the end of the run.

**When asking IS necessary** (LOW confidence only): numbered options, opinionated, recommendation first.

> Decision needed: <one-line question>. 1) X (recommended because Y). 2) Z. 3) Park for later.

Never open-ended. Match the Teflon prompt format.

## Decision breadcrumbs

Every MODERATE-confidence decision during a Leroy run drops a breadcrumb. Append to the project's `DEVLOG.md` under a dedicated section:

```markdown
## Leroy run YYYY-MM-DD (HH:MM)

**Mode:** <Full Treatment | Audit Blitz>
**Duration:** <minutes>
**Branch:** <branch name if a Leroy branch was created>

### Decisions logged

- **<short title>** — What: <action taken>. Why: <reasoning + alternatives
  considered>. Where to look if you disagree: <file:line>.

- ...

### Findings handed off

- Audit report: <link or inline>
- Workflow fixes applied: <list>
- Outstanding LOW-confidence questions: <list>
```

The user reviews breadcrumbs at the end. Wrong turns are cheap because the breadcrumbs say *why* — easy to undo selectively with `git revert` on a Leroy branch.

## Branching (recommended)

Before starting a Leroy run, create a branch named `leroy/YYYY-MM-DD` (or `leroy/YYYY-MM-DD-HHMM` if more than one per day). Commit autonomous changes there. The user can review the diff and cherry-pick / merge whatever they like back into main.

If the user declines branching, work on the current branch but make smaller, themed commits (one per decision class) so revert remains granular.

## Time-aware aggressiveness

If the user provided minutes-until-reset, scale accordingly:

| Time available | Suggested mode    | Notes                                            |
|----------------|-------------------|--------------------------------------------------|
| 90+ min        | Full Treatment    | full sequence, take your time                    |
| 30-90 min      | Full Treatment    | trim to active components per project-checkup's pulse |
| 15-30 min      | Audit Blitz       | pick one surface set, ship the report            |
| < 15 min       | Decline           | not worth the setup overhead — note this back to the user |

## Anti-patterns

- **Treating Leroy as "do whatever you want."** Leroy is autonomy bias, not chaos. The actual work goes through a real skill. Don't freelance new tasks.
- **Skipping the decision breadcrumbs.** The breadcrumbs are what makes autonomy safe. No log, no Leroy.
- **Pausing for confirmation on MODERATE decisions.** That defeats the purpose. Log and proceed.
- **Touching the user's main branch by default.** Use a Leroy branch unless the user explicitly says otherwise.
- **Running across multiple projects in one invocation.** One project per Leroy run; multi-project sweeps lose coherence.
- **Inventing extra modes on the fly.** If a use case doesn't fit Full Treatment or Audit Blitz, end the Leroy run cleanly and ask the user whether to add a new mode for next time.
