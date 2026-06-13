---
name: grill
description: Adversarial pre-build alignment. Interrogates you one question at a time — recommended answer on each — walking every branch of the decision tree until "done" is crisp and bounded, then sharpens fuzzy domain terms into CONTEXT.md inline. The fix for a fuzzy plan, creeping scope, or unclear done-criteria. Explicit invocation via /grill before starting a change; use when you want to be grilled, stress-tested, or pinned down before writing code.
allowed-tools: [Read, Glob, Grep, Edit, Write]
---

# /grill — Adversarial pre-build alignment

The most common failure mode in building software is misalignment: you think
the plan is clear, the agent builds something else, and you discover the gap
only after the work is done. The fix is to close that gap *before* writing
code — by having the agent interrogate you until every branch of the decision
tree is resolved.

This is a **deliberately uncomfortable** skill. Its job is to make you confront
the parts of the plan you haven't actually decided yet — the edge case you
skipped, the term you're using two ways, the contradiction between what you
just said and what the code does. Soft consensus is the failure mode, not the
goal. Push.

## When to invoke

Explicit invocation via `/grill`, typically *before* starting a change while the
plan is still fuzzy. Good triggers: scope feels like it's creeping, "done" isn't
crisp, you're about to hand a vague brief to an implementation loop, or you just
want to be stress-tested. Do **not** auto-fire on phrases like "let's build X" —
wait for the command.

This is the alignment step that sits *between* having an idea
(`project-genesis`) and implementing against a spec (`lifecycle-manager`). It
does not write the feature, run tests, or produce a spec document — it produces
a *resolved plan* and a sharper shared language.

## The grilling discipline

Interview the user relentlessly about every aspect of this plan until you reach
a genuinely shared understanding. Walk down each branch of the design tree,
resolving dependencies between decisions one at a time.

- **One question at a time.** Wait for the answer before asking the next. A wall
  of ten questions gets one skimmed answer; one sharp question gets a real one.
- **Recommend an answer to every question.** Don't just ask — say what you'd do
  and why. The user reacts faster to a concrete proposal than to an open prompt,
  and disagreement surfaces the real constraint.
- **Explore the codebase instead of asking, whenever you can.** If a question is
  answerable by reading the code, go read it. Only spend the user's attention on
  what the code can't tell you.
- **Follow dependencies, not a checklist.** Resolve the decision that unblocks
  the most others first. When an answer opens new branches, walk them.
- **Stop when "done" is crisp.** The exit condition is a bounded plan with no
  unresolved forks that matter — not a fixed number of questions. When you get
  there, say so and summarize the resolved plan.

The user is AFK-tolerant: if they go quiet, proceed with your recommended
answers and flag the assumptions you made, rather than blocking.

## Sharpening the language (CONTEXT.md)

A grilling session is the richest source of terminology you will ever get — the
user is being forced to be precise about what their words mean. Capture it.

Look for a **`CONTEXT.md`** at the project root (the domain glossary — distinct
from `onboarding.md`, which is the office tour, and from the spec, which is what
to build). During the session:

- **Challenge against the glossary.** When the user uses a term that conflicts
  with `CONTEXT.md`, call it out: "Your glossary defines 'cancellation' as X,
  but you seem to mean Y — which is it?"
- **Sharpen fuzzy or overloaded terms.** "You said 'account' — do you mean the
  Customer or the User? Those are different things." Propose the precise term.
- **Stress-test with concrete scenarios.** Invent edge cases that force the user
  to be precise about the boundaries between concepts.
- **Cross-reference with code.** If the user states how something works and the
  code disagrees, surface the contradiction.
- **Update `CONTEXT.md` inline, as terms resolve** — not batched at the end.
  Format in [CONTEXT-FORMAT.md](CONTEXT-FORMAT.md).

`CONTEXT.md` is a **glossary and nothing else** — totally devoid of
implementation details, plans, or decisions. Not a spec, not a scratchpad. If
those leak in, it stops being a fast shared language and becomes another stale
doc.

**Graceful degradation.** No `CONTEXT.md`? Still grill — the alignment is the
point, the glossary is the bonus. Create the file lazily, only when the first
term is actually worth pinning down, and offer it rather than imposing it:
"'materialization' keeps coming up with a specific meaning — want me to start a
CONTEXT.md so it's defined once?" If the user declines, drop it and keep
grilling.

## Load-bearing decisions → DEVLOG

When the grilling resolves a decision that a future reader would need explained,
record it where this workflow already keeps decisions: the **DEVLOG**. Don't
stand up a parallel decision-record system.

Offer to log a decision only when **all three** are true:

1. **Hard to reverse** — changing your mind later has real cost.
2. **Surprising without context** — a future reader will wonder "why this way?"
3. **The result of a real trade-off** — there were genuine alternatives and you
   picked one for specific reasons.

If any one is missing, skip it — most decisions don't need recording. Frame the
offer as: "This one's load-bearing — want it in the DEVLOG so it isn't
re-litigated later?" If the project has no DEVLOG (not a workflow project), note
the decision wherever the project records them, or just in the conversation —
don't manufacture a DEVLOG to hold it.

## When done

End with a tight summary of the **resolved plan**: what's being built, what
"done" means, the decisions that were made, and any assumptions you proceeded on
while the user was AFK. That summary is the handoff into implementation
(`lifecycle-manager`) — it should be crisp enough to build from without
re-deriving anything.

## Anti-patterns

- **Going soft.** The value is the pressure. If you find yourself agreeing to
  keep things pleasant, you're not grilling — you're rubber-stamping.
- **Batching glossary updates.** Capture terms the moment they resolve; a
  "I'll update CONTEXT.md at the end" never happens and loses the precision.
- **Treating CONTEXT.md as a spec.** It's a glossary. Implementation details,
  plans, and decisions belong in the spec and DEVLOG, not here.
- **Asking what the code can answer.** Spend the user's attention only on what
  the code can't tell you. Explore first.
- **A fixed interrogation length.** Stop when the plan is crisp, not at question
  N. Five questions on a simple change, thirty on a hairy one.
- **ADR sprawl.** Decisions go to the DEVLOG, not a separate `docs/adr/` tree —
  this workflow has one decision log, keep it that way.
- **Firing in this repo's own workflow.** This skill ships to downstream hobby
  projects. The plugin-factory repo itself has no sprint workflow, no DEVLOG,
  and no CONTEXT.md to grill against.

---

## Credit

Adapted from [Matt Pocock's skills](https://github.com/mattpocock/skills)
(MIT — © 2026 Matt Pocock): his `grill-me` and `grill-with-docs`, merged into one
docs-aware skill and rewired to this workflow's `CONTEXT.md` glossary and DEVLOG
decision log. The adversarial-alignment idea and the grilling discipline are his.
