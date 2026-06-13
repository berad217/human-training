# Design — `tasks` skill (+ `start` integration)

**Date:** 2026-06-13
**Status:** Design (pre-implementation)
**Lives at:** `skills-drafts/tasks/` while iterating; graduates to
`skills-source/tasks/` when ready. Plus a small edit to the existing
`skills-source/start/SKILL.md`.

---

## Purpose

A per-project forward queue that doubles as a mission-creep guardrail. Ships
downstream alongside the other workflow skills (`start`, `lifecycle-manager`,
etc.). It gives a hobby project a lightweight "what's next / what's parked"
surface that complements DEVLOG (which records what *happened* and *why*), and
it surfaces at session open via `/start` so a single opening prompt answers
both "where are we" and "what's queued."

Motivated by two stated user pain points: parking tangent ideas reliably, and
fighting mission creep (scattered priorities, excitement about tangents,
unclear "done").

## Non-goals (deliberate cuts from productivity's task-management)

- **No `dashboard.html`.** Terminal workflow; a drag-drop HTML board is dead weight.
- **No external-tracker sync** (Asana/Linear/Jira/GitHub Issues). Solo hobby
  projects, direct-to-main.
- **No workplace-shorthand decoding / people-and-deals memory.** That's the
  productivity plugin's reason for existing; not this user's context. Memory is
  already handled by the existing two-tier memory system.
- **No "Waiting On" section.** That's for waiting on colleagues; the user is
  solo. (A "Blocked" section for external dependencies is a possible future
  add, not v1.)
- **Not a decision log.** Completed-task records are one-liners, not rationale.
  Real decisions go in DEVLOG.

## The artifact — `TASKS.md` at project root

Three sections, created from a template on first use if absent:

```markdown
# Tasks

## Active
- [ ] **Wire the retry logic into the fetch client** — needs the backoff util first

## Someday
- [ ] **Try the streaming parser approach** — parked 2026-06-13, tangent from the retry work

## Done
- [x] ~~Add the backoff util~~ (2026-06-12)
```

- **Active** — current + next-up work.
- **Someday** — the parking lot. Tangents, "ooh I should also…", deferred
  ideas. The creep killer: when excited about a tangent mid-task, it lands here
  instead of derailing the Active item.
- **Done** — completed, with a date. Lightweight; strikethrough + date, no rationale.

Task format: `- [ ] **Title** — short context`. Done: `- [x] ~~Title~~ (YYYY-MM-DD)`.

## Behavior

**Explicit management via `/tasks`** (consistent with `/start` being explicit):

- *show* (default) — summarize Active, flag anything that reads stale; Someday
  only on request.
- *add* — insert into Active (or Someday for parked ideas) with short context.
- *done* — toggle checkbox, strikethrough, date, move to Done.

**Notices & offers (the guardrail), while the skill is loaded in a session:**

- When the user voices a tangent / "I should also…" / a commitment mid-work,
  offer to park it: "Want me to drop that in Someday so we stay on
  \<current Active item\>?"
- **Always confirms before writing. Never auto-adds.**
- Mechanical honesty: a skill only watches while its instructions are in
  context (i.e., a session where `/tasks` or `/start` has loaded it).
  Persistent always-on capture would need a hook — explicitly out of scope for v1.

## Boundary vs DEVLOG (what keeps it from bloating)

- **DEVLOG** = backward-looking: decisions, rationale, what happened per sprint.
  (Owned by `lifecycle-manager`.)
- **TASKS** = forward-looking: what's queued, what's parked, what's done.
- Done entries are NOT decisions. When completing a task involved a real call,
  that rationale goes to DEVLOG; TASKS Done just records the checkbox + date.

## The `start` integration (second v1 piece)

`start` currently reads onboarding/CONTEXT/DEVLOG/handover and proposes the next
move. Add `TASKS.md` to that flow:

- **Step 1 (locate):** add `TASKS.md` to the existence check
  (project root → `./docs/TASKS.md`).
- **Step 2 (read temporal context):** read the **Active** section only. Not
  Someday (parking lot ≠ queue), not Done. Keeps `start`'s "don't read
  everything" discipline.
- **Step 3 (next move):** the recommended next move draws from Active when
  present, reconciled with what the handover flagged as in-flight. The top
  Active item is often literally the next move.
- **Graceful degradation:** if `TASKS.md` is absent, `start` behaves exactly as
  today. No hard dependency.

## File layout

```
skills-drafts/tasks/             (while iterating)
├── SKILL.md          ~80-110 lines  trigger + the three sections + format +
│                                    explicit verbs + notices-&-offers + DEVLOG boundary
├── assets/
│   └── TASKS-template.md          the 3-section starter written on first use
└── evals/
    └── trigger-eval.json          should / should-not trigger candidates

skills-source/tasks/             (after graduation — same contents)

skills-source/start/SKILL.md     EDIT: add TASKS.md to locate + read Active + inform Next
```

Track 2: the SKILL.md is the artifact. No `workflow/guides/` source, no
build-script `$skillDefinitions` edit — `tasks` is not a Track 1
workflow-derived skill. The `start` edit is a plain content edit to an existing
Track 2 skill.

## SKILL.md structure (the spine)

1. **Frontmatter.** `name: tasks`; `description` tuned to trigger on
   task-management intent (see tuning below); `allowed-tools: [Read, Write,
   Edit, Glob]` — no Bash; it only reads/writes `TASKS.md`.
2. **What it is (~10 lines).** Per-project forward queue + creep guardrail; the
   three sections; the DEVLOG boundary in one line.
3. **The file (~20 lines).** Location, the 3-section template, the task/done
   line format, the create-if-absent rule.
4. **Explicit verbs (~20 lines).** show / add / done — each a couple of lines.
5. **Notices & offers (~20 lines).** The guardrail behavior; the always-confirm
   rule; the "while loaded" honesty note.
6. **Boundaries / anti-patterns (~15 lines).** vs DEVLOG; don't turn Done into a
   changelog; don't surface Someday unprompted; don't auto-add.

## Trigger description tuning

`description` enumerates concrete triggers, modeled on the repo's other Track 2
skills:

> Use when managing a project's task list / todos — adding, reviewing, or
> completing tasks, or parking a tangent or "I should also…" idea so it doesn't
> derail current work. Maintains a per-project `TASKS.md` (Active / Someday /
> Done). Triggers on `/tasks`, "add a task", "what's on my list", "park that for
> later", "what was I going to do next". Offers to capture commitments and
> tangents mid-work, always confirming first. Do NOT use for recording decisions
> or rationale (that's the DEVLOG) or for workplace contact/jargon memory.

## evals/trigger-eval.json

Format matches `skills-source/robustness-audit/evals/trigger-eval.json`: array
of `{query, should_trigger}` objects.

Should-trigger (4):
- "add a task to wire up the retry logic"
- "park that idea for later so I don't lose it"
- "what's on my list / what was I going to do next?"
- "mark the backoff util task done"

Should-NOT-trigger (4):
- "log why we chose the backoff approach" (DEVLOG, not tasks)
- "remember that Todd owns the Oracle deal" (memory, not tasks)
- "what does this function do?" (unrelated)
- "create a handover for the next session" (handover-manager)

## Success criteria

1. `/tasks` with no file creates `TASKS.md` from the 3-section template.
2. add/show/done manipulate the right sections with the right formatting
   (strikethrough + date on done).
3. Mid-work, when the user voices a tangent, the session offers to park it in
   Someday and only writes after confirmation.
4. In a project with `TASKS.md`, `/start` includes an "Active tasks" line in
   orientation and the proposed next move reflects Active; in a project WITHOUT
   it, `/start` is unchanged.
5. The description triggers on the should-trigger evals and not the
   should-not ones.
6. Build pipeline accepts it as Track 2: drop graduated `skills-source/tasks/`,
   run `./scripts/build-skills.ps1`, `diff -r skills /tmp/skills-rebuild` empty,
   bump version, both manifests aligned.

## Open questions

None blocking. Minor implementation calls:

1. **`/tasks` sub-verb syntax.** Whether to support `/tasks add …` arg parsing
   vs natural language ("add a task to…"). Lean natural-language with bare
   `/tasks` = show; decide during implementation.
2. **Someday → Active promotion.** Probably just an edit/`add`, no special verb.
   Confirm during implementation.

## Out of scope (future revisions)

- **Persistent always-on capture** via a `UserPromptSubmit` (or similar) hook,
  so tangent-parking works without first loading the skill. Heavier
  (settings.json, hook script); revisit if the in-session-only behavior proves
  insufficient.
- **Global cross-project parking lot.** Considered (Approach B in brainstorming)
  and rejected for v1 — per-project fits the plugin model. A separate
  personal/global skill is the right shape if the portfolio-level need surfaces.
- **"Blocked" section** for external dependencies. Easy add if real blockers
  (waiting on an upstream fix, a purchase) start accumulating.
