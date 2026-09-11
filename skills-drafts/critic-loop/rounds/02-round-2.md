# Critic round 2 — SKILL.md v3 (the rewrite)

**Date:** 2026-09-11 (evening). **Read type:** informed only — the gate was met in round 1
and saturates on prose; a blind stage would measure nothing new. Two fresh `general-purpose`
Sonnet critics in parallel. **Author:** Claude (Opus 5). **Budget: 2 of 1 — deviation, in
the open:** `00-precommit.md` budgeted round zero + one round. Brad ruled the harness-as-
proposal framing, the rounds unit and the split after round 1; v3 is a materially different
artifact (new §0, §3a, §3c; stories out), and he asked for a round on it. One round extended
on that instruction. Same rubric, unedited.

## 0. What was judged

| artifact | sha1 (12) |
|---|---|
| `SKILL.md` v3 at `93312cb` | `5e514fc7f151` |
| `reference.md` at `93312cb` — critics could open it *after* SKILL.md and had to say whether they needed to | `7b952ffe44ce` |

Walls: frontmatter — PASS; every `[ref: key]` resolves — PASS (by script). 427 + 191 lines.

**Last round's changes named in the prompt:** (a) stories → `reference.md`, one clause of
why per rule; (b) §0 with the approval gate; (c) §3a the sort; (d) §3c the proposal
template. **Hardest question:** did you need `reference.md` to act on any rule — and on a
LEGO-from-concept-image invocation, would §0 + §3 stop you before a round is spent?

## 1. The vector, four reads over two rounds

| # | Criterion | Wt | R1 A | R1 B | **R2 A** | **R2 B** | Δ (R1 mean → R2) | Critics' reasons, round 2 |
|---|---|---:|---:|---:|---:|---:|---:|---|
| 1 | When to reach for it | 20 | 18 | 19 | **18** | **18** | −0.5 | Both: "Not the right tool for" + §3a's yes/no sort route a quality to test / wall / rubric on first read |
| 2 | Can set up a run | 20 | 18 | 19 | **19** | **19** | +0.5 | Both: §0 → §3a → §3b → §3c is an ordered recipe ending in a document and "approve to run" |
| 3 | Can run a round | 20 | 19 | 19 | **19** | **19** | 0 | Both: §4 + §5 copy-ready |
| 4 | Can read a result | 15 | 14 | 14 | **14** | **14** | 0 | Both: bins, pricing, vector "stated as actions" |
| 5 | Can stop | 10 | 9 | 10 | **9** | **9** | −0.5 | Both: four stop states; "do not spend to exhaustion" |
| 6 | Trusts it correctly | 15 | 14 | 15 | **12** | **12** | **−2.5** | **Both, same reason:** the untested-class starting points now live only in `reference.md`; `SKILL.md` alone "can flag 'untested,' not rewrite it from a run" (A); "knowing which rows to trust for a new class requires reference.md — §3b only gestures at it" (B) |
| | **Capability** | 100 | 92 | 96 | **91** | **91** | −3 | |
| | `want/20` (ceiling 16) | 20 | 16 | 14 | **16** | **16** | +1 | Both: rigorous, dense; "a tool, not a methodology paper" (A); "reach for it when stuck, not by default" (B) |

**Round 2's inter-rater spread is zero on every line.** Round 1's was ≤ 1. `want` converged
on the ceiling.

**The vector caught what the total would have hidden.** Total 94 → 91 reads as "the rewrite
made it slightly worse." The lines say: line 2 up (the harness sections landed), line 6 down
2.5 (the split moved the per-class rows out, and both critics independently priced that as
the cost). That is the `[ref: vector]` story — a deficiency fixed on advice costing points
on a different line — happening to the document that tells it.

## 2. Last round's changes, judged

| change | A | B |
|---|---|---|
| (a) stories out, one clause left | **Works, one miss.** "Nearly every `[ref:]` clause is independently actionable." Miss: §1 files `path-leak` and `own-table` under one clause though they are different failure classes — contamination vs. mismarked hypothesis; the own-table guard reaches the reader only via §6's row | **Works.** Fifteen refs checked; "the ref supplies corroboration, not the instruction." Cost is a *resource*, not a rule: the concrete precedent (four-view sheet, 2.2 joints/brick, exact stage-1 wording) is only in reference.md — "fine for acting correctly, costly for acting fast" |
| (b) §0 approval gate | **Works cleanly.** "Closes move 1 on an explicit gate" | **Works, cleanly.** "Converts the whole skill from an invitation into a gate" |
| (c) §3a the sort | **Works, strongest addition.** "Operational, not taxonomic" | **Works.** "Closes exactly the failure (`twelve-rounds`) the document exists to prevent" |
| (d) §3c template | **Works, minor gap:** no worked Gate example; the only concrete gate shown is identity-shaped | **Works, minimally:** scaffolding with no worked example; a first-timer pattern-matches from §5's prompts instead |

## 3. The hardest question

**(i) Did you need `reference.md` to act on any rule?** A: *no* — "every `[ref:]` clause
held up against its story… none pointed to a guard the skill body didn't already give."
B: *no* — "every `[ref:]` clause carries its own instruction; I opened it to confirm that."
Both: where it *is* load-bearing is the untested-class starting points (code/UI/schema) —
anyone invoking on those needs it to draft a first harness. **The whys carry. The split's
one cost is line 6, and both name it.**

**(ii) Would §0 + §3 stop you on a LEGO-from-concept-image invocation?** A: *yes* — quotes
§0 "does not spend a round until the human has approved it" and §3c "End with: approve to
run. Then wait."; "nothing in §0/§3 offers a shortcut past the approval line." B: *yes* —
same two quotes; "structural, not advisory"; and §3b's fidelity row "matches a
concept-image LEGO build exactly, so there's no ambiguity about which read type to
propose." **§0 is a checkpoint. n=2.**

## 4. Deficiencies, merged, with the critics' rulings

| # | Item | A | B | Safe? |
|---|---|---|---|---|
| a | Worked example of a §0 / a gate for a non-identity read type | #1 — **not safe** ("what a *good* function/fidelity gate looks like is an assertion") | #3 — **safe** ("additive, illustrative only") | **split** |
| b | Cost figures (~80k tokens a critic, two minutes) next to the Budget line, so the human prices rounds in real units | #2 — safe | — | safe |
| c | Sibling (measured pass) pointer dead-ends two levels deep | #3 — **not safe** (commits to a claim about an unbuilt skill) | — | not safe |
| d | `path-leak` / `own-table` double-tag in §1 misfiles own-table as contamination | #4 — safe | — | safe |
| e | Anchor a typical round count in Budget, descriptively, from the runs (3, 5, 7) | #5 — safe ("descriptive, sourced") | — | safe |
| f | n / evidence marker on §3b so trust in a class doesn't require leaving SKILL.md | — | #1 — **not safe** ("touches the epistemic core; own-table shows this edit going wrong once") | not safe |
| g | §0 says the agent "reads the artifact and its subject" — a concept-image invocation has no artifact yet | — | #2 — **not safe** (changes the §0 / round-zero ordering) | not safe |
| h | Cross-link §6 rows at their trigger points in §4 | — | #4 — safe | safe |
| i | One line of concrete contrast for the three read types in §3b | — | #5 — safe | safe |
| j | §6's table is 25+ unranked rows with no "start here" | *undermines* | — | (not a change) |
| k | §8 states n=1 procedure as settled inside the bullets; the caveat lives only in the heading | — | *undermines* | (not a change) |

## 5. Reading it — bins, then pricing

**Bin 1, ground truth:** nothing contradicted by a test.

**Bin 2, checkable claims — facts the author holds:**
- (a) A calls a gate example "an assertion." The record has two gates that *ran* — the
  Refinery's fidelity gate (`REFINERY_BUILD.md` §0) and this document's function gate
  (`00-precommit.md`). A worked §0 compressed from a real one is a record, not an assertion.
  B's "safe" holds for that version and A's objection is answered by it.
- (g) B calls the subject-before-artifact wording a change to the procedural contract. The
  record shows the harness *was* written before the artifact existed, every time: the
  Refinery's §0 is headed "written after inspecting the reference and before opening the
  DSL." The wording is a correction to match the record, not a new procedure.
- (f) B is right that a new column on the questionnaire is the own-table edit. But the
  regression on line 6 is measured by both critics; the cheapest fix that does not touch
  the questionnaire is a *status index* — class, n, where the starting point lives — which
  is a pointer table, not hypothesis content. Different edit from the one B ruled on.

**Bin 3, the instrument:** (b), (d), (e), (h), (i), (j), (k).

**Pricing.** (h) cross-links §6 into §4 — each §4 rule already carries a `[ref:]`; a second
pointer per rule is clutter for little. Declined. (j) A's "undermines" on the unranked
table — grouping its rows under the three invariants would give it a start-here without
changing a row; not on either safe list and it is the canonical table. Declined this round;
open. (k) B's "undermines" on §8 — hedging the bullets to "in that run" cannot be wrong.
Taken as wording.

## 6. Author's response — v4

**Taken, the safe list:** (b) cost figures at Budget in §3c; (d) `own-table` moved out of
§1's contamination clause to the anti-pattern it belongs to; (e) the run counts at Budget,
descriptively — "3 of 5, 5 of 5, 7 of 7, 1 of 1"; (i) one line contrasting the three read
types under §3b's table; (k) §8 bullets hedged to the run.

**Taken, bin-2 items, in the open — the third and fourth times an author has overruled a
"not safe" on "I hold the fact":** (a) a compressed worked §0 in §3c, from the Refinery's
real pre-commit, two lines per heading, labelled as that run; (g) §0 "reads the subject —
and the artifact, if one exists yet — then…"; (f) a five-row status index in §3b (class,
n, where) — not a column on the questionnaire. *The README's open question about this
pattern now has four instances. It is still not a rule of the skill.*

**Declined, the open list:** (c) the sibling pointer — write the measured-pass skill or cut
the paragraph; Brad's call, top of the list, flagged in both rounds now. (h) declined on
price. (j) the §6 grouping — a good idea nobody was asked to rule on; next round.

## 7. What the round cost and bought

One round, ~95k tokens a critic, two critics. It bought: **§0 works as a checkpoint** (n=2,
both quoting the same two lines); **the whys carry without the stories** (n=2, fifteen refs
checked by one critic); the split's exact cost, on one line, from two independent reads
that agreed to the point; and `want` converging on the ceiling. Capability 92/96 → 91/91 is
not a regression in the document — it is line 2 up and line 6 down, and the fix for line 6
costs six lines.
