# Tasks

The forward queue for this repo. Backward-looking decisions live in the release
notes and `HANDOVER.md`; this file is only what's next.

Most of **Active** came out of the 2026-08-19 audit of
[cursor/plugins/pstack](https://github.com/cursor/plugins/tree/main/pstack) (MIT,
Lauren Tan). Items are ordered by recommended sequence, not priority — earlier
ones unblock or inform later ones.

## Active

<!-- pstack: new skills -->

- [ ] **Decide whether `project-checkup` and `robustness-audit` should keep a
  trail** — `show-me-your-work` now exists and owns the format, so wiring either
  in is a one-line reference. The open question is whether they *should*: both are
  usually single interactive passes, and the skill's own rule says a trail nobody
  reviews after the fact is bookkeeping. Probably yes for `project-checkup` in
  force-all mode, probably no for a normal audit.
- [ ] **Draft `blast-radius`** — what a specific diff breaks *elsewhere*, beyond
  the diff. No overlap with `robustness-audit` (that reads code for latent
  defects; this reads a change for reach). Core move: find the one fact the
  change is safe because of, then prove that one fact by running code. Lands in
  `skills-drafts/blast-radius/` first.
- [ ] **Fork `unslop` into a house style guide** — take pstack's rules 1–12 and
  20–31 (the abstract-metaphor→plain-word table and "say what it does, not how it
  feels" are the valuable parts). Drop or invert 13–19: pstack bans em dashes,
  mid-sentence colons, and "surface"/"scaffolding" as metaphors, and this repo's
  prose uses all three deliberately. Adopting it verbatim means either rewriting
  every skill body or shipping a rule we ignore.
- [ ] **Cross-vendor review of a Leroy trail** — end every trail-producing run
  with an `Attention` section written by a *different vendor's* model reading the
  trail and the diff, flagging what still deserves scrutiny. We can do this better
  than pstack can: `codex-cli` and `antigravity-cli` give genuine cross-vendor
  eyes, not a second Claude. **Unblocked** — the trail exists and `show-me-your-work`
  owns it, so this is the next natural step on that thread.
- [ ] **Verification-skill generator** — a skill that generates a *project-local*
  verify skill plus a feature map: launch, doctor, drive, evidence, cleanup, one
  file per user-facing feature. This is the structural answer to the behavioural
  checklist being unrun for five releases — the checklist is unrun because it's
  prose a human executes. Non-negotiable rule from pstack: the generator runs its
  own output end to end once before handing it over, because a generated skill
  that was never executed is a draft, not a deliverable. Biggest item here.
- [ ] **Draft `teach`** — explain a subsystem so a person actually understands it.
  The transferable rule: for anything with 3+ moving parts, never draw one
  diagram; draw a short series where each redraws the last and adds exactly one
  part. Plus the negative constraints (no pacing theater, no "here's the key
  insight").
- [ ] **Draft `reflect`** — mine the session transcript for durable learnings and
  route each to a concrete skill edit. This is literally what this repo does by
  hand. Steal the Accepted/Rejected/Backlog split and the structural-enforcement
  check: before applying anything, ask whether a lint rule or script would enforce
  it more reliably than more prose. Needs porting off Cursor transcript paths.

<!-- pstack: pearls for existing skills -->

- [ ] **`grill`: classify before you ask** — if the answer to a question is a fact
  you could observe by running something, it is not the human's to answer. Sketch
  it and let the result decide. Grill's design is one question at a time; this
  says some of those questions shouldn't be asked at all. Also adopt "done as a
  falsifiable predicate" over "crisp and bounded".
- [ ] **`start`: status tags on every thread** — steal `recall`'s output contract.
  Exactly one tag per thread: `[merged #N]`, `[open PR #N]`, `[in flight <branch>]`,
  `[verified, uncommitted]`, `[reverted]`, `[planned, not started]`. "A thread
  with no tag is not done yet, so tag it." Sharper than the current prose
  "In flight" line.
- [ ] **`handover-manager`: a pickup is inheritance** — the handover skill says
  what to write; it never tells the reader not to redo the work. Add: the prior
  agent already paid the cost, resist re-deriving. And name the tell — a "let me
  verify from scratch" pass means treating the trail as untrustworthy when it's
  actually authoritative. Also mandate the `wip:` commit before handing over.
- [ ] **`onboarding-creator`: the Diátaxis mode-picker** — one document, one mode.
  Two questions (action vs understanding, learning vs work) pick tutorial /
  how-to / reference / explanation. One paragraph, not a skill; the rest of
  pstack's 11KB `technical-writing` doesn't earn its keep here.

<!-- skill-authoring craft, applies across skills-source/ -->

- [ ] **Add a `**Reply:**` contract to every skill** — one closing line naming
  exactly what to hand back. Every pstack skill has one; almost none of ours do.
  Cheapest quality win in the audit.
- [ ] **Adopt the `skip: <reason>` rule** — a step you choose not to do stays in
  the list with a one-line reason. Skipping silently is not allowed. Directly
  addresses the failure `/start`'s anti-patterns section already worries about.
- [ ] **Write down the eval blinding rules** — no `eval`/`test`/`judge`/`candidate`
  /`rubric` in any path or prompt the candidate sees; the prompt reads like an
  organic user request; no chain-eliciting cues (asking which skills it applied
  inflates citation behaviour); grade from which files it actually opened, never
  self-report; one judge scores both variants in a single pass or calibration
  drifts. Better-specified than the blind-subagent-judge approach we improvised
  when skill-creator's optimizer turned out broken on Windows.

<!-- carried from HANDOVER.md, not from the audit -->

- [ ] **Exercise the behavioural checklist** — unrun across 1.17–1.21 and the
  largest unverified surface in the repo. Cheapest entry point is one `/start` on
  a machine whose `autoUpdate` is off, confirming a `Toolchain:` line appears.
- [ ] **Confirm `autoUpdate` fires on relaunch**, not just once when set. 2d is
  built on the assumption that `lastUpdated` keeps advancing.
- [ ] **Bring one other machine current by hand** — also tests whether the
  two-step recovery in `onboarding.md` §2 is written correctly.

## Someday

- [ ] **`claude-plugins-official` has `autoUpdate` off** (`lastUpdated`
  2026-06-12). Found in passing twice now. 2d should surface it on any fresh
  `/start`; fixing it is a one-line settings edit whenever it next annoys.
- [ ] **§6 memory migration** — 9 entries stranded at the global path for this
  repo; 216 files / 26 projects / 666 KB across all projects. Never run.
- [ ] **The `principle-*` decomposition pattern** — pstack ships 21 single-rule
  skills indexed inline by its router, so other skills can cite a principle by
  name. Real architectural idea, but 21 files to maintain and the payoff shows up
  at team scale. Revisit only if a rule starts getting restated across skills.
- [ ] **`ollama` draft** — carried from earlier handovers.
- [ ] **image-gen empirical gaps** — identity fidelity, multi-`-i` compositing,
  macOS/Linux copy-out.
- [ ] **`genesis.md` as the target pattern for guide bodies.**

## Done

- [x] ~~Extract the decision trail into `show-me-your-work`; Leroy references it~~ (2026-08-19)
- [x] ~~Ship 1.22.0 — "Show Your Work"~~ (2026-08-19)
- [x] ~~`robustness-audit`: evidence ladder + disposition buckets~~ (2026-08-19)
- [x] ~~`leroy-jenkins`: TSV decision trail + pause protocol~~ (2026-08-19)
- [x] ~~Audit cursor/plugins/pstack for adoptable skills and pearls~~ (2026-08-19)
