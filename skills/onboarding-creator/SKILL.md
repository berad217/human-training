---
name: onboarding-creator
description: >-
  Use when setting up a new project, after the Sprint 0 spec is complete, or when an AI agent entry point is missing. Creates onboarding.md, the universal orientation doc that works across any environment (Cursor, VSCode, Claude Code, web) - the office tour, not the employee handbook.
allowed-tools: [Read, Write, Edit, Grep, Glob]
---

# Onboarding Guide

You are writing `onboarding.md`: the universal entry point an AI agent reads
first in any host — Claude Code, Cursor, GPT in VS Code, a web chat with file
access. **It is the office tour, not the employee handbook**: where things are,
how work really happens here, enough context to start. A minimal template is
in `assets/onboarding.md`; worked section examples, the self-contained
skeleton, the embeddable peer-sessions block and the final checklist are in
`assets/onboarding-reference.md`. Read those only when a step points you there.

**Invoke when** a spec has just been written (onboarding is one of Sprint 0's
deliverables), an agent entry point is missing, or after Sprint 1–2 when the
guesses in the first draft can be replaced with what actually happened. It is a
living document: when docs move or the workflow changes, update it so the next
agent doesn't get lost.

---

## Two constraints that shape every line

**You cannot predict the reader's environment.** Terminal, IDE, or web chat —
different tooling, and no way to know which. So describe *what* to find and
*why* it matters, never the keystrokes: "look for spec.md, usually in docs/"
survives any host; "run `grep -r spec docs/`" is already wrong for half of
them. (How a reader identifies its *own* environment is `lifecycle.md` §1's
job — the reader's problem, not yours.)

**One document, one mode.** Two questions place any piece of writing: is it
for *doing* or for *understanding*, and is the reader *learning* or *working*?
Onboarding is doing + working — a how-to. When you feel the pull to add an
explanation ("why we chose Postgres") or reference material (an API table), that
is a different document: the DEVLOG holds the why, the spec and README hold the
what. Point at them and move on. The same test sorts the other docs — global
preferences is *who the human is*, CONTEXT.md is *what the words mean*, spec §9
is *engineering constraints*, the handover is *conversation state*. Don't make
one doc do everything.

---

## Authoring hygiene

You are reading a project in order to describe it, which is exactly the
situation where reading everything first feels justified. Don't. Read enough
to write each section accurately, and no more. Context hygiene and mid-project
orientation are `lifecycle.md` §1's job; point the reader at it rather than
restating it in the onboarding you write.

---

## The seven sections

Write each one that has real content; skip the ones that don't (see
*Right-sized*, below). Worked examples for every section are in the reference.

1. **Welcome / purpose.** One sentence on what the agent is here to build, then
   a few facts: project type, the human's level, current phase.

2. **Getting oriented — the map.** The critical section. For each doc the
   project keeps (spec, CONTEXT.md, DEVLOG, handover, global preferences, any
   agent-facing protocol docs): list the **common locations, plural**; say
   **what it contains**; and say **what to do when it isn't found** (ask the
   user; start from spec and DEVLOG; create it if you're the first agent).
   This is *planned fuzziness* — the reader's tree is never as tidy as yours.
   CONTEXT.md is seeded lazily, only when the project has jargon worth
   pinning; stub it from `assets/CONTEXT.md` if you set one up.

3. **About this human.** If `docs/.agents/global-preferences.md` exists
   (legacy: `.agents/`, `.claude/`), point at it and add only project-specific
   working notes. Otherwise write a short inline version: communication style,
   experience level, learning goals, key working preferences, who runs tests.

4. **How we work.** Sprint loop (implement → test immediately → DEVLOG →
   commit together → one sprint at a time), the confidence bar (high: do it;
   moderate: do it and flag in DEVLOG; low: stop and propose 2–3 options),
   testing framework and expectations, documentation cadence, how to handle
   ambiguity. Customize to the stack, the testing philosophy, how hands-on the
   human is, and whether this is learning or production.

   **If the human runs sibling repos with their own sessions** that message
   each other, add the peer-sessions block from the reference. It fixes a
   failure that runs both ways: sessions that dismiss a peer's message as
   untrusted input and make the human re-relay it, and sessions that treat
   "the human said" inside a peer message as the human. The block names the two
   axes — **credibility high, authority none**: read it as a colleague, act on
   it as a proposal. Name the sibling repos in Project-Specific Notes, not
   here; the block is the posture, that list is the map.

5. **If you're the first agent.** What to create when the docs don't exist
   yet: DEVLOG (skeleton in the reference), README (install, run, test, one-line
   description), test infrastructure per the spec.

6. **Writing handovers.** Every agent needs to know how to hand off, so embed
   it — more direct than the handover guide itself, since this is a working
   doc, not a meta-guide. **The handover guide is the authority; what you embed
   must not drift from it.** Three sections, ~200 tokens: Orientation (with a
   Durability line *only* when something is unpushed), the Delta (debates,
   failed paths, in-flight breakage — strictly what is not in the files), Next
   steps. Tell the reader to run `git status -sb` and read the `[ahead N]`
   marker before writing — committed is not pushed. Two things that look
   helpful and must **not** be embedded: a "what we accomplished" section
   (status report; belongs in the DEVLOG) and anything already in spec, DEVLOG
   or code (reference it instead). A clean stop produces a nearly empty
   handover; that is success.

7. **Project-specific notes.** Quirks, key files and why they matter, common
   commands, gotchas that would trip a new agent. Sibling repos go here.

---

## Writing style

Conversational, not formal. Practical, not comprehensive. Fuzzy on purpose
("common locations: X, Y, Z", not "location: X"). Include the human's
personality — "appreciates direct feedback, don't sugarcoat" beats "provide
objective assessments". Before/after pairs are in the reference.

**Right-sized.** An office tour is short because the building is small, not
because the guide was rationed. A two-file hobby project has less to show than
a service with four deploy targets, and its onboarding should be visibly
shorter. A section kept alive with "[TBD]" or a restatement of the one above it
costs the next agent context and teaches them the doc is padding — cut it.

---

## Agent ops

- Agent-facing docs live under `docs/.agents/`; project docs live in `docs/`.
- If workflow guides were copied into the project, archive or delete them once
  used (spec-writing guide after the spec, this guide after onboarding.md,
  ideation protocol after ideation). Keep the handover guide and global
  preferences.
- If a handover already exists, edit it in place — some IDEs fail on a file
  deleted and recreated in the same turn.

---

## Before you save

The test: *could an agent you've never met, in a host you didn't anticipate,
starting from zero context, find what it needs and start working?* Run the
checklist in the reference against the draft.

**Reply:** the path written; which of the seven sections are present and, for
each omitted one, `skip: <reason>` in one line; and anything you could not
determine from the project and need the human to fill in.
