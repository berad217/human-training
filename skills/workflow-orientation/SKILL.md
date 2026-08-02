---
name: workflow-orientation
description: >-
  Use when entering a project to align it with the sprint-based workflow: empty project (scaffold rails), existing project with no workflow (propose onboarding), partial setup (gap report), canonical-healthy (drift check), or mature project with its own conventions (bridge mode via onboarding.md). Also owns project memory placement: migrating memory out of a harness's global path (~/.claude/projects/...) and into the repo, for private repos only. Always audits read-only first, discusses, then acts non-destructively.
allowed-tools: [Read, Write, Edit, Grep, Glob, Bash]
---

# Workflow Orientation: Audit, Discuss, Adapt

**Purpose**: When you're invoked in a project — empty, existing, or mature — figure out what state the project is in relative to the human-training workflow, discuss it with the user, and lay down whatever's needed without bulldozing what's already there.

The unifying deliverable across every state is an accurate `onboarding.md`. Other skills (`lifecycle-manager`, `handover-manager`) consume `onboarding.md` to find the project's workflow documents. Getting that file right is the point.

---

## The Three Phases

1. **Audit (read-only)** — Classify the project. No filesystem writes. No questions asked.
2. **Discuss** — Present what you found. Propose actions appropriate to the state.
3. **Act** — Take confirmed actions. Authority scales with risk (see §4).

Run them in order. Never skip discuss. Never act without explicit user confirmation in non-empty projects.

---

## 1. The Audit

Classify the project into exactly one of five states. Run checks in this order; first match wins.

### State Detection

| State | Detection signals |
|-------|-------------------|
| **Empty** | No source files outside README/LICENSE/.gitignore-style boilerplate. |
| **Mature-divergent** | Source code + structured doc system with non-canonical names: `CONTRIBUTING.md` present, `docs/` folder with non-human-training structure, multiple committers in `git log`. |
| **Code, no workflow** | Source code present + no `onboarding.md` / `DEVLOG.md` / handover doc / `docs/.agents/` folder anywhere. |
| **Partial** | At least one canonical workflow doc present, at least one missing or visibly incomplete. |
| **Canonical-healthy** | All canonical workflow docs present, all template sections present. |

**Heuristics, not certainties.** When you classify, also report your confidence (high/medium/low). If you're between mature-divergent and partial, default to partial and ask the user before treating it as divergent.

### What to Check

- File existence: check each canonical doc at its candidate locations:
  - `onboarding.md`: project root, `./docs/onboarding.md`, `./docs/.agents/onboarding.md`
  - `DEVLOG.md`: project root, `./docs/devlog.md`, `./docs/DEVLOG.md`
  - Handover: `./HANDOVER.md`, `./docs/.agents/current-handover.md`, `.agents/current-handover.md`, legacy `.claude/current-handover.md`
  - Global preferences: `./docs/.agents/global-preferences.md`, legacy `.agents/global-preferences.md`
  - Project memory: `./memory/MEMORY.md`, `./docs/memory/MEMORY.md`
- Folder existence: `docs/.agents/`, `docs/`, `.claude/`, `memory/`.
- **Out-of-repo memory:** does a global memory directory exist for this project? See §6.
- Source-code heuristic: count source files outside boilerplate. <3 → empty; >0 → has code.
- Git history: `git log --pretty=format:"%an" | sort -u | wc -l` for committer count; >1 unique committer suggests external project.
- Doc structure cues: presence of `CONTRIBUTING.md`, `CODE_OF_CONDUCT.md`, `.github/ISSUE_TEMPLATE/`, or a substantial `docs/` tree without canonical names.

Don't read entire files during the audit. Existence checks plus title + first-paragraph skim are sufficient.

---

## 2. Per-State Behavior

### State 1: Empty

Batch the following into one user confirmation:

- Create an empty `docs/.agents/` folder. This is the canonical home for agent-facing meta-docs (e.g., `current-handover.md`) that will accumulate as work proceeds. Do NOT copy guide content into the project — the plugin provides the guides at runtime via skill invocation.
- Create `onboarding.md` at project root by invoking `human-training:onboarding-creator`. Tell it the project is empty so it produces a skeleton with the candidate doc paths listed above (under "What to Check") and no project-specific inferences.
- Create `DEVLOG.md` at project root with this minimal skeleton:

  ````markdown
  # Development Log - <Project Name>

  ## Sprint 0 - Genesis

  **Status:** Not yet started.

  ---

  <!-- Sprint entries accumulate below as work proceeds. Each entry: Summary, Decisions, Testing, Concerns/Risks, Next Sprint. -->
  ````

Do NOT create `spec.md` — that is `project-genesis`'s output.

Then ask: **"Want to flesh out the idea now?"** If yes, invoke `human-training:project-genesis`. If no, stop. Rails are in place for whenever an idea arrives.

### State 2: Code, no workflow

Audit additionally (read-only):

- Sample the codebase to infer purpose, stack, structure. Read `package.json` / `pyproject.toml` / `Cargo.toml` / equivalent. Read the README if present. Skim the entry-point file(s). Do not read the whole codebase.

Propose, with per-item user confirmation:

- An `onboarding.md` draft with inferences pre-filled. User reviews the draft inline before you write it. Use `human-training:onboarding-creator` to compose, passing the inferences as inputs.
- A `DEVLOG.md` skeleton with a "Pre-skill history" section noting that prior work is not captured (because git pre-dates the workflow).
- Discuss the handover convention with the user before creating any handover-related file.

Do NOT retroactively write `spec.md`. Do NOT assume tests or CI exist.

### State 3: Partial

Produce a gap report. For each canonical doc, mark status and recommended action:

| Doc | Status | Recommended action |
|-----|--------|--------------------|
| `onboarding.md` | present / present-but-incomplete / missing | propose patch / propose creation / skip |
| `DEVLOG.md` | same options | same options |
| Handover doc | same options | same options |
| `docs/.agents/` meta-guides | check each | propose copy from plugin assets |

Confirm each row individually. Do NOT offer a single "fix everything" action.

### State 4: Canonical-healthy (drift check)

Check these signals:

1. **Path resolution.** Every file path referenced in `onboarding.md`'s "Getting Oriented" section resolves to a real file. Use a Bash check for each path.
2. **DEVLOG freshness.** Read the last DEVLOG entry. Compare its referenced sprint number and date against `git log --since=<last-devlog-date> --oneline | wc -l`. Significant commit volume without a new DEVLOG entry → flag.
3. **Handover staleness.** If a current-handover doc exists, parse its "Orientation" section for the sprint/branch reference. Compare against `git rev-parse --abbrev-ref HEAD` and recent commits. Mismatch → flag. Also check its Durability line against `git status -sb`: a handover claiming a clean stop while the branch reads `[ahead N]` is stale in the way that costs work, not just accuracy.
4. **Template completeness.** Each canonical workflow doc has its expected sections:
   - `onboarding.md` should contain: a top-level project heading, a "Getting Oriented" section with doc-location pointers, an "About This Human" section (or reference to `global-preferences.md`), and a "How We Work" / workflow section.
   - `DEVLOG.md` should contain at least one sprint entry with Summary, Decisions, Testing, Concerns/Risks, Next Sprint subsections.
   - The current-handover doc (if used) should contain: Orientation, The Delta, Next Steps — plus a Durability line whenever work is unpushed. Note what is *not* required: a "what we accomplished" section is a status report, belongs in the DEVLOG, and its absence is correct rather than a gap. A short handover is a healthy one; flag a handover for duplicating the DEVLOG, not for being brief.

   Missing required sections → flag.
5. **Spec divergence.** If `spec.md` exists, check `git log -- spec.md` for commits since the last DEVLOG mention of "spec". Untracked spec edits → flag.

Output is a short inline markdown report — do NOT write the report to a file. Each flagged item gets its own "want me to fix this one?" prompt. No bulk auto-fix mode in v1.

### State 5: Mature-divergent (bridge mode)

Audit additionally (read-only):

- Survey the existing doc structure. Read titles + first paragraphs only for: README, CONTRIBUTING.md, CODE_OF_CONDUCT.md, files in `docs/`, files in `.github/`.
- Identify the *functional equivalent* of each human-training concept in the project's existing system:
  - Onboarding ≈ README + CONTRIBUTING.md (usually)
  - DEVLOG ≈ commit messages or release notes (often nothing closer)
  - Handover ≈ usually missing entirely
  - Spec ≈ a design doc, RFC, or substantial issue (varies)

Propose:

- A new `onboarding.md` at project root that *bridges*. It does NOT impose canonical structure. Its "Getting Oriented" section points at the project's actual files (their CONTRIBUTING, their docs/, etc.) and notes which concepts have no equivalent.
- For genuinely missing pieces (usually just a handover convention), offer minimal scaffolding only — and only with explicit confirmation, at a location that does not fight the project's existing structure (e.g., `.agents/current-handover.md` if they already use dot-prefixed dirs).

Discussion happens before any write. The user can veto bridge mode entirely and walk away with just the audit report.

---

## 3. The Discussion Phase

After the audit, present findings as a concise summary:

```
**Project state:** <state-name> (confidence: <high|medium|low>)

**Key findings:**
- <observation>
- <observation>

**Proposed actions:**
- <action 1>
- <action 2>
```

Wait for the user's response. Do NOT act yet.

When the user is ready, walk through actions one at a time (States 2-5) or batch them with single confirmation (State 1). Match the action-authority rules below.

---

## 4. Action Authority

Maps to the confidence bar from `lifecycle.md` §2:

| Action | Authority | Confirmation pattern |
|--------|-----------|----------------------|
| Audit pass (read, grep, git log) | HIGH | None — read-only |
| Scaffold files in empty project | HIGH | Single batch: "here's the N files I'll create, proceed?" |
| Add new files in non-empty project | MODERATE | Per-file: path + content preview, confirm before each write |
| Modify existing workflow files | LOW | Show diff, discuss, write only on explicit go-ahead |
| Touch a file the user did not author through this workflow | NEVER | Always discuss; never auto-modify |
| Delete any file | NEVER | Not a power this skill has |

---

## 5. Universal Deliverable: onboarding.md

Every state ends with an accurate, current `onboarding.md` at the project's standard location (project root, or wherever the project keeps its docs). This is what makes downstream skills work without modification:

- `handover-manager` reads `onboarding.md` to know where things live.
- `lifecycle-manager` reads `onboarding.md` first when joining a moving train (see lifecycle.md §1).

For bridge mode (State 5), `onboarding.md`'s "Getting Oriented" section points at the project's actual files. For canonical states (1-4), it points at canonical locations. Same artifact, different contents, same downstream consumers.

---

## 6. Project memory belongs in the repo

Some agent harnesses keep per-project memory **outside the project**, in a
home-directory path derived from the working directory — Claude Code uses
`~/.claude/projects/<slugified-cwd>/memory/`. That default is right for a repo
with several contributors, where "how this human and this agent work together"
shouldn't be committed for everyone else to carry.

**It is wrong for a solo developer working across more than one machine**, and
it fails silently: memory written there travels with no push and no handover, so
the other machine simply doesn't know. Nobody gets an error. The usual way it
surfaces is a human noticing an agent has forgotten something they're certain
they said.

### The rule

> **If the repo is not public, project memory lives in the repo** — `memory/`,
> indexed by `memory/MEMORY.md`. If the repo is public, leave memory at the
> harness default.

Public is the multi-contributor case the default was designed for, and in-repo
memory gets *pushed* — memory records how a human works, what they've corrected,
sometimes their frustrations. Fine in private, a deliberate choice in public.

**Determining visibility** — cheap, in order:

1. `gh repo view --json visibility -q .visibility` → `PUBLIC` / `PRIVATE`.
2. No remote, or not a git repo → nothing can be published → **treat as
   private**, in-repo is safe.
3. `gh` missing or unauthenticated → **unknown. Ask once, then record the answer
   in the repo** (a line in `memory/MEMORY.md` or `CLAUDE.md`) so it is decided
   once per project rather than re-derived every session. Never guess: guessing
   "private" on a public repo publishes the memory.

### Finding the out-of-repo directory

The Claude Code path is `~/.claude/projects/<slug>/memory/`, where `<slug>` is
the working directory with `:`, `\`, `/` and `_` each replaced by `-`. So
`P:\software_projects\Blendy_McBlendface` becomes
`P--software-projects-Blendy-McBlendface`.

**The slug is case-sensitive to how the path was typed.** Launching from
`p:\...` instead of `P:\...` produces a *different* directory and therefore a
*second, empty* memory, with no warning. If the derived slug finds nothing, list
`~/.claude/projects/` and match case-insensitively before concluding there is no
memory — and if two case-variants both exist, that is a fork: surface it, don't
merge unilaterally.

### Migrating (only after the discussion phase, only on a private repo)

1. **Copy** every `*.md` from the global memory directory into `<repo>/memory/`.
   If the repo already has entries, **merge by filename and surface any
   collision** rather than overwriting — a name in both places means two
   canonicals, which is itself the finding.
2. **Verify** the copies are byte-identical before touching anything else.
3. **Rebuild `memory/MEMORY.md`** as the index: one line per entry. If the
   global copy had an index, its content is a starting point, not the answer —
   entries may have been added or dropped.
4. **Plant the pointer in `CLAUDE.md`** at project root, creating the file if it
   doesn't exist. This is the step that makes the whole thing work: **`CLAUDE.md`
   is the only project-local file most harnesses auto-load every session.**
   `onboarding.md` is not; skills are not. Without this line, in-repo memory is
   invisible to any session that doesn't happen to run an orientation skill.
   ```markdown
   ## Memory is repo-local
   Project memory lives in `memory/`, indexed in `memory/MEMORY.md`. Never write
   memory to `~/.claude/` — it does not travel between machines. If your harness
   hands you a global memory directory, override it and write here instead.
   ```
5. **Tombstone the global index.** Replace the global `MEMORY.md` with a pointer
   at the repo. Do **not** delete the global directory — deletion is not this
   skill's power (§4), and the harness may re-create the folder anyway. A
   tombstone is better than a deletion here regardless: that file gets read
   automatically every session, so it is the one place a redirect is guaranteed
   to be seen.
   ```markdown
   # Moved
   This project's memory now lives in `<repo path>/memory/`, indexed in
   `memory/MEMORY.md`. Read it there. Do not write memory here — it does not
   travel between machines.
   ```
6. **Tell the user the global folder is still on disk** and that removing it is
   theirs to do.

### Writing memory from then on

New memory goes to `<repo>/memory/` with a pointer line appended to
`memory/MEMORY.md`. **Never write to the harness's global path**, even when it
is the documented default and even when it already exists — a tombstoned
directory that starts accumulating fresh entries is the duplicate-canonical
problem wearing a hat.

---

## Anti-Patterns

- **Writing during audit.** Don't write a single byte during the audit phase.
- **Migrating memory out of a public repo's default.** The rule is private-only.
  On a public repo the harness default is correct — don't "fix" it.
- **Migrating without planting the `CLAUDE.md` pointer.** The move succeeds, the
  memory becomes invisible, and it looks like the memory was lost. Worse than
  not migrating.
- **Bulk auto-fix.** Each non-empty-project change gets its own confirmation. No "fix everything" button.
- **Overwriting user-authored files.** Never modify a file the user authored outside this workflow without explicit per-file confirmation.
- **Inventing convention.** When the project has its own structure, bridge to it. Don't impose human-training canonical names.
- **Retroactive spec generation.** Don't write `spec.md` for existing projects. That's `project-genesis`'s job for forward-looking idea work.
- **Skipping discuss.** Never go from audit straight to act without surfacing what you found.
- **Reimplementing onboarding-creator.** When you need to compose `onboarding.md`, invoke `human-training:onboarding-creator`. Don't duplicate its logic here.

---

## Quick Reference

Invocation order in every project:

1. Audit (read-only state detection)
2. Discuss findings + propose actions
3. Act on confirmed actions
4. Universal output: accurate `onboarding.md`
