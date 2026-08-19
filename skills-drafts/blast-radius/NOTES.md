# blast-radius — draft notes

Not built, not shipped. `skills-drafts/` is scratch; nothing here reaches
`skills/`.

Source: the `blast-radius` skill in
[cursor/plugins/pstack](https://github.com/cursor/plugins/tree/main/pstack)
(MIT, Lauren Tan), audited 2026-08-19. Adapted rather than ported — pstack's
version composes with `why`, `arena`, and a multi-model panel, none of which
exist here.

## Graduation blockers

**1. ~~The evidence ladder has two consumers and no owner.~~ Settled 2026-08-19:
don't centralize it.**

The first instinct was to extract the ladder the way the TSV format became
`show-me-your-work` in 1.23.0. Measuring it killed that. Of the 32 lines in
`robustness-audit`, roughly 14 are portable and 18 are local, and the most
load-bearing cell is one of the local ones: **rung 3 means "read caller and
callee side by side" in an audit and "walk whether the bad case reaches across a
boundary" in blast-radius.** Those are not the same test. A shared definition
covering both collapses to "you reasoned about it carefully", which teaches
nothing.

The TSV and the ladder are different kinds of thing, and calling them the same
trigger was the error:

- **The TSV is a data format.** Tools and humans read it across runs; drift
  breaks compatibility; there is exactly one correct schema. It earned an owner.
- **The ladder is a vocabulary.** The definitions are *supposed* to differ per
  skill. The only real drift risk is the five names, and forcing uniformity below
  the name costs accuracy.

**Resolution.** Each skill defines the rungs in its own terms. Both use the same
five names in the same order, and each states its own ceiling and why.
`robustness-audit` carries a note saying the names are shared and the tests are
local; this draft carries its own table plus the line that rungs 4 and 5 are
available here, so a reader doesn't inherit the audit's rung-3 ceiling by
association. Revisit only if a third consumer turns up with a genuinely identical
test.

**2. Never exercised.**

Not run against a real change. The whole skill turns on step 5 (write the script,
run it, paste the result), and whether that actually happens in practice or gets
skipped in favour of a confident writeup is exactly what the skill claims to
prevent — and exactly what a draft cannot tell you. Run it on a real diff before
graduating. A skill about proving things that was itself never proven is a poor
look.

Good candidate: a change in one of the hobby projects that touches a serialized
shape, since that's the case the skill claims grep misses.

## Deliberate divergences from pstack's version

- **Dropped the `arena` step.** pstack runs several models over the same question
  and merges. No cross-vendor parallel subagents here; `codex-cli` /
  `antigravity-cli` could give a second opinion, but that belongs in the same
  thread as the Leroy cross-vendor trail review, not bolted on separately.
- **Dropped the `why`-skill dependency** in step 1 for reading the PR and commits.
  Replaced with reading the working tree or the commit directly.
- **Added an explicit boundary against `robustness-audit`.** Ours exists and
  pstack's doesn't, so the overlap needs naming or both will trigger on
  "what could go wrong". The distinction: audit fans out across surfaces with no
  change in view; blast-radius goes deep on one change.
- **Made the rung-4 expectation explicit.** pstack says get as far as is cheap.
  Since `robustness-audit` ships a hard rung-3 ceiling, this skill has to say
  loudly that its ceiling is different, or the reader will inherit the wrong one.
- **Added "if you can't find the one fact, that's the finding"** — the change
  isn't contained and wants to be smaller. Implied in pstack, worth stating.

## Open questions

- Should this be `disable-model-invocation`-equivalent (explicit-invocation only)?
  The description currently has a NOT-clause steering away from `robustness-audit`.
  Untested whether that's enough separation.
- Does it need a subagent step at all? Currently entirely main-thread, which is
  right for depth-on-one-change but means it eats context on a big diff.
