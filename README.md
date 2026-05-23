# Human-Training: Workflow for AI-Human Hobby Projects

A standardized workflow and template system for effective collaboration between non-professional developers and AI coding agents.

**Key feature:** Model-agnostic workflow documents that work with ANY AI (Claude, GPT, Gemini, Cursor, etc.), with optional Claude Code skills auto-generated from the same source.

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
`/human-training:workflow-orientation`.

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
│   ├── plugin.json              # Plugin manifest (name, version 1.1.0)
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
│   ├── global-preferences.md    # Communication style (customize this!)
│   └── claude-code.md           # Global CLAUDE.md for Claude Code
│
├── skills/                      # GENERATED (don't edit directly)
│   ├── project-genesis/         # SKILL.md + assets/
│   ├── lifecycle-manager/
│   ├── handover-manager/
│   ├── onboarding-creator/
│   └── workflow-orientation/
│
├── scripts/
│   ├── build-skills.ps1         # Generate skills/ from workflow docs
│   ├── build-skills.sh          # Same, for Linux/Mac
│   └── setup-machine.ps1        # Link the global CLAUDE.md
│
└── .github/workflows/
    └── verify-skills.yml        # CI: skills/ in sync with workflow/
```

---

## The Key Insight: Single Source of Truth

```
┌─────────────────────────────────────────────────────────────┐
│  workflow/guides/*.md                                       │
│  ─────────────────────                                      │
│  Source of truth. Model-agnostic markdown.                  │
│  Works with Claude, GPT, Gemini, Cursor, any AI.            │
│                                                             │
│                    ↓ build-skills.ps1                       │
│                                                             │
│  skills/<name>/SKILL.md                                     │
│  ──────────────────────                                     │
│  Generated Claude Code skills, bundled by the plugin.       │
│  Same content + Claude Code frontmatter.                    │
└─────────────────────────────────────────────────────────────┘
```

**Edit the workflow docs. Run the build script. Skills stay in sync.**

CI (`verify-skills.yml`) rebuilds `skills/` from `workflow/` on every push and
fails if the committed `skills/` is stale — so a forgotten rebuild is caught
automatically.

---

## Multi-Machine Setup

The skills are a plugin, so each machine just installs the plugin once through
Claude Code's `/plugin` system — Claude Code keeps it updated.

**When you change the workflow docs:**
```powershell
# Edit workflow/ files, then regenerate skills/ and bump the version:
./scripts/build-skills.ps1
# edit .claude-plugin/plugin.json -> bump "version"
git add . && git commit -m "Update workflow"
git push
```

Other machines pick up the new version through Claude Code's plugin update flow.
The `version` bump is what tells Claude Code an update is available.

---

## Available Skills (Claude Code)

| Skill | Purpose | When to Use |
|-------|---------|-------------|
| **project-genesis** | Sprint 0: ideation + spec writing | Brainstorming an idea, or turning one into a spec |
| **lifecycle-manager** | Active development loop | During implementation |
| **handover-manager** | Context resets | Switching sessions, context full |
| **onboarding-creator** | Create onboarding.md | New project setup |

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

Edit `workflow/global-preferences.md` to reflect how YOU work:

```markdown
# Communication & Cognition
[Your thinking style, what you value...]

# Background & Fluency
[Your expertise, what to explain vs assume...]

# Feedback & Collaboration
[How you want feedback delivered...]
```

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
A: Yes! Add a guide to `workflow/guides/`, add a matching definition in both
`build-skills.ps1` and `build-skills.sh`, then run the build.

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
