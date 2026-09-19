---
name: leroy-jenkins
description: Autonomy-biased operating mode for converting otherwise-wasted token quota (near 5-hour or weekly window resets) into useful work. Runs the goal you state — or, if you state none, delegates to project-checkup or robustness-audit — with a relaxed confidence bar, logging decisions to a trail instead of pausing for moderate-confidence calls. Can run unattended for a long single turn, using subagents to stay context-lean. Explicit invocation via /human-training:leroy-jenkins (Claude Code) or $human-training:leroy-jenkins (Codex).
---

# Leroy Jenkins Mode

An overlay, not a task source. Leroy changes *how* work gets done — relaxed
confidence bar, decision breadcrumbs instead of pauses, a branch of its own —
for tokens that would otherwise reset unused. The *what* is the goal you state
at invocation or, if you state none, one of two canned modes.

**Invoke only when explicitly selected:** `/human-training:leroy-jenkins` in
Claude Code or `$human-training:leroy-jenkins` in Codex. Not on "I have tokens
to spare", "let's run wild", or "burn the quota" — the user named those as
exactly the accidental triggers to avoid.

Optional arguments, any combination:

- **A stated goal** — this *is* the work. No menu. Treat it as first-class,
  not as a deviation to flag; Leroy owns the how, never relitigates the what.
- **Minutes until reset** — scales aggressiveness (see the table in
  [reference.md](reference.md)). Under 15 minutes with no stated goal, decline:
  setup overhead exceeds the window. With a stated goal, never decline on time
  alone — scope the goal to the window and log what was deferred.
- **An unattended signal** — "do as much as you can in one turn", "I'm going
  to bed", "I won't be able to reply". Switches on the long-haul posture below.

Use the active runtime to decide which host mechanics apply (subagent tool,
config paths). Do not infer the host from an installed `claude` or `codex`
command. The confidence bar Leroy relaxes is the one in the user's global
instructions as loaded by that host.

## The work surface

**1. Stated goal.** Execute it.

**2. No goal.** Present exactly two options, recommendation first:

> Pick a Leroy mode:
> 1) **Full Treatment** (recommended) — `human-training:project-checkup` in
>    force-all mode: every component runs, no skipping on pulse state.
> 2) **Audit Blitz** — `human-training:robustness-audit` at 7–10 surfaces
>    instead of 3–5, and no pause after synthesis for triage: full report with
>    action menu in one shot.

Don't invent a third option on the fly. If a no-goal use case keeps recurring,
end cleanly and ask whether to add it next time. Leroy never picks up work the
user didn't ask for — "don't freelance" means that, and faithfully executing a
stated goal is the opposite of freelancing.

One project per run. Multi-project sweeps lose coherence.

## The overlay

| Bar      | Standard                    | Leroy                                          |
|----------|-----------------------------|------------------------------------------------|
| HIGH     | just do it                  | just do it                                     |
| MODERATE | do it, flag in DEVLOG       | **do it, drop a trail row, move on**           |
| LOW      | STOP and ask                | STOP and ask — *unless unattended, see below*  |

Pausing on a MODERATE call defeats the purpose. When a LOW call does need the
user: numbered options, opinionated, recommendation first, never open-ended.

> Decision needed: <one line>. 1) X (recommended because Y). 2) Z. 3) Park.

**Branch first.** Create `leroy/YYYY-MM-DD-HHMM` and commit there; the user
cherry-picks or merges what they like. If they decline, stay on the current
branch but make small themed commits (one per decision class) so revert stays
granular. Never touch main by default.

## The decision trail

Every MODERATE decision and every unattended LOW fork gets a row, written **as
it happens**. A run that dies partway — context exhausted, quota hit, machine
slept — is exactly the one whose reasoning you need, and exactly the one an
end-of-run write-up loses. No trail, no Leroy.

The format belongs to `human-training:show-me-your-work` — columns, append-only
rule, end-of-run audit. Don't restate it; two copies drift. Leroy adds three
things:

- **Path:** `docs/leroy/<run-id>.tsv` if the project keeps working docs under
  `docs/`, else `leroy/<run-id>.tsv` at root. `<run-id>` is the branch's
  `YYYY-MM-DD-HHMM`.
- **Committed**, overriding that skill's local-by-default. The whole point of
  the trail is reviewing work nobody watched; it lands beside the diff it
  explains.
- **Unattended LOW forks** are flagged distinctly as open questions, not as
  routine rows.

The DEVLOG gets one short closing entry that points at the trail (template in
[reference.md](reference.md)) — the chronicle records that the run happened
and what came out, not every decision inside it. Per-decision detail in the
DEVLOG is what made the old prose breadcrumbs unreadable.

## Unattended / long-haul runs

Orthogonal to mode and goal; combines with any of them.

**Plan first, then batch.** Write the session plan to the trail as its first
rows before executing anything, then a row per completed chunk. The plan must
never live only in context.

**Delegate meaty chunks to subagents** — build a feature demo, run an audit
surface, write a test pass — using whatever the host provides. Leroy stays the
planner/synthesizer; the subagent does the heavy reading and editing and
returns a compact summary, not a transcript. Prompts must be self-contained:
the subagent shares none of Leroy's context, so spell out goal, files, and the
return shape. This is what lets one turn run for hours without the
orchestrator's context degrading. If the host offers no subagent mechanism, do
the chunk inline and checkpoint to the trail more often.

**There is a floor, and the parallelism bias will push you under it.** Don't
delegate what you can finish in a handful of tool calls, don't spawn several
agents where one will do, and never spawn one to re-check your own output.
"Meaty chunk" is the unit; a single file edit is not one.

**LOW forks can't pause, so they don't.** Reversible: take the most reversible
option, log it as an open question, continue. Irreversible or destructive:
do not guess — skip it, park it, move to work that isn't blocked on it.

**Stop at the budget deliberately**, not by getting cut off mid-write. Run the
pause protocol.

## Pausing

Run this at the budget, on an explicit "stop", or when context is about to
compact. "Keep going", "I'm going to bed", and "don't stop" mean *continue*.

1. **Stop at a safe boundary.** Finish or back out of the step in flight.
   Never leave a known-broken state. Start nothing new; let dispatched
   subagents finish or cancel them — don't strand them.
2. **Cross no irreversible line in order to pause.** No push to a shared
   branch, no release, no deploy that wasn't already the plan.
3. **Commit** everything to the Leroy branch as one `wip:` commit. If the tree
   is broken, say so in one line of the body.
4. **Write the resume note to disk**, beside the trail as `<run-id>-resume.md`
   (contents in [reference.md](reference.md)). Context does not survive
   compaction, let alone the session ending.

A run that ends mid-edit with the plan only in context is unresumable, which
costs more than the work it saved.

**Reply:** where the run stopped; what is on disk versus still in your head
(paths, not diffs); commits made and whether the tree is clean; the trail's
path; and the first action on resume.
