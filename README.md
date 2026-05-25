# Human-Training: Workflow for AI-Human Hobby Projects

A standardized workflow and template system for effective collaboration between non-professional developers and AI coding agents.

**Key feature:** Model-agnostic workflow documents that work with ANY AI (Claude, GPT, Gemini, Cursor, etc.), with optional Claude Code skills auto-generated from the same source.

> **AI agents arriving in this repo: read [onboarding.md](onboarding.md) first.**
> It covers how *this* repo works (the workflow infrastructure), which is
> different from how downstream projects using this plugin work.

---

## Quick Start

### For Any AI Tool (Model-Agnostic)

1. Copy `workflow/` contents to your project's `docs/.agents/`
2. Tell your AI: "Read `docs/.agents/onboarding-guide.md` and help me create onboarding.md"
3. Start working: "Read onboarding.md and let's begin Sprint 1"

### For Claude Code Specifically

The workflow skills ship as a Claude Code **plugin**. Install once per machine,
in Claude Code:

```
/plugin marketplace add berad217/human-training
/plugin install human-training@human-training
```

After install, the skills are namespaced under the plugin:
`/human-training:project-genesis`, `/human-training:lifecycle-manager`,
`/human-training:handover-manager`, `/human-training:onboarding-creator`,
`/human-training:workflow-orientation`, `/human-training:robustness-audit`.

Claude Code manages updates — a new version is picked up when `version` is
bumped in `.claude-plugin/plugin.json`.

For local development of this repo itself, `claude --plugin-dir .` from the
repo root loads the plugin straight from disk without going through the
marketplace.

Optionally run `./scripts/setup-machine.ps1` to also link the global CLAUDE.md.

---

## Repository Structure

```
human-training/
├── .claude-plugin/
│   ├── plugin.json              # Plugin manifest (name, version)
│   └── marketplace.json         # Single-plugin marketplace catalog
│
├── workflow/                    # SOURCE OF TRUTH (model-agnostic)
│   ├── guides/                  # Core workflow documents
│   │   ├── genesis.md           # Sprint 0: idea → spec
│   │   ├── lifecycle.md         # Sprint 1-N: active development
│   │   ├── handover-guide.md    # Context resets between sessions
│   │   ├── onboarding-guide.md  # Creating agent entry points
│   │   ├── ideation-protocol.md # Brainstorming conversations (asset)
│   │   └── spec-writing-guide.md# Writing specifications (asset)
│   ├── templates/               # Starter templates
│   │   ├── devlog.md
│   │   ├── handover.md
│   │   ├── onboarding.md
│   │   ├── spec.md
│   │   └── testing-standards.md
│   └── claude-code.md           # Global CLAUDE.md template (communication
│                                # style + workflow rules — customize this!)
│
├── skills-source/               # Session-authored skills, READY TO SHIP (Track 2)
│   └── robustness-audit/        # Complete SKILL.md + assets/evals — copied through as-is
│
├── skills-drafts/               # In-progress skill development (not shipped)
│   └── gemini-api/              # one folder per skill-idea
│       └── research/            # raw material, notes, drafts
│
├── skills/                      # BUILD OUTPUT (don't edit directly)
│   ├── project-genesis/         # SKILL.md + assets/  ─┐ generated from
│   ├── lifecycle-manager/                              │ workflow/guides/
│   ├── handover-manager/                               │
│   ├── onboarding-creator/                             │
│   ├── workflow-orientation/                          ─┘
│   └── robustness-audit/        # copied through from skills-source/
│
├── scripts/
│   ├── build-skills.ps1         # Generate skills/ from both source tracks
│   ├── build-skills.sh          # Same, for Linux/Mac
│   └── setup-machine.ps1        # Link the global CLAUDE.md
│
└── .github/workflows/
    └── verify-skills.yml        # CI: committed skills/ matches a fresh build
```

---

## The Three Workspaces

Skills move through three workspaces as they mature: from scratch → polished
→ shipped. Two of those workspaces feed the build output; the third is a
git-tracked scratchpad that never ships.

```
┌─────────────────────────────────────────────────────────────┐
│  skills-drafts/<idea>/         (DEV: not built, not shipped) │
│  ────────────────────                                        │
│  Scratchpad for in-progress skill development. Raw research, │
│  half-formed SKILL.md drafts, footgun notes, candidate eval  │
│  queries. Tracked in git so it follows you across machines.  │
│                                                              │
│  Both builders ignore this dir entirely; CI does not watch   │
│  it. A draft cannot leak into the shipped plugin.            │
│                                                              │
│                    ↓ (graduate to one of the two tracks)     │
└─────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────┐
│  workflow/guides/*.md          (Track 1: GENERATED)         │
│  ────────────────────                                       │
│  Model-agnostic markdown. Source of truth for the           │
│  sprint-workflow skills. Works with any AI.                 │
│                                                             │
│  Frontmatter (name, description, allowed-tools) lives in    │
│  $skillDefinitions inside scripts/build-skills.{ps1,sh}.    │
│                                                             │
│                    ↓ build-skills script                    │
│                                                             │
│  skills/<name>/SKILL.md                                     │
│                                                             │
├─────────────────────────────────────────────────────────────┤
│  skills-source/<name>/         (Track 2: PASS-THROUGH)      │
│  ─────────────────────                                      │
│  Fully-formed session-authored skill packages. Drop them    │
│  here complete (SKILL.md + any assets/evals).               │
│                                                             │
│                    ↓ build-skills script (copy-through)     │
│                                                             │
│  skills/<name>/  (byte-identical to skills-source/<name>/)  │
└─────────────────────────────────────────────────────────────┘
```

**Use `skills-drafts/`** when you have raw material, notes, or a SKILL.md
you're still iterating on. Anything not yet ready to ship.

**Use Track 1 (`workflow/guides/`)** when the skill body is genuinely
model-agnostic and you also want a standalone doc usable by GPT/Gemini/Cursor.

**Use Track 2 (`skills-source/`)** when the skill is Claude-specific (uses
subagents, Claude Code tooling, etc.) and was authored in-session — the
session-context SKILL.md *is* the artifact, not a translation of a generic doc.

CI (`verify-skills.yml`) rebuilds `skills/` on every push and fails if the
committed `skills/` is stale — so a forgotten rebuild is caught automatically.

---

## Multi-Machine Setup

The skills are a plugin, so each machine just installs the plugin once through
Claude Code's `/plugin` system — Claude Code keeps it updated.

**When you change anything that goes into the plugin:**
```powershell
# Edit workflow/ files or drop a new skill into skills-source/, then:
./scripts/build-skills.ps1
# edit .claude-plugin/plugin.json -> bump "version"
git add . && git commit -m "Update workflow"
git push
```

Other machines pick up the new version through Claude Code's plugin update flow.
The `version` bump is what tells Claude Code an update is available.

### Adding a new session-authored skill (Track 2)

When a session produces a high-yield workflow worth keeping:

1. Have that session package the wisdom into a complete `<skill-name>/`
   folder: `SKILL.md` with valid frontmatter (`name:` matches dir name,
   `description:` written for trigger accuracy) + any `assets/` or `evals/`.
2. Drop the folder into `skills-source/<skill-name>/`.
3. Open a session in this repo: "I dropped a new skill in skills-source — wire it in."
4. That session will: validate the frontmatter, run `./scripts/build-skills.ps1`,
   bump `.claude-plugin/plugin.json`, commit, push.
5. `/plugin update human-training@human-training` on each machine.

### Developing a skill in this repo (skills-drafts/)

When you don't have a session with perfect context elsewhere and want to
build a skill *here*:

1. Create `skills-drafts/<idea-name>/` and drop in whatever raw material
   you have — research docs, API references, footgun notes, transcripts.
2. Iterate on `skills-drafts/<idea-name>/SKILL.md` in place. Nothing here
   ships in the plugin, so you can be messy.
3. When it's polished, **graduate** it: move `skills-drafts/<idea-name>/`
   → `skills-source/<idea-name>/`, drop research/notes you don't want
   shipping, then follow the Track 2 steps above.

See `skills-drafts/README.md` for the convention.

---

## Available Skills (Claude Code)

| Skill | Source Track | Purpose | When to Use |
|-------|--------------|---------|-------------|
| **project-genesis** | workflow/guides/ | Sprint 0: ideation + spec writing | Brainstorming an idea, or turning one into a spec |
| **lifecycle-manager** | workflow/guides/ | Active development loop | During implementation |
| **handover-manager** | workflow/guides/ | Context resets | Switching sessions, context full |
| **onboarding-creator** | workflow/guides/ | Create onboarding.md | New project setup |
| **workflow-orientation** | workflow/guides/ | Align an existing project with this workflow | Entering a project that doesn't yet use the sprint scaffold |
| **robustness-audit** | skills-source/ | Defect-class audit of existing code | Returning to a codebase after a long absence; pre-release hardening pass; "what's likely broken?" |
| **gemini-api** | skills-source/ | Current-Gemini-API working reference | Writing/reviewing/migrating Gemini 3.x code; preventing the training-data-default stumble when wiring up Gemini for text/image/function calling |

---

## The Workflow

### Phase 0: Idea to Spec

1. **Brainstorm** with `/human-training:project-genesis`
   - Challenge assumptions, red-team the idea
   - Check if solution already exists
   - Force scope definition

2. **Write spec** with `/human-training:project-genesis` (same skill — ideation flows into speccing)
   - Concrete JSON examples, not vague descriptions
   - Brief `spec.md` template, depth from the bundled spec-writing guide

3. **Create onboarding** using `onboarding-guide.md` (or `/human-training:onboarding-creator`)
   - Entry point for any AI agent
   - "Office tour" style, not formal policy

### Phase 1-N: Implementation

Follow `lifecycle.md` (or `/human-training:lifecycle-manager`):

1. **Orient**: Read onboarding → handover → spec → DEVLOG
2. **Implement**: Feature from spec
3. **Test**: Write tests immediately (part of "done")
4. **Document**: Update DEVLOG with decisions + rationale
5. **Assess**: Use Confidence Bar to decide next action

### Context Management

Use `handover-guide.md` (or `/human-training:handover-manager`) when:
- Context window filling up
- Stuck and need fresh perspective
- Natural pause point (end of sprint)

**Key concept: Ephemeral Delta**
- Handover captures what's NOT in files yet
- Once decisions are committed to code/docs, DELETE from handover
- Keep it lean (~200 tokens when possible)

---

## Customization

### Your Communication Style

Edit `workflow/claude-code.md` (the global CLAUDE.md template) to reflect how YOU work. The **About This Human** section is the place — covers communication, background, learning style, feedback preferences, and what you value. Run `./scripts/setup-machine.ps1` after editing to install your customized version to `~/.claude/CLAUDE.md`.

> **Note:** Earlier versions of this plugin shipped a separate `workflow/global-preferences.md`. That has been folded into `claude-code.md` so there's a single source of truth.

### Project-Specific Overrides

Projects can have their own `.claude/` folder that overrides global settings:
- Project CLAUDE.md overrides global CLAUDE.md
- Project skills override global skills
- Project `docs/.agents/` docs are used preferentially

---

## Design Principles

1. **Conversational, not prescriptive** - "Office tour" style, not formal checklists
2. **Planned fuzziness** - Handle missing docs, varied locations
3. **AI codes AND tests** - Same agent implements and verifies
4. **Examples over descriptions** - Show JSON, not describe it
5. **Honest assessment** - No sugarcoating, DEVLOG concerns are action items
6. **Model-agnostic first** - Works with any AI; Claude Code is optional enhancement

---

## FAQ

**Q: Do I need Claude Code to use this?**
A: No. The workflow docs work with any AI. Claude Code skills are optional.

**Q: What if I switch AI tools mid-project?**
A: The project docs (spec.md, DEVLOG.md, onboarding.md) are plain markdown. Any AI can read them.

**Q: How do I update skills after editing workflow docs?**
A: Run `./scripts/build-skills.ps1` to regenerate `skills/`, bump `version` in
`.claude-plugin/plugin.json`, then commit. Claude Code picks up the new version.

**Q: Can I add my own skills?**
A: Yes — two ways:
- **Workflow-derived (Track 1):** add a guide to `workflow/guides/<name>.md`,
  add a matching definition in both `build-skills.ps1` and `build-skills.sh`,
  then run the build. Use this when the body is model-agnostic and you also
  want a standalone doc.
- **Session-authored (Track 2):** drop a complete `<name>/` folder (SKILL.md
  + any assets/evals) into `skills-source/`, then run the build. Use this
  for Claude-specific skills where the SKILL.md *is* the artifact.

---

## Philosophy

**This is a partnership.** Human designs top-level, AI implements. Communication is key.

**For hobby projects.** Optimized for non-professional developers who want AI to handle technical complexity.

**Iterative improvement.** These guides should evolve. Update them as you discover better patterns.

---

## License

Use freely, modify as needed, share improvements.

---

**Next:** Install the plugin, then start your next project with `/human-training:project-genesis`
