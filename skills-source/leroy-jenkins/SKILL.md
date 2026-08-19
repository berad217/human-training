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

## The decision trail

Every MODERATE-confidence decision drops a breadcrumb **as it happens**, into an
append-only TSV. Not at the end of the run — as it happens. A run that dies
partway (context exhausted, quota hit, machine sleeps) must leave its reasoning
on disk, not in a context window nobody will ever read again. One row costs one
command; that is the whole argument for the format.

### The file

`docs/leroy/<run-id>.tsv` when the project keeps working docs under `docs/`,
otherwise `leroy/<run-id>.tsv` at the project root. `<run-id>` is
`YYYY-MM-DD-HHMM`, matching the Leroy branch. It is **committed** — unlike most
decision logs, this one exists precisely so the user can review autonomous work
they did not watch, and it renders as a sortable table on GitHub.

Six columns, tab-separated, one row per decision:

| Column | What goes in it |
|-----------|-----------------|
| `ts` | ISO8601 timestamp. The timeline axis. |
| `phase` | Which chunk of the run this belongs to. |
| `decision` | What you chose or did. One line. |
| `why` | The reason in plain words, plus the alternative you rejected. |
| `evidence` | A **pointer**, never prose: commit SHA, `file:line`, an artifact path. |
| `result` | The outcome: `tests green`, `reverted`, `deferred`, `open question`. |

Write rows the way you would tell a colleague what you did. Plain words,
concrete actions. A reviewer should understand a row without decoding it.

```bash
printf '%s\t%s\t%s\t%s\t%s\t%s\n' "$(date -u +%Y-%m-%dT%H:%M:%SZ)" "$PHASE" "$DECISION" "$WHY" "$EVIDENCE" "$RESULT" >> docs/leroy/2026-08-19-1430.tsv
```

```powershell
"{0}`t{1}`t{2}`t{3}`t{4}`t{5}" -f (Get-Date -Format s), $Phase, $Decision, $Why, $Evidence, $Result | Add-Content -Encoding utf8 docs/leroy/2026-08-19-1430.tsv
```

**Three rules the format depends on:**

- **One row is one decision.** If it does not fit on one line, the decision is not
  crisp yet. Cells stay single-line; strip stray tabs and newlines.
- **Append-only.** A wrong call gets a *new* row that supersedes it. Never edit or
  delete history — the reversals are the most useful rows in the file.
- **Prefix any cell starting with `=`, `+`, `-`, or `@` with a single quote.**
  Findings and file paths land in these cells verbatim, and a reviewer opening
  the log in Excel should not execute one.

Log decision points and checkpoints, not every action: a fork taken, a chunk
completed with its verification result, a pivot or revert with what triggered it,
a blocker parked, an open question flagged. Skip the trivial and self-evident.

### Audit the trail before handing back

At the end of the run, walk the trail against what actually happened. Every row
maps to a real action — cut invented or aspirational entries. Every `evidence`
pointer resolves and shows what its row claims. A fork or abandoned approach that
shaped the run but never got logged is a gap; add it. **Fix the log, not the
story:** where the work diverged from what a row claims, the row is wrong.

### The DEVLOG closing entry

The trail is the detail. The DEVLOG gets one short entry that points at it —
this is the durable chronicle, so it records that the run happened and what came
out of it, not every decision inside it.

```markdown
## Leroy run YYYY-MM-DD (HH:MM)

**Mode:** <stated goal | Full Treatment | Audit Blitz>
**Duration:** <minutes> · **Branch:** <branch> · **Trail:** `<path to .tsv>`

- **Shipped:** <one line per outcome>
- **Deferred / open questions:** <the LOW-confidence forks that were skipped>
- **Where to look if you disagree:** the trail, sorted by `ts`.
```

Wrong turns stay cheap because the trail says *why* — easy to undo selectively
with `git revert` on a Leroy branch.

## Branching (recommended)

Before starting a Leroy run, create a branch named `leroy/YYYY-MM-DD` (or `leroy/YYYY-MM-DD-HHMM` if more than one per day). Commit autonomous changes there. The user can review the diff and cherry-pick / merge whatever they like back into main.

If the user declines branching, work on the current branch but make smaller, themed commits (one per decision class) so revert remains granular.

## Unattended / long-haul runs

When the user signals they won't be around to reply — "do as much as you can in one turn", "I'm going to bed", "I won't be able to answer" — Leroy shifts into a long-haul posture. This is orthogonal to mode and to the stated goal: it combines with any of them.

**Plan first, then batch.** Lay out the session plan up front and write it to the decision trail as the first rows before executing anything, then log a row as each chunk completes. A long unattended run that dies partway must leave a trail the user (or the next session) can pick up — never hold the whole plan only in context. This is the reason the trail is written as it happens rather than assembled at the end.

**Delegate to stay context-lean.** Leroy stays the planner/synthesizer; each meaty chunk of work — build a feature demo, run an audit surface, write a test pass — is dispatched to a subagent via the Agent tool. The subagent does the heavy reading and editing and returns a *compact summary*, not a transcript dump. This is what lets one turn run for hours without the orchestrator's context ballooning and degrading. Subagent prompts must be self-contained: the subagent does not share Leroy's context, so spell out the goal, the relevant files, and the return shape you expect back.

**There is a floor, and Leroy's parallelism bias will push you under it.** Delegation buys context headroom on genuinely independent, sizeable tracks; on small work it just multiplies cost and wall-clock for a summary you could have earned directly. So: don't delegate what you can finish in a handful of tool calls, don't spawn several agents where one can do the job, and don't spawn one to check work you already did — a subagent re-reading your own output is pure overhead. "Meaty chunk" is the unit. A single file edit is not one.

**LOW-confidence forks can't pause — so they don't.** Normally LOW confidence means STOP and ask. Unattended, there is no one to ask, so:

- If the fork is **reversible**, take the most reversible option, drop a breadcrumb flagged distinctly as an open question (not a routine MODERATE breadcrumb), and continue.
- If the fork is **irreversible or destructive**, do **not** guess. Skip that branch, park it as an open question for review, and move on to work that isn't blocked on it.

The Leroy branch plus the breadcrumbs make both outcomes cheap to review and selectively undo later.

**Stop cleanly at the budget.** As you approach the time or quota limit, stop deliberately rather than getting cut off mid-write. Run the pause protocol below.

## Pausing safely

A Leroy run ends one of three ways: it finishes, it hits the budget, or something
cuts it off. Only the first two are under your control, so make them clean. Run
this whenever you stop — at the budget, on an explicit "stop", or when context is
about to compact.

This is explicit-stop only. "Keep going", "I'm going to bed", and "don't stop"
mean *continue*; the trail already checkpoints each chunk.

1. **Stop at a safe boundary.** Finish the atomic step in flight or back out of
   it. Never stop mid-edit in a known-broken state. Start nothing new, and let
   any dispatched subagents finish or cancel them — don't strand them.
2. **Don't cross an irreversible line in order to pause.** No push to a shared
   branch, no release, no deploy that wasn't already the plan. Pausing is not a
   deadline.
3. **Make the work durable.** Commit whatever is uncommitted to the Leroy branch
   as one clear `wip:` commit so nothing is lost. If the tree is broken, say so
   in one line of the commit body.
4. **Write the resume note to a file, not to context.** Context does not survive
   compaction and definitely does not survive the session ending. Put it next to
   the trail as `<run-id>-resume.md`: what you were doing, what is verified vs.
   merely written, the current state, the next concrete action, and any gotcha
   the next session would otherwise rediscover. Point at the trail for the
   decision history rather than restating it.

**Report back:** where you stopped in the run, **what is on disk versus still in
your head** (paths, not diffs), the commits made and whether the tree is clean,
and the first action on resume.

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
- **Skipping the decision trail, or deferring it to the end of the run.** The trail is what makes autonomy safe, and a trail assembled at the end is exactly the one a crash destroys. No log, no Leroy.
- **Stopping without the pause protocol.** A run that ends mid-edit with the plan only in context is unresumable, which costs more than the work it saved.
- **Pausing for confirmation on MODERATE decisions.** That defeats the purpose. Log and proceed.
- **Touching the user's main branch by default.** Use a Leroy branch unless the user explicitly says otherwise.
- **Running across multiple projects in one invocation.** One project per Leroy run; multi-project sweeps lose coherence.
- **Padding the fallback menu.** The two canned modes (Full Treatment, Audit Blitz) are the menu shown *only* when the user states no goal. Don't invent a third on the fly; if a recurring no-goal use case keeps surfacing, end cleanly and ask whether to add it for next time. A user-*stated* goal is never a "mode" and needs no menu entry.
