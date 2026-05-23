# Workflow Orientation — Design Spec

**Date:** 2026-05-23
**Status:** Approved, ready for implementation planning
**Plugin:** human-training
**New skill:** `workflow-orientation`

---

## Problem

The human-training plugin gives Claude Code a repeatable session loop — onboarding, sprint-based development, handovers between sessions. But the loop only works if a project has the workflow scaffolding in place. Today there is no entry point that handles the moments when scaffolding is missing, partial, or divergent from the human-training conventions.

Concrete failure modes:

1. **Empty project, no rails.** Brad summons Claude into an empty folder. Work starts. Context swells. When he finally tries to set up onboarding/handover docs, he's at the worst possible moment — low context budget, fatigued, mid-feature.
2. **Existing project, no workflow.** Brad opens a personal project that grew organically without any of the human-training conventions. He wants the rails in place but doesn't want to scaffold them by hand.
3. **Mature project with its own conventions.** Brad opens a project (his own from months ago, or someone else's) that has *some* doc system — a README, a CONTRIBUTING.md, ad-hoc notes — but doesn't match the human-training mental model. He wants to work in his style without bulldozing what's there.
4. **Drift in a previously-set-up project.** Brad returns to a project that *did* have the workflow set up. He doesn't know whether onboarding.md is still accurate, whether DEVLOG has fallen behind git activity, whether handover references are stale.

The shared root cause: no skill diagnoses project state and proposes appropriate, non-destructive action.

## Goals

- Single entry point that adapts behavior based on detected project state.
- Read-only audit pass before any action. Never modify files without confirmation in non-empty projects.
- Preserve and bridge to existing conventions where they exist; do not impose canonical structure on projects that already have working systems.
- Produce a deliverable (an accurate `onboarding.md`) that the rest of the human-training skills can consume without modification.
- Fail safe: in any ambiguous state, surface the ambiguity to the user rather than guess.

## Non-goals

- Auto-fixing drift. Drift is flagged; fixes are user-confirmed per-item.
- Authoring `spec.md` for existing projects. Specs are written by `project-genesis` (forward-looking, idea-driven). Retroactive spec generation is out of scope.
- Modifying any file the user didn't author through this workflow (existing READMEs, contributor guides, etc.).
- Deleting any files. Stale template copies in `docs/.agents/` are left for `onboarding-creator`'s existing cleanup logic.
- Cross-tool support beyond what's already in the plugin. (This skill follows the existing `docs/.agents/` convention and the model-agnostic pitch.)

## Design Overview

One new skill: `workflow-orientation`, living at `skills/workflow-orientation/SKILL.md` in the plugin source and generated to the user-facing namespace as `human-training:workflow-orientation`.

On invocation, the skill executes in three phases:

1. **Audit (read-only).** Classify project state. No filesystem writes.
2. **Discuss.** Present findings to the user. Propose actions appropriate to the detected state.
3. **Act.** Take confirmed actions. Authority level scales with risk (see Action Authority).

The skill's universal output across all states is an accurate, current `onboarding.md`. This is the unifying artifact: every other skill in the plugin already consumes `onboarding.md` to locate workflow documents, so getting that file right makes the plugin's downstream behavior correct in every project state, including bridge-mode mature-divergent projects.

## State Detection

The audit pass classifies the project into exactly one of five states. Detection runs in this order; first match wins.

| State | Detection signals |
|-------|-------------------|
| **Empty** | No source files outside README/LICENSE/.gitignore-style boilerplate. |
| **Mature-divergent** | Source code present + existing structured doc system that diverges from human-training canonical names. Heuristics: presence of CONTRIBUTING.md, docs/ folder with non-canonical structure, multiple committers in git log suggesting external project, etc. Conservative: when uncertain between divergent and partial, classify as partial. |
| **Code, no workflow** | Source code present + no onboarding.md / DEVLOG.md / handover doc / docs/.agents/ folder anywhere. |
| **Partial** | At least one canonical workflow doc present, at least one missing or visibly incomplete. |
| **Canonical-healthy** | All canonical workflow docs present and structurally complete (template sections present). |

Heuristics — not certainties. The audit reports its classification *and* its confidence; if confidence is low, the discussion phase asks the user to confirm before acting.

## Per-State Behaviors

### State 1: Empty

**Actions, batched into one confirmation:**

- Create `docs/.agents/` and copy in the template guides currently shipped in the plugin's `skills/*/assets/` directories — specifically the meta-guides agents need to reference (handover-guide.md, ideation-protocol.md, spec-writing-guide.md). Reuse the existing template files rather than duplicating content.
- Create `onboarding.md` at project root from the existing skeleton in `workflow/templates/onboarding.md`, with the "Getting Oriented" section pre-filled to point at the standard locations.
- Create `DEVLOG.md` skeleton from `workflow/templates/devlog.md`.

**Then ask:** "Want to flesh out the idea now?" → if yes, invoke `project-genesis`. If no, stop. Rails are in place.

No `spec.md` is created — that's `project-genesis`'s output.

### State 2: Code, no workflow

**Audit additionally:**

- Sample the codebase to infer purpose, stack, structure. Read package.json/pyproject.toml/equivalent. Read top-level README if present. Skim entry-point files. Do not read everything.

**Then propose:**

- Draft `onboarding.md` with inferences pre-filled. User reviews draft before write.
- Offer `DEVLOG.md` skeleton with a "Pre-skill history" section noting that prior work isn't captured.
- Discuss handover location convention with the user before any handover-related file is created.

No retroactive `spec.md`. No assumption about what tests/CI exist.

### State 3: Partial

**Discussion output is a gap report:**

| Doc | Status | Recommended action |
|-----|--------|-------------------|
| onboarding.md | present but missing Getting Oriented section | propose patch |
| DEVLOG.md | missing | propose skeleton |
| handover | missing | discuss convention |
| docs/.agents/ | missing handover-guide.md | propose copy from template |

Each row gets per-item confirmation. No bulk action.

### State 4: Canonical-healthy (drift check)

**Drift signals checked:**

1. **Path resolution.** Every file path mentioned in `onboarding.md`'s "Getting Oriented" section resolves to a real file. Broken pointers flagged.
2. **DEVLOG freshness.** Compare the last DEVLOG entry's sprint reference and date against git activity since. Significant lag flagged.
3. **Handover staleness.** If a current-handover doc exists, check whether its referenced sprint/branch/state matches the actual current branch and recent commits. Mismatch flagged.
4. **Template completeness.** Each canonical workflow doc has the required template sections from `workflow/templates/`. Missing sections flagged.
5. **Spec divergence.** If `spec.md` exists, check whether its acceptance criteria have been touched since last DEVLOG mention. Untracked spec changes flagged.

Output is a short markdown report inline in the conversation (not written to a file). Each flagged item gets a "want me to fix this one?" prompt. No bulk auto-fix.

### State 5: Mature-divergent (bridge mode)

**Audit additionally:**

- Survey existing doc structure. Read README, CONTRIBUTING.md, docs/ folder contents (titles and first paragraphs only — do not deep-read).
- Identify the *functional equivalent* of each human-training concept in the project's existing system. Examples: their README + CONTRIBUTING may cover what onboarding.md does; they may have no handover system at all; their commit messages may serve as a de-facto devlog.

**Then propose:**

- A new `onboarding.md` that bridges. It does *not* impose canonical structure; it documents the project's actual structure in terms the other human-training skills can consume.
- The "Getting Oriented" section points at the project's actual files (their CONTRIBUTING, their docs/, etc.) and notes which concepts have no equivalent in the project.
- For genuinely missing pieces (usually just a handover convention), offer to add minimal scaffolding — but only with explicit confirmation, and at locations that don't fight the project's existing structure.

Discussion happens before any write. The user can veto bridge-mode entirely and walk away with just the audit report.

## Action Authority

Mapped to the user's existing confidence bar:

| Action | Authority | Confirmation |
|--------|-----------|--------------|
| Audit pass (read, grep, git log) | HIGH | None — read-only |
| Scaffold files in empty project | HIGH | Single batch ("here's the 5 files I'll create, proceed?") |
| Add new files in non-empty project | MODERATE | Per-file: path + content preview, confirm before write |
| Modify existing workflow files | LOW | Show diff, discuss, write only on explicit go-ahead |
| Touch files user didn't author through this workflow | NEVER | Always discuss; never auto-modify |
| Delete any file | NEVER | Not a power this skill has |

## Interaction with Existing Skills

- **`onboarding-creator`** — `workflow-orientation` reuses its onboarding.md authoring logic rather than reimplementing. Implementation may require extracting a small shared helper or invoking the skill internally. `onboarding-creator` remains the canonical entry point for direct onboarding work.
- **`project-genesis`** — unchanged. `workflow-orientation` chains into it for the State 1 empty-project flow when the user opts in.
- **`handover-manager`** — unchanged. Already references `onboarding.md` (with planned fuzziness on paths) for orientation and instructs next-agent flows to read it first. Bridge-mode works for it as-is.
- **`lifecycle-manager`** — needs a small update. Currently its "Joining a Moving Train" section sends the agent directly to DEVLOG and the current handover at default locations. For bridge mode to work, it needs an orientation step that reads `onboarding.md` first (if present) to resolve document paths from the "Getting Oriented" section, then proceeds. Falls back to default search if no `onboarding.md` is found. Single-section edit; no structural change.

No existing skill becomes load-bearing on a new file type. The plugin stays coherent.

## Files to Add

Source files (in `workflow/` — the model-agnostic source of truth):

- `workflow/guides/workflow-orientation.md` — the skill body, following the existing pattern where `workflow/guides/*.md` is the source and `skills/*/SKILL.md` is generated.

Generated by `scripts/build-skills.ps1` (and `.sh`):

- `skills/workflow-orientation/SKILL.md`
- `skills/workflow-orientation/assets/` if any template references are needed (likely none — assets stay in the canonical `workflow/templates/` and are referenced by path).

Build script update:

- `scripts/build-skills.ps1` and `scripts/build-skills.sh` — add `workflow-orientation` to the skills list these scripts generate.

Existing files to modify:

- `workflow/guides/lifecycle.md` (source of truth for `lifecycle-manager`'s SKILL.md) — update the "Joining a Moving Train" section to read `onboarding.md` first (when present) and resolve document paths from its "Getting Oriented" section, with fallback to default search if absent.

CI:

- `.github/workflows/verify-skills.yml` — no change needed if it already iterates over all `skills/` subdirectories.

Plugin version:

- `.claude-plugin/plugin.json` — bump version (1.0.0 → 1.1.0 for the new skill).

Documentation:

- `README.md` — add `workflow-orientation` to the list of skills under "For Claude Code Specifically" and to the directory tree.

## Future Considerations (Out of Scope for This Spec)

- **Hooks for automatic invocation.** A SessionStart hook could auto-run the audit when Claude Code starts in a project. Deferred: hooks are a separate concern and the manual invocation pattern is sufficient for v1.
- **Schema for bridge-mode metadata.** If bridge mode proves to need richer mapping than `onboarding.md` can express, a dedicated `docs/.agents/workflow-map.md` schema could emerge. v1 keeps everything in `onboarding.md`; revisit only if friction shows up.
- **Multi-project audit.** Running across a directory of projects to surface which ones need attention. Out of scope.
- **State 4 auto-fix mode.** Currently every drift fix is per-item confirmed. A future "auto-fix safe drift" option could batch low-risk fixes (broken path pointers to obvious renames, etc.).

## Open Questions

None blocking. Implementation can begin.
