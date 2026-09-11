---
name: critic-loop
description: Iterate an artifact whose quality has no test — only a perceiver — against fresh, blind critic agents. Pre-commits a rubric, gate, budget and executable walls; runs a free inner loop and rationed critic rounds; logs a per-line vector, not a score; treats a documented stop as a deliverable. Triggers include "does this read as X", "would a stranger get this", "am I too close to this", "fresh eyes", "critic round", "review loop", "iterate with a reviewer", "is this recognisable / persuasive / clear / obvious what it's for". Explicit invocation via /critic-loop. Not for qualities that have a test — use the test.
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
into changes.** Everything below exists to keep that agent actually fresh, to
keep the signal it returns actually a gradient, and to keep the rounds — which
are the scarce thing — spent on questions the author cannot answer alone.

**Provenance and evidence.** Brad's design, run in `Shapey_McShapeface` on
three visual subjects over fifteen rounds (an A-10 model, two LEGO structures
built from reference images). `docs/CRITIC_LOOP.md` v3 in that repo is the
evidence record — every rule there carries the round that earned it or the
`n=0` that says it has not. **This skill is n=15 on images and n=0 on
everything else.** §4 marks which is which; the first run off images is
expected to correct that table, not confirm it.

## When to invoke

Explicit `/critic-loop`, when an artifact's remaining faults are ones the
author can no longer see. Signs: you have looked at it enough times that it
looks fine; you are about to ask someone "does this look like X?"; you are
arguing with yourself about a proportion, a paragraph, a layout, and cannot
settle it by looking again.

Do **not** auto-fire on "review this" — a code review has a test-shaped answer
and its own tools.

## Not the right tool for

- **Anything with a test.** Compile, lint, unit tests, a measurement, a wall.
  The critic will assert things about these that the test disproves (§7).
- **A quality the deliverable has but the critic cannot perceive.** A structure
  that must stand, a page that must load in 200 ms, a function that must be
  constant-time. The critic judges the *picture* of the artifact; a quality it
  cannot see gets optimised away while every round reports improvement. That
  quality needs a **wall** — see §3 — or the loop will run over it. This was
  measured: twelve rounds, two structures, both weaker than everything they
  replaced, every round scored as progress.

**The sibling loop.** When the quality *does* have a test, the critic is the
wrong instrument but the iteration discipline is not. A **measured pass** runs
the same skeleton — pre-commit the question, change one variable per version,
measure by the verdict rather than the proxy, log the vector, treat a
documented stop as a deliverable — with the instrument where the critic would
be. Same protocol, perceiver swapped out. This skill does not describe it
further.

## 1. The three things every rule guards

Every rule in this skill protects one of three properties. Knowing which lets
you reason about a medium the skill has never seen.

1. **Contamination — is the perceiver actually independent?** The author's
   intent reaches the critic through channels the author does not notice: a
   caption, a filename, the category named in the question, the rubric in the
   same prompt as the blind question, the critic's memory of its last answer,
   the brief the artifact was generated from. A contaminated read returns a
   confident answer that measured nothing, and **nothing inside the loop can
   reveal it.** Guards for this must be executable, not prose; a prose guard was
   tested and did not hold (§8).
2. **Gradient validity — is the signal the goal?** A scalar score is not a
   gradient (it fell twice on versions that had plainly improved). Recognition
   saturates. Rubric lines trade against each other. A deficiency gives
   direction, not magnitude, so the author overshoots. The critic's read of a
   *reference* is a claim about the world and can be wrong. And the loop's
   gradient can run directly against a hard constraint the critic cannot
   perceive. What survives: the **per-line vector**, a **falsifiable gate**,
   and **walls** the inner loop runs.
3. **Spend discipline — is a round bought for a question only a stranger can
   answer?** Rounds are rationed to stop the author outsourcing judgement.
   A round spent on a defect the author has already written down is wasted; a
   round spent past the toolkit's ceiling measures the critic, not the artifact;
   a budget spent to exhaustion is a number, not a plan.

## 2. The two loops

```
OUTER: critic round        <- expensive, budgeted, each one a real judgement
  INNER: author iterates   <- cheap, unbudgeted, run until you stop finding things
```

**The inner loop is free.** Build, look, judge, fix, look again. The walls (§3)
run here, on every version, before anything is sent.

**The outer loop is rationed.** Send to the critic only when your honest answer
to "what is wrong with this?" is *"I have stopped being able to tell."* If your
own verdict names a defect, that defect is inner-loop work. "I'll send it early
to see what the critic says" is a round spent on a question you can already
answer — calibrate in round zero instead, where it is free.

**The inner loop has a blind spot exactly where the last round's advice was
applied.** Acting on a critic's list adds a second intention to read back in:
you look at the change through the note, see "I made it not-a-staircase," and
tick it off. Two guards: judge a changed feature against the *subject*, not
against the note; and name last round's changes at the top of the next round's
questions, so a stranger checks your compliance — you cannot.

## 3. Pre-commit, before anything is built

Four things, fixed in writing before round 1, because each is something the
author will otherwise tune to whatever they happened to achieve. On a workflow
project they go in the build/state doc as **§0**, dated, and are not edited
after round 1 except for factual error, in the open.

**The rubric.** The recognisable features of the target, weighted by how much
each carries. **Written from the subject, never from the reference material or
the prompt that generated the artifact** — a rubric written from the brief
scores prompt-adherence and returns a high number carrying no information.
Five to seven lines; every line scored every round.

**The gate.** What ends the loop. A falsifiable claim by a stranger, never a
score and never "does it look good." Three forms, by subject (§5): a *named*
subject gates on identity; an *invented* one on function; an artifact built
*from a reference* on fidelity.

**The budget.** How many rounds, and what happens when they run out. A
documented failure with the toolkit's gaps priced is a legitimate deliverable —
often more useful than a pass.

**The walls.** Everything the artifact must satisfy that **the critic cannot
perceive and will not weigh.** The rule, measured at a cost of twelve rounds:

> **A constraint is a wall or it is not a constraint.** If the inner loop can
> compute it, the inner loop computes it and rejects. A line in a pre-commit
> that no tool checks is a prediction about what you will notice, and the
> prediction is wrong. If it can only be measured downstream, **measure
> version 1 before round 1** and re-measure whenever the structure changes —
> not at the end. An uncalibrated proxy is a wall at a conservative value,
> not a note that says "investigate"; the loop will run over a note.

If you catch yourself arguing that a wall violation "reads better," that is
the failure mode arriving, not an exception to it. The point of pre-committing
is that this argument is persuasive at the moment it is wrong.

**A second scale, if the rubric cannot say it.** Fidelity asks whether the
artifact is *the* thing; desirability asks whether anyone would *want* it. If
both matter, the second is a separate scale (`cool/20` beside `fidelity/100`),
never a re-weighting of the first, so earlier rounds stay comparable — and a
subjective line is scored on the reference or exemplar every round, as its
ceiling. A line added mid-run is always a new scale.

## 4. Parameterise the subject

Fill this table before round zero. It is the whole difference between media;
the protocol in §5–§7 does not change.

| Parameter | What it means | Question to answer |
|---|---|---|
| **Presentation** | What the critic actually sees | Is it the artifact, or a rendering of it? Which views / sections / states? What does the medium hide? |
| **Leak channels** | Every path by which intent reaches the critic | Title, caption, filename, path, metadata, comments, commit message, branch name, the brief, identifiers visible in a screenshot. **Each guard executable.** |
| **Read type + blind question** | Identity / function / fidelity, and the exact stage-1 wording | Never names the category. "What is this?" not "what aircraft is this?" |
| **Ground truth** | What tests, measurements or walls exist | The critic's remarks on these are re-filed as legibility notes (§7) |
| **Walls** | Qualities the critic cannot perceive, as executable checks | Run in the inner loop; version 1 measured before round 1 |
| **Rubric source** | Where the rubric's lines come from | The subject. Not the reference, not the prompt, not the brief. |
| **Second scale** | A desirability line, if it matters | Separate scale, reference scored as ceiling |

**Per-class instances.** The image row is measured; every other row is a
hypothesis written before any run and marked so. **The first run in a new
class should rewrite its row from what happened.**

| Class | n | Presentation | Leak channels found / expected | Blind question | Ground truth / walls |
|---|---|---|---|---|---|
| **Rendered model / image** | **15 rounds** | Multi-view contact sheet; add the view critics keep asking for (rear three-quarter) | Caption band (found), **output path** (found — prose guard failed; content-addressed dir + a test), EXIF, legend, watermark | Identity: "what is this a model of, how confident, which features drove it?" Fidelity: reference beside build, no blind stage | Overlap, floating, connectivity, joints-per-brick wall; downstream physics sweep |
| **Prose** (doc, spec, memo, README) | **0** | The text, as the reader gets it | Title, filename, author line, headers that name the audience, any pasted brief, self-reference ("this skill…") | Function: "what is this for, who is it for, what would you do after reading it?" | Word count, link check, spell/lint; "does the reader's next action match the author's intent" is *not* a test — it is the gate |
| **Code** (module, API surface, PR) | **0** | The diff or the file, without its PR description | PR title/body, commit message, branch name, issue link, docstrings that state intent rather than behaviour | Function: "what does this do, and what would you expect calling it to do?" — the gap between the two is the finding | Tests, types, lint. Identifiers are *part of the artifact*, not a leak — the question is whether they carry the meaning |
| **UI** (screen, flow) | **0** | Screenshot or live page, one state at a time | Page title, route/URL, placeholder copy, the ticket | Task: "what is this screen for, what would you click first, what do you expect to happen?" | Accessibility checks, load time, the form's validation |
| **Schema / data model** | **0** | The schema alone, no migration notes | Table/field comments, the migration's name, the PR | Function: "what does this store, what would you query it for, what can't you express?" | Constraints, migrations run, referential integrity |

## 5. The protocol

### Round zero — the control arm

Before trusting the instrument, run it on things that are not your work:

- **A known-good exemplar of the target.** Tests whether the critic can reach
  the answer at all — and sets the ceiling. The A-10 exemplar scored 84/100;
  without that number a version in the seventies reads as failure. **Calibrate
  the target against the control, never against the scale.**
- **Something you have already accepted, in the same medium.** Tests whether
  the critic can perceive *your* medium.
- **Prove the pipeline is live.** Change something visible, re-export, confirm
  the artifact you are about to send actually changed. A stale render was
  re-served under a new caption for twenty minutes once; had a round gone out,
  nothing in the loop could have caught it.
- **Measure version 1 on every wall and every downstream instrument you have**
  before a round is spent on its appearance.

Round zero also tends to find a bug in the rubric — which the author could not
find, because the author wrote it.

### A round

**One round = one version judged**, however many critics that takes. A read
that obtained no information — contaminated, truncated, could not open the
file — is not a round and is re-run. Log which.

**Fresh agent, every read.** No source, no brief, no intent, no prior rounds,
no round number. An agent that remembers its last answer defends it.

**Three read types.** The subject decides (§3, gate):

| Read | Stage 1 | Then |
|---|---|---|
| **Blind identity** — subject has a name | Blind critic(s), *separate agent*: "what is this?" recorded before anything is revealed | Informed critic: rubric, per line |
| **Blind function** — invented, no reference *(n=0)* | Blind: "what is this, and what is it for?" | Informed critic: rubric, per line |
| **Fidelity** — built from a reference | **None.** Informed from the first question, reference beside artifact | Same critic continues |

Blinding measures whether the artifact declares itself. When the question is
"is this a faithful build of that," a blind read spends a critic answering
something nobody asked.

**Stage 1 and stage 2 are separate agents with no shared context.** A model
reads the whole prompt before its first token; the rubric in the same prompt
as the blind question has already named the target.

**Poll two, in parallel.** Two blind reads for stage 1 (the gate needs two
independent identifications; this also measures inter-rater spread for free).
Two informed reads for stage 2 — not for the score, whose spread is about a
point a line, but because **a single critic misreads the reference**, and each
misread cost a whole round when the author built to it.

**Tables first, and cap the length.** A read that returns prose before its
numbers can lose the numbers — one did, ~134k tokens of work, the score tables
never arrived. Scores first, then the deficiency list, then the argument;
answer capped.

**Stage the questions:**

1. *Blind* — what is this, how confident, which features drove it.
2. *Informed* — here is the target; score every rubric line and justify each.
3. *Last round's changes, by name* — matched, overshot, or fell short?
4. *Deficiencies* — the N changes that would most improve it, in priority
   order, **in the artifact's own language** ("the engines need twice the
   diameter"), never the implementation's ("change line 40").
5. *Your hardest question, phrased so the answer has a number in it.* A
   deficiency gives direction; a question gets magnitude. "Too high by roughly
   a full nacelle diameter; daylight should be a quarter to a third of one"
   was buildable where "stand the engines clear" produced two overcorrections.
6. *Which view or section carries it, and which undermines it.*
7. **On the last round only:** *which of these can be taken without another
   look, and which must not be?* The author takes the safe list and nothing
   else; the unsafe list, priced, is the stop's open list.

**Ask for bluntness explicitly.** Agents default to soft, and a soft review is
worthless.

**Check the artifact for its own answer, then make something else check it.**
Look at exactly what you are sending, with your own eyes, and confirm the
answer is not in it. Then make the guard executable — the blind copy goes to a
content-addressed path in its own directory and a test asserts the subject's
name cannot reach it. Looking is not repeatable; the prose version of this
rule was written, and the tool built to serve it wrote the subject's name into
its own output path anyway.

### Reading the result

Sort the critic's list into three bins **before** acting:

1. **Ground truth wins.** The critic scored "reads as one solid body" 2/5 on a
   model that was provably one connected component. Legitimate for a line
   phrased "reads as"; not evidence of a structural defect. Re-file as a
   legibility note.
2. **Claims about the reference are checkable.** "The domes stop under the
   deck" is a statement about a picture and is right or wrong. Check it against
   the reference yourself; treat one critic's claim as unconfirmed until a
   second read or your own re-read agrees.
3. **Everything else is the best instrument available.**

Then **price every item against the whole rubric.** Lines trade: "stand the
engines clear" executed exactly cost 1/5 on "reads as one solid body" for the
voids it opened. The critic cannot see the trade (it sees one version), cannot
price an item, and cannot see what it is *not* failing on — the largest defect
in one version was never named because the critic had used it to make its
identification. Filtering is the author's job, and its contamination risk is
the price.

**Log the per-line vector, never just the total.** One run logged "64/100" and
when the next came back 62 nothing could be decomposed. The vector showed a
later 62 → 58 landing on exactly the two components the author had changed on
advice and overshot — two regressions he was calling improvements.

### Stopping

- **The gate is met.** Two independent strangers, confident, unaided. Note:
  the gate is pass/fail on recognisability and **will close on a mediocre
  artifact.** After it, recognition has saturated; a further round buys only
  the per-line reading and the deficiency list, and is bought on §2's rule.
- **The budget is spent.** Take the last round's safe list; document the open
  list with the critic's price on each.
- **Plateau at the toolkit's ceiling.** When the deficiency list keeps asking
  for what the medium cannot produce and the score walks ±1 around a level,
  the plateau is real. Seven rounds went 49 → 49 → 52 → 57 → 59 → 57 → 59 with
  the critic naming the missing part from round 4. Stop; **the list of what
  the toolkit is missing is the deliverable.**
- **A wall is discovered late.** Pause. Run a measured pass until the artifact
  is over it. Resume with rounds spent on something that can exist.

**Do not spend the budget to exhaustion.** "Gate met, the remaining faults are
ones I can see myself" is a better stop than a fifth round bought to use the
allowance.

## 6. Prompt templates

Adapt the wording; keep the structure. Never include the subject's name, the
brief, or the rubric in a blind prompt.

**Blind read (stage 1, its own agent):**

```
You are looking at <an image / a document / a diff / a screenshot> at <path>.
You have no other context and will be given none.

Answer, in this order, briefly:
1. What is this? (If you cannot tell, say so — that is a valid answer.)
2. How confident are you: certain / confident / probable / guess.
3. Which three features drove your answer.
4. Is there any text, label, filename or metadata in what you were given
   that told you the answer rather than the content itself? Quote it.

Be blunt. Do not soften.
```

**Informed / fidelity read (stage 2, a different agent):**

```
You are judging <artifact at path> [against the reference at <path>].
Target: <one line — what it is meant to be>.

Answer in this order. Tables first. Total under <N> words.

1. Score every line of this rubric, with one sentence of justification each:
   <rubric table, weights>
   [Also score the reference on line <k> — it is that line's ceiling.]
2. Last round's changes — for each, does it now match, overshoot, or fall
   short, and by how much:
   <list, by name>
3. The <N> changes that would most improve it, in priority order, described
   in the artifact's own terms, not the implementation's.
4. <Your hardest question, phrased for a numeric answer.>
5. Which view/section carries it; which undermines it.
[6. Last round only: which of your items can be taken without another look,
    and which must not be?]

Be blunt. Do not soften. Where you make a claim about the reference, say
where in it you are looking.
```

**Round log** (`docs/reviews/<subject>-round-N.md` on a workflow project):

```
# Critic round N — <version>
Date. Critic(s): fresh <model>, <read type>. Author. Budget: N of M.
## 0. What was judged        <- table of paths + content hashes; ground truth
## 1. Per-line vector         <- R1 … RN columns, Δ, critic's reason per line
## 2. Last round's changes    <- matched / overshot / short
## 3. The questions           <- answers, with the numbers
## 4. Author's response       <- what the next version takes, what it declines, why
```

## 7. Failure modes

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
| **Prose constraint** | Every version passes the pre-commit; the thing it named arrives anyway | A constraint is a wall or it is not one; measure v1 before round 1 | **2** |
| **Gradient runs against a wall the critic can't see** | Each round more recognisable and less viable; every round reports improvement | Walls in the inner loop; the downstream measurement early | **2** |
| Blind read on a fidelity subject | Critic reports whether the build declares itself; nobody asked | Match the read type to the question | 2 |
| **Critic misreads the reference** | Next round reverses last round's reference claim; author built to both | Two informed reads; a reference claim is unconfirmed until a second agrees | 2 |
| Read loses its head | Numbers never arrive; transcript empty | Tables first, length cap; a lost read is re-run, not a round | 1 |
| Toolkit ceiling | Same deficiency every round for a feature the medium can't make; score walks ±1 | Stop; the gap list is the deliverable | 1 |
| Furniture read as the artifact | "Loose parts", "not fully assembled" | Anything in frame that isn't the subject must read as an instrument | 1 |
| Medium hides the artifact | Critic can judge silhouette only, and says so | Contrast against the ground; check the reference isn't presented better than your work | 1 |
| Cherry-picked sample | Every version scores well, no round teaches anything | Write your own verdict on the chosen sample *before* the round | 0 |
| Rubric scored against the generating prompt | High scores, no information | Rubric from the subject | held, 2 |
| Invented subject, no right answer | Gate slides to "does it look good" | Gate on function | 0 |

## 8. On a workflow project

- Pre-commit → the build/state doc, **§0**, dated, unedited after round 1.
- Round logs → `docs/reviews/<subject>-round-N.md`, one per round, with the
  content hashes of what was judged.
- The stop → the DEVLOG, with the open list and the toolkit's gaps priced.
  Sweep the TASKS card in the same commit.
- Terms the run coins (the gate's name, the second scale, "fidelity read") →
  `CONTEXT.md`, as they resolve.

No workflow docs? Keep §0 and the round logs together in one file next to the
artifact. The discipline is the point; the filing is the bonus.

## 9. In Claude Code

- A critic is an `Agent` call: `general-purpose`, a fresh call per read, never
  `SendMessage` to a previous critic. Run stage-1 blind reads in one block so
  they are parallel and cannot see each other.
- The informed read is a *second* `Agent` call, never a follow-up to the blind
  one.
- For images, the critic needs `Read` on the blind copy's path. Put the blind
  copy in a directory whose name is a content hash; do not pass the design's
  output directory.
- Author and critic need not be the same model. One run had a different model
  author and Claude judge; a different model is a cheaper independence than a
  fresh context. n=1, no claim.

## Anti-patterns

- **Sending early to "see what it says."** That is a round on a question you
  can already answer. Round zero is where calibration is free.
- **A prose guard.** For leaks and for walls both. Looking is not repeatable;
  a note is not a constraint. Both were tested; both failed.
- **Scoring against the brief.** The artifact matches its own prompt by
  construction. Rubric from the subject.
- **Chasing the total.** It is not a gradient. Log the vector.
- **Executing the deficiency list.** Price each item against the whole rubric;
  the critic cannot see the trade.
- **Building to one critic's reference claim.** Check it. It was wrong twice
  in seven rounds and each time cost the round.
- **Spending past the ceiling.** When the list asks for what the medium cannot
  do, the remaining rounds measure the critic.
- **Treating "gate met" as "good."** Different states. The gate was never a
  quality bar.
- **Writing confident rules for a medium you have not run.** This skill's own
  §4 is half hypothesis and says so. A rule from zero observations reads
  exactly like a tested one. Mark the n.

---

## Credit

Brad's design. The evidence record, with every rule's provenance and the
questions still open, is `Shapey_McShapeface/docs/CRITIC_LOOP.md` (v3,
2026-09-11) and the round logs under `docs/reviews/` and
`docs/A10_CRITIC_EXPERIMENT.md` in that repo.
