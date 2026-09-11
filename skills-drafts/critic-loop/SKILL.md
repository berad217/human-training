---
name: critic-loop
description: Iterate an artifact whose quality has no test — only a perceiver — against fresh, blind critic agents. On invocation, designs a harness for THIS artifact (rubric, gate, budget in rounds, walls for what the critic cannot see) and proposes it for approval before any round is spent; then runs a free inner loop and rationed critic rounds, logs a per-line vector, and treats a documented stop as a deliverable. Model- and artifact-agnostic. Triggers include "does this read as X", "would a stranger get this", "am I too close to this", "fresh eyes", "critic round", "review loop", "iterate with a reviewer", "is this recognisable / persuasive / clear / obvious what it's for". Explicit invocation via /critic-loop. Not for qualities that have a test — use the test.
---

# /critic-loop — Iterating against a fresh pair of eyes

Some qualities have an objective test: does it compile, do the tests pass, is
the overlap count zero. **Use the test.** This skill adds nothing there.

Other qualities have no test at all: *does this read as an A-10, is this
document persuasive, would a stranger know what this screen is for.* The only
instrument is a perceiver — and the author is the worst available one, because
they know what they meant and read the intention back into the artifact.

The critic loop is the other tool: **a fresh agent that sees the artifact and
nothing else, judges it cold, and hands back deficiencies the author converts
into changes.** This skill is the method, independent of model and artifact.
What it produces first, on every invocation, is a **harness** for the artifact
in hand — and it does not spend a round until the human has approved it.

**Evidence.** Brad's design. Three image subjects over fifteen rounds and one
prose subject over one round, every rule tagged with the round that earned it
or the `n=0` that says it has not. The stories behind each rule, the harnesses
that have run, and the untested classes are in [reference.md](reference.md);
`[ref: key]` below points into it.

## When to invoke

Explicit `/critic-loop`, when an artifact's remaining faults are ones the
author can no longer see: you have looked at it enough times that it looks
fine; you are about to ask someone "does this look like X?"; you are arguing
with yourself about a proportion, a paragraph, a layout, and cannot settle it
by looking again.

Do **not** auto-fire on "review this" — a code review has a test-shaped answer
and its own tools.

## Not the right tool for

- **Anything with a test.** Compile, lint, unit tests, a measurement, a wall.
  The critic will assert things about these that the test disproves.
- **A quality the deliverable has but the critic cannot perceive.** A structure
  that must stand, a page that must load in 200 ms. The critic judges the
  *picture*; a quality it cannot see gets optimised away while every round
  reports improvement `[ref: twelve-rounds]`. That quality needs a **wall** —
  §3.

**The sibling.** When the quality *does* have a test, the critic is the wrong
instrument but the iteration discipline is not: a **measured pass** runs the
same skeleton with the instrument where the critic would be. Not a skill yet;
`reference.md` has the pointer.

## 0. What you get back when you invoke this

The skill runs in three moves, and the first ends with a question to you.

**1. Harness proposal.** The agent reads the subject — and the artifact, if
one exists yet; on a build-from-concept there is only the concept — then
comes back with a §0 document (§3 has the template): what the critic will see,
what it must not see, what it scores and how, what ends the loop, how many
rounds, and — separately — what the walls check because the critic cannot.
Everything the human said "matters" is sorted into one of those two bins,
visibly. **The proposal ends in "approve to run."** Rubric lines are what every
round optimises toward; they are the human's to ratify, not the agent's to
assume.

**2. Round zero.** Free. The instrument is proved on things that are not the
artifact — an exemplar, an already-accepted piece, the pipeline itself — and
version 1 is measured on every wall before a round is spent on its appearance.

**3. Rounds, then a stop.** Inner loop unlimited; outer loop budgeted in
*rounds* — one version judged, however many critics that takes. Every round
logged as a per-line vector. The stop — gate met, budget spent, ceiling, or a
wall found late — is written up as a deliverable with the open list priced.

## 1. The three things every rule guards

Every rule below protects one of three properties. Knowing which lets you
design a harness for a medium the skill has never seen.

1. **Contamination — is the perceiver actually independent?** Intent reaches
   the critic through channels the author does not notice: a caption, a
   filename, the category in the question, the rubric in the same prompt as
   the blind question, the critic's memory of its last answer, the brief the
   artifact was generated from. A contaminated read returns a confident answer
   that measured nothing, and **nothing inside the loop can reveal it.** Guards
   must be executable; the prose version of a leak guard was tested and did not
   hold `[ref: path-leak]`.
2. **Gradient validity — is the signal the goal?** A scalar score is not a
   gradient. Recognition saturates. Rubric lines trade. A deficiency gives
   direction, not magnitude. A critic's read of a reference is a claim about
   the world and can be wrong. And the loop's gradient can run against a
   constraint the critic cannot perceive. What survives: the **per-line
   vector**, a **falsifiable gate**, and **walls** the inner loop runs.
3. **Spend discipline — is a round bought for a question only a stranger can
   answer?** Rounds are rationed to stop the author outsourcing judgement —
   which is why the unit is a *round*, not a critic call: a version judged by
   four agents is one measurement, and charging per call pushes toward the
   single read that misreads the reference `[ref: reference-misread]`.

## 2. The two loops

```
OUTER: critic round        <- expensive, budgeted, each one a real judgement
  INNER: author iterates   <- cheap, unbudgeted, run until you stop finding things
```

**The inner loop is free.** Build, look, judge, fix, look again. The walls run
here, on every version, before anything is sent.

**The outer loop is rationed.** Send to the critic only when your honest answer
to "what is wrong with this?" is *"I have stopped being able to tell."* If your
own verdict names a defect, that is inner-loop work `[ref: known-defect]`.
"I'll send it early to see what the critic says" is a round spent on a
question you can already answer — calibrate in round zero, where it is free.

**The inner loop has a blind spot exactly where the last round's advice was
applied.** You look at the change through the note, see "I made it
not-a-staircase," and tick it off. Two guards: judge a changed feature against
the *subject*, not the note; and name last round's changes at the top of the
next round's questions, so a stranger checks your compliance — you cannot.

## 3. Designing the harness

This is move 1 of §0, and it is the artifact-specific part. Everything after
it is the same for a LEGO build, a README, a screen.

### 3a. Sort what matters

Take every quality the human named — *fidelity, practicality, coolness* — and
ask of each: **can a fresh perceiver see this in what we will show it?**

- **Yes** → a rubric line, or a second scale. The critic scores it.
- **No** → a **wall.** An executable check the inner loop runs, or a downstream
  measurement taken on version 1 before round 1. The critic never scores it.

Practicality — will it stand, will it load, will it compile — is almost always
a *no*. The one time it was left as a note in the harness ("a useful
measurement to investigate"), the loop optimised the picture for twelve rounds
and both artifacts came out unable to stand `[ref: twelve-rounds]`.

> **A constraint is a wall or it is not a constraint.** A line in a harness
> that no tool checks is a prediction about what you will notice, and the
> prediction is wrong. An uncalibrated proxy is a wall at a conservative
> value, not a note. If you catch yourself arguing that a wall violation
> "reads better," that is the failure mode arriving.

### 3b. Answer the questionnaire

| Parameter | Question |
|---|---|
| **Presentation** | What does the critic actually see — the artifact or a rendering? Which views, sections, states? What does the medium hide? |
| **Leak channels** | Every path by which intent reaches the critic — title, caption, filename, path, metadata, comments, commit message, the brief. **Each guard executable**, and the strip recipe written down. |
| **Read type** | Identity (the subject has a name), function (invented, no reference), or fidelity (built from a reference — informed from the first question, no blind stage). And the exact stage-1 wording, never naming the category. |
| **Ground truth** | What tests, measurements or walls exist. The critic's remarks on these are re-filed as legibility notes. |
| **Rubric source** | The subject. Never the reference, the prompt, or the brief — a rubric from the brief scores prompt-adherence and returns a high number carrying no information. |
| **Second scale** | A desirability line, if it matters — separate scale, never a re-weighting, reference scored on it every round as the ceiling. A line added mid-run is always a new scale `[ref: cool]`. |

The three read types, by example: **identity** — *"what is this a model of?"*,
the A-10; **function** — *"what is this, and what is it for?"*, an invented
structure or this document; **fidelity** — reference beside the build, informed
from the first question, the outposts built from concept images.

**Starting points, by class.** `reference.md` Part 1 holds the harness each
class has run with. Which rows to trust:

| Class | Status | Starting point |
|---|---|---|
| Rendered model / image | **n=15 rounds, three subjects** | `reference.md` — the image harness |
| Prose (doc, spec, README) | **n=1 round** | `reference.md` — the prose harness |
| Code, UI, schema | **UNTESTED** — hypotheses written before any run | `reference.md` — the untested rows; the first run rewrites the row |

### 3c. Write §0 and propose it

The proposal is a dated document, unedited after round 1 except for factual
error in the open, in this shape:

```
# §0 — <artifact>, pre-committed <date>
## Rubric — <name>/100          five to seven lines, weights, written from the subject
## Second scale — <name>/20     if any; reference scored as ceiling
## Gate                         a falsifiable claim by a stranger — never a score, never "looks good"
## Budget                       N rounds; what happens when they run out
## Walls                        each with HOW it is checked, and when (inner loop / v1 before round 1)
## Read type + blind question   and the strip recipe for the blind copy
## Deliberate deviations        what the artifact will knowingly not match, decided now
```

On the budget line, price it in real units so the human is approving a cost:
a round of two blind + two informed reads was ~80k tokens a critic and two
minutes wall-clock on prose. Runs so far spent 3 of 5, 5 of 5, 7 of 7, 1 of 1.

**A filled one, compressed** — the Refinery's, from the image record, two lines
a heading:

```
# §0 — Refinery, pre-committed 2026-09-11, after inspecting the reference, before any placement
## Rubric — fidelity/100   Tank cluster 25 · Tapered truss frame 20 · Hoppers and base works 15 ·
                           Service annex 10 · Proportions 15 · Colour and detail 15
## Second scale — cool/20  Would a stranger want this in their outpost, shown it alone; the
                           reference scored on it too, as the ceiling
## Gate                    The critic says STOP: side by side, a stranger would say the build is
                           of that picture, and nothing on the deficiency list is priced above marginal
## Budget                  7 rounds; a read that loses its measurement is re-run and is not a round;
                           stop at 7, at the gate, or when stuck — a documented stop is a deliverable
## Walls                   overlap 0, floating 0, pieces 1 (author tool); no wide mass on a narrow
                           neck, no unsupported cantilever  <- prose; this is the list that failed
## Read type               Fidelity — reference and build side by side, informed from the first question
## Deviations              Hazard stripes → plain bands (no printed parts); X-bracing → posts and rails
                           (no diagonal in the part table); bands as rings per tank, not pipes across
```

**End with: approve to run.** Then wait.

## 4. The protocol

### Round zero — the control arm

Before trusting the instrument, run it on things that are not your work:

- **A known-good exemplar of the target.** Tests whether the critic can reach
  the answer at all — and sets the ceiling. **Calibrate the target against the
  control, never against the scale** `[ref: ceiling-84]`.
- **Something you have already accepted, in the same medium** — skip when the
  exemplar already is your medium.
- **Prove the pipeline is live.** Change something visible, re-export, confirm
  the artifact you are about to send changed `[ref: stale-render]`.
- **Measure version 1 on every wall and downstream instrument** before a round
  is spent on its appearance.

Round zero tends to find a bug in the rubric — which the author could not
find, because the author wrote it.

### A round

**One round = one version judged**, however many critics that takes. A read
that obtained no information — contaminated, truncated, could not open the
file — is not a round and is re-run. Log which.

**Fresh agent, every read.** No source, no brief, no intent, no prior rounds,
no round number. An agent that remembers its last answer defends it.

**Stage 1 and stage 2 are separate agents with no shared context.** A model
reads the whole prompt before its first token; the rubric in the same prompt
as the blind question has already named the target `[ref: one-prompt]`.

**Poll two, in parallel.** Two blind reads for stage 1 — the gate needs two
independent identifications, and the spread comes free. Two informed reads for
stage 2 — not for the score, whose spread is about a point a line on both
media tried, but because a single critic misreads the reference and the
author builds to it `[ref: reference-misread]`.

**Tables first, and cap the length.** A read that returns prose before its
numbers can lose the numbers `[ref: lost-head]`.

**The questions, in this order** (§5's templates carry them):

1. *Blind* — what is this, how confident, which features drove it, **and what
   in what you were given told you rather than the content.**
2. *Informed* — here is the target; score every rubric line and justify each.
3. *Last round's changes, by name* — matched, overshot, or fell short?
4. *Deficiencies* — the N changes that would most improve it, in priority
   order, **in the artifact's own language**, never the implementation's.
5. *Your hardest question, phrased so the answer has a number in it.* A
   deficiency gives direction; a question gets magnitude `[ref: nacelle]`.
6. *Which view or section carries it, and which undermines it.*
7. **Last round only:** *which of these can be taken without another look,
   and which must not be?* The author takes the safe list and nothing else;
   the unsafe list, priced, is the stop's open list `[ref: safe-list]`.

**Ask for bluntness explicitly.** Agents default to soft.

**Check the artifact for its own answer, then make something else check it.**
Look at exactly what you are sending. Then make the guard executable: the blind
copy goes to a content-addressed path in its own directory, and a test asserts
the subject's name cannot reach it `[ref: path-leak]`.

### Reading the result

Sort the critic's list into three bins **before** acting:

1. **Ground truth wins.** A critic's "reads as broken" on a thing your test
   proves connected is a legibility note, not a defect `[ref: solid-body]`.
2. **Claims about the reference — or about facts the author holds — are
   checkable.** Check them. One critic's claim is unconfirmed until a second
   read or your own re-read agrees.
3. **Everything else is the best instrument available.**

Then **price every item against the whole rubric.** Lines trade; the critic
sees one version and cannot see the trade, cannot price an item, and cannot
see what it is *not* failing on `[ref: engines-voids]` `[ref: planform]`.
Filtering is the author's job; its contamination risk is the price.

**Log the per-line vector, never just the total.** A total cannot be
decomposed; a vector showed two regressions the author was calling
improvements `[ref: vector]`.

### Stopping

- **The gate is met.** Two independent strangers, confident, unaided. The gate
  is pass/fail on recognisability and **will close on a mediocre artifact**;
  after it, a further round buys only the per-line reading, bought on §2's
  rule.
- **The budget is spent.** Take the last round's safe list; document the open
  list with the critic's price on each.
- **Plateau at the toolkit's ceiling.** The deficiency list keeps asking for
  what the medium cannot produce and the score walks ±1 `[ref: plateau]`.
  Stop; **the list of what the toolkit is missing is the deliverable.**
- **A wall is discovered late.** Pause. Run a measured pass until the artifact
  is over it. Resume with rounds spent on something that can exist.

**Do not spend the budget to exhaustion.** "Gate met, the remaining faults are
ones I can see myself" is a better stop than a round bought to use the
allowance.

## 5. Prompt templates

Adapt the wording; keep the order — it is §4's question list. Never include
the subject's name, the brief, or the rubric in a blind prompt.

**Blind read (stage 1, its own agent):**

```
Read the <document / image / diff> at <path> and nothing else. You have no
other context and will be given none. Do not open any other file.

Answer, in this order, briefly:
1. What is this [for]? (If you cannot tell, say so — that is a valid answer.)
2. [Who is it for?] [What would you do first, having seen it?]
3. How confident: certain / confident / probable / guess.
4. Which three features drove your answer.
5. Was there any title, label, filename, path, metadata or line in what you
   were given that told you the answer rather than the content? Quote it, or
   say "none".
[6. Would you want this, shown it alone? /20, one sentence.]

Be blunt. Do not soften.
```

**Informed / fidelity read (stage 2, a different agent):**

```
You are judging <artifact at path> [against the reference at <path>].
Read it in full; open nothing else. Target: <one line>.

Answer in this order. Tables first. Total under <N> words.

1. Score every line of this rubric, one sentence of justification each.
   Score what a reader/viewer could DO or SEE — not whether a part exists.
   <rubric table, weights>
   [Also score the reference on line <k> — it is that line's ceiling.]
2. Last round's changes — for each: matched, overshot, or short, and by
   how much: <list, by name>
3. The <N> changes that would most improve it, in priority order, in the
   artifact's own terms, not the implementation's.
4. <Your hardest question, phrased for a numeric answer.>
5. Which section/view carries it; which undermines it.
[6. Last round only: which of your items can be taken without another look,
    and which must not be? Say why for each.]

Be blunt. Do not soften. Where you claim something about the reference or
the text, say where you are looking.
```

**Round log** — one file per round (`rounds/01-round-1.md` here is a filled
one):

```
# Critic round N — <version>
Date. Critic(s): fresh <model>, <read type>. Author. Budget: N of M. §0: <where>.
## 0. What was judged        <- paths + content hashes; walls run; leak check
## 1. Stage 1                 <- both blind reads, side by side; gate verdict
## 2. The vector              <- R1 … RN columns, spread, critics' reasons per line
## 3. Deficiencies, merged    <- with each critic's safe / not-safe ruling
## 4. Reading it              <- the three bins; pricing against the rubric
## 5. Author's response       <- taken, declined, deviations in the open
```

## 6. Failure modes

The canonical table. `n` is how many times it has been seen; a dash is a rule
that has not yet been caught failing.

| Failure | Symptom | Guard | n |
|---|---|---|---|
| Artifact self-labels | Critic names the subject suspiciously fast, or quotes text it saw | Strip captions, filenames, metadata; ask the critic what told it | 1 |
| Self-labels through its **path** | Critic mentions the filename | Content-address the blind copy; assert it in a **test** — prose did not hold | 1 |
| Category in the question | Critic finds an instance of the category you named | "What is this?" | — |
| Both stages in one prompt | Stage 1 lands suspiciously on-target | Separate agents, no shared context | 1 |
| Critic's memory | Critic defends its previous answer | Fresh agent per read, no history | — |
| Round spent on a known defect | Critic returns the author's own verdict | Inner loop until you stop finding things | 1 |
| Target set against the scale | A good result reads as failure | Round zero sets the ceiling | 1 |
| Rubric tuned after the fact | Score rises, artifact does not | Pre-commit; correct factual error only, in the open | — |
| Critic asserts beyond its senses | A structural claim your tests disprove | Ground truth wins; re-file as legibility | 1 |
| Fixed item costs points elsewhere | Score falls while the artifact plainly improved | Price against the whole rubric; log per line | 2 |
| Overshooting a deficiency | Next round faults the same feature from the other side | Ask for the magnitude, not the direction | 2 |
| Judging a stale render | The picture does not change when the artifact does | Export deletes its outputs first; prove live in round zero | 1 |
| **Prose constraint** | Every version passes the harness; the thing it named arrives anyway | A constraint is a wall or it is not one; measure v1 before round 1 | **2** |
| **Gradient runs against a wall the critic can't see** | Each round more recognisable and less viable; every round reports improvement | Sort it into the walls at harness design (§3a) | **2** |
| Blind read on a fidelity subject | Critic reports whether the build declares itself; nobody asked | Match the read type to the question | 2 |
| **Critic misreads the reference** | Next round reverses last round's reference claim; author built to both | Two informed reads; a reference claim is unconfirmed until a second agrees | 2 |
| Read loses its head | Numbers never arrive; transcript empty | Tables first, length cap; a lost read is re-run, not a round | 1 |
| Toolkit ceiling | Same deficiency every round for a feature the medium can't make; score walks ±1 | Stop; the gap list is the deliverable | 1 |
| Prose guard over the skill's own hypotheses | Untested rows formatted like measured ones, warning *above* the table | The marker goes in the row | 1 |
| Function gate saturates on prose | Any document that states its purpose passes "what is this for" | The gate's teeth are "what would you do first" | 1 |
| Furniture read as the artifact | "Loose parts", "not fully assembled" | Anything in frame that isn't the subject must read as an instrument | 1 |
| Medium hides the artifact | Critic can judge silhouette only, and says so | Contrast against the ground; check the reference isn't presented better than your work | 1 |
| Cherry-picked sample | Every version scores well, no round teaches anything | Write your own verdict on the chosen sample *before* the round | 0 |
| Rubric scored against the generating prompt | High scores, no information | Rubric from the subject | held, 2 |
| Invented subject, no right answer | Gate slides to "does it look good" | Gate on function | 1 |

## 7. Where the writing goes

- **§0** → wherever the project keeps state for the artifact, dated.
- **Round logs** → one file per round, next to §0, with content hashes.
- **The stop** → the project's chronicle, with the open list and the toolkit's
  gaps priced; sweep the queue in the same commit.
- **Terms the run coins** → the project's glossary, as they resolve.

On a DEVLOG / TASKS / CONTEXT.md project: §0 of the build doc,
`docs/reviews/<subject>-round-N.md`, the DEVLOG entry plus the TASKS card,
`CONTEXT.md`. No workflow docs? One file next to the artifact. The discipline
is the point; the filing is the bonus.

## 8. In Claude Code — what the prose runs did (n=2 rounds)

What was done, not what must be; a run on another medium may find otherwise.

- Each critic was one `Agent` call, `general-purpose`, fresh — never a
  `SendMessage` to a previous critic. Blind reads were dispatched back-to-back
  in the background so they ran in parallel and could not see each other;
  informed reads likewise, as separate calls.
- The same model served the control and the reads, so the round-zero ceiling
  was comparable.
- The blind copy was produced by a script (strip the label channels), hashed,
  and written to `<session scratchpad>/<sha1>/doc.md`; the parent path was
  checked not to name the subject.
- Walls ran by script before each round. The one that could not run was
  recorded as a gap, not waived.
- Cost was ~80–95k tokens a critic, under two and a half minutes wall-clock for
  a round.

## Anti-patterns

The failure table is canonical; these are the behaviours that produce its rows.

- **Running before the harness is approved.** The rubric is what every round
  optimises toward. It is the human's to ratify.
- **Leaving "practicality" in the rubric.** If the critic cannot see it, it is
  a wall. Sort at harness design, not after round twelve.
- **Sending early to "see what it says."** A round on a question you can
  already answer. Round zero is where calibration is free.
- **Chasing the total.** It is not a gradient. Log the vector.
- **Executing the deficiency list.** Price each item against the whole rubric;
  the critic cannot see the trade.
- **Treating "gate met" as "good."** Different states. It was never a quality
  bar.
- **Writing confident rules for a medium you have not run.** A rule from zero
  observations reads exactly like a tested one. Mark the n — *in the row*, not
  in a warning above the table; the first draft of this skill did the latter
  and both critics named it as the section that undermined the document
  `[ref: own-table]`.

---

Brad's design. Evidence and stories: [reference.md](reference.md);
`Shapey_McShapeface/docs/CRITIC_LOOP.md` v3 and its `docs/reviews/` are the
primary record.
