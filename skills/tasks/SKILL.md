---
name: tasks
description: Use when managing a project's task list / todos — adding, reviewing, or completing tasks, or parking a tangent or "I should also…" idea so it doesn't derail current work. Maintains a per-project TASKS.md (Active / Someday / Done). Triggers on /tasks, "add a task", "what's on my list", "park that for later", "what was I going to do next". Offers to capture commitments and tangents mid-work, always confirming first. Do NOT use for recording decisions or rationale (that's the DEVLOG) or for workplace contact/jargon memory.
allowed-tools: [Read, Write, Edit, Glob]
---

# /tasks — Per-project forward queue

A lightweight task list for the current project that doubles as a mission-creep
guardrail. It holds what's **next** and what's **parked**, so a tangent gets
captured instead of derailing the task in hand.

It complements the DEVLOG, it does not duplicate it: **DEVLOG is
backward-looking** (decisions made and why); **TASKS is forward-looking** (what's
queued, parked, done). Don't put rationale here; don't put todos there.

## The file

One file per project: `TASKS.md` at the project root (fall back to
`./docs/TASKS.md` if the project keeps working docs under `docs/`). Three
sections. If the file is absent when you need it, create it from this template:

```markdown
# Tasks

## Active
<!-- current + next-up work -->

## Someday
<!-- the parking lot: tangents, "I should also…", deferred ideas -->

## Done
<!-- completed, newest first -->
```

Line format:
- Open task: `- [ ] **Short title** — one-line context (for what / blocked on what)`
- Done task: `- [x] ~~Short title~~ (YYYY-MM-DD)`

## Managing tasks

Invoked explicitly with `/tasks`, or in natural language ("add a task to…",
"what's on my list?", "mark X done").

- **Show** (default, no verb): summarize **Active**, and flag anything that reads
  stale or overdue. Don't dump Someday or Done unless asked.
- **Add**: insert into **Active** (or **Someday** for a parked idea) with a
  one-line context. Confirm the wording if it's ambiguous.
- **Done**: tick the checkbox, strike the title, append `(today's date)`, move it
  under **Done** (newest first).

## Notices & offers (the guardrail)

While this skill is loaded in a session, watch for the user voicing a tangent, a
fresh idea, or a commitment mid-work ("oh, I should also refactor X", "we need to
handle Y eventually"). When you spot one, **offer** to capture it:

> "Want me to park that in Someday so we stay on \<current Active item\>?"

Rules:
- **Always confirm before writing. Never auto-add a task.**
- Default a tangent to **Someday** (a parking lot, not a new priority); only put
  it in Active if the user says it's the next thing.
- This watching only works while the skill's instructions are in context — a
  session where `/tasks` or `/start` has loaded it. There is no background
  capture; that's by design.

## Anti-patterns

- **Turning Done into a changelog.** Done is a checkbox + date. The *why* of a
  decision goes in the DEVLOG, not here.
- **Surfacing Someday unprompted.** The parking lot stays parked until asked.
  Showing it during normal work re-introduces the exact distraction it exists to
  prevent.
- **Auto-adding.** Always offer and confirm. The user's list is the user's.
- **Recording decisions or workplace/jargon memory here.** Wrong tool — that's
  the DEVLOG and the memory system respectively.
