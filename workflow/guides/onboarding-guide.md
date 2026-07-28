# Onboarding Guide

**Purpose**: How to write an onboarding document that works as a universal entry point for any AI agent in any environment (Claude, GPT, Gemini, etc.)

---

## Why Onboarding Documents Matter

**The scenario:** You summon an AI agent into your project. Maybe it's Claude Code, maybe Cursor, maybe GPT in VS Code, maybe even Claude.ai with MCP file access. The agent appears, doesn't know where it is, what project this is, or where to find anything.

**Without onboarding:** You type a paragraph explaining the project, where the docs are, what workflow to follow, what you expect...

**With onboarding:** You type: "Read onboarding.md and let me know when you're ready."

**Onboarding is the office tour, not the employee handbook.** It's the person who walks you around on your first day, shows you where things are, explains how things really work (not just the official policy), and gives you the context you need to actually get started.

---

## Write for an environment you can't predict

The agent reading your onboarding.md may be in a terminal, an IDE, or a web chat
with file access — with wildly different tooling and no way for you to know which.
That constraint shapes the whole document: describe *what* to find and *why* it
matters, not the keystrokes to find it. "Look for spec.md, usually in docs/"
survives any environment; "run `grep -r spec docs/`" is already wrong for half of
them.

(Guidance for an agent identifying its *own* environment lives in `lifecycle.md`
§1 — that's the reader's problem, not the author's.)

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

| Onboarding.md | Spec.md Section 9 |
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

**Context (glossary):**
- Common locations: `CONTEXT.md`, `./docs/CONTEXT.md`
- What it contains: The project's shared language — terms defined once and used everywhere. A glossary and nothing else (no plans, decisions, or implementation — those live in the spec and DEVLOG).
- If it doesn't exist yet: That's fine. Seed it lazily — only when the project has domain jargon worth pinning down. `/grill` maintains it inline during design sessions; you can stub it from the `CONTEXT.md` template when first setting up.

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

## Working practice while you author

Context hygiene and mid-project orientation are the lifecycle guide's job, not
this one's — see `lifecycle.md` §1 (Orientation & Context Hygiene, including
"Joining a Moving Train"). Its version is the current one and covers steps this
guide used to omit, so don't restate it here or in the onboarding.md you write.
Point at it.

The one piece that *is* this guide's business: apply that hygiene to yourself
while authoring. You are reading a project in order to describe it, which is
exactly the situation where it's tempting to read everything first. Read enough
to write each section accurately, and no more.

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

**What to include.** The handover guide is the authority on this; what you embed
must not drift from it. Three sections, ~200 tokens total:

```markdown
# Handover - [Project Name]

## 1. Orientation
Oriented via onboarding.md. [Phase / sprint, in one more sentence.]

**Durability:** [Only when something is NOT pushed — e.g. "ahead 4, committed
but NOT pushed". Omit this line entirely when every repo is clean.]

## 2. The Delta
Strictly what is NOT already in the files:
- **Active debates:** choosing between X and Y; leaning Z because [reason].
- **Failed paths:** A didn't work because [reason] — don't retry it.
- **In-flight:** [what is half-done or currently broken, and where.]

## 3. Next Steps
1. [Specific task]
2. [Specific task]
```

**Before writing it, run `git status -sb`** and read the `[ahead N]` marker on the
first line. Committed is not pushed, and a handover that says "all work committed"
about unpushed commits is the failure this line exists to prevent. Report and offer
to push; never push unasked.

**Two things NOT to embed**, both of which look helpful and aren't:

- **A "what we accomplished" section.** That is a status report, and it belongs in
  the DEVLOG. A handover carries only what has no home in a file yet — the moment
  a decision lands in code or the DEVLOG, it leaves the handover.
- **Anything already in the spec, DEVLOG, or code.** Reference it instead:
  "See DEVLOG Sprint 4." Length should track the size of the unresolved delta, so
  a clean stop produces a nearly empty handover — that is success, not an omission.

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

**Right-sized:**

An office tour is short because the building is small, not because the guide was
rationed. Match the length to what the project actually has: a two-file hobby
project has less to show than a service with four deploy targets, and its
onboarding should be visibly shorter. Cover every section that has real content,
then stop — a section kept alive with "[TBD]" or a restatement of the section
above it costs the next agent context and teaches them the doc is padding.

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
- **Context:** `CONTEXT.md` - The project's shared language / glossary (if it has one).
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
- Orientation (one or two sentences) + a **Durability** line if anything is unpushed
- **The Delta** (active debates, failed paths, what's in flight) — the whole point
- Next steps
- Not accomplishments; those go in the DEVLOG

---

## Project-Specific Notes

[Important quirks, key files, common commands, gotchas]
```

---

## Checklist: Is Your Onboarding Good?

**Test:** Could an agent you've never met, in an IDE you didn't anticipate, starting from zero context, find what they need and start working?

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
- **Context** - What the project's words mean (the shared glossary/language)
- **Spec Section 9** - Technical implementation constraints (engineering rules)
- **Handover** - Current conversation state (ephemeral, constantly changing)

They're all different jobs. Don't try to make one doc do everything.
