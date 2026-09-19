# Handover Guide

A handover bridges a context reset. It works with any AI agent, in any host.
The template is in `assets/handover.md`; worked examples, the incident this
guide was rewritten after, and the bootstrap/pickup checklists are in
`assets/handover-reference.md`. Read those only when a step points you there.

**Invoke when** the user asks for a handover, the context is getting full or
laggy, at a natural pause (end of sprint, milestone), or when stuck and a fresh
session would help. Not on "let's wrap up" alone — ask first.

---

## The one idea: Ephemeral Delta

A handover is not a status report. It is the **conversation context that does
not live in the files yet**: the debate in progress, the path that failed, the
thing that is half-done and currently broken.

- **Record** (permanent): code, spec, DEVLOG, tests, CONTEXT.md.
- **Bridge** (temporary): the handover.

**If it is in a file, it does not belong in the handover. Once a decision
lands in a file, delete it from the handover.** The budget is ~200 tokens —
about 150 words, one screen. A clean stop needs almost nothing; length comes
from unresolved context, never from filling empty sections.

---

## Outgoing: writing one

### Step 0 — Durability, before you write a word

"In a file" is not "safe". A file is one disk away from gone, and a commit that
was never pushed is invisible to every other machine and every future session.

**Commit first.** Whatever is uncommitted goes into one `wip:` commit on the
current branch before the handover is written. If the tree is broken, say so in
one line of the commit body. A handover that describes work only the working
tree holds is describing work that a crash deletes.

**Then check, in every repo the session touched** — the one you are in, any
sibling repo named in `onboarding.md` or the current handover, and if you are
not sure, ask: "did we touch any repo besides X today?"

```bash
git status -sb
```

Read the **first line**, specifically the `[ahead N]` marker. The file list
below it tells you about *uncommitted* work; the marker tells you about
*undurable* work. They are different failures and only one is obvious.

| First line | Meaning | Write |
|---|---|---|
| `## main...origin/main` | committed **and** pushed | nothing — a clean stop is clean |
| `## main...origin/main [ahead 4]` | 4 commits exist **only on this disk** | say so, and **offer** to push |
| `## main` (no upstream) | no remote | say it plainly; "committed" is the ceiling |

**Never push on your own.** Report and offer; the remote is usually shared and
consent is not yours to assume. If you cannot run commands, say *"push state
unverified — I can't run git here."* An honest unknown is useful; a confident
wrong "all work committed" is what this step exists to prevent. Never cite a
commit SHA as evidence of safety: it proves the commit exists on this disk and
nothing more, and its precision makes the claim more convincing, not more true.
The incident that taught this is in the reference.

### Step 1 — Inventory

Don't assume docs exist. Glob for `onboarding.md`, `CONTEXT.md`, `DEVLOG.md`,
`spec.md`, and the current handover (`HANDOVER.md`, `docs/.agents/current-handover.md`,
or wherever `onboarding.md` says it lives — its map is the authority). Adapt to
what is missing; the full candidate-path list is in the reference.

### Step 2 — Decide where it goes

**A handover follows the work, not the cwd.** The default is the repo the work
happened in. The case that breaks the default: a session that graduated or
moved work into another repo. The next session on that work starts *there*, and
will never see a handover left in the sandbox.

- Write it in the repo where the next session on that work will start.
- The origin repo keeps its own handover, scoped to itself, **citing the
  departure**: what left, when, where to, what remains.
- A session that touched several repos may owe several handovers, one per repo
  with unfinished business. Never one fat handover in whichever directory you
  were standing in.

### Step 3 — Write it

Use `assets/handover.md`. Three sections: **Orientation** (two sentences;
include the `Durability:` line *only* when something is not pushed),
**The Delta** (active debates, failed paths, in-flight breakage — strictly what
is not in the files), **Next steps** (specific, numbered). Delete any section a
file already covers. Capture the discussion, not just the state: if the next
agent has to ask "why did we choose X?" or "what have we tried?", it failed.

**Overwrite, never delete-and-recreate.** Some IDEs fail to process a file
recreated in the same turn. Edit the existing file; keep its name; create only
if none exists.

### Step 4 — Flush what is Record

Before saving: land any sharpened or coined terms in `CONTEXT.md` if the
project keeps one (terms are Record, not Delta), and make sure the DEVLOG has
the decisions that were made. Then tell the user it is prepared, summarize the
Delta in a sentence, and save.

**Reply:** the durability state per repo (or "unverified"), the handover's
path, and the one-line Delta summary.

---

## Incoming: using one

**A pickup is an inheritance, not an audit.** The previous agent already paid
for what is in the handover and the DEVLOG. Resist re-deriving it. The tell is
a "let me verify from scratch" pass over decisions the trail already records —
that treats the trail as untrustworthy when it is authoritative. Verify the
*build* (tests, a smoke run) because state drifts; do not re-litigate the
*decisions* unless something you observe contradicts them.

1. Read in order: `onboarding.md` (map) → handover (the live feed) → spec /
   DEVLOG only as a question requires.
2. Verify the build immediately.
3. **Prune as you go.** When an in-flight item in the handover is now fixed,
   delete it from the handover before you end your session. Zombie Delta —
   a decision still listed as "in flight" after it was made — is the most
   common rot.
4. **Say so if it was bad.** A novel instead of a delta, or a question the
   handover should have answered: tell the user in one line, and prune it.

**Reply:** what the handover said was in flight, what you verified, and what
you pruned.
