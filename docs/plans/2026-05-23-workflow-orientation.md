# Workflow Orientation Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add a new `workflow-orientation` skill to the human-training plugin that audits any project's workflow state, discusses findings non-destructively, and scaffolds or bridges as appropriate. Update `lifecycle-manager` to consult `onboarding.md` so bridge mode propagates through the whole plugin.

**Architecture:** New skill source at `workflow/guides/workflow-orientation.md` (the model-agnostic source of truth), generated to `skills/workflow-orientation/SKILL.md` by the existing build pipeline. Both `build-skills.ps1` and `build-skills.sh` are extended to register the new skill. `workflow/guides/lifecycle.md`'s "Joining a Moving Train" section is updated to read `onboarding.md` first (with fallback to defaults), making bridge mode work transparently for downstream skills. Plugin version bumps 1.0.0 → 1.1.0.

**Tech Stack:** Markdown content authored in `workflow/`. PowerShell + Bash build scripts generate `skills/`. CI (`.github/workflows/verify-skills.yml`) verifies both builders produce byte-identical output. Plugin manifest at `.claude-plugin/plugin.json`. Local-dev loop via `claude --plugin-dir .`.

**Repo root in all paths below:** `D:\Coding_projects\human-training\` (Windows). Use forward slashes in bash; back- or forward-slashes in PowerShell.

**Spec:** `docs/specs/2026-05-23-workflow-orientation-design.md`

---

## Task 1: Author the workflow-orientation guide source

**Files:**
- Create: `workflow/guides/workflow-orientation.md`

- [ ] **Step 1: Create the guide file with the full skill body**

Write exactly the following content to `workflow/guides/workflow-orientation.md`:

```markdown
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

- File existence: `onboarding.md`, `DEVLOG.md`, `HANDOVER.md` plus the `./docs/...` and `./docs/.agents/...` variants (see the planned-fuzziness list in the onboarding-creator skill).
- Folder existence: `docs/.agents/`, `docs/`, `.claude/`.
- Source-code heuristic: count source files outside boilerplate. <3 → empty; >0 → has code.
- Git history: `git log --pretty=format:"%an" | sort -u | wc -l` for committer count; >1 unique committer suggests external project.
- Doc structure cues: presence of `CONTRIBUTING.md`, `CODE_OF_CONDUCT.md`, `.github/ISSUE_TEMPLATE/`, or a substantial `docs/` tree without canonical names.

Don't read entire files during the audit. Existence checks plus title + first-paragraph skim are sufficient.

---

## 2. Per-State Behavior

### State 1: Empty

Batch the following into one user confirmation:

- Create `docs/.agents/` and copy in the meta-guides agents reference: `handover-guide.md`, `ideation-protocol.md`, `spec-writing-guide.md`. Source these from this plugin's existing assets (e.g. `${CLAUDE_PLUGIN_ROOT}/skills/handover-manager/assets/`, `${CLAUDE_PLUGIN_ROOT}/skills/project-genesis/assets/`).
- Create `onboarding.md` at project root by invoking `human-training:onboarding-creator` (rather than duplicating its logic). Pass through that the project is empty so it produces a skeleton with planned-fuzziness paths and no project-specific inferences.
- Create `DEVLOG.md` skeleton from `${CLAUDE_PLUGIN_ROOT}/skills/lifecycle-manager/assets/devlog.md` (if present) or use a minimal sprint-0 skeleton.

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
4. **Template completeness.** Each canonical workflow doc has its expected template sections. For `onboarding.md`, the expected sections are listed in the onboarding-creator skill body. For DEVLOG and handover, see their respective templates.
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
```

- [ ] **Step 2: Verify the file was written correctly**

Run:
```bash
wc -l D:/Coding_projects/human-training/workflow/guides/workflow-orientation.md
head -5 D:/Coding_projects/human-training/workflow/guides/workflow-orientation.md
```

Expected: roughly 150–180 lines. First line is `# Workflow Orientation: Audit, Discuss, Adapt`.

---

## Task 2: Register the skill in build-skills.ps1

**Files:**
- Modify: `scripts/build-skills.ps1:39-64` (the `$skillDefinitions` hashtable)

- [ ] **Step 1: Add the new skill entry to the hashtable**

Edit `scripts/build-skills.ps1`. Inside the `$skillDefinitions = @{ ... }` block (lines 39–64 currently), add a fifth entry. The hashtable currently ends like this:

```powershell
    "genesis.md" = @{
        name = "project-genesis"
        description = "Use when starting a new project, brainstorming an idea, evaluating whether something is worth building, or turning a concept into a technical spec. Covers Sprint 0 end to end: ideation (challenge ideas, red-team, force scope) and spec writing (concrete specs for coding agents). Enter at brainstorming, enter at speccing, or flow through both."
        allowedTools = @("Read", "Write", "Edit", "Grep", "Glob", "WebSearch", "WebFetch")
        assets = @("ideation-protocol.md", "spec-writing-guide.md", "spec.md", "testing-standards.md")
    }
}
```

Change it to (add the new entry before the closing `}`):

```powershell
    "genesis.md" = @{
        name = "project-genesis"
        description = "Use when starting a new project, brainstorming an idea, evaluating whether something is worth building, or turning a concept into a technical spec. Covers Sprint 0 end to end: ideation (challenge ideas, red-team, force scope) and spec writing (concrete specs for coding agents). Enter at brainstorming, enter at speccing, or flow through both."
        allowedTools = @("Read", "Write", "Edit", "Grep", "Glob", "WebSearch", "WebFetch")
        assets = @("ideation-protocol.md", "spec-writing-guide.md", "spec.md", "testing-standards.md")
    }
    "workflow-orientation.md" = @{
        name = "workflow-orientation"
        description = "Use when entering a project to align it with the sprint-based workflow: empty project (scaffold rails), existing project with no workflow (propose onboarding), partial setup (gap report), canonical-healthy (drift check), or mature project with its own conventions (bridge mode via onboarding.md). Always audits read-only first, discusses, then acts non-destructively."
        allowedTools = @("Read", "Write", "Edit", "Grep", "Glob", "Bash")
        assets = @()
    }
}
```

- [ ] **Step 2: Parse-check the script**

Run:
```powershell
powershell -NoProfile -Command "[scriptblock]::Create((Get-Content D:/Coding_projects/human-training/scripts/build-skills.ps1 -Raw)) | Out-Null; Write-Host 'syntax OK'"
```

Expected: `syntax OK` with no errors. Don't run the full builder yet — Task 5 does that.

---

## Task 3: Register the skill in build-skills.sh

**Files:**
- Modify: `scripts/build-skills.sh:97-100` (append a new `build_skill` call)

- [ ] **Step 1: Add the new build_skill call**

Edit `scripts/build-skills.sh`. Find the last `build_skill` call (it currently builds `project-genesis`, lines 97–100). After it, add:

```bash
build_skill "workflow-orientation.md" "workflow-orientation" \
    "Use when entering a project to align it with the sprint-based workflow: empty project (scaffold rails), existing project with no workflow (propose onboarding), partial setup (gap report), canonical-healthy (drift check), or mature project with its own conventions (bridge mode via onboarding.md). Always audits read-only first, discusses, then acts non-destructively." \
    "Read, Write, Edit, Grep, Glob, Bash"
```

Note: no asset arguments — workflow-orientation has no asset files (it references other skills' assets via `${CLAUDE_PLUGIN_ROOT}` paths).

The block to add comes right before the `echo ""` / `echo "Build complete!"` lines.

- [ ] **Step 2: Verify the script syntax**

Run:
```bash
bash -n D:/Coding_projects/human-training/scripts/build-skills.sh && echo "syntax OK"
```

Expected: `syntax OK` with no errors.

---

## Task 4: Update lifecycle.md for bridge-mode awareness

**Files:**
- Modify: `workflow/guides/lifecycle.md:22-28` (the "Joining a Moving Train" section)

- [ ] **Step 1: Replace the "Joining a Moving Train" section**

Edit `workflow/guides/lifecycle.md`. Find this exact block (lines 22–28):

```markdown
### Joining a "Moving Train"

If you arrive mid-project:

1. **Read the latest DEVLOG entry**: Learn the recent technical baggage.
2. **Read the current Handover**: Learn what's currently "breaking" or being debated.
3. **Verify the Build**: Run the tests immediately. Don't trust the environment until the terminal proves it.
```

Replace it with:

```markdown
### Joining a "Moving Train"

If you arrive mid-project:

1. **Read `onboarding.md` (if present)**: Use its "Getting Oriented" section as your map for where DEVLOG, handover, spec, and other docs actually live in this project. This is essential in projects bridged to non-canonical layouts; in canonical layouts it just confirms the defaults. If no `onboarding.md` exists, proceed with the defaults below.
2. **Read the latest DEVLOG entry**: At the path from `onboarding.md`, or default: `DEVLOG.md`, `./docs/devlog.md`. Learn the recent technical baggage.
3. **Read the current Handover**: At the path from `onboarding.md`, or default: `HANDOVER.md`, `./docs/.agents/current-handover.md`. Learn what's currently "breaking" or being debated.
4. **Verify the Build**: Run the tests immediately. Don't trust the environment until the terminal proves it.
```

- [ ] **Step 2: Verify the edit landed**

Run:
```bash
grep -A 12 'Joining a "Moving Train"' D:/Coding_projects/human-training/workflow/guides/lifecycle.md
```

Expected: 4 numbered steps; first one references `onboarding.md`.

---

## Task 5: Rebuild skills/ and verify both builders agree

**Files:**
- Regenerated: `skills/workflow-orientation/SKILL.md`
- Regenerated: `skills/lifecycle-manager/SKILL.md` (because lifecycle.md changed)

- [ ] **Step 1: Run the PowerShell builder**

Run from the repo root:
```powershell
powershell -NoProfile -File D:/Coding_projects/human-training/scripts/build-skills.ps1
```

Expected output includes:
```
Building: workflow-orientation
  -> workflow-orientation/SKILL.md
```
And `Build complete!` at the end. The final summary should report `Skills built: 5` (was 4).

- [ ] **Step 2: Verify the new skill file exists with correct frontmatter**

Run:
```bash
head -5 D:/Coding_projects/human-training/skills/workflow-orientation/SKILL.md
```

Expected:
```
---
name: workflow-orientation
description: Use when entering a project to align it with the sprint-based workflow: empty project (scaffold rails), ...
allowed-tools: [Read, Write, Edit, Grep, Glob, Bash]
---
```

- [ ] **Step 3: Verify lifecycle-manager was regenerated with the new section**

Run:
```bash
grep -A 3 'Joining a "Moving Train"' D:/Coding_projects/human-training/skills/lifecycle-manager/SKILL.md | head -8
```

Expected: the new 4-step list with `onboarding.md` as step 1.

- [ ] **Step 4: Cross-check that the bash builder produces byte-identical output**

This is what CI does. Run locally to catch drift before pushing:
```bash
OUTPUT_DIR=/tmp/skills-rebuild bash D:/Coding_projects/human-training/scripts/build-skills.sh
diff -r D:/Coding_projects/human-training/skills /tmp/skills-rebuild && echo "BUILDERS AGREE"
```

Expected: `BUILDERS AGREE`. If `diff` reports differences, the two builders have drifted — fix the formatting in whichever you edited before continuing.

- [ ] **Step 5: List the skills tree to confirm count and structure**

Run:
```bash
ls D:/Coding_projects/human-training/skills/
```

Expected:
```
handover-manager
lifecycle-manager
onboarding-creator
project-genesis
workflow-orientation
```

(5 directories, no extras.)

---

## Task 6: Bump version and update README

**Files:**
- Modify: `.claude-plugin/plugin.json` (version field)
- Modify: `README.md` (skill list and directory tree)

- [ ] **Step 1: Bump plugin version 1.0.0 → 1.1.0**

Read current `plugin.json`:
```bash
cat D:/Coding_projects/human-training/.claude-plugin/plugin.json
```

Edit `.claude-plugin/plugin.json`. Change:
```json
  "version": "1.0.0",
```
to:
```json
  "version": "1.1.0",
```

Reason: minor bump for additive feature (new skill, additive change to lifecycle skill, no breaking changes).

- [ ] **Step 2: Update README.md skill list**

Edit `README.md`. Find the line listing namespaced skills (around line 28–29):

```markdown
After install, the skills are namespaced under the plugin:
`/human-training:project-genesis`, `/human-training:lifecycle-manager`,
`/human-training:handover-manager`, `/human-training:onboarding-creator`.
```

Replace with:

```markdown
After install, the skills are namespaced under the plugin:
`/human-training:project-genesis`, `/human-training:lifecycle-manager`,
`/human-training:handover-manager`, `/human-training:onboarding-creator`,
`/human-training:workflow-orientation`.
```

- [ ] **Step 3: Update README.md directory tree**

In the same README, find the `skills/` block in the directory tree (around line 60–65):

```
├── skills/                      # GENERATED (don't edit directly)
│   ├── project-genesis/         # SKILL.md + assets/
│   ├── lifecycle-manager/
│   ├── handover-manager/
│   └── onboarding-creator/
```

Replace with:

```
├── skills/                      # GENERATED (don't edit directly)
│   ├── project-genesis/         # SKILL.md + assets/
│   ├── lifecycle-manager/
│   ├── handover-manager/
│   ├── onboarding-creator/
│   └── workflow-orientation/
```

- [ ] **Step 4: Verify edits**

Run:
```bash
grep '"version"' D:/Coding_projects/human-training/.claude-plugin/plugin.json
grep -c 'workflow-orientation' D:/Coding_projects/human-training/README.md
```

Expected: version is `"1.1.0"`. README has at least 2 mentions of `workflow-orientation`.

---

## Task 7: Local smoke test via --plugin-dir

**Files:** none modified. This is a manual verification.

- [ ] **Step 1: Launch a fresh Claude Code session loading the plugin from disk**

In a NEW terminal (not this session), from any directory you want to test against:
```bash
claude --plugin-dir D:/Coding_projects/human-training
```

- [ ] **Step 2: In that session, check the skill is loaded**

Type:
```
/skill human-training:workflow-orientation
```

Expected: the skill body is loaded and prints. If you see "skill not found," the build or the plugin manifest is wrong — go back to Task 5 and re-verify.

- [ ] **Step 3: Smoke-test the audit phase in an empty directory**

Make a temp empty dir and launch Claude there:
```bash
mkdir /tmp/wo-empty-test
cd /tmp/wo-empty-test
claude --plugin-dir D:/Coding_projects/human-training
```

In the session, invoke:
```
Use the human-training:workflow-orientation skill.
```

Expected: Claude announces it's using the skill, then audits, classifies the project as **Empty** with high confidence, presents the proposed scaffold actions (create `docs/.agents/`, create `onboarding.md` skeleton, create `DEVLOG.md` skeleton), and asks for confirmation. It should NOT have written any files yet.

You can cancel out at this point. The smoke test is just verifying that the skill loads and the audit phase runs. Full per-state behavioral verification will happen organically as you use it in real projects.

- [ ] **Step 4: Smoke-test bridge mode against a real mature project**

In another directory containing a mature project (any open-source clone on your machine — e.g., one of the projects under `D:/Coding_projects/` that has its own `README.md` + `CONTRIBUTING.md`):
```bash
cd D:/Coding_projects/<some-existing-project>
claude --plugin-dir D:/Coding_projects/human-training
```

Invoke the skill. Expected: Claude classifies it as either **Code, no workflow** or **Mature-divergent**, surfaces the existing doc structure, and proposes either an onboarding draft (State 2) or a bridge `onboarding.md` (State 5). Again, no writes without confirmation.

If both smoke tests behave as expected, the implementation is correct. If not, note specifically what was wrong and revisit the relevant per-state section in `workflow/guides/workflow-orientation.md`.

---

## Task 8: Commit and push

**Files:** none modified beyond what previous tasks did. This is the publish step.

- [ ] **Step 1: Review the staged changes**

Run:
```bash
cd D:/Coding_projects/human-training
git status
git diff --stat
```

Expected file list:
- `workflow/guides/workflow-orientation.md` (new)
- `workflow/guides/lifecycle.md` (modified)
- `scripts/build-skills.ps1` (modified)
- `scripts/build-skills.sh` (modified)
- `skills/workflow-orientation/SKILL.md` (new)
- `skills/lifecycle-manager/SKILL.md` (modified, regenerated)
- `.claude-plugin/plugin.json` (modified)
- `README.md` (modified)
- `docs/specs/2026-05-23-workflow-orientation-design.md` (new — if not yet committed from brainstorming)
- `docs/plans/2026-05-23-workflow-orientation.md` (new — this plan, if not yet committed)

If any other files are staged, investigate before committing.

- [ ] **Step 2: Stage and commit as a single feature commit**

```bash
cd D:/Coding_projects/human-training
git add workflow/guides/workflow-orientation.md \
        workflow/guides/lifecycle.md \
        scripts/build-skills.ps1 \
        scripts/build-skills.sh \
        skills/workflow-orientation/ \
        skills/lifecycle-manager/SKILL.md \
        .claude-plugin/plugin.json \
        README.md \
        docs/specs/2026-05-23-workflow-orientation-design.md \
        docs/plans/2026-05-23-workflow-orientation.md

git commit -m "$(cat <<'EOF'
Add workflow-orientation skill (v1.1.0)

New skill audits any project's workflow state (empty / no-workflow /
partial / canonical-healthy / mature-divergent), discusses non-
destructively, then scaffolds or bridges as appropriate. Bridge mode
produces an onboarding.md pointing at the project's actual file
locations so downstream skills work transparently.

lifecycle-manager updated to read onboarding.md first when joining a
moving train, with fallback to default paths if none exists.

Co-Authored-By: Claude Opus 4.7 (1M context) <noreply@anthropic.com>
EOF
)"
```

- [ ] **Step 3: Verify the commit landed cleanly**

```bash
git log -1 --stat
```

Expected: one commit with the file list from Step 1.

- [ ] **Step 4: Push**

```bash
git push origin main
```

Expected: clean push to GitHub. CI (`verify-skills.yml`) will run; it should pass because both builders were run locally in Task 5 and produced agreeing output.

- [ ] **Step 5: Confirm CI passes**

Either watch the GitHub Actions tab in a browser, or:
```bash
gh run list --limit 1
gh run watch
```

Expected: green check on the "Verify skills are in sync with source" workflow.

If CI fails, the most likely cause is that the two builders produced different bytes for the same skill (one builder was edited, the other wasn't, or formatting drifted). Re-run both builders, compare, and amend the commit.

---

## Task 9: Update the installed plugin on this machine

**Files:** none in the repo. This updates the local Claude Code plugin cache.

- [ ] **Step 1: Refresh the marketplace cache from GitHub**

In your active Claude Code session, run:
```
/plugin marketplace update human-training
```

Expected: Claude Code pulls the latest commit of the `human-training` marketplace and reports success. Until this step runs, Claude Code does not know the new version exists.

- [ ] **Step 2: Update the installed plugin**

```
/plugin update human-training@human-training
```

Expected: Claude Code installs version 1.1.0 from the refreshed cache. If `/plugin update` doesn't exist in your CLI version, run `/plugin install human-training@human-training` instead — it picks up the new version the same way.

- [ ] **Step 3: Verify the new version is installed**

```powershell
powershell -NoProfile -Command "Get-Content C:/Users/brad/.claude/plugins/installed_plugins.json | Select-String 'human-training' -Context 0,8"
```

Expected: the entry shows `"version": "1.1.0"` and an updated `lastUpdated` timestamp.

- [ ] **Step 4: Verify the skill is available in your session**

In Claude Code (you may need to start a fresh session for the new skill list to load):

Look at your available skills list. You should see `human-training:workflow-orientation` alongside the existing four. Try invoking:
```
/skill human-training:workflow-orientation
```

Expected: skill loads and prints its body.

- [ ] **Step 5: Repeat on the other PC**

When you switch back to the daily-driver PC, run the same `/plugin marketplace update human-training` → `/plugin update human-training@human-training` flow to bring it up to 1.1.0. No code changes needed; just the marketplace refresh + update.

---

## Verification Summary

After all tasks complete:

- [ ] `skills/workflow-orientation/SKILL.md` exists, frontmatter is correct
- [ ] `skills/lifecycle-manager/SKILL.md` shows the updated "Joining a Moving Train" section
- [ ] Both builders produce byte-identical output (CI passes)
- [ ] Plugin version is 1.1.0 in both `.claude-plugin/plugin.json` and the locally installed plugin
- [ ] README lists the new skill in both the namespaced-skills paragraph and the directory tree
- [ ] Skill loads via `claude --plugin-dir .` and via the installed plugin
- [ ] Smoke test against an empty directory classifies as State 1 and proposes scaffolding without writing
- [ ] Smoke test against a mature project classifies as State 2 or State 5 and surfaces existing structure without writing

If any line is unchecked at the end, do not consider the implementation complete.
