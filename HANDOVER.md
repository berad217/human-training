# Handover — human-training

**Session date:** 2026-08-19
**State:** **1.22.0 and 1.23.0 both shipped.** Committed, pushed, tagged,
released; CI green on both; builders byte-identical; tree clean and in sync.
Nothing in flight.

What shipped is in the release notes; don't restate it here.

---

## First: this repo now has a TASKS.md

New this session, and it changes what a handover is for. The split:

- **`TASKS.md` is the queue.** Everything with a next action. It absorbed the
  carried items that used to live in this file's "Parked / carried" section.
- **This file is the delta.** What is contested, unproven, or decided-but-not-
  written-down. Things a fresh session would get *wrong*, not things it should
  get *around to*.

If you find yourself writing a to-do here, it belongs in `TASKS.md`. If you find
yourself explaining why something is not what it looks like, it belongs here.

---

## The delta (not in the files)

- **Both releases changed instruction surfaces with no scripted check behind
  them, and their failure modes are asymmetric.** A skipped decision trail is
  loud (the file is absent or two rows long). An inflated evidence rung in
  `robustness-audit` is silent, and is the same class of error the ladder was
  written to catch. If you verify one thing, verify that — run an audit and see
  whether findings actually come back labelled `Cited` when they were not traced.

- **`show-me-your-work` introduced a failure mode 1.22.0 did not have.** The
  trail format used to be inline in `leroy-jenkins`; it is now referenced by
  name. If the composed skill fails to load, Leroy degrades to a vaguer
  instruction rather than a wrong one — the safer direction, but still a real
  regression against having it inline. Unverified either way.

- **The evidence ladder deliberately does *not* fold into the confidence score.**
  This is the obvious simplification and it is wrong. Confidence is how sure the
  agent feels and was kept deliberately non-suppressive so agents report
  low-confidence findings rather than dropping them. The rung is what was
  actually checked. The finding worth catching is the one that is 95-confident at
  rung 2, and collapsing the axes is precisely what hides it. **Don't "tidy" this
  into one number.**

- **`leroy-jenkins` commits its trail; `show-me-your-work` does not by default.**
  That inversion is intentional and easy to "fix" wrongly. Most trails are
  working artifacts; Leroy's case (review work nobody watched) is the unusual
  one. A default encoding the unusual case is a default people ignore.

- **The pstack audit's rejections are recorded, so they aren't re-derived.**
  Roughly two-thirds of [pstack](https://github.com/cursor/plugins/tree/main/pstack)
  does not transfer: it assumes a team, Graphite stacks, MCP-backed observability,
  and subagents spawnable on named cross-vendor models that Claude Code's Agent
  tool cannot address. Rejected on those grounds: `poteto-mode`'s 22-playbook
  router, `swarm`, `arena`, `interrogate`, `architect`, `how`/`why`, `recall`
  (overlaps `/start`, and ours reads files rather than mining transcripts),
  `automate-me` (this whole plugin *is* Brad's mode skill), and the
  Graphite/PR/babysit/shipping playbooks. The reasoning is in the
  2026-08-19 audit; `TASKS.md` Someday holds the two that might come back.

- **`unslop` would fight this repo's own prose, and that is a real blocker, not a
  detail.** pstack bans em dashes outright, mid-sentence colons, and
  "surface"/"scaffolding" as metaphors. Every skill body here uses all three
  deliberately. The `TASKS.md` item says fork rules 1–12 and 20–31 and drop
  13–19 — adopting it verbatim means either rewriting every skill or shipping a
  rule we ignore.

- **Branch protection is still settled; don't reopen it.** Both pushes this
  session printed "Bypassed rule violations". That is the rule working, not
  failing — `enforce_admins` is `false`, `required_approving_review_count` is 0,
  and `berad217` is the only write path. Reviewed and kept on 2026-08-03.

- **`skills-drafts/` was deliberately skipped for `show-me-your-work`.** The
  convention is drafts-first and it exists for skills whose shape is unknown.
  That one was written, reviewed, and shipped a release earlier. Not a precedent
  for skipping drafts on genuinely new skills — `blast-radius` should go through
  drafts.

## Next steps

The queue is `TASKS.md`. The three worth naming here because they are *stale*
rather than merely queued:

1. **The behavioural checklist is now unrun across seven releases** (1.17–1.23).
   Carried in every handover since 1.17.0 and never the thing that got done. It
   is the largest unverified surface in the repo and the gap widens per release.
2. **`autoUpdate` firing at startup is still unproven** — one refresh observed on
   2026-08-03, never across a relaunch. `/start` step 2d assumes `lastUpdated`
   keeps advancing.
3. **Every other machine is now four releases behind** (1.20–1.23) and cannot
   receive any of them until someone runs `update-plugin.bat` there by hand and
   sets `autoUpdate` after.

---

*Ephemeral bridge — prune once absorbed. Durable record: the 1.22.0 and 1.23.0
release notes, `TASKS.md` for the queue, and the skill bodies themselves.*
