---
name: blast-radius
description: Work out what a specific change breaks somewhere else, beyond the diff, and prove the one fact its safety depends on by running code rather than writing it up. Triggers on /blast-radius, "blast radius of X", "what could this break", "is this safe to change", "what else touches this", or reviewing a small diff you don't trust. Do NOT use for a wide audit of existing code with no particular change in view — that's robustness-audit.
---

# Blast radius

What does this change break somewhere *else*? Not what it does — what it does to
things that aren't in the diff.

Listing the callers is not the job. Grep finds those in a second. The job is the
breakage grep won't show you: a JSON shape another process parses, a column an
old row still has, a wire format read by a different language, a pinned library
version with a local patch, code three hops downstream that assumed something
you just changed.

## When to invoke

- `/blast-radius`, "blast radius of X", "what could this break".
- A small diff that feels riskier than its size.
- Before touching something load-bearing you haven't read in months.
- Before a change you can't easily undo — a migration, a format change, anything
  that writes to disk in a new shape.

## Not this skill

- **`robustness-audit`** reads existing code across several surfaces looking for
  latent defects, with no particular change in view. This reads **one change**
  and asks what it reaches. Different question, different shape: that one fans
  out to parallel agents, this one goes deep on a single blast site.
- **A code review.** Whether the change is *good* is not this. Whether it is
  *contained* is.
- **"Is this safe?" with no change to point at.** Needs a diff, a commit, a
  branch, or at minimum a described edit.

## Don't trust your own writeup

A blast-radius writeup that sounds right is worthless, and this is the trap
rather than a caveat. The output reads as convincing whether or not it is true,
and it is *especially* convincing when it concludes the change is fine — because
that is the conclusion you wanted before you started.

So the deliverable is not the writeup. It is one or two proven facts with a
writeup around them. Words are where you start, not what you ship.

### How sure are you

Use the **evidence ladder** — Asserted, Cited, Traced, Executed, Reproduced.
It is written down in `human-training:robustness-audit`; read it there rather
than working from memory.

The difference here: **that skill ceilings at Traced because it never runs the
code. This one does not.** You are allowed to run things, which means rungs 4
and 5 are on the table, which means stopping at 3 is a *choice you have to
justify* rather than a constraint you inherited.

For the one or two facts the change's safety actually rests on, get to **rung 4**
unless it is genuinely expensive. Rung 4 is usually one small script that imports
the same library the app ships and calls the exact function you are worried
about. If you cannot get there cheaply, say so out loud and mark the fact
unproven. Never round up.

## Steps

### 1. Read the change

The diff, the symbols it adds, changes, and deletes — and what now behaves
differently, **including the part the diff doesn't spell out**. A one-line change
to a default, a serialization order, or an error type has a diff of one line and
a blast radius that isn't.

If the change isn't committed yet, read the working tree. If it is, read the
commit and anything that landed alongside it.

### 2. Find the one fact it's safe because of

This is the step that earns the skill.

Most changes that look frightening are safe because of a **single fact** — "this
only ever drops cache entries that were already dead", "nothing else reads this
file after startup", "the old and new formats are byte-identical for every input
we actually produce". Find that fact and state it in one sentence.

If it holds, most of the scary cases die at once and you know exactly what to
prove. If you can't find one, that is itself the finding: the change is not
contained, and the honest answer is that it needs to be smaller.

Spend your time here, not on assembling a long list of maybes.

### 3. Look where grep stops

Symbol search is the floor, not the work. Go where it can't:

- **Serialized shapes.** JSON on disk or over the wire, a DB column, a cache
  entry, a config file, a saved session, a pickle. Old data written by old code
  outlives the code that wrote it.
- **Cross-language and cross-process boundaries.** Anything where one side reads
  bytes the other side wrote, and the compiler checks neither.
- **The library's own source.** Read it, and check the pinned version *and* any
  local patch. What the docs say and what the installed version does are two
  different facts.
- **Timing.** What runs before what: startup order, teardown, async boundaries,
  a callback that now fires one tick later.
- **Flags and config.** A path that only executes when something is enabled, and
  is therefore invisible to a test run with it off.
- **Downstream of downstream.** Two hops past the direct callers, where the
  assumption you changed has been quietly relied on.

A search that finds nothing is still an answer — record it as one.

### 4. Be honest about each risk

For each way this could break, give it a real likelihood and a real cost. Not
"could theoretically" — how would it actually happen, to whom, and what would
they see?

Keep the risks you confirmed. List separately the ones you checked and cleared,
because "I looked at this and it's fine" is information the next reader needs
and will otherwise re-derive.

Cite a real `file:line`. **Never invent a caller, an API, or a config key.** A
fabricated risk in a blast-radius report is worse than no report, because it
sends someone to defend against something that does not exist.

### 5. Prove the one fact

Write the script. Run it. Paste what happened.

The script calls the real code — the same import the app uses, the same function,
the same inputs — and **fails loud if you are wrong**. A script that prints
something you then interpret is not proof; a script that exits non-zero when the
assumption breaks is.

Keep it. A reviewer can rerun it, and it is the artifact that turns "I checked"
into "run this". If the change ships, the script often wants to become a test.

If you genuinely can't prove it cheaply, mark it **unproven** and say what
stopped you. Don't round up.

## What to hand back

- **What it does.** What changed, including the part that isn't obvious from the
  diff.
- **The one fact it's safe because of.** Stated in a sentence, with its rung, and
  the proof pasted. Or marked unproven, with what stopped you.
- **Risks.** Only the real ones. Each names how it breaks, a real `file:line`,
  how likely, how bad, and how to check.
- **Cleared.** What you checked and why it's fine. Include the searches that
  found nothing.
- **Before you merge.** The cheapest test or repro that would catch the real bug,
  including the script you wrote.

**Reply:** the five sections above, with the safety fact either proven at rung 4
or explicitly marked unproven. Never both hedged and reassuring.

## Anti-patterns

- **Handing back a writeup with nothing run.** The failure this skill exists to
  prevent. A confident survey of everything that *might* break, with no fact
  proven, is the exact artifact that gets trusted and shouldn't be.
- **Listing every caller.** That's grep's job and it is not the interesting set.
  The interesting set is what grep can't see.
- **Rounding a rung up.** "I read the function and it looks fine" is Traced at
  best, usually Cited. Say which.
- **Concluding "safe" without naming the fact.** If you can't say *why* in one
  sentence, you haven't finished step 2.
- **Padding the risk list.** Ten speculative risks hide the one real one. If you
  wouldn't act on it, it goes in Cleared or nowhere.
- **Running this as a general audit.** No change in view means the wrong skill —
  that's `robustness-audit`.
