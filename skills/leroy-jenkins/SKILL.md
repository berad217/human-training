---
name: leroy-jenkins
description: Autonomy-biased operating mode for converting otherwise-wasted token quota (near 5-hour or weekly window resets) into useful work. Runs the goal you state — or, if you state none, delegates to project-checkup or robustness-audit — with a relaxed confidence bar, logging decisions to DEVLOG instead of pausing for moderate-confidence calls. Can run unattended for a long single turn, using subagents to stay context-lean. Explicit invocation via /leroy-jenkins.
---

# Leroy Jenkins Mode

Autonomy-biased operating posture for spending tokens that would otherwise reset unused. The signature is not *what* work gets done but *how* it gets done: aggressive parallelism, relaxed confidence bar, decision breadcrumbs instead of pauses for confirmation.

The *what* can be a goal you state at invocation, or — if you state none — one of two canned modes that delegate to `human-training:project-checkup` or `human-training:robustness-audit`. Either way, Leroy is the overlay that changes the cadence; it is not the source of the task.

## When to invoke

Direct, explicit invocation via `/leroy-jenkins`. Optionally accepts:

- **A stated goal** — what to actually work on this run (e.g., "run with the Unreal curriculum, pick sensible next features, document the choices, playtest when there's time"). If given, this *is* the work (see Modes).
- **An estimated minutes-until-reset** — scales aggressiveness (see Time-aware aggressiveness).
- **An unattended signal** — "do as much as you can in one turn", "I'm going to bed", "I won't be able to reply". Switches on the long-haul posture (see Unattended / long-haul runs).

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

Leroy's work surface comes from one of two places, in priority order:

**1. Your stated goal** — if you named one at invocation, that *is* the work. There is no menu. Leroy applies its overlay (relaxed bar, breadcrumbs, branch) to executing the goal you gave: e.g., "run with the curriculum, pick sensible next features, document the choices, playtest when there's time." A stated goal is as valid a Leroy run as either canned mode below — treat it as first-class, not as a deviation to flag or apologize for. Leroy owns the *how* (autonomy, parallelism, breadcrumbs); it does not relitigate the *what* you already chose.

**2. A canned mode** — if you gave no goal, present the choice with a recommendation. Numbered options, recommendation first:

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
| LOW — STOP and ask                      | LOW — STOP and ask (unchanged — except unattended; see below) |

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

## Unattended / long-haul runs

When the user signals they won't be around to reply — "do as much as you can in one turn", "I'm going to bed", "I won't be able to answer" — Leroy shifts into a long-haul posture. This is orthogonal to mode and to the stated goal: it combines with any of them.

**Plan first, then batch.** Lay out the session plan up front and checkpoint it to `DEVLOG.md` before executing, then re-checkpoint as each chunk completes. A long unattended run that dies partway must leave a trail the user (or the next session) can pick up — never hold the whole plan only in context.

**Delegate to stay context-lean.** Leroy stays the planner/synthesizer; each meaty chunk of work — build a feature demo, run an audit surface, write a test pass — is dispatched to a subagent via the Agent tool. The subagent does the heavy reading and editing and returns a *compact summary*, not a transcript dump. This is what lets one turn run for hours without the orchestrator's context ballooning and degrading. Subagent prompts must be self-contained: the subagent does not share Leroy's context, so spell out the goal, the relevant files, and the return shape you expect back.

**LOW-confidence forks can't pause — so they don't.** Normally LOW confidence means STOP and ask. Unattended, there is no one to ask, so:

- If the fork is **reversible**, take the most reversible option, drop a breadcrumb flagged distinctly as an open question (not a routine MODERATE breadcrumb), and continue.
- If the fork is **irreversible or destructive**, do **not** guess. Skip that branch, park it as an open question for review, and move on to work that isn't blocked on it.

The Leroy branch plus the breadcrumbs make both outcomes cheap to review and selectively undo later.

**Stop cleanly at the budget.** As you approach the time or quota limit, finish the chunk in flight, write a closing summary breadcrumb, and stop — don't get cut off mid-write.

## Time-aware aggressiveness

If the user provided minutes-until-reset, scale accordingly:

| Time available | Suggested mode    | Notes                                            |
|----------------|-------------------|--------------------------------------------------|
| 90+ min        | Full Treatment    | full sequence, take your time                    |
| 30-90 min      | Full Treatment    | trim to active components per project-checkup's pulse |
| 15-30 min      | Audit Blitz       | pick one surface set, ship the report            |
| < 15 min       | Decline           | not worth the setup overhead — note this back to the user |

With a **stated goal**, don't decline on time alone — scope the goal to the window (fewer features, one playtest instead of three) and note in the breadcrumbs what you deferred. The table above governs the canned modes.

## Anti-patterns

- **Treating Leroy as "do whatever *Leroy* wants."** Leroy is autonomy bias, not chaos. The work is either the goal the user stated at invocation or a canned mode — never tasks Leroy picks up for itself. "Don't freelance" means don't take on work the user didn't ask for; faithfully executing the user's stated goal is the *opposite* of freelancing.
- **Skipping the decision breadcrumbs.** The breadcrumbs are what makes autonomy safe. No log, no Leroy.
- **Pausing for confirmation on MODERATE decisions.** That defeats the purpose. Log and proceed.
- **Touching the user's main branch by default.** Use a Leroy branch unless the user explicitly says otherwise.
- **Running across multiple projects in one invocation.** One project per Leroy run; multi-project sweeps lose coherence.
- **Padding the fallback menu.** The two canned modes (Full Treatment, Audit Blitz) are the menu shown *only* when the user states no goal. Don't invent a third on the fly; if a recurring no-goal use case keeps surfacing, end cleanly and ask whether to add it for next time. A user-*stated* goal is never a "mode" and needs no menu entry.
