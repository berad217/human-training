# How to Write a Spec from Ideation

**Audience**: AI agents transitioning from ideation conversation to spec creation

**Purpose**: Transform a successful ideation conversation into a clear, actionable specification that another AI (coding agent) can implement from.

---

## The Transition

After ideation conversation reaches "ready to build" decision:

1. **Summarize what you understand** from the conversation
2. **Ask explicitly**: "Ready to write the spec based on this conversation?"
3. **Wait for confirmation** - Don't start writing until they say yes
4. If they have more questions or ideas, continue ideation
5. Once approved, write the spec using this guide

---

## Who This Spec Is For

**Primary audience**: AI coding agent (possibly different session, zero shared context)

**Requirements:**
- Coding agent should be able to implement without asking clarifying questions
- Must be concrete enough to prevent assumption drift
- Must be flexible enough to allow discovery during implementation
- Must define success clearly (anti-mission-creep)

**Remember**: This spec is the source of truth. It's a living document that will be updated as implementation reveals better approaches.

---

## Spec Structure

### 1. Project Overview

**What to include:**
- **Name** - Actual project name
- **Purpose** - One sentence: what it does OR why it's cool
- **Context** - Why this exists (problem it solves, learning goal, just for fun)
- **User** - Who will use this (e.g., "Personal tool for the developer's kids")

**Keep it brief** - 3-4 sentences max.

---

### 2. Success Criteria (Definition of Done)

**Critical section** - This human struggles with mission creep. Define success clearly:

- **What does "done" look like?**
- **What's the minimum viable version?**
- **How do you know it's working?**

**Format as checklist:**
```
Project is complete when:
- [ ] User can [specific action]
- [ ] System handles [specific scenario]
- [ ] Tests prove [specific behavior]
```

**Example:**
```
Quiz app is complete when:
- [ ] User can load quiz from JSON file
- [ ] User can answer all question types
- [ ] System tracks and displays score
- [ ] Works as Electron desktop app
```

---

### 3. Technical Foundation

**Be prescriptive** - Decided during ideation, don't make coding agent guess:

- **Tech stack**: React + TypeScript + Vite + Node/Express (or whatever)
- **Runtime**: Web app / Desktop (Electron) / CLI / etc.
- **Testing framework**: Vitest + @testing-library/react (or whatever)
- **Key dependencies**: Any specific libraries decided during ideation
- **Build/dev tools**: What commands run the project

**Why prescriptive here?** Prevents tech stack drift. Coding agent shouldn't pick a different framework.

---

### 4. Architecture & Modules

**Show the mental model:**

- **High-level components** - What are the major pieces?
- **Single responsibilities** - Each component does one thing
- **Loose coupling** - Prefer modularity when feasible (not mandatory, but encouraged)
- **Module boundaries** - What's separate from what

**Example:**
```
Core components:
1. Config Loader - Loads/validates configuration (no UI dependencies)
2. Quiz Engine - Manages quiz state (no file I/O, uses loaded data)
3. Question Renderer - Displays questions (no quiz logic, just presentation)
4. Score Tracker - Tracks progress (independent of rendering)

Philosophy: Each component is testable in isolation. No "epoxy" coupling.
```

**Visual structure** - Show actual file tree:
```
/project-root
  /src
    /config
      loader.ts
      schema.ts
    /quiz
      engine.ts
      types.ts
    /components
      QuestionRenderer.tsx
    /tests
```

This prevents file structure mismatch.

---

### 5. Data Models (Show, Don't Tell)

**CRITICAL**: Use concrete examples, not descriptions.

**Bad:**
```
Config file with app settings and theme options
```

**Good:**
```json
// config/app.config.json
{
  "appName": "Quiz App",
  "defaultTheme": "light",
  "quizDirectory": "./quizzes",
  "scoreTracking": true,
  "themes": {
    "light": { "bg": "#ffffff", "text": "#000000" },
    "dark": { "bg": "#1a1a1a", "text": "#ffffff" }
  }
}
```

**Show:**
- Actual JSON structure
- Example values
- All fields (required and optional)
- Data types
- Nested structures

**For each data model:**
- What file/location
- What it represents
- Validation rules (if any)
- How it's used

---

### 6. Sprint Breakdown

**Philosophy**: Flexible granularity. Sprints should be completable in one focused session but allow for context resets between sprints.

**For each sprint:**

#### Sprint N: [Descriptive Title]

**Goal**: [One sentence - what should work after this sprint]

**Success Criteria** (testable outcomes):
- ✓ [Specific behavior works]
- ✓ [Specific scenario handled]
- ✓ [Specific validation works]
- ✓ [Error cases covered]

**Deliverables**:
- [Concrete artifact - file, component, module]
- [Tests proving success criteria]
- [DEVLOG entry documenting decisions]

**Testing Guidance**:
- Test count target: ~X-Y tests
- Types: Unit / Integration / Component
- Coverage: All success criteria must be validated

**Context for Handover**:
[Enough detail that if there's a context reset after this sprint, the next AI can pick up smoothly]

---

**Sprint Template Example:**

```markdown
### Sprint 2: Quiz Loader

**Goal**: Load and validate quiz files from JSON

**Success Criteria**:
✓ Loads quiz from valid JSON file
✓ Validates required fields (id, title, questions array)
✓ Rejects invalid question types with clear error
✓ Handles missing optional fields gracefully
✓ Returns structured error messages for malformed JSON

**Deliverables**:
- QuizLoader module (src/quiz/loader.ts)
- Quiz schema types (src/quiz/types.ts)
- Loader validation logic
- Unit tests: 8-12 tests covering all criteria
- DEVLOG Sprint 2 entry

**Testing Guidance**:
- Unit tests for loader function
- Test both success and failure cases
- Mock file system operations
- Validate error messages are helpful

**Context for Handover**:
Quiz loader is independent of UI. Takes file path, returns validated Quiz object or error. Uses config from Sprint 1 to know where quiz directory is.
```

---

### 7. Testing Strategy

**Testing is non-negotiable.** Make this explicit:

**Framework**: [Specified in Technical Foundation]

**Requirements**:
- Tests written **during** sprint, not after
- Sprint not complete until tests passing
- Tests committed with implementation code
- Tests must validate actual behavior, not just exist

**Test Types**:
- **Unit tests**: Business logic, utilities, data transformations
- **Integration tests**: APIs, module interactions
- **Component tests**: UI rendering, user interactions

**Coverage expectations**:
- Business logic: High coverage (most functions tested)
- UI components: Reasonable coverage (main paths tested)
- Integration points: All critical flows tested

**Success criteria define what to test** - Each sprint's criteria should map to specific tests.

---

### 8. Constraints & Boundaries

**Explicit rules for coding agent:**

**Do:**
- ✅ Follow this spec
- ✅ Write tests for each sprint
- ✅ Document decisions in DEVLOG
- ✅ Ask if something is ambiguous
- ✅ Propose better approaches if spec has issues

**Do NOT:**
- ❌ Add features not in spec (no "helpful" additions)
- ❌ Skip tests or defer them
- ❌ Make speculative features
- ❌ Tightly couple modules unnecessarily
- ❌ Make major technical decisions without documenting

**Module coupling guidelines** (when applicable):
- Prefer loose coupling when feasible
- Each module should be testable in isolation
- Avoid "epoxy" coupling that makes changes hard
- Document dependencies explicitly

---

### 9. Out of Scope

**Explicitly list what we're NOT building:**

This prevents scope creep and helps coding agent know boundaries.

**Future Possibilities** (Parking Lot):
- Ideas that came up but deferred
- Potential extensions
- Nice-to-haves that aren't V1

**Known Limitations We're Accepting**:
- Things we know won't work perfectly but are OK with
- Tradeoffs we consciously made

---

### 10. Spec Maintenance

**Living Document Philosophy:**

This spec is **not frozen**. Implementation is a discovery process.

**When implementation reveals better approach:**
1. Update spec to reflect new approach
2. Document change in DEVLOG with rationale
3. Spec should reflect as-built, not just as-planned

**Process:**
- Coding agent notices spec issue during implementation
- Proposes change with rationale
- Gets approval
- Updates spec inline
- Notes change in DEVLOG

**The spec is the source of truth** - Keep it accurate.

---

### 11. Meta-Feedback (Continuous Improvement)

**This section is for YOU (the AI writing the spec) to provide feedback on this spec-writing process.**

After writing the spec, reflect:

**What worked well:**
- Which sections of this guide were helpful?
- What made the spec clear and actionable?
- What from ideation conversation translated smoothly?

**What was difficult:**
- Which sections were unclear or hard to write?
- What guidance was missing from this template?
- Where did you have to guess or make assumptions?

**Suggestions for improvement:**
- How could this guide be better?
- What sections should be added/removed/changed?
- What examples would help future AIs write better specs?

**Format this feedback two ways:**

1. **In conversation** (as you finish writing spec):
   - "I've written the spec. Here's what worked well and what was tricky about the process: [feedback]"
   - Give user chance to discuss and refine

2. **In spec document** (at the very end):
   - Add a "## Process Notes" section
   - Document what was easy/hard about writing THIS spec
   - Note any ambiguities that needed clarifying questions
   - Suggest improvements for next time

**This feedback loop improves the templates over time.**

---

## Writing Process

### Step 1: Confirm Readiness
- "Based on our ideation conversation, I'm ready to write the spec. Should I proceed?"
- Wait for explicit approval

### Step 2: Draft the Spec
- Use structure above
- Pull details from ideation conversation
- Add concrete examples (JSON, file trees, etc.)
- Define success criteria clearly
- Break into sprints with good handover context

### Step 3: Review with User
- Present the spec (or key sections)
- Ask clarifying questions if needed
- "Does this capture what we discussed?"

### Step 4: Finalize and Create Supporting Documents
- Make any adjustments based on feedback
- Save spec to project root (e.g., `SPEC.md` or `[project-name]-spec.md`)
- **Create onboarding.md** - Universal entry point for any AI agent (see `./docs/.agents/onboarding-guide.md` for how; legacy aliases `.agents/onboarding-guide.md`, `.claude/onboarding-guide.md`)
- **Create DEVLOG.md skeleton** - Initial structure for sprint documentation
- Confirm user is ready to start implementation

### Step 5: Provide Meta-Feedback
- Tell user what worked/what was tricky in writing this spec
- Document process notes in spec itself
- This helps improve templates for future projects

---

## Supporting Documents Created During Spec Writing

When you write the spec, you're also creating the foundation for the entire project workflow. These documents work together:

### onboarding.md - Universal Entry Point

**Purpose**: Single entry point for ANY AI agent in ANY environment (Claude Code, Cursor, GPT in VS Code, etc.)

**Location**: Project root or `./docs/onboarding.md`

**What it contains**:
- Welcome / project purpose (one sentence)
- Document locations (with "planned fuzziness" - spec could be in multiple locations)
- About this human (brief or pointer to `./docs/.agents/global-preferences.md` — legacy aliases `.agents/global-preferences.md`, `.claude/global-preferences.md`)
- Workflow explanation (sprints, testing, DEVLOG updates)
- How to write handovers (embedded instructions since every agent needs to know)
- Project-specific quirks and gotchas

**Why separate from spec**:
- Spec = WHAT to build (technical details)
- Onboarding = HOW to get started (navigation + process)
- Onboarding helps agents FIND the spec in chaotic real-world scenarios

**How to write it**: See `./docs/.agents/onboarding-guide.md` (legacy: `.agents/onboarding-guide.md`, `.claude/onboarding-guide.md`) for detailed instructions. The guide includes a template and explains the "office tour" conversational style.

**When to refine it**: After Sprint 1-2, update with actual document locations and workflow patterns that emerged.

---

### DEVLOG.md - Sprint Journal

**Purpose**: Record what was built, why, and concerns for future

**Location**: Project root or `./docs/DEVLOG.md`

**Initial skeleton**:
```markdown
# Development Log - [Project Name]

## Sprint 1 - [Title from Spec]

[This will be filled in during implementation]
```

**What gets added each sprint**:
- Summary of what was built
- Decisions made (choice, rationale, tradeoffs)
- Testing details (coverage, test count)
- Concerns/risks identified
- Questions for user
- Preview of next sprint

**Why create skeleton now**: Signals to implementation agent that DEVLOG updates are part of "done", not optional.

**Format**: See sprint deliverables in spec Section 10 for what each DEVLOG entry should contain.

---

## Common Pitfalls

**Vague data models** - ALWAYS show JSON examples, don't just describe
**Unclear success criteria** - Make them testable, specific
**Bundled sprints** - Break them smaller if they can't be done in one session
**Missing handover context** - Sprint descriptions should enable context resets
**Tech stack ambiguity** - Be prescriptive about frameworks/tools
**Testing as afterthought** - Integrate into each sprint's deliverables
**Frozen mindset** - Remind coding agent spec is living document

---

## Example: Good vs Bad Sprint

**Bad Sprint:**
```
Sprint 2: Build the quiz system
- Implement quiz functionality
- Add tests
```

**Good Sprint:**
```
Sprint 2: Quiz Loader & Validator

Goal: Load quiz files and validate structure

Success Criteria:
✓ Loads quiz from JSON file path
✓ Validates required fields (id, title, questions)
✓ Rejects invalid question types
✓ Returns helpful error messages
✓ Handles edge cases (empty file, malformed JSON)

Deliverables:
- QuizLoader module (src/quiz/loader.ts)
- Type definitions (src/quiz/types.ts)
- Unit tests: ~10 tests covering all criteria
- DEVLOG Sprint 2 entry

Testing: Unit tests with mocked file system. Test both success paths and error cases.

Context: Quiz loader is independent of UI. Next sprint will use loaded quiz data in the engine.
```

---

## Remember

You're writing this spec for **another AI with zero context**. Make it:
- **Concrete** - Examples, not descriptions
- **Clear** - Unambiguous success criteria
- **Complete** - Enough detail to implement without guessing
- **Flexible** - Room for discovery and improvement

The spec is a **communication tool**, not a contract. It should enable great implementation, not constrain it unnecessarily.

---

**After writing a spec, provide feedback on this process so we can improve it.**
