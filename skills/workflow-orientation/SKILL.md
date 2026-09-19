---
name: workflow-orientation
description: >-
  Use when entering a project to align it with the sprint-based workflow: empty project (scaffold rails), existing project with no workflow (propose onboarding), partial setup (gap report), canonical-healthy (drift check), or mature project with its own conventions (bridge mode via onboarding.md). Also owns project memory placement: migrating memory out of a harness's global path (~/.claude/projects/...) and into the repo, for private repos only. Always audits read-only first, discusses, then acts non-destructively.
allowed-tools: [Read, Write, Edit, Grep, Glob, Bash]
---

# Workflow Orientation: Audit, Discuss, Adapt

Entering a project — empty, existing, or mature — figure out where it stands
relative to the workflow, say so, and lay down only what is needed without
bulldozing what is there. The deliverable in every state is an accurate
`onboarding.md`: `start`, `lifecycle-manager` and `handover-manager` all read it
to find where things live, so getting that file right is the point.

Templates, the candidate path list and the memory-migration boilerplate are in
`assets/workflow-orientation-reference.md`; each step points at what it needs.

Three phases, always in order: **Audit** (read-only, no questions), **Discuss**
(present, propose), **Act** (confirmed actions only). Never skip Discuss. In a
non-empty project, never act without explicit confirmation.

---

## 1. Audit

Classify into exactly one state. Check in this order; first match wins.

| State | Signals |
|---|---|
| **Empty** | no source files beyond README / LICENSE / .gitignore-style boilerplate |
| **Mature-divergent** | source + a structured doc system with non-canonical names (`CONTRIBUTING.md`, a `docs/` tree of its own, several committers in `git log`) |
| **Code, no workflow** | source + no `onboarding.md`, `DEVLOG.md`, handover doc or `docs/.agents/` anywhere |
| **Partial** | at least one canonical doc present, at least one missing or visibly incomplete |
| **Canonical-healthy** | all canonical docs present with their expected sections |

These are heuristics: report confidence (high / medium / low) with the
classification. Between mature-divergent and partial, default to partial and
ask before treating the project as divergent.

**How to check.** Glob for each canonical doc at its candidate locations (list
in the reference) — never conclude "missing" from one hardcoded path. Count
source files outside boilerplate (<3 → empty). Count unique committers (>1
suggests an external project). Note `CONTRIBUTING.md`, `CODE_OF_CONDUCT.md`,
`.github/ISSUE_TEMPLATE/`. Check for out-of-repo memory (§6). Existence plus a
title-and-first-paragraph skim is enough; don't read whole files, and don't
write a byte.

---

## 2. Per-state behaviour

**Empty.** One batched confirmation for three things: an empty `docs/.agents/`
(the home for agent meta-docs like `current-handover.md`; do *not* copy guide
content in — the plugin provides guides at runtime), `onboarding.md` via
`human-training:onboarding-creator` told the project is empty so it emits a
skeleton with the candidate paths and no inferences, and a `DEVLOG.md`
skeleton (in the reference). Never `spec.md` — that is `project-genesis`'s
output. Then ask once: "Want to flesh out the idea now?" Yes → invoke
`human-training:project-genesis`. No → stop; the rails are in place.

**Code, no workflow.** Read-only first: infer purpose, stack and structure from
the manifest (`package.json`, `pyproject.toml`, `Cargo.toml`…), the README and
the entry point — a sample, not the codebase. Then propose, confirming each
item: an `onboarding.md` draft with inferences pre-filled (compose it with
`onboarding-creator`, review the draft inline before writing), a `DEVLOG.md`
skeleton whose first entry says prior history is not captured, and a
*discussion* of the handover convention before any handover file exists. Do not
retroactively write `spec.md`; do not assume tests or CI exist.

**Partial.** A gap report: one row per canonical doc, status (present /
incomplete / missing) and the recommended action (table in the reference).
Confirm each row individually. Never offer "fix everything".

**Canonical-healthy — drift check.** Five signals, reported inline, never
written to a file, each flag with its own "want me to fix this one?":

1. Every path in `onboarding.md`'s "Getting Oriented" resolves.
2. DEVLOG freshness: commits since the last entry's date
   (`git log --since=<date> --oneline | wc -l`) — volume without an entry is a flag.
3. Handover staleness: its Orientation sprint/branch versus `git rev-parse
   --abbrev-ref HEAD` and recent commits; and its Durability line versus
   `git status -sb`. A handover claiming a clean stop while the branch reads
   `[ahead N]` is stale in the way that costs work, not just accuracy.
4. Template completeness (expected sections in the reference). A short handover
   is a healthy one — flag it for duplicating the DEVLOG, never for brevity.
5. Spec divergence: `git log -- spec.md` commits since the DEVLOG last mentioned
   the spec.

**Mature-divergent — bridge mode.** Survey titles and first paragraphs only
(README, CONTRIBUTING, CODE_OF_CONDUCT, `docs/`, `.github/`) and map each
workflow concept to its functional equivalent: onboarding ≈ README +
CONTRIBUTING; DEVLOG ≈ commits or release notes; handover ≈ usually nothing;
spec ≈ a design doc, RFC or big issue. Propose a *bridging* `onboarding.md`
whose "Getting Oriented" points at the project's actual files and names the
concepts with no equivalent. For what is genuinely missing (usually a handover
convention) offer minimal scaffolding only, on confirmation, somewhere that
doesn't fight the existing layout. Don't impose canonical names on a project
that has its own. The user may veto bridge mode and keep just the report.

---

## 3. Discuss

Present the audit as state + confidence, key findings, proposed actions
(format in the reference), then **wait**. Walk through actions one at a time
(all states except Empty, which batches).

## 4. Action authority

| Action | Authority | Confirmation |
|---|---|---|
| Audit (read, grep, git log) | HIGH | none |
| Scaffold an empty project | HIGH | one batch: "these N files, proceed?" |
| Add files to a non-empty project | MODERATE | per file: path + preview, then write |
| Modify an existing workflow doc | LOW | show the diff, discuss, write on explicit go |
| Touch a file the user authored outside this workflow | NEVER | discuss only |
| Delete anything | NEVER | not a power this skill has |

## 5. The deliverable

Every state ends with an accurate `onboarding.md` at the project's standard
location. Canonical states point it at canonical paths; bridge mode points it
at the project's own files. Same artifact, same downstream readers. Compose it
with `onboarding-creator` — never re-implement that logic here.

---

## 6. Project memory belongs in the repo

Some harnesses keep per-project memory outside the project in a path derived
from the working directory — Claude Code uses `~/.claude/projects/<slug>/memory/`.
Right for a multi-contributor repo; **wrong for a solo developer on more than
one machine**, and it fails silently: nothing pushes it, no handover carries
it, and the other machine simply doesn't know. It surfaces as a human noticing
the agent forgot something they are certain they said.

> **If the repo is not public, memory lives in the repo** — `memory/`, indexed
> by `memory/MEMORY.md`. If the repo is public, leave it at the harness default:
> memory records how a human works and what they've corrected, and in-repo
> memory gets pushed.

**Visibility**, cheapest first: `gh repo view --json visibility -q .visibility`;
no remote or not a git repo → nothing can be published, treat as private; `gh`
missing or unauthenticated → **unknown — ask once and record the answer in the
repo** so it is decided once, not every session. Never guess: guessing
"private" on a public repo publishes the memory.

**Finding the global directory.** `<slug>` is the cwd with `:`, `\`, `/` and
`_` each replaced by `-` (`P:\software_projects\Blendy_McBlendface` →
`P--software-projects-Blendy-McBlendface`). **The slug is case-sensitive to how
the path was typed**: a session launched from `p:\` gets a different, empty
memory with no warning. If the derived slug finds nothing, list
`~/.claude/projects/` and match case-insensitively; two case-variants both
present is a fork — surface it, never merge unilaterally.

**Migrating** — only after Discuss, only on a private repo, boilerplate in the
reference:

1. Copy every `*.md` from the global directory into `<repo>/memory/`. If the
   repo already has entries, merge by filename and **surface collisions** — a
   name in both places is two canonicals, which is itself the finding.
2. Verify the copies are byte-identical before touching anything else.
3. Rebuild `memory/MEMORY.md` as the index, one line per entry. A global index
   is a starting point, not the answer.
4. **Plant the pointer in `CLAUDE.md`** at the project root, creating it if
   absent. This is the step that makes it work: `CLAUDE.md` is the only
   project-local file most harnesses load every session — `onboarding.md` is
   not, skills are not. Migrating without it makes the memory invisible and
   looks like it was lost, which is worse than not migrating.
5. Tombstone the global `MEMORY.md` with a pointer at the repo. Do **not**
   delete the directory (§4, and the harness may recreate it anyway); the
   index is read automatically every session, so it is the one place a
   redirect is guaranteed to be seen.
6. Tell the user the global folder is still on disk and removing it is theirs.

From then on, new memory goes to `<repo>/memory/` with a line in
`memory/MEMORY.md`. **Never write to the harness's global path**, even when it
is the documented default and already exists — a tombstoned directory that
starts accumulating fresh entries is the duplicate-canonical problem wearing a
hat.

---

**Reply:** the state and confidence, the findings that drove it, the actions
taken (each with its confirmation), what was proposed and declined, and the
path of the resulting `onboarding.md`.
