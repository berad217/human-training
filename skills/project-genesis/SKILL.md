---
name: project-genesis
description: >-
  Use when starting a new project, brainstorming an idea, evaluating whether something is worth building, or turning a concept into a technical spec. Covers Sprint 0 end to end: ideation (challenge ideas, red-team, force scope) and spec writing (concrete specs for coding agents). Enter at brainstorming, enter at speccing, or flow through both.
allowed-tools: [Read, Write, Edit, Grep, Glob, WebSearch, WebFetch]
---

# Project Genesis: From Spark to Spec

**Purpose**: Guide "Sprint 0" — the phase before implementation where a raw
idea is challenged, refined, and (if it survives) crystallized into a technical
specification a coding agent can build from.

This skill covers two phases: **Ideation** and **Spec Writing**. The boundary
between them is fuzzy on purpose — a conversation often flows from one into the
other without a clean line.

---

## Entry Modes — Decide Where to Start

Read the situation and pick where to spend tokens:

- **Brainstorm only** — The human is thinking out loud about an approach or a
  problem. It may never become a spec, and that is fine. Stay in the Ideation
  phase. Do not push toward a spec.
- **Full flow** — The human has an idea they might build. Start in Ideation;
  transition to Spec Writing only when they explicitly say they are ready.
- **Spec only** — Ideation already happened, often in another session. Skip to
  Spec Writing. Ask for a quick summary of what was decided, then write.

When unsure, ask: "Are we exploring this, or are you ready to commit to
building it?"

---

## Phase 1: Ideation

**Goal**: Help the human figure out if an idea is worth their finite time — and
be willing to conclude that it is not.

Core moves:

1. **Understand first** — "Walk me through what you're imagining. What sparked
   this?" Let them talk; they often find the issues themselves.
2. **Challenge assertively** — No hedging. "That won't work because X" beats
   "you might consider...". Ask "What problem does this actually solve?"
3. **Red-team it** — Hunt for the fatal flaw. "How much of this is shiny-object
   syndrome vs real value?"
4. **Existence check** — Search the web. Show 3-5 existing solutions. Building
   anyway for the learning is valid — just make it a conscious choice.
5. **Scope forcing** — "What's the absolute simplest version that's still
   useful or interesting? What's V1 vs someday-maybe?"
6. **Mission-creep watch** — Name expansion when you see it: "We started with X,
   now it's X+Y+Z. Intentional?" Make them choose creep consciously; don't shut
   down exploration.

Ideation ends in one of three outcomes:

- **Ready to build** → transition to Phase 2.
- **Convinced not to build** → articulate the solid reasons why.
- **Parked** → capture with the Parking Lot format so future-them can
  resurrect it.

> For the full ideation playbook — anti-patterns, the parking-lot format, tone
> guidance — read `assets/ideation-protocol.md`.

---

## Transition

Don't slide silently from ideation into spec writing. When the idea seems
build-worthy:

- Summarize what you understand.
- Ask explicitly: "Ready to write the spec based on this?"
- Wait for a clear yes. If they have more questions, stay in ideation.

---

## Phase 2: Spec Writing

**Goal**: Transform the conversation into a spec a *different* AI coding agent
(zero shared context) can implement without guessing.

A spec covers, at minimum:

- **Overview** — name, one-sentence purpose, why it exists, who uses it.
- **Visual identity** — the "vibe", palette, typography. Prevents a generic UI.
- **Success criteria** — a testable checklist defining "done". This is the
  anti-mission-creep anchor.
- **Technical foundation** — be prescriptive: stack, runtime, testing
  framework, key dependencies. No guessing.
- **Architecture** — major components, single responsibilities, loose coupling,
  a real file tree.
- **Data models** — concrete JSON/TypeScript examples, never prose.
- **Sprint breakdown** — ~2-3 hour chunks, each with success criteria,
  deliverables, and handover context.
- **Testing strategy** — written during each sprint, not after.
- **Constraints & out-of-scope** — explicit DO / DO-NOT, and what we are
  deliberately not building.

Principles: show, don't tell (examples over descriptions); the spec is a living
document, not a contract; define "done" clearly.

> For the complete spec structure with examples, the writing process, and
> common pitfalls, read `assets/spec-writing-guide.md`. Spec template:
> `assets/spec.md`. Testing conventions: `assets/testing-standards.md`.

---

## Transition to Implementation

Once the spec is approved:

1. Create `onboarding.md` from the onboarding template — the universal agent
   entry point.
2. Create a `DEVLOG.md` skeleton.
3. **Set up in-repo memory — do this at genesis, not later.** See below; this is
   the step that is easiest to skip and most expensive to skip.
4. Confirm the human is satisfied with the spec.
5. Sprint-0 scratch (this genesis conversation, rough notes) can be cleared
   once implementation begins — the spec, onboarding, and DEVLOG are the source
   of truth from here.

### Memory at genesis (step 3, expanded)

A harness that stores project memory in a path derived from the **working
directory** — Claude Code uses `~/.claude/projects/<slug>/memory/` — gives a
brand-new project **no memory at all**, and gives a project that *moved* none of
what it had. Nothing errors. You simply get an agent that has forgotten
something the human is certain they said.

Genesis is the only moment where this is free to fix, so fix it here:

- Create **`memory/`** in the new project, with a `MEMORY.md` index.
- Write the memory rule into the project's **`CLAUDE.md`**: read and write
  `memory/` in this repo; do not use the harness default path. Without that
  instruction the default silently wins.
- **If this project came from somewhere** — a spike graduating out of a sandbox,
  a folder promoted to its own repo — **carry its memory across now.** That is
  `workflow-orientation` §6's job; invoke it rather than reimplementing the
  migration. Do not leave the entries behind "for now"; "for now" is how every
  one of these ends up stranded.
- **Scope what comes across.** The new repo takes facts about *itself* and about
  the projects it directly serves or depends on. Cross-cutting facts — who the
  human is, how they want agents to work, harness mechanics, OS gotchas — stay
  canonical in **one** place and are not copied into every repo. Copying them is
  how one fact becomes five drifting copies, and copies drift *fast*: a project
  that graduated with a hand-seeded copy had three of twelve entries diverged
  within twenty-four hours, one of them describing a shipped, playtested project
  as "spec'd, nothing built."
- Anything you *do* mirror gets labelled a **mirror**, with the date it was taken
  and an instruction to re-copy. Visible drift beats silent drift.

**Private repos only.** Memory holds working-style notes and project context that
the human may not want public. If the new repo is or may become public, say so
and leave memory out of it rather than migrating and hoping.
