# Onboarding Guide

**Purpose**: How to write an onboarding document that works as a universal entry point for any AI agent in any environment (Claude, GPT, Gemini, etc.)

---

## Why Onboarding Documents Matter

**The scenario:** You summon an AI agent into your project. Maybe it's Claude Code, maybe Cursor, maybe GPT in VS Code, maybe even Claude.ai with MCP file access. The agent appears, doesn't know where it is, what project this is, or where to find anything.

**Without onboarding:** You type a paragraph explaining the project, where the docs are, what workflow to follow, what you expect...

**With onboarding:** You type: "Read onboarding.md and let me know when you're ready."

**Onboarding is the office tour, not the employee handbook.** It's the person who walks you around on your first day, shows you where things are, explains how things really work (not just the official policy), and gives you the context you need to actually get started.

---

## Environment Detection

**Know where you are.** Different tools have different strengths. Before you start, try to identify your "home":

- **Cursor/Windsurf**: High IDE integration. You can see many files, run terminal commands, and have a long-lived session.
- **Claude Code (CLI)**: Fast, terminal-centric. Very good at search and bulk edits.
- **Web App (Claude.ai/Gemini/GPT)**: Might have MCP access to files. Less terminal control, but often "smarter" about high-level design.

**Tip:** If you're in a specialized environment (like Cursor), use its features (like codebase search) instead of just `grep`.

---

## When to Write Onboarding

**During spec writing** - Create the initial version when writing the spec. The spec-writing-guide includes creating an onboarding document as one of its deliverables.

**Refine during Sprint 1-2** - After working together for a bit, update with:

- Actual document locations (not guesses)
- Workflow patterns that emerged
- Any quirks or preferences specific to this project

**Keep it updated** - If the workflow changes significantly or documents move, update onboarding so the next agent doesn't get lost.

---

## What Onboarding Is vs What It Isn't

| Onboarding.md | Spec.md Section 11 |
|---------------|-------------------|
| Navigation + orientation | Technical constraints |
| "Where to find things" | "What not to do" |
| "How we work" | "Implementation rules" |
| Getting started | Building features |
| Works across environments | Project-specific technical details |

**Different jobs, different docs.**

---

## Structure of a Good Onboarding Document

### Section 1: Welcome / Purpose

**Start with why the agent is here:**

```markdown
# Onboarding - [Project Name]

Welcome! You're here to help build [project description in one sentence].

**Project type:** [hobby/learning/production/experiment]
**Human's level:** [hobbyist/learning/experienced]
**Current phase:** [ideation/spec/implementation/maintenance]
```

**Keep it brief.** One or two sentences for purpose, a few quick facts for context.

---

### Section 2: Getting Oriented (Document Locations)

**This is the critical section.** The agent needs to find other documents, but you can't predict every environment or folder structure.

**Use "planned fuzziness":**

```markdown
## Getting Oriented

**Look for these documents (locations may vary):**

**Spec/Specification:**
- Common locations: `spec.md`, `SPEC.md`, `./docs/spec.md`, `./documentation/spec.md`
- What it contains: Technical specification, architecture, **Visual Identity**, and the **Sprint Plan**.
- If you can't find it: Ask the user.

**DEVLOG:**
- Common locations: `DEVLOG.md`, `./docs/devlog.md`, `./docs/DEVLOG.md`
- What it contains: Sprint-by-sprint record of what was built and why.
- If it doesn't exist yet: You may need to create it (see DEVLOG section below).

**Handover:**
- Common locations: `HANDOVER.md`, `./docs/.agents/current-handover.md`, `.agents/current-handover.md`, `.claude/current-handover.md` (legacy), `./docs/handover.md`
- What it contains: Current conversation context, where we are NOW, and the **Parking Lot** for deferred ideas.
- Note: User might have given you the handover directly in their message.
- If none exists: That's OK, start from spec and DEVLOG.

**Ideation Protocol (meta):**
- Common locations: `./docs/.agents/ideation-protocol.md`
- What it contains: How we brainstorm. Check for **Red Teaming** notes if we're pivot-testing.

**Global Preferences (optional):**
- Common locations: `./docs/.agents/global-preferences.md`, `.agents/global-preferences.md`, `.claude/global-preferences.md` (legacy)
- What it contains: How this human communicates and works
- If it exists: Read it first before continuing here
- If it doesn't exist: See "About This Human" section below
```

**Key principles:**

- List common locations, not just one
- Explain what each doc contains
- Handle the "not found" case gracefully
- Don't assume perfect organization

---

### Section 3: About This Human

**If `./docs/.agents/global-preferences.md` exists (legacy aliases: `.agents/global-preferences.md`, `.claude/global-preferences.md`):**

```markdown
## About This Human

See `./docs/.agents/global-preferences.md` for detailed communication style and preferences.

**Quick summary for this project:**
- [Any project-specific working style notes]
```

**If global-preferences doesn't exist, include brief description:**

```markdown
## About This Human

**Communication style:** [direct/conversational/formal]
**Experience level:** [hobbyist learning to code / experienced developer / etc.]
**Learning goals:** [what they want to learn from this project]

**Working preferences:**
- [Key preference 1 - e.g., "Explain technical choices, they want to learn"]
- [Key preference 2 - e.g., "Direct feedback appreciated, no sugar-coating"]
- [Key preference 3 - e.g., "Move fast, refactor later"]

**Testing expectations:**
- [Who runs tests, when, what's expected]
```

---

## Context Hygiene

**Don't drown in data.** Even with large context windows, focus is key:

1. **Be lazy**: Don't read a 1000-line file until you need to edit it.
2. **Summaries first**: Prefer `view_file_outline` or `list_dir` to understand structure before deep-diving.
3. **Reference, don't copy**: If you mention a doc, just name it. Don't dump its entire content back into the conversation unless requested.

---

## Joining a "Moving Train"

If you're joining mid-project (not Sprint 1):

1. **Read the latest DEVLOG entry**: This tells you the most recent technical baggage.
2. **Read the current Handover**: This tells you what's currently "breaking" or being debated.
3. **Verify the build**: Run the tests. Don't trust that the project is in a working state until the terminal proves it.

---

### Section 4: The Workflow

**Explain how work actually happens on this project:**

```markdown
## How We Work

**Sprint-based development:**
1. **Implement** a feature from the spec
2. **Write tests** immediately after implementation
3. **Update DEVLOG** with decisions, rationale, and concerns
4. **Commit together** (code + tests + docs in one commit)
5. **One sprint at a time** - complete current work before starting next

**The Confidence Bar (When to stop):**
- **HIGH CONFIDENCE**: Routine task, follows spec exactly. -> *Just do it.*
- **MODERATE CONFIDENCE**: Spec is ambiguous, but there's a clear "best" path. -> *Do it, but highlight in DEVLOG.*
- **LOW CONFIDENCE**: Multiple valid paths with significant tradeoffs, or spec is silent. -> **STOP. Propose 2-3 options to the human and wait.**

**Testing approach:**
- Framework: [Vitest/Jest/pytest/etc.]
- Write tests for: [business logic 100%, APIs 100%, UI 70%]
- Tests must pass before moving on
- [Who runs tests: AI runs them / user runs them / both]

**Documentation:**
- Update DEVLOG every sprint (while decisions are fresh)
- Keep README current with user-facing changes
- Write handovers when context needs reset (see Handover section below)

**Communication:**
- [How to handle ambiguity - ask user / make reasonable choice and document / etc.]
- [When to stop and ask vs keep going]
- [Tone: explain choices / just implement / etc.]
```

**Customize this section** based on:

- Tech stack
- Testing philosophy
- How hands-on the human is
- Whether this is a learning project or production code

---

### Section 5: Starting Fresh (If First Agent)

**Handle the case where the agent is setting up the project:**

````markdown
## If You're the First Agent (Sprint 1)

If documents don't exist yet, you may need to create them:

**DEVLOG.md:**
```markdown
# Development Log - [Project Name]

## Sprint 1 - [Title]

**Summary:**
-   [What you built]

**Decisions:**
-   **[Topic]**: Chose [X] because [rationale]. Tradeoffs: [what was sacrificed]

**Testing:**
-   [Test coverage details]

**Concerns/Risks:**
-   [Honest assessment of potential issues]

**Next Sprint:**
-   [Preview of upcoming work]
```

**README.md:**

-   How to install dependencies
-   How to run the project
-   How to run tests
-   Basic project description

**Test infrastructure:**

-   Set up testing framework per spec requirements
-   Create initial test file(s)
-   Ensure `npm test` or equivalent works

````

---

### Section 6: Writing Handovers

**This is where you embed the handover instructions.** Every agent needs to know how to hand off, so include it here.

**Pull the core content from `./docs/.agents/handover-guide.md` (legacy: `.agents/handover-guide.md`, `.claude/handover-guide.md`) but adapt it to be more direct/instructional:**

```markdown
## Writing Handovers

**When to write a handover:**
-   User asks you to prepare a handover
-   You're stuck and need to hand off to a fresh agent
-   Major milestone completed and natural breaking point

**Where to write it:**
-   Preferred: `./docs/.agents/current-handover.md` or `HANDOVER.md` in project root
-   Legacy accepted: `.agents/current-handover.md` or `.claude/current-handover.md`
-   Or provide it to the user directly if they request it

**What to include:**

### 1. Quick Start
Tell the next agent what to read first:
```markdown
# Handover - [Project Name]

## Quick Start
New agent:
1. Read onboarding.md if you haven't already
2. [Any other critical docs to read]
3. Come back here for current context
```

### 2. Project Context (Brief)

```markdown
## Project Context
Project: [name]
Current phase: [Ideation/Spec writing/Implementation Sprint N]
Current branch: [git branch name if relevant]
```

### 3. What Was Accomplished

```markdown
## This Session's Accomplishments
- [Concrete completed work]
- [Key decisions made]
- [Tests written: X new tests, Y total passing]
```

### 4. Conversation Context (MOST IMPORTANT)

**This is what's NOT in other docs:**

```markdown
## Conversation Context

**Active discussions:**
- [Topic 1]: We discussed [X vs Y], leaning toward [X] because [reason]
- [Topic 2]: User asked about [Z], no decision yet

**Decisions in flight:**
- [What's being decided, options considered, pros/cons discussed]

**What was tried:**
- Attempted [approach A], didn't work because [reason]
- Switched to [approach B], seems promising

**Current concerns:**
- [Issue 1]: [Why it's a concern, potential impact]
- [Issue 2]: [What needs to be figured out]
```

### 5. Next Steps

```markdown
## Next Steps

**Immediate (next session):**
1. [Specific task]
2. [Specific task]

**Upcoming work:**
- Sprint N+1: [Brief description]
```

````markdown
### 6. What NOT to Include

```markdown
❌ Don't duplicate what's in spec, DEVLOG, or code
❌ Don't copy/paste large code snippets
❌ Don't write a novel - be concise
✅ DO capture the ephemeral conversation context
✅ DO reference other docs: "See DEVLOG Sprint 4 for details"
✅ DO be honest about problems and unknowns
```
````

**Tone for handover instructions:** More direct than the handover-guide itself, since this is embedded in the working doc, not a meta-guide.

---

### Section 7: Project-Specific Notes

**Add anything unique to this project:**

```markdown
## Project-Specific Notes

**Important quirks:**
- [Anything non-standard about how this project works]

**Key files to know:**
- `[path/to/file]`: [What it does, why it's important]

**Common commands:**
```bash
npm install        # Install dependencies
npm test          # Run tests
npm run dev       # Start development server
```

**Gotchas:**

- [Thing that might trip up a new agent]
- [Weird configuration detail to be aware of]

```

---

## Writing Style

**Conversational, not formal:**
- ✅ "Look for spec.md - usually in docs/ but sometimes root"
- ❌ "The specification document shall be located in the designated documentation directory"

**Practical, not comprehensive:**
- ✅ "Tests must pass before moving on"
- ❌ "Execute the complete test suite utilizing the designated testing framework and ensure all assertions evaluate successfully across all modules and components"

**A bit fuzzy on purpose:**
- ✅ "Common locations: X, Y, Z"
- ❌ "Location: X (exactly)"

**Include personality:**
- ✅ "This human appreciates direct feedback - don't sugarcoat"
- ❌ "Provide objective assessments in professional manner"

**Remember:** This is the office tour, not the employee handbook. Write like you're showing someone around, not writing a legal document.

---

## Agent Ops (for onboarding authors)
- Store agent-facing docs under `docs/.agents/`; project docs live in `docs/`.
- If guides are copied locally, archive/delete them after use to save context: remove `docs/.agents/spec-writing-guide.md` once spec is written; remove `docs/.agents/onboarding-guide.md` once onboarding.md exists; remove `docs/.agents/ideation-protocol.md` after ideation. Keep `docs/.agents/handover-guide.md` and `docs/.agents/global-preferences.md`.
- If handover exists (`HANDOVER.md` or `docs/.agents/current-handover.md`), edit in place rather than delete+recreate.

---

## Template Skeleton

Here's a starting template:

```markdown
# Onboarding - [Project Name]

Welcome! You're here to help build [one sentence description].

**Project type:** [hobby/learning/production]
**Human's level:** [hobbyist/experienced]
**Current phase:** [ideation/implementation/etc.]

---

## Getting Oriented

**Look for these documents (locations may vary):**

- **Spec:** `spec.md`, `./docs/spec.md` - Technical specification & **Visual Identity**.
- **DEVLOG:** `DEVLOG.md`, `./docs/devlog.md` - What's been built and why.
- **Handover:** `HANDOVER.md`, `./docs/.agents/current-handover.md` - Current state & **Parking Lot**.
- **Global Preferences:** `./docs/.agents/global-preferences.md` - How this human works (if exists).

---

## How We Work

**Sprint-based development:**
1. Implement feature
2. Write tests immediately
3. Update DEVLOG with decisions
4. Commit together

**The Confidence Bar:**
- **HIGH**: Routine task -> Just do it.
- **MODERATE**: Ambiguous but clear best path -> Highlight in DEVLOG.
- **LOW**: Significant tradeoffs -> STOP and ask human.

**Testing:** [Framework, expectations]
**Context Management:** [e.g., "Don't read large files until needed"]

---

## Writing Handovers

**When:** User requests it, when stuck, at milestones
**Where:** `./docs/.agents/current-handover.md` or `HANDOVER.md`

**Include:**
- Quick start (what to read)
- This session's accomplishments
- **Conversation context** (discussions, decisions in flight, what was tried)
- Next steps

---

## Project-Specific Notes

[Important quirks, key files, common commands, gotchas]
```

---

## Checklist: Is Your Onboarding Good?

**Test:** Could a GPT-5 agent in Cursor, starting from zero context, find what they need and start working?

- [ ] Purpose stated clearly in one sentence
- [ ] Document locations listed with common variations
- [ ] Handles "not found" cases gracefully
- [ ] Workflow explained (sprints, testing, documentation)
- [ ] Handover instructions embedded
- [ ] Project-specific quirks noted
- [ ] Conversational tone, not formal/legal
- [ ] Planned fuzziness (not assuming perfect organization)
- [ ] Works across different agent/IDE environments

---

## Refinement During Project

**After Sprint 1-2, update with:**

- Actual document locations (remove guesses that were wrong)
- Workflow patterns that emerged
- Any surprises or gotchas discovered
- Project-specific working style that crystallized

**Onboarding is a living document.** Keep it current so the next agent (or the next context reset) starts smoothly.

---

## Meta Notes

**This guide is for the meta-project.** When you create an onboarding.md for an actual project, you're adapting this guidance into a concrete document for that specific project.

**Onboarding vs other docs:**

- **Global preferences** - Who the human is (reusable across projects)
- **Onboarding** - How to work on THIS project (project-specific entry point)
- **Spec Section 11** - Technical implementation constraints (engineering rules)
- **Handover** - Current conversation state (ephemeral, constantly changing)

They're all different jobs. Don't try to make one doc do everything.
