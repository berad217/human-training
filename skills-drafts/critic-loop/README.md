# critic-loop — draft

**Status: genuine draft** (no `skills-source/critic-loop/` exists). Started 2026-09-11.

## What it is

Brad's critic loop, generalised out of `Shapey_McShapeface` — iterating an artifact whose
quality has no test (only a perceiver) against fresh, blind critic agents, with a
pre-committed rubric / gate / budget / walls, a free inner loop, rationed rounds, a per-line
vector instead of a score, and a documented stop as a deliverable.

The evidence record is **`Shapey_McShapeface/docs/CRITIC_LOOP.md` v3** (2026-09-11): three
subjects, fifteen rounds, every rule tagged with the round that earned it or the `n=0` that
says it has not. This draft is the *general form* of that document: the three invariants
(contamination, gradient validity, spend discipline) and the per-subject-class parameter
table, with the image class as the one instance that has data.

## What is n=0, and why that matters here

The whole method is **n=15 on images and n=0 on everything else** — prose, code, UI, schema.
§4 of the SKILL.md says so per row. The source doc's own oldest lesson is that a rule written
from zero observations reads exactly like a tested one (its v2 wrote four such rules; one
failed outright when run). So this draft must not graduate on the strength of its image
evidence alone.

**Graduation criterion:** at least one run off images, logged here, with §4's row for that
class rewritten from what happened. The cheapest candidate is the draft itself — prose,
invented subject, function gate: *"what is this document for, who is it for, what would you
do after reading it?"* Round zero + one round.

## Plan

1. ~~Draft `SKILL.md` from CRITIC_LOOP v3.~~ Done 2026-09-11.
2. Round zero on the draft: a known-good exemplar skill from `skills-source/` (e.g. `grill`),
   read cold by a fresh agent with the same function question — sets the ceiling and proves
   the critic can perceive a SKILL.md. Then the draft, blind: title, frontmatter and
   filename stripped (those are the prose leak channels §4 hypothesises).
3. Round 1: informed read against a rubric written *from the subject* (what a skill for this
   method must make a reader able to do), not from this README. Log to `rounds/`.
4. Rewrite §4's prose row from the run. Decide Track 1 (`workflow/guides/`) vs Track 2
   (`skills-source/`) — the method is model-agnostic, the §9 mechanics are Claude's.
5. Graduate per `skills-drafts/README.md`.

## Open questions the run should answer

- Does a fresh agent reading a SKILL.md cold identify its *function* without the frontmatter?
- What leaks in prose that the §4 row did not list?
- Is "what would you do after reading it" a gate a stranger can fail, or does every
  competent reader pass it (recognition saturating on round zero)?
- Is the second scale ("would you want this skill installed?") worth its line?

## Folder

```
critic-loop/
├── README.md        this file
├── SKILL.md         the draft, iterated in place
├── eval-queries.md  candidate triggers for the eventual trigger-eval
└── rounds/          round-zero and round logs, when run
```
