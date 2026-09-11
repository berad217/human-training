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
2. ~~Round zero on the draft~~ Done 2026-09-11 — `rounds/00-precommit.md`, `rounds/01-round-1.md`.
   Exemplar `grill` read cold: function/audience/first-action all correct, confident;
   `want` ceiling 16/20.
3. ~~Round 1~~ Done. Gate met 2/2 on the blind reads. Informed vector **92 / 96**, spread
   ≤ 1 per line; `want` 16 / 14. v2 of the SKILL.md takes the critics' safe list and two
   logged deviations; the open list is in the round log §5.
4. ~~Rewrite §4's prose row from the run.~~ Done.
5. ~~Brad's rulings, 2026-09-11 (evening):~~ **(a) the skill is high-level, model- and
   artifact-agnostic; on invocation its first move is to design the harness for *this*
   artifact and propose it for approval before any round is spent. (b) Budget unit is
   rounds, not critic calls. (c) Split: `SKILL.md` operational, `reference.md` carries the
   harnesses that have run and the stories. (d) Track 2.** → v3 written: §0 "what you get
   back when you invoke this", §3 harness design with the sort (critic-visible → rubric;
   not → wall), the §0 proposal template ending in "approve to run"; per-class rows and all
   stories moved to `reference.md`, keyed by `[ref: …]`. 427 lines + 191.
6. ~~Second round on v3~~ Done — `rounds/02-round-2.md`. **Both answers yes, n=2:** the whys
   carry (one critic checked fifteen refs: "corroboration, not the instruction"); §0 stops
   the agent (both quote "approve to run. Then wait."). Vector **91 / 91, spread 0 on every
   line**; `want` 16 / 16 = the ceiling. Line 6 fell 14→12 on both reads for one reason —
   the untested-class rows had left the file — and v4 restores a status index in §3b (six
   lines) without putting the hypotheses back. v4 also takes the safe list (cost and run
   counts at Budget, read-type contrast, own-table refiled, §8 hedged) and a compressed
   *real* §0 — the Refinery's — as the worked example both critics asked for. 469 lines.
7. **Graduate.** The criterion (one run off images, row rewritten) is met twice over. Ritual
   per `skills-drafts/README.md`: move to `skills-source/critic-loop/` with `SKILL.md` +
   `reference.md` (leave `rounds/`, `eval-queries.md`, this README here as residue), build,
   bump version, commit.

## What the run answered

- **Does a fresh agent identify a SKILL.md's function without its frontmatter?** Yes,
  confidently, from voice and cross-references — for the exemplar *and* the draft. Which
  means:
- **The function gate saturates on prose.** A document that states its purpose passes
  "what is this for" by construction. The discriminating question is *what would you do
  first* — both critics answered "the pre-commit," which is the right answer; a doc that
  produced "send it to critics" would fail. Recorded in §4's prose row and §7.
- **What leaks in prose that the row did not list?** Nothing the strip missed — but the
  body's own self-references ("Explicit `/critic-loop`") were the primary driver for both
  critics, and those cannot be stripped. The row now says so.
- **Is the second scale worth its line?** It produced the run's most useful disagreement
  (14–17 around a ceiling of 16, both citing "personal research log / would trim before
  trusting") — the finding that the *evidence-marking* the skill's own §6 rewards is what
  makes it feel uninstallable. Yes, worth it.

## Open, after round 1

- ~~**Length vs receipts.**~~ Ruled: split. The `n` stays in the skill's failure table; the
  stories live in `reference.md`. v3 is 427 — the stories left (−60) and the harness-design
  sections Brad asked for arrived (+45). Whether the one-clause whys carry is round 2's
  question, not a line count's.
- **The critics' "not safe" list**, declined in v2: a default budget number (would be a
  claim generalised past n=15); a worked trace stitched from other subjects' numbers
  (`rounds/01-round-1.md` is the honest substitute — a real one).
- **The sibling pointer** ("measured pass — not a skill yet") was flagged in both rounds as a
  dead end. Write the skill or cut the paragraph. Brad's call.
- **§6's failure table** is 25+ unranked rows; round 2 A named it as what undermines the
  document. Grouping the rows under the three invariants would give it a start-here without
  changing a row. Not taken — nobody was asked to rule on it.
- **One method observation, now n=4, still not a rule:** across two rounds, four of the
  critics' "needs a second look" rulings were conditional on a fact only the author held
  (the sibling's existence; §9 had been run; a real gate exists in the record; the harness
  *was* written before the artifact every time). Each taken and logged as a deviation. The
  pattern: **a critic marks "not safe" when it cannot verify; the author can, from the
  record.** Whether that stays honest under a less scrupulous author is the question a
  rule would have to answer, and one author cannot answer it.

## Folder

```
critic-loop/
├── README.md        this file
├── SKILL.md         the draft, iterated in place — operational: invariants, harness design, protocol, templates, failure table
├── reference.md     the harnesses that have run, the untested rows, and every [ref: key] story
├── eval-queries.md  candidate triggers for the eventual trigger-eval
└── rounds/          round-zero and round logs, when run
```
