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

```powershell
# Clone repo
git clone https://github.com/berad217/human-training.git
cd human-training

# Set up this machine (run once per machine)
./scripts/setup-machine.ps1
```

Now skills like `/project-genesis`, `/lifecycle-manager`, `/handover-manager` are available in ALL Claude Code sessions.

---

## Repository Structure

```
human-training/
├── workflow/                    # SOURCE OF TRUTH (model-agnostic)
│   ├── guides/                  # Core workflow documents
│   │   ├── genesis.md           # Sprint 0: idea → spec
│   │   ├── lifecycle.md         # Sprint 1-N: active development
│   │   ├── handover-guide.md    # Context resets between sessions
│   │   ├── onboarding-guide.md  # Creating agent entry points
│   │   ├── ideation-protocol.md # Brainstorming conversations
│   │   └── spec-writing-guide.md# Writing specifications
│   ├── templates/               # Starter templates
│   │   ├── devlog.md
│   │   ├── handover.md
│   │   ├── onboarding.md
│   │   ├── project-spec-template.md
│   │   └── testing-standards.md
│   ├── global-preferences.md    # Communication style (customize this!)
│   └── claude-code.md           # Global CLAUDE.md for Claude Code
│
├── claude-skills/               # GENERATED (don't edit directly)
│   ├── project-genesis.skill
│   ├── lifecycle-manager.skill
│   ├── handover-manager.skill
│   ├── onboarding-creator.skill
│   ├── ideation-helper.skill
│   └── spec-writer.skill
│
└── scripts/
    ├── build-skills.ps1         # Generate skills from workflow docs
    ├── build-skills.sh          # Same, for Linux/Mac
    └── setup-machine.ps1        # Install skills globally
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
│  claude-skills/*.skill                                      │
│  ──────────────────────                                     │
│  Auto-generated Claude Code packages.                       │
│  Same content + Claude Code frontmatter.                    │
└─────────────────────────────────────────────────────────────┘
```

**Edit the workflow docs. Run the build script. Skills stay in sync.**

---

## Multi-Machine Setup

Your workflow docs live in this git repo. On each machine:

1. Clone this repo
2. Run `./scripts/setup-machine.ps1`
3. Skills and CLAUDE.md are installed to `~/.claude/`

**When you update workflow docs:**
```powershell
# On any machine, edit workflow/ files, then:
./scripts/build-skills.ps1
git add . && git commit -m "Updated workflow"
git push

# On other machines:
git pull
./scripts/setup-machine.ps1 -Force
```

---

## Available Skills (Claude Code)

| Skill | Purpose | When to Use |
|-------|---------|-------------|
| **project-genesis** | Idea → Spec (Sprint 0) | Starting a new project |
| **lifecycle-manager** | Active development loop | During implementation |
| **handover-manager** | Context resets | Switching sessions, context full |
| **onboarding-creator** | Create onboarding.md | New project setup |
| **ideation-helper** | Brainstorming | Evaluating ideas |
| **spec-writer** | Write specifications | After ideation, before coding |

---

## The Workflow

### Phase 0: Idea to Spec

1. **Brainstorm** using `ideation-protocol.md` (or `/ideation-helper`)
   - Challenge assumptions, red-team the idea
   - Check if solution already exists
   - Force scope definition

2. **Write spec** using `spec-writing-guide.md` (or `/spec-writer`)
   - 4 rounds: info gathering → architecture → review → deliver
   - Concrete JSON examples, not vague descriptions

3. **Create onboarding** using `onboarding-guide.md` (or `/onboarding-creator`)
   - Entry point for any AI agent
   - "Office tour" style, not formal policy

### Phase 1-N: Implementation

Follow `lifecycle.md` (or `/lifecycle-manager`):

1. **Orient**: Read onboarding → handover → spec → DEVLOG
2. **Implement**: Feature from spec
3. **Test**: Write tests immediately (part of "done")
4. **Document**: Update DEVLOG with decisions + rationale
5. **Assess**: Use Confidence Bar to decide next action

### Context Management

Use `handover-guide.md` (or `/handover-manager`) when:
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
A: Run `./scripts/build-skills.ps1` then `./scripts/setup-machine.ps1 -Force`

**Q: Can I add my own skills?**
A: Yes! Add a guide to `workflow/guides/`, update the skill definitions in `build-skills.ps1`, run build.

---

## Philosophy

**This is a partnership.** Human designs top-level, AI implements. Communication is key.

**For hobby projects.** Optimized for non-professional developers who want AI to handle technical complexity.

**Iterative improvement.** These guides should evolve. Update them as you discover better patterns.

---

## License

Use freely, modify as needed, share improvements.

---

**Next:** Clone this repo, run setup, and start your next project with `/project-genesis`
