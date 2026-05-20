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
> common pitfalls, read `assets/spec-writing-guide.md`. Spec templates:
> `assets/project-spec-template.md` (comprehensive) and `assets/spec.md`
> (brief). Testing conventions: `assets/testing-standards.md`.

---

## Transition to Implementation

Once the spec is approved:

1. Create `onboarding.md` from the onboarding template — the universal agent
   entry point.
2. Create a `DEVLOG.md` skeleton.
3. Confirm the human is satisfied with the spec.
4. Sprint-0 scratch (this genesis conversation, rough notes) can be cleared
   once implementation begins — the spec, onboarding, and DEVLOG are the source
   of truth from here.
