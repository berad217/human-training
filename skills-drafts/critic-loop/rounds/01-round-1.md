# Critic round 1 — SKILL.md draft v1 (and round zero)

**Date:** 2026-09-11. **Subject class: prose — the first run off images.** **Read type:**
blind function (two critics) + informed (two critics), all four fresh `general-purpose`
agents, model Sonnet, dispatched in parallel, no shared context. **Author:** Claude (Opus 5).
**Budget: 1 of 1.** Pre-commit: `00-precommit.md`, written before the blind copy was made.

## 0. What was judged

| artifact | sha1 (12) |
|---|---|
| `skills-drafts/critic-loop/SKILL.md` at commit `6dc8dc6` (informed reads) | `fd94b5da7d0d` |
| blind copy of the same — frontmatter, H1, Credit stripped (blind reads) | `d2e9e6fd8b2c` (also the directory name) |
| blind copy of `skills-source/grill/SKILL.md`, same strip (round zero) | `c421a40f7dca` |

Walls before the round: frontmatter `name` matches directory — PASS; `description` present —
PASS; trigger eval — **not runnable, recorded as the wall this run could not run.** 456 lines.

**Leak check on the blind copy** (§5's "look at what you send"): the strip script's grep hit
one line — the intro's provenance paragraph ("Brad's design, run in `Shapey_McShapeface`…").
Judged evidence, not function; left in per the pre-commit recipe. Both blind critics were
asked what told them (Q6).

## Round zero — the control arm

One read on the `grill` exemplar, blind function questions. Result: function, audience and
first action all correct, *confident*, no leak reported; the critic identified the genre
("a Claude Code skill body") from second-person imperative voice and cross-references to
sibling workflow stages. **The instrument can perceive a SKILL.md with its label stripped.**
`want/20` on the exemplar: **16** — the ceiling.

## 1. Stage 1 — blind function, two reads

| | A | B |
|---|---|---|
| What is it for | An iterative review process where fresh, blind agents judge an artifact against a pre-committed rubric and gate, with guards against contamination, false gradients, wasted rounds | Using fresh, blind agents as independent judges of artifacts with no objective test, guarding against contaminated judgement, non-gradient scores, wasted rounds |
| Who for | An agent in Claude Code, invoked via `/critic-loop`; names Brad from the provenance | A Claude Code agent acting for a technical author doing iterative design work |
| First action | Fill the §4 table, then run round zero | Fill the §4 table, then write the §3 pre-commit before building or running round zero |
| Confidence | confident | confident |
| Leak (Q6) | none — path is a hash, no H1, no frontmatter | none — same |
| `want/20` | 15 | 17 |

**Gate: met, 2 of 2** — all three parts, both critics. Both cited body self-references as
drivers: "Explicit `/critic-loop`", "This skill adds nothing there", "`docs/CRITIC_LOOP.md`
v3". See §5 below for what that means for the prose row.

## 2. Stage 2 — the vector, two informed reads

| # | Criterion | Wt | A | B | spread | Critics' reasons |
|---|---|---:|---:|---:|---:|---|
| 1 | When to reach for it | 20 | 18 | 19 | 1 | Both: "Not the right tool for" routes tested qualities to the test and imperceptible ones to a wall, with the measured cost |
| 2 | Can set up a run | 20 | 18 | 19 | 1 | A docks 2: "never gives a starting round-budget number" |
| 3 | Can run a round | 20 | 19 | 19 | 0 | Both: §5 "A round" executable cold, each step tied to the failure that earned it |
| 4 | Can read a result | 15 | 14 | 14 | 0 | Three bins + price-against-rubric + vector; the 62→58 example |
| 5 | Can stop | 10 | 9 | 10 | 1 | Four conditions with symptoms; the 49→59 trace |
| 6 | Trusts it correctly | 15 | 14 | 15 | 1 | A: "the table's uniform formatting undercuts the prose warning" |
| | **Capability** | 100 | **92** | **96** | 4 | |
| | `want/20` (ceiling 16) | 20 | 16 | 14 | 2 | A: "would trim it before trusting it as a daily driver"; B: "reads as a personal research log more than an installable tool" |

**Inter-rater spread ≤ 1 per line** — the image finding (~1 pt/line) holds on prose, n=1.
`want` spread is 2 on both stages (15/17 blind, 16/14 informed), straddling the ceiling.

## 3. Deficiencies, merged, with the critics' safe/unsafe rulings

| # | Item | A | B | Safe? (critics) |
|---|---|---|---|---|
| a | **§4's per-class table formats four n=0 rows identically to the n=15 row; the bold warning above it is a prose guard** — the skill's own "undermines it" answer from both critics, independently | #3, undermines | #2, undermines | **safe** (both) |
| b | §5's "Stage the questions" (7) and §6's template (6) are two near-identical numbered lists that don't line up | #1 | — | safe (A) |
| c | Anti-patterns restates §7's failure rows in a second format | #4 | — | safe with a check that nothing is dropped (A) |
| d | The war stories are told in prose in §1/§3/§5 *and* as rows in §7 | — | #1 | safe (B) |
| e | Provenance is a research trail; §8's filing paths are one repo's | length answer | length answer, `want` reason | safe (both, as length) |
| f | A default budget number | #2 | — | **not safe** — "generalised past its n=15 evidence" |
| g | A worked end-to-end trace / filled round log | #5 | #3 | **not safe** (both) — composite-run risk (A); fabrication risk on a doc whose credibility is its n's (B) |
| h | "Sibling loop" points at nothing | — | #4 | not safe — "depends on whether the sibling skill exists" |
| i | §9 is 13 lines: doesn't say how poll-two becomes parallel Agent calls, or how the blind path avoids the parent directory | — | #5 | not safe — "untested procedural claims should carry an n" |

**Hardest question — length:** A **~350** (fold §6 into §5 ~40, anti-patterns into §7 ~30,
§4 rows ~20, provenance ~15). B **~330** (prose retellings → §7 refs ~60, §4 rows ~10, §8
paths ~8, provenance ~4). Both say *fold, don't cut*; both keep §3/§5/§6/§7 intact.

## 4. Reading it — the three bins, then pricing

**Bin 1, ground truth wins:** nothing in the list is contradicted by a test. The walls
passed.

**Bin 2, checkable claims:** two "not safe" rulings rest on a fact the critic did not
have and the author does. (h) — the sibling loop is not a skill; it is a paragraph,
`CRITIC_LOOP.md` v3 §1, and the pre-commit's own §1 knew it. (i) — this round *is* the run
§9 lacked: four `Agent` calls, blind reads in one parallel block, content-hashed directory in
the session scratchpad, informed reads as separate calls. Both are now n=1 and can be stated
as what was done, not as procedure.

**Bin 3, the instrument.** Everything else.

**Pricing against the whole rubric.** (d) trades against lines 1 and 2: critic A scored
those high *because* the costs are in the prose ("a worked wall-cost that makes the
abstraction land"). Folding every story into a §7 reference would buy length with line-1/2
points. Taken as: one prose telling per story, at the rule it justifies; the *second*
telling goes; §7 carries the one-line form. (c) trades against the plugin's house
convention — every sibling skill has an Anti-patterns section. Taken as: keep the section,
cut the rows that duplicate §7, keep the ones that are not failure modes (sending early;
gate-met ≠ good; confident rules for unrun media).

## 5. Author's response — v2

**Taken, the safe list:** (a) per-row `**UNTESTED**` marker inside each n=0 row, and the
image row's evidence stated in the row; (b) one question sequence in §5, the template
references it; (c) anti-patterns deduplicated against §7; (d) second tellings removed; (e)
provenance to two sentences, §8 filing made generic with the Shapey layout as the one
example.

**Taken, two deviations from "safe list and nothing else", in the open:** (h) a one-line
status — no such skill; `CRITIC_LOOP.md` v3 §1 has the paragraph. (i) §9 rewritten as what
this run did, marked n=1, nothing beyond it. Both "not safe" rulings were conditional on a
fact the author holds; the log is the guard. *This is one observation; it is not a rule of
the skill.*

**Declined, the open list:** (f) budget default — a number generalised past n=15, exactly
as A said; (g) worked trace — both critics' reason stands, and the fix is a *real* round log
in this folder, which this file now is; the skill can point at it once it has been read as
one.

**Not a change, a finding — the prose row of §4, rewritten from the run:**

- The label channels (frontmatter, H1, filename) stripped cleanly; neither critic reported
  a leak. **But a document's own self-references are the primary identification channel
  and cannot be stripped** — both critics named "Explicit `/critic-loop`" and the body's
  mention of the evidence doc as what drove them. A document that states its purpose
  passes "what is this for" by construction. **On prose, the function question saturates
  at round zero; the gate's teeth are Q3, *what would you do first*** — a reader who
  answers "send it to critics" fails; both answered "the §4 table, then the pre-commit."
  n=1.
- The exemplar passed the same questions at the same confidence, which is the saturation
  showing on the control. The ceiling on `want` (16) was the useful number round zero
  returned.
- The medium is cheap: four critics, ~80k tokens each, under two minutes wall-clock in
  parallel. The rationing argument for a round is weaker here than on images; the
  contamination argument is unchanged.

## 6. What the round cost, and what it bought

One round. It converted §4's prose row from hypothesis to n=1, found that the skill's own
table violated the skill's own rule (a prose guard over the n=0 rows), and gave two
length targets 20 lines apart. The gate closed on the first round — and, as §11 of the
source doc predicts, that says the document declares itself, not that it is good; the
informed reads say 92–96 on capability and 14–17 on wanting it, around a ceiling of 16.
