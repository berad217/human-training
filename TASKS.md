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
- [ ] **Drop the hardcoded skill list from `plugin.json`'s description** — it
  enumerates every session-authored skill by hand and went stale twice on
  2026-08-19 alone. `check-skill-refs.py` now guards it, but the guard treats the
  symptom; a description that doesn't enumerate can't go stale. Needs a call on
  whether the list earns its place for discoverability.
- [ ] **Write the `--plugin-dir` probe technique down properly, with its safety
  rules** — currently only in release notes and the handover, so it evaporates
  when the handover is pruned. **It must not be used again without both rules**,
  which cost one release to learn: pass `--allowedTools Skill Read Glob Grep Bash`
  so the permission posture is explicit rather than variable, and read outcomes
  from `tool_result` (checking for `has been denied`) rather than `tool_use`
  requests. Without those, a denied `Skill` call looks like a skill that ran and
  chose not to act. Candidates: `onboarding.md`'s workflow list, or a section in
  whatever skill ends up owning verification.
- [ ] **Probe the never-observed skills now the instrument is sound** — `grill`,
  `tasks`, `handover-manager`, `robustness-audit` have never been watched running.
  Each needs a fixture with planted discriminators (the widget-forge pattern
  worked: plant something in a section the skill is told *not* to surface, and
  check it doesn't leak). Follow the two probe rules in `HANDOVER.md` or the
  results are worthless.
- [ ] **Decide whether the evidence ladder should cover instrument failure** — it
  grades how much evidence backs a claim, and both overclaims on 2026-08-19 were
  a different shape: the check ran, produced output, and the output was misread.
  A rung-4 "I ran a script" is worthless if the script measured the wrong thing.
  Either the ladder gains a rung-0 "is the instrument sound?" gate, or it stays
  scoped and something else covers this. Currently nothing does.
- [ ] **Re-probe `project-checkup` with `Skill` permitted** — its only probe was
  invalid (Skill denied), so nothing is known about whether it invokes
  `workflow-orientation` and `robustness-audit` as its Component Invocations
  section specifies. Note the synthetic project classified as Active healthy,
  where the routing table says to skip both, so the test needs a dormant fixture
  to mean anything.
- [ ] **`ollama` draft** — carried from earlier handovers.
- [ ] **image-gen empirical gaps** — identity fidelity, multi-`-i` compositing,
  macOS/Linux copy-out.
- [ ] **`genesis.md` as the target pattern for guide bodies.**

## Done

- [x] ~~Prove a by-name skill reference resolves at runtime (rung 5); found and fixed a UTC bug~~ (2026-08-19)
- [x] ~~Graduate `blast-radius` to `skills-source/`~~ (2026-08-19)
- [x] ~~Wire `check-skill-refs.py` into CI, negative-tested both ways~~ (2026-08-19)
- [x] ~~Exercise `blast-radius` against a real diff; two fixes fed back~~ (2026-08-19)
- [x] ~~Settle evidence-ladder ownership: names shared, definitions local~~ (2026-08-19)
- [x] ~~Extract the decision trail into `show-me-your-work`; Leroy references it~~ (2026-08-19)
- [x] ~~Ship 1.22.0 — "Show Your Work"~~ (2026-08-19)
- [x] ~~`robustness-audit`: evidence ladder + disposition buckets~~ (2026-08-19)
- [x] ~~`leroy-jenkins`: TSV decision trail + pause protocol~~ (2026-08-19)
- [x] ~~Audit cursor/plugins/pstack for adoptable skills and pearls~~ (2026-08-19)
