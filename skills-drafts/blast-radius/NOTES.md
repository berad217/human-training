# blast-radius — draft notes

Not built, not shipped. `skills-drafts/` is scratch; nothing here reaches
`skills/`.

Source: the `blast-radius` skill in
[cursor/plugins/pstack](https://github.com/cursor/plugins/tree/main/pstack)
(MIT, Lauren Tan), audited 2026-08-19. Adapted rather than ported — pstack's
version composes with `why`, `arena`, and a multi-model panel, none of which
exist here.

## Graduation blockers

**1. The evidence ladder has two consumers and no owner.**

The draft references the ladder rather than restating it, and points at
`human-training:robustness-audit` as where it's written down. That is the right
call for a draft and the wrong shape to ship: `robustness-audit` is an odd owner
for a concept two skills share, and pointing a second skill at a *third* skill's
section is a cross-reference that will rot.

This is the same trigger that produced `show-me-your-work` in 1.23.0 — a format
with a second consumer either gets an owner or becomes two formats. Three options:

- Extract the ladder into its own small skill. Honest, but it would be one table
  and a paragraph, which is thin for a skill.
- Let `blast-radius` own it and have `robustness-audit` reference *it*. Cleaner
  conceptually (the ladder's full range only matters where code can be run), but
  it inverts the dependency between a shipped skill and a draft.
- Keep the ladder in `robustness-audit` and accept the cross-reference. Cheapest,
  and the option that drifts.

**Decide before graduating.** Shipping with the current cross-reference is the
one choice that is definitely wrong.

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
