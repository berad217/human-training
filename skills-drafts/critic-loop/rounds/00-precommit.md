# §0 — Pre-committed before round zero (2026-09-11)

**Subject class: prose** (a SKILL.md). **First run off images.** Written before any critic
saw the artifact, and before the blind copy was made. Not to be edited after round 1 except
for factual error, in the open.

## Rubric — capability, 100

Written from the *subject* — what a reader must be able to do after reading a skill for this
method — not from `README.md` or the conversation that produced the draft.

| # | Criterion | Wt |
|---|---|---:|
| 1 | **Knows when to reach for it, and when not to.** Reaches for it on a quality with no test; refuses one that has a test; knows a quality the critic cannot perceive needs a wall, not a round | 20 |
| 2 | **Can set up a run.** Pre-commits a rubric written from the subject, a falsifiable gate, a budget and executable walls — before building; runs a round zero | 20 |
| 3 | **Can run a round correctly.** Fresh agent per read; blind stage as a separate agent; read type matched to the question; two reads polled; tables first and capped; the last round asks what is safe to take | 20 |
| 4 | **Can read a result.** Sorts into the three bins; prices each item against the whole rubric; logs the vector, not the total | 15 |
| 5 | **Can stop.** Recognises gate / budget / ceiling / late wall, and treats a documented stop as a deliverable | 10 |
| 6 | **Trusts it correctly.** Can tell which rules are measured and which are hypotheses, and would rewrite the hypothesis rows from a run rather than treat them as settled | 15 |

**Second scale — `want/20`:** would a competent agent-driving developer, shown this skill
alone, want it installed? Scored on the exemplar too, as the ceiling.

## Gate

**Function recognition** (invented subject; no reference). Two fresh blind critics, in
parallel, given the stripped copy and no context, both say: *what it is for* (iterating an
artifact against independent fresh reviewers when there is no objective test), *who it is
for* (an agent, or a person driving one, building such an artifact), and *what they would do
next* is the pre-commit — not "start sending it to reviewers."

Both must get all three. One of three is a fail.

## Budget

**Round zero + one round.** One round is the deliverable — this run exists to convert §4's
prose row from n=0 to n=1, not to polish the skill. The round's stage 4 carries the
last-round question (what is safe to take unreviewed); the response takes the safe list and
nothing else; the rest is the open list for a later round.

## Walls — run in the inner loop, never spend a round

- **Frontmatter valid:** `name:` matches the directory; `description:` present, single
  paragraph. Checked by script before the round.
- **Triggers:** `eval-queries.md` is the eventual test; not runnable yet. Noted as the wall
  this run *cannot* run — the §3 rule says measure it before round 1 and this run cannot.
  Recorded as a gap, not waived silently.

## Leak channels — the prose hypothesis from §4, made executable for this run

The blind copy strips: the YAML frontmatter (its `description:` is the answer verbatim),
the H1 (`/critic-loop — Iterating against a fresh pair of eyes` — also the answer), and the
Credit section (provenance, not function, but it names the repo and its doc). The body keeps
every use of "critic loop" — a document's own vocabulary is the artifact, not a label on it.
**This is the hypothesis under test.** Stage 1 asks the critic what told it.

The blind copy lives at a content-hashed path in the session scratchpad, not in the draft
folder — the folder is named `critic-loop`.

## Hardest question, phrased for a number

The draft is ~400 lines. `grill` is 142, `robustness-audit` 395. **What length would carry
the same capability, and which sections go first?** I cannot tell whether the length is the
evidence-marking (the n per rule, which §6 of the rubric says is load-bearing) or bloat.

## Deliberate deviations

- **No "already-accepted artifact in your medium" control.** The exemplar (`grill`) *is*
  the medium — a shipped SKILL.md from the same plugin. One control covers both purposes.
- **The informed read sees the full SKILL.md including frontmatter and Credit.** The
  informed stage is not blind; it judges the real artifact.
