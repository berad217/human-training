# Handover — human-training

**Session date:** 2026-08-19
**State:** **Five releases shipped: 1.22.0, 1.23.0, 1.23.1, 1.24.0, 1.24.1.**
All committed, pushed, tagged, released; CI green on each; builders
byte-identical; tree clean and in sync. Nothing in flight.

All of it traces to an audit of [pstack](https://github.com/cursor/plugins/tree/main/pstack)
(MIT) that opened the session. What shipped is in the release notes; don't
restate it here.

---

## The queue is `TASKS.md`

Anything with a next action lives there. This file carries only what is
contested, unproven, or decided-but-not-obvious — the things a fresh session
would get *wrong*, not the things it should get *around to*.

---

## The delta (not in the files)

- **There is now a cheap way to actually watch a skill run, and it is not
  written down in any skill.** `claude -p --plugin-dir <repo> "<organic prompt>"`
  loads the **working tree**, so a skill can be exercised before it is released
  and without touching the installed plugin — which matters, since this machine's
  install is still on 1.21.1 and could not have run today's tests. Two rules
  learned the hard way:
  - **Run it from a scratch directory, never from this repo.** `onboarding.md`
    tells agents not to invoke `human-training:*` skills here, which suppresses
    the trigger and produces a false negative.
  - **Grade on a content discriminator, not self-report.** Pick something that
    exists *only* in the skill under test (the spreadsheet-injection rule worked),
    write an organic prompt, and never ask which files it read.

  This is the first tool that has ever dented the behavioural-checklist gap, and
  it took minutes. It is the obvious lever for the rest of the backlog.

- **It found a real bug on first use.** `show-me-your-work`'s PowerShell snippet
  used `Get-Date -Format s`, which is local time with no offset, against bash's
  UTC. Shipped in 1.22.0, survived the 1.23.0 extraction and three readings
  including one where the file was moved wholesale. An agent reading it cold
  caught it in one pass. **The lesson is the ladder's whole thesis**: a claim at
  rung 1 stays at rung 1 no matter how many times its author re-reads it.

- **Don't fold the evidence ladder into the confidence score.** This is the
  obvious tidy-up and it is wrong. Confidence is how sure the agent feels, and
  was kept deliberately non-suppressive. The rung is what was actually checked.
  The finding worth catching is the one that is 95-confident at rung 2.

- **Don't centralize the ladder either.** Settled 1.23.1 after measuring it:
  ~14 of 32 lines are portable and rung 3 means genuinely different things in
  `robustness-audit` and `blast-radius`. Names and order are shared; definitions
  are local and *meant* to differ. A data format earns an owner; a vocabulary
  does not. Reasoning is in `skills-drafts/blast-radius/NOTES.md`.

- **`leroy-jenkins` commits its trail; `show-me-your-work` does not by default.**
  Intentional and easy to "fix" wrongly. Most trails are working artifacts;
  Leroy's case is the unusual one.

- **`plugin.json`'s description enumerates every session-authored skill by hand,
  and went stale twice in one day.** `scripts/check-skill-refs.py` now catches it
  in CI, which is a guard rather than a cure — the enumeration itself is the
  defect and dropping it is parked in `TASKS.md` Someday.

- **The pstack rejections are recorded so they aren't re-derived.** Roughly
  two-thirds does not transfer: it assumes a team, Graphite stacks, MCP-backed
  observability, and subagents spawnable on named cross-vendor models that the
  Agent tool cannot address. Rejected on those grounds: `poteto-mode`'s
  22-playbook router, `swarm`, `arena`, `interrogate`, `architect`, `how`/`why`,
  `recall` (overlaps `/start`, and ours reads files rather than transcripts), and
  `automate-me` (this plugin *is* the mode skill).

- **`unslop` would fight this repo's own prose**, which is a real blocker rather
  than a detail. It bans em dashes, mid-sentence colons, and
  "surface"/"scaffolding" as metaphors; every skill body here uses all three
  deliberately. The `TASKS.md` item says fork it, not adopt it.

- **Branch protection is settled; don't reopen it.** Every push this session
  printed "Bypassed rule violations". That is the rule working — `enforce_admins`
  is `false`, required reviews are 0, and `berad217` is the only write path.
  Reviewed and kept 2026-08-03.

## Stale, not merely queued

1. **The behavioural checklist is unrun across eight releases** (1.17–1.24.1),
   and today added two skills to the pile. It now has a cheap tool pointed at it
   for the first time; `/start` is the obvious next target.
2. **Every other machine is five releases behind** and cannot receive any of them
   until someone runs `update-plugin.bat` there by hand and sets `autoUpdate`.
   **This machine is too** — still on 1.21.1.
3. **`autoUpdate` firing at startup remains unproven** across a relaunch. `/start`
   step 2d assumes `lastUpdated` keeps advancing.

---

*Ephemeral bridge — prune once absorbed. Durable record: the 1.22.0–1.24.1
release notes, `TASKS.md` for the queue, and the skill bodies themselves.*
