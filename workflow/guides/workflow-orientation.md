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
- Folder existence: `docs/.agents/`, `docs/`, `.claude/`.
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
3. **Handover staleness.** If a current-handover doc exists, parse its "Project Context" section for the sprint/branch reference. Compare against `git rev-parse --abbrev-ref HEAD` and recent commits. Mismatch → flag.
4. **Template completeness.** Each canonical workflow doc has its expected sections:
   - `onboarding.md` should contain: a top-level project heading, a "Getting Oriented" section with doc-location pointers, an "About This Human" section (or reference to `global-preferences.md`), and a "How We Work" / workflow section.
   - `DEVLOG.md` should contain at least one sprint entry with Summary, Decisions, Testing, Concerns/Risks, Next Sprint subsections.
   - The current-handover doc (if used) should contain at minimum: Quick Start, Project Context, This Session's Accomplishments, Conversation Context, Next Steps.

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

## Anti-Patterns

- **Writing during audit.** Don't write a single byte during the audit phase.
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
