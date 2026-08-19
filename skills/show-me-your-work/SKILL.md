---
name: show-me-your-work
description: Keep a reviewable decision trail for work a human reviews after the fact — unattended runs, multi-phase efforts, anything they stepped away from. One append-only TSV, a row per decision, written as decisions happen rather than assembled at the end. Owns the trail format that other skills compose with. Triggers on /show-me-your-work, "keep a decision trail", "log your decisions so I can review", or an autonomous run that needs an auditable record.
---

# Show me your work

For work a human reviews after the fact, a decision trail lets them reconstruct
what was decided, why, and on what evidence — without rerunning the work or
reading the whole transcript.

This skill owns **one format**, so that every skill producing a trail produces
the same one and a future session knows where to look. Other skills say *when* to
log and *which* decisions qualify; they don't redefine the columns.

## When to invoke

- Explicitly, via `/show-me-your-work`, or "keep a decision trail I can review".
- Composed by another skill that runs unattended or across phases. `leroy-jenkins`
  is the main one.
- Any run the user steps away from and reviews later.

**Not for a normal interactive session.** When the user is watching, the
conversation *is* the trail, and a TSV alongside it is bookkeeping nobody reads.
The trail earns its place exactly when nobody was watching.

## Write it as it happens

Not at the end. As it happens.

A run you watched barely needs a log. A run that died partway — context
exhausted, quota hit, machine slept — is precisely the one whose reasoning you
need, and a trail assembled at the end is the one that run destroys. That
asymmetry is the whole argument for the format: a row costs one command, so
there is no reason to defer it.

## The file

One TSV per run. Default location `docs/decisions/<run-id>.tsv` when the project
keeps working docs under `docs/`, otherwise `decisions/<run-id>.tsv` at the
project root. `<run-id>` is `YYYY-MM-DD-HHMM`. A composing skill may name its own
path — `leroy-jenkins` uses `docs/leroy/<run-id>.tsv` to match its branch — but
the columns and rules below don't move.

TSV, because GitHub renders it as a sortable table, `column -s$'\t' -t` and
spreadsheets read it, and a row appends with one command.

| Column | What goes in it |
|-----------|-----------------|
| `ts` | ISO8601 timestamp, **UTC**. The timeline axis. |
| `phase` | Which chunk of the run this belongs to. |
| `decision` | What you chose or did. One line. |
| `why` | The reason in plain words, plus the alternative you rejected. |
| `evidence` | A **pointer**, never prose: commit SHA, `file:line`, an artifact path. |
| `result` | The outcome: `tests green`, `reverted`, `deferred`, `open question`. |

```bash
printf '%s\t%s\t%s\t%s\t%s\t%s\n' "$(date -u +%Y-%m-%dT%H:%M:%SZ)" "$PHASE" "$DECISION" "$WHY" "$EVIDENCE" "$RESULT" >> docs/decisions/2026-08-19-1430.tsv
```

```powershell
"{0}`t{1}`t{2}`t{3}`t{4}`t{5}" -f (Get-Date).ToUniversalTime().ToString("yyyy-MM-ddTHH:mm:ssZ"), $Phase, $Decision, $Why, $Evidence, $Result | Add-Content -Encoding utf8 docs/decisions/2026-08-19-1430.tsv
```

Write the header row once, on first use.

Both snippets emit **UTC**, and they have to agree. PowerShell's `-Format s`
looks right and is not: it prints local time with no offset marker, so a trail
written on Windows would carry a `ts` column hours off from every commit SHA it
cites, with nothing in the file saying so. `.ToUniversalTime()` is the fix and
works on Windows PowerShell 5.1; `-AsUTC` does not exist before PowerShell 7.

### Three rules the format depends on

- **One row is one decision.** If it does not fit on one line, the decision is not
  crisp yet. Cells stay single-line; strip stray tabs and newlines.
- **Append-only.** A wrong call gets a *new* row that supersedes it. Never edit or
  delete history — the reversals are the most useful rows in the file.
- **Prefix any cell starting with `=`, `+`, `-`, or `@` with a single quote.**
  Findings, paths, and flags land in these cells verbatim, and a reviewer opening
  the log in a spreadsheet should not execute one.

## What earns a row

Decision points and checkpoints, not every action:

- A fork taken, with the option rejected.
- A chunk completed, with its verification result.
- A pivot or revert, with what triggered it.
- A blocker parked or an open question flagged.
- One row per iteration, for loop-shaped runs.

Skip the trivial and self-evident. A row nobody would audit does not earn its
place.

Write rows the way you would tell a colleague what you did. Plain words,
concrete actions, no jargon. A reviewer should understand a row without decoding
it. `explored both, this one was a one-way door` beats
`applied irreversibility heuristic`.

## Should it be committed?

Default **no** — it is a working artifact, and most runs just need the trail to
exist while they run.

Commit it when a reviewer needs the trail to trust the result: an unattended run
nobody watched, a large migration, anything where confidence has to be shown
rather than assumed. A composing skill may override this default; `leroy-jenkins`
commits by default, because reviewing work nobody watched is the entire reason
that skill produces a trail.

## Audit the trail before handing back

At the end of the run, walk the trail against what actually happened:

- Every row maps to a real action. Cut invented or aspirational entries.
- Every `evidence` pointer resolves and shows what its row claims.
- A fork or abandoned approach that shaped the run but never got logged is a gap.
  Add it.
- Drop padding.

**Fix the log, not the story.** Where the work diverged from what a row claims,
the row is wrong.

## Reading a trail

Top to bottom, following the evidence pointers and spot-checking. GitHub renders
a committed TSV as a table; `column -s$'\t' -t <file>` renders it in a terminal.
A row whose evidence does not resolve, or whose `result` is unverified, is the
audit catching a gap — that is the format working.

## Composing this skill

Other skills route their trail here rather than inventing one. Reference it by
name, say which of your decisions earn a row, and let this skill own the format.
**Do not restate the columns.** Three copies of a schema is how they drift.

## Anti-patterns

- **Assembling the trail at the end.** The failure this skill exists to prevent.
  A trail written after the fact is reconstruction, and it is missing exactly the
  run that needed it.
- **Prose in the `evidence` column.** It is a pointer. If you are explaining, you
  are in the wrong column — that is `why`.
- **Editing a row that turned out wrong.** Supersede it with a new row. The
  history of being wrong is the most useful thing in the file.
- **Logging every action.** A trail nobody can skim is a transcript, and they
  already had one of those.
- **Keeping a trail for a session the user watched.** Bookkeeping. The
  conversation was the trail.

**Reply:** the trail's path, one line on what it covers, and anything the audit
pass changed about it.
