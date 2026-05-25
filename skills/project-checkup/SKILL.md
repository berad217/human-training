---
name: project-checkup
description: State-aware project health check that composes workflow-orientation, robustness-audit, a "next-move" inventory, and a friction audit. Designed to minimize re-entry friction on dormant or abandoned hobby projects. Explicit invocation via /project-checkup.
allowed-tools: [Read, Write, Edit, Grep, Glob, Bash]
---

# Project checkup

A state-aware project health check. Composes existing skills (`workflow-orientation`, `robustness-audit`) with two new components — a **friction audit** and a **next-move inventory** — and surfaces a single unified report with the next move at the top.

Designed for the case that drives this skill's existence: a hobby project that's been parked for weeks or months, and re-entry feels like cold-starting a stranger's repo. The checkup makes that re-entry friction-free.

## When to invoke

Direct, explicit invocation via `/project-checkup`. Useful when:

- Returning to a project after a break (the bread-and-butter case)
- At a sprint boundary (start or end)
- Before a milestone or handoff
- When the question "what should I do next on this?" has no obvious answer

Do **not** auto-invoke on ambiguous phrases like "check my project" or "audit X" — those could mean any of `robustness-audit`, `workflow-orientation`, or this skill. Wait for the explicit command.

## Structure

Three phases:

1. **Pulse** — read-only state read.
2. **Compose** — invoke sub-skills based on what the pulse reveals.
3. **Surface** — unified report with the next move at the top.

---

## Phase 1: Pulse

Read-only. The goal is to classify the project's state in under a minute so Phase 2 can route intelligently.

Collect:

- Last commit date: `git log -1 --format=%cd`
- Branch state: `git status -sb` (uncommitted? unstashed? not on main?)
- Activity over last 30 days: `git log --since="30 days ago" --oneline | wc -l`
- Existence and last-edit date of canonical docs: `onboarding.md`, `DEVLOG.md`, handover doc (check canonical locations from CLAUDE.md's Document Hierarchy)
- Build/run signal: lockfile-vs-manifest drift (`package-lock.json` older than `package.json`, etc.), CI status if `gh` is available

Present the pulse as a brief table:

```
| Signal           | Value                                |
|------------------|--------------------------------------|
| Last commit      | 2025-08-12 (9 months ago)            |
| Branch           | main, clean                          |
| Activity (30d)   | 0 commits                            |
| onboarding.md    | exists, edited 9 months ago          |
| DEVLOG.md        | exists, last sprint 8 months ago     |
| Handover         | missing                              |
| Build signal     | package-lock.json older than package.json |
```

Then classify into one of four states (this drives Phase 2 routing):

| State            | Signals                                                            |
|------------------|--------------------------------------------------------------------|
| Active healthy   | Commits this week, docs fresher than commits                       |
| Active doc-rot   | Commits this week, docs older than commits                         |
| Dormant          | 4 weeks–6 months since last commit                                 |
| Abandoned        | 6+ months since last commit                                        |

Heuristics, not certainties. State the confidence (high/medium/low) when it's ambiguous.

---

## Phase 2: Compose

Route based on the pulse state. Default routing:

| State           | What runs                                                                |
|-----------------|--------------------------------------------------------------------------|
| Active healthy  | Friction audit + next-move inventory only. Skip workflow-orientation and robustness-audit unless something in the pulse flags them. |
| Active doc-rot  | `workflow-orientation` + friction audit + next-move inventory.           |
| Dormant         | Full sequence: `workflow-orientation` + `robustness-audit` + friction audit + next-move inventory. |
| Abandoned       | Full sequence + a "is this worth resurrecting?" prompt before the report is acted on. |

**Force-all mode:** When invoked from `leroy-jenkins`'s "full treatment" mode, run all four components regardless of pulse state — no skipping.

### Component invocations

- **`human-training:workflow-orientation`** — invoke for doc/workflow state. Pass forward any user notes about the project; let it run its own audit-discuss-act cycle, then collect its summary for the unified report.
- **`human-training:robustness-audit`** — invoke when the project has meaningful code activity (skip for pure-docs projects or projects with <10 source files). Collect its triage menu for the unified report.

### Friction audit (this skill's own work)

Things `workflow-orientation` doesn't cover. Quick scan:

- **Build/run friction.** Lockfile older than manifest. Deprecated config files. Removed peer deps in major-version-bumped packages. Existence of a working start command (don't run it — just check it's documented somewhere).
- **Dead branches.** `git branch -a` — any stale feature branches that should be deleted or merged?
- **Stashed work.** `git stash list` — was something left in flight?
- **TODOs/FIXMEs.** `grep -rn "TODO\|FIXME"` on source dirs only. Count + sample 3-5.
- **Broken doc paths.** Every file path mentioned in `onboarding.md`, `README.md`, `DEVLOG.md` should resolve. Test each with `Test-Path` / `ls`.

Output: a short list of friction items, ordered by impact on re-entry.

### Next-move inventory (this skill's own work)

The highest-value component. Goal: compute the smallest, most obvious concrete next action so cold-start future-you doesn't have to generate it.

Read:

- The last 2-3 DEVLOG entries (where did things stop?)
- Any handover doc (what was in flight?)
- The most recent commit message and diff
- The current branch (if not main, what was being built?)
- Open TODOs/FIXMEs from the friction audit

Decide:

- What was being worked on last?
- Was it complete or mid-stream?
- What's the smallest concrete next action?

Output format:

```
**Next move:** <one concrete action — start a command, write a test, finish a function, decide a question>
**Why:** <one line — what state the project is in after this move>
**Effort:** <small (<15 min) | medium (1-2 hr) | session (longer)>
**Prerequisites:** <any blockers — broken deps, missing decisions, etc.>
```

If multiple valid candidates exist, present 2-3 with the recommended one first. Match the Teflon Mode default — numbered options with a recommendation.

---

## Phase 3: Surface

One unified report. **Next move at the top.** Findings follow.

```markdown
# Project checkup — <project-name>

## Next move
<from the next-move inventory — front and center>

## State
<pulse table from Phase 1, plus state classification>

## Friction
<friction items, ordered by re-entry impact>

## Workflow state
<summary from workflow-orientation if it ran>

## Robustness findings
<summary from robustness-audit if it ran>

## What we skipped and why
<transparency: what the pulse routed away from, so the user can ask for it explicitly>
```

The "next move" at the top is non-negotiable. The whole point of this skill is to remove the inertia of "what do I do?", and burying that under audit findings defeats it.

---

## Composition with other skills

- **`leroy-jenkins`** invokes this skill in *force-all mode* and applies its autonomy-bias overlay to any follow-up actions. project-checkup itself is mode-neutral — it produces a report and stops. Leroy adds the "now act on it" layer.
- **`workflow-orientation`** is invoked *by* this skill, not the other way around. The dependency arrow goes one way: project-checkup is the orchestrator; workflow-orientation is a component.
- **`robustness-audit`** likewise — invoked by this skill, never the inverse.

---

## Anti-patterns

- **Skipping the pulse.** Running every component every time wastes context and produces noise. State-aware routing is the entire point.
- **Burying the next move.** It's not finding #5 of 20 — it's the lead. Top of the report.
- **Auto-acting on findings.** This skill produces a report. It does not fix things on its own. `lifecycle-manager`, `robustness-audit`, and the user (with approval) do the actual work afterward.
- **Generating ten "next moves".** If you can't pick one with rationale, read the DEVLOG and handover more carefully. The Teflon ethos applies here too: propose, don't ask.
- **Re-running components that just ran.** If `workflow-orientation` was run an hour ago and its outputs are still current, surface the prior result instead of re-running.
