# critic-loop — reference

The evidence behind [SKILL.md](SKILL.md). Two parts: **the harnesses that have run**
(starting points for §3, with what each run taught), and **the stories** each `[ref: key]`
in the skill points at. Primary record: `Shapey_McShapeface/docs/CRITIC_LOOP.md` v3 and
`docs/reviews/` there; `rounds/` here for the prose run.

The sibling loop — a **measured pass**, the same skeleton with an instrument where the
critic would be — is described in `CRITIC_LOOP.md` v3 §1. Not a skill yet.

---

## Part 1 — Harnesses that have run

### Rendered model / image — n=15 rounds, three subjects

**Subjects.** An A-10 LEGO model (blind identity, 3 rounds of 5, gate met at round 2). Two
LEGO structures built from image-model reference pictures — CargoDepot (fidelity, 5 of 5,
54 → 71) and a Refinery (fidelity, 7 of 7, 49 → 59).

| Parameter | What the harness was |
|---|---|
| Presentation | Four-view contact sheet plus a presentation render; a rear three-quarter added after every round asked for it |
| Leak channels | Caption band (found round 1 — stripped); **output path** (found round 2 — the tool wrote the design's name into its own path; now content-addressed into its own directory with a test); EXIF, legend, watermark listed |
| Read type | A-10: blind identity, *"what is this a model of?"* Outposts: **fidelity** — critic sees reference and build side by side, informed from the first question, no blind stage (Brad's ruling 2026-09-10) |
| Ground truth | Overlap 0, floating 0, one connected piece — walls in the author tool |
| Walls | The three above, plus — from round thirteen on — joints-per-brick ≥ 2.2 at author time, and a downstream physics sweep taken on version 1. **Before that, the harness had "no wide mass on a narrow neck, no unsupported cantilever" as prose, and bond density as "a measurement to investigate."** See `[ref: twelve-rounds]` |
| Rubric source | The subject (the aircraft; the structure's function), written before the reference was opened |
| Second scale | `cool/20`, added before CargoDepot round 4 on Brad's instruction, reference scored as ceiling (18/20) |

**What the fifteen rounds taught, in order of cost:** the prose constraint list failed and
the bond-density wall replaced it (twelve rounds); a single informed critic misreads the
reference (two rounds); rounds plateau at the toolkit's ceiling and the critic names it
(three rounds of ±1 around 58); the last round's critic can rule which items are safe to
take unreviewed (one protocol, followed exactly); a read that runs long loses its head (one
re-run).

### Prose — n=1 round, one subject

**Subject.** This skill's own first draft, judged by its own protocol (`rounds/00-precommit.md`,
`rounds/01-round-1.md`).

| Parameter | What the harness was |
|---|---|
| Presentation | The text, as a reader gets it |
| Leak channels | Frontmatter (its `description` is the answer verbatim), H1, filename, Credit section — all stripped by script to a content-hashed path. **Stripped cleanly; neither blind critic reported a leak.** But both cited the body's own self-references ("Explicit `/critic-loop`") as their driver — *a document's own vocabulary is the artifact and cannot be stripped* |
| Read type | Blind function: *what is this for, who is it for, what would you do first?* |
| Ground truth | Frontmatter validity by script. The trigger eval was the wall that could not run — recorded as a gap |
| Rubric source | What a reader must be able to *do* after reading (six lines) |
| Second scale | `want/20` — would a developer install it, shown it alone; exemplar (`grill`) scored 16 as ceiling |

**What the round taught.** Round zero on a shipped sibling skill: function, audience, first
action all correct, confident — **the function question saturates on prose.** A document
that states its purpose passes "what is this for" by construction; the gate's teeth are
"what would you do first," and both critics answered "the pre-commit," not "send it to
critics." Gate met 2/2 on round 1. Vector 92/96 with spread ≤ 1 a line — the image noise
figure holds. `want` 15/17 blind, 16/14 informed, around the ceiling of 16; both informed
reads independently named the draft's per-class table as the section that undermined it —
untested rows formatted like the measured one, with a warning *above* the table. A prose
guard, in the document that says prose guards do not hold. Four critics, ~80k tokens each,
under two minutes.

### Untested classes — hypotheses, written before any run

**A run in one of these rewrites its row from what happened.** Until then these are
starting points, not guidance.

| Class | Presentation | Leak channels (expected) | Blind question | Ground truth / walls |
|---|---|---|---|---|
| **Code** (module, API surface, PR) — UNTESTED | The diff or file without its PR description | PR title/body, commit message, branch name, issue link, intent-stating docstrings. Identifiers are *part of the artifact* | "What does this do, and what would you expect calling it to do?" — the gap is the finding | Tests, types, lint |
| **UI** (screen, flow) — UNTESTED | Screenshot or live page, one state at a time | Page title, route, placeholder copy, the ticket | "What is this screen for, what would you click first, what happens?" | Accessibility, load time, validation |
| **Schema / data model** — UNTESTED | The schema alone, no migration notes | Field comments, migration name, the PR | "What does this store, what would you query, what can't you express?" | Constraints, migrations, integrity |

---

## Part 2 — The stories, by key

Each is the observation that earned the rule it is cited from. Dates are 2026.

**`twelve-rounds`** — *§3a, the sort; §1 contamination; "Not the right tool for".* Two
outpost structures were iterated to 71 and 59 fidelity over twelve rounds on a harness
whose constraint list said *no wide mass on a narrow neck, no unsupported cantilever, walls
clean, courses interlock.* Every version passed every line. Rubric line 6 rewarded detail
density; every round asked for smaller bricks on smaller joints. Measured at the end: both
hold an eighth and a quarter of their own weight — weaker than all six structures they
replaced. The list guarded shape; the failure was joint strength; and joints-per-brick was
*in the file before round 1* — rho = +0.912 against six measured margins — filed in the
harness as "a useful measurement to investigate, not a calibrated threshold." The loop ran
over the note. The wall that replaced it (2.2 joints/brick at author time) would have
rejected both before round 1. (09-11; DEVLOG fifty-sixth, fifty-eighth.)

**`path-leak`** — *§1; §4 "check the artifact for its own answer"; §6 rows 1–2.* Round 1 of
the A-10: the rendering tool stamped the design's name and one-line brief across every
contact sheet — five critics would have "identified" an A-10 off the author's caption. Fixed
by cropping the caption band. The doc then *listed* "a filename" as a leak channel, and the
tool written to serve that list wrote the design's name into its default output path:
`designs/out/a10/a10.blind.png`. The critic identified the aircraft and volunteered that the
path had told it. Two reads void. Now: content-addressed directory, and a test asserts the
subject's name cannot reach the path. (09-08.)

**`own-table`** — *§1; §6.* The first draft of this skill formatted four untested
per-class rows identically to the one measured row, with a bold "these are hypotheses"
above the table. Both informed critics, independently, named it as the section that
undermined the document — "exactly the failure the document itself names." The marker now
goes in the row. (09-11; `rounds/01-round-1.md`.)

**`reference-misread`** — *§1 spend; §4 "poll two"; §6.* Refinery rounds 2/3 and 5/6 each
contradicted the other about the reference image itself: round 2 read a braced member at
0.6 height and domes a diameter above the ring, round 3 read no member and domes under the
deck (round 3 was right, on re-reading the image); round 5 said push the feet out, round 6
said too squat (settled by measuring against the tanks). The author built to each before the
next critic reversed it. Each misread cost the whole round; two informed reads would have
saved rounds 2 and 6 of seven. Meanwhile the *score* spread between consecutive critics on
near-identical versions was about a point a line — not where a second read earns its cost.
(09-11; DEVLOG fifty-third.)

**`known-defect`** — *§2.* The author wrote *"the side and front views read as a flat grey
pancake — the fuselage is a featureless box, the nacelles are too small"* and dispatched a
critic round anyway. The critic came back and said the fuselage had no vertical volume and
the nacelles were too small. One round of five, spent to be told what was already written
down. (09-08, A-10 round 1.)

**`cool`** — *§3b second scale.* Before CargoDepot round 4, Brad: "having it look cool
should also be something that can be graded and improved." Added as `cool/20` beside
`fidelity/100`, not as a seventh fidelity line, so rounds 1–3 stayed comparable with 4–5; the
critic scores the reference on it too (18/20), as the ceiling. (09-10.)

**`ceiling-84`** — *§4 round zero.* The A-10's known-good exemplar scored 84/100 on the
rubric. Without that number, a later version in the seventies reads as failure when it is
close to what a good example achieves. Round zero also caught a factual error in the rubric
(the wing is low-mounted; the engines sit high) — which the author could not have found,
having written it. (09-08.)

**`stale-render`** — *§4 round zero.* A rendering bug let the tooling report success while
re-serving the *previous* model's images under a caption naming the current one — for
twenty minutes, across two design judgements. Had it started one command earlier, a round
would have judged the wrong version and nothing inside the loop could have revealed it. Now
the export step deletes its outputs before it runs. (09-08.)

**`one-prompt`** — *§4 "separate agents".* Version 0 of the method said one agent could do
all four stages, "the uncontaminated answer is already on the record." True of a person
turning a page; false of a language model, which has the whole prompt — rubric included —
in context before it emits its first token. Stage 1 had been shown the target's name before
answering "what is this?" (09-08, round 2.)

**`lost-head`** — *§4 "tables first".* CargoDepot round 5: one informed read did ~134k
tokens of work and delivered its conclusion truncated at the head — the two score tables,
the changes-judged table and the deficiency list never arrived; the transcript file was
empty afterwards. Re-run with the tables first and the answer capped at 900 words; every
Refinery round was prompted that way and none was lost. (09-10.)

**`nacelle`** — *§4 question 5.* Round 1 told the A-10's author "stand the engines clear of
the body"; two versions overcorrected. Round 3 was asked *"too high, about right, or too
low, and what should the gap look like?"* and answered *"too high by roughly a full nacelle
diameter; the visible daylight should be a quarter to a third of a diameter"* — directly
buildable. A deficiency gives direction; a question gets magnitude. (09-08.)

**`safe-list`** — *§4 question 7; stopping.* Refinery round 7, budget exhausted, was asked
which items could be taken without another look. It sorted: three banding and lamp items
safe; "do NOT touch without a look: base-zone infill, leg geometry, foot height, annex,
hopper." V11 took exactly the safe list; the unsafe list, priced, is the build doc's open
list. The prose run's critics did the same, both refusing a "worked trace" for the same
reason — fabrication risk on a document whose credibility is its n's. (09-11.)

**`solid-body`** — *§4 reading, bin 1.* The A-10's critic scored "reads as one solid
aircraft" 2/5, citing gaps breaking the body — on a model with zero floating parts and one
connected component, verified by a geometric wall. It was judging an appearance of
brokenness from an edge-on view: legitimate for a line phrased "reads as," not evidence of a
structural defect. (09-08.)

**`engines-voids`** — *§4 pricing.* Round 1 said the engines must stand clear of the body.
Version 2 stood them clear on pylons — and round 2 scored "reads as one solid aircraft" 1/5
for the voids that clearance had opened. Neither critic was wrong; rubric lines trade, and a
deficiency list cannot see the trade because each round sees one version. (09-08.)

**`planform`** — *§4 pricing.* The largest defect in the A-10's version 1 was its planform.
Round 2's critic never named it — it had already used the planform to make its
identification. A critic reports what it can see failing; it cannot see what it is not
failing on. (09-08.)

**`vector`** — *§4 "log the vector".* Round 1 logged only "64/100." Round 2 came back 62 on a
version that had plainly improved — and nothing could be decomposed. Round 3, scored per
line, showed a 62 → 58 fall landing exactly on the two components the author had changed on
round 2's advice and overshot: two regressions he would have gone on calling improvements.
(09-08.)

**`plateau`** — *§4 stopping.* The Refinery's seven rounds: 49 → 49 → 52 → 57 → 59 → 57 →
59. From round 4 the critic said the same thing each round: line 2 caps near 11/20 without a
diagonal member, and the 24-orientation part table has none. The last three rounds bought a
point a line of noise around a ceiling the medium set. The stop's deliverable was a
fifteen-part catalogue ask, priced per rubric line. (09-11.)
