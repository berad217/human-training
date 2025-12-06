# Human-Training: Workflow for AI-Human Hobby Projects

A standardized workflow and template system for effective collaboration between non-professional developers and AI coding agents.

---

## What Is This?

A collection of guides and templates that optimize the workflow from **idea → spec → implementation** for hobby projects where a human designer works with AI coding agents.

This is not software you run. It's a methodology you follow, with reusable documents you copy into your projects.

---

## Motivation

This project emerged from a practical need during the development of the Quazy Quizzer app.

**The testing problem:** When building with AI agents, testing often gets handed off to the human. But for hobby developers without deep technical expertise, setting up proper test frameworks and writing comprehensive tests isn't realistic. The result? Either no testing happens, or it's just manual "happy path" verification.

**The insight:** In AI-human collaboration where the human designs and the AI implements, the AI should also handle testing. But this requires a different approach than traditional "separate tester" methodology. The AI codes AND tests, which means we need guards against the failure mode where an AI misunderstands the spec, implements the wrong thing, writes tests that verify the wrong thing, and reports "all tests passing."

**The solution evolved:** Testing standards led to documenting sprints, which led to handover processes, which led to this complete workflow system.

---

## What's Inside

### Foundational Guides

These guides define how to work effectively with AI coding agents:

- **`global-preferences.md`** - Communication style and cognitive preferences (customize for yourself)
- **`ideation-protocol.md`** - How to conduct brainstorming conversations with AI
- **`spec-writing-guide.md`** - How to write technical specifications (4-round process, examples over descriptions)
- **`onboarding-guide.md`** - Universal entry point for AI agents joining a project (handles chaos, planned fuzziness)
- **`handover-guide.md`** - How to write and use handover documents for context resets

### Templates

Structural templates for your projects:

- **`templates/project-spec-template.md`** - Standard sections for technical specifications
- **`templates/testing-standards.md`** - Testing framework guide for AI-codes-and-tests scenario

---

## The Workflow

### Phase 1: Idea to Spec

**You do:** Brainstorm with AI using `ideation-protocol.md`

**You create:** Technical specification using `spec-writing-guide.md` (4 rounds: info gathering → architecture → review → deliver)

**AI helps:** Ask questions, suggest approaches, challenge assumptions

**Output:**
- `spec.md` - What to build
- `onboarding.md` - How to work on this project
- `DEVLOG.md` - Empty skeleton for sprint notes

### Phase 2: Implementation

**AI does:** Implement in sprints, write tests, document in DEVLOG

**You do:** Review DEVLOG entries to verify assumptions, test happy path

**Guidance:**
- AI follows `testing-standards.md` for testing approach
- Each sprint: implement → test immediately → document in DEVLOG → commit
- Tests prove AI got it right (integration tests prevent over-mocking)
- DEVLOG documents decisions with rationale and honest risk assessment

**Output:** Working software with tests and documentation

### Phase 3: Context Management

**When:** Context window filling up, or at natural pause points

**AI does:** Write handover using `handover-guide.md`

**You do:** Start fresh session when ready

**New AI reads:**
1. `onboarding.md` - How to work on this project
2. `global-preferences.md` - How to communicate with this human
3. Current handover - Where things stand

### Phase 4: Iteration

**Continue:** Same workflow for new features or refinements

**Evolve:** Update onboarding.md as you learn better patterns

---

## Key Design Principles

### 1. Conversational, Not Prescriptive

The guides use an "office tour" style - practical, with personality and fuzziness. Not formal checklists. Trust AI agents to internalize principles rather than follow rigid templates.

### 2. Planned Fuzziness

Onboarding works across different IDEs, different AI models, missing documents, and documents in random locations. It handles real-world chaos.

### 3. AI Codes AND Tests

Testing standards designed specifically for the scenario where the same AI implements and tests. Guards against the "misunderstood spec → wrong implementation → tests verify wrong thing" failure mode.

### 4. Examples Over Descriptions

Show actual JSON structures, file trees, and concrete examples. Vague descriptions cause AI misunderstandings.

### 5. Honest Assessment

No sugarcoating. "User can handle the truth." DEVLOG concerns are action items, not just notes.

### 6. Separation of Concerns

| Document | Purpose | Audience | Stability |
|----------|---------|----------|-----------|
| global-preferences.md | Who the human is | All agents, all projects | Very stable |
| onboarding.md | How to work on THIS project | All agents, this project | Semi-stable |
| spec.md | What to build | Implementation agents | Stable but living |
| handover.md | Current state | Next agent | Ephemeral |

---

## Getting Started with Your Project

### 1. Copy the guides you need:

```bash
# In your project root:
mkdir docs/.agents

# Copy core guides (customize global-preferences for yourself):
cp human-training/docs/.agents/global-preferences.md docs/.agents/
cp human-training/onboarding-guide.md docs/.agents/
cp human-training/handover-guide.md docs/.agents/
cp human-training/spec-writing-guide.md docs/.agents/

# Optional: ideation protocol if starting from scratch
cp human-training/ideation-protocol.md docs/.agents/
```

### 2. Write your spec:

```bash
# Copy template
cp human-training/templates/project-spec-template.md ./spec.md

# Fill in all sections following spec-writing-guide.md
# Include: architecture, data schemas (with JSON examples!), sprint plan
```

### 3. Create onboarding:

Follow `spec-writing-guide.md` Step 4 to create `onboarding.md` for your project. This becomes the universal entry point for any AI agent.

### 4. Start implementing:

Tell your AI agent: "Read onboarding.md and let's start Sprint 1"

AI will follow testing-standards.md for testing, update DEVLOG.md after each sprint, and maintain handovers when needed.

---

## Real Example

This meta-project (human-training) follows its own workflow:

- Uses the same principles documented here
- No spec (this IS the spec-creation system)
- Creates `HANDOVER.md` when needed; none active now

## Example Workflow: "Connect-5" App

This is how a human should use these docs for a new project.

1) Ideation → “ready to spec”
- Brainstorm the idea (Connect-5). If useful, follow `ideation-protocol.md`.
- Outcome: clear goal, constraints, and agreement to write a spec.

2) Write the spec (what to build)
- Start from `templates/project-spec-template.md`.
- Follow `spec-writing-guide.md` to fill in: overview, success criteria, tech stack, architecture/modules, data models with examples, sprint plan, testing requirements, constraints/out-of-scope.
- Save as `spec.md` (root or `./docs/`). Keep it living.

3) Write onboarding (how to start)
- Create `onboarding.md` (root or `./docs/`) using `onboarding-guide.md`.
- Include doc locations (with planned fuzziness), about this human (or point to `docs/.agents/global-preferences.md`), workflow (sprints, testing, DEVLOG), handover instructions, and project-specific notes.

4) Create DEVLOG skeleton
- Add `DEVLOG.md` with Sprint 1 heading from the spec. Fill entries each sprint (summary, decisions/tradeoffs, testing, risks, next sprint).

5) Implementation cycles (per sprint)
- Agent read order (recommended): onboarding → global preferences → handover (if present) → spec → DEVLOG.
- Implement sprint scope; write tests as part of “done.”
- Update `DEVLOG.md` for the sprint.
- If pausing/resetting, update `HANDOVER.md` (or `docs/.agents/current-handover.md`) with conversation context, decisions in flight, what was tried, and next steps.

6) Iterate and finish
- Complete sprints, keep spec updated when plans change, and keep onboarding current if doc locations/workflow change.
- When done: finalize DEVLOG, ensure spec reflects as-built, optionally add a user-facing README for the app, and leave a final HANDOVER if handing off for maintenance.

## Suggested Folder Structure (per project)

```
connect-5/
  docs/
    .agents/                   # agent-working set (primary audience: AI)
      global-preferences.md    # human profile (shared across projects)
      handover-guide.md        # keep (used multiple times)
      onboarding-guide.md      # temporary during setup; archive/delete after onboarding.md is written
      spec-writing-guide.md    # temporary during spec; archive/delete after spec.md is written
      ideation-protocol.md     # optional; archive after ideation is done
      current-handover.md      # optional alias if you prefer
    onboarding.md              # entry point for any agent
    spec.md                    # project spec (living)
    DEVLOG.md                  # sprint log
    HANDOVER.md                # current handover if active
  src/                         # implementation
  package.json / etc.          # build tooling
```

Notes on cleanup:
- Agent-facing guides (ideation, spec-writing, onboarding guides) can be archived or deleted after they’re used to reduce context clutter. Keep handover-guide for repeated use.
- If your IDE dislikes delete+create in one turn, edit files in place rather than replacing them.

### Agent Ops (quick reference)
- If `docs/.agents/` is missing, create it and move global-preferences there.
- Prefer editing handover in place (`HANDOVER.md` or `docs/.agents/current-handover.md`), not delete+recreate.
- After you’ve produced the real project docs, archive/delete helper guides (ideation, spec-writing, onboarding guides); keep handover-guide.
- Store agent-facing docs under `docs/.agents/`; project-facing docs live in `docs/`.

### Archiving helper guides
- When spec is written: remove or archive `docs/.agents/spec-writing-guide.md`.
- When onboarding.md is written: remove or archive `docs/.agents/onboarding-guide.md`.
- When ideation is done: remove or archive `docs/.agents/ideation-protocol.md` (if copied).
- Keep: `docs/.agents/handover-guide.md` for repeated handovers; `docs/.agents/global-preferences.md` as the human profile.

## For Incoming Agents to This Project (human-training)

- Read this `README.md` to understand the workflow and example.
- Read `docs/.agents/global-preferences.md` to know the human’s style.
- Review the guides (`onboarding-guide.md`, `handover-guide.md`, `spec-writing-guide.md`) if you will refine them.
- There is no active `HANDOVER.md` for this meta-project unless one has been added; create or update it in place if needed.

For a real implementation example, see the Quazy Quizzer project that sparked this workflow.

---

## Philosophy

**This is a partnership.** Human designs top-level, AI implements. Communication is key. The workflow should evolve based on real experience.

**For hobby projects.** Not production code where money changes hands. Optimized for non-professional developers who want AI to handle technical complexity.

**Iterative improvement.** These guides should evolve. Update them as you discover better patterns. Version control your improvements.

**Trust but verify.** AI writes tests to prove correctness. You verify assumptions through DEVLOG and manual happy-path testing. You don't need deep technical skills to confirm the AI got it right.

---

## FAQ

**Q: Do I need all these documents?**
A: Minimum viable: spec, onboarding.md, DEVLOG.md. Add others as needed.

**Q: Is this only for Claude?**
A: No. Works with any AI coding agent. Use `docs/.agents/` as the neutral folder name; `.agents/` or `.claude/` are legacy aliases if you already have them.

**Q: What if I'm not using sprints?**
A: Adapt to your workflow. The core principles (document decisions, test immediately, honest assessment) matter more than the structure.

**Q: Can I modify these guides?**
A: Yes! Customize for your needs. Especially global-preferences.md - that's YOUR communication style.

**Q: Why no prescriptive checklists?**
A: Modern AI agents can internalize principles from conversational docs. Rigid checklists feel corporate and don't adapt to different projects.

---

## Contributing

This is a living workflow. Found something that works better? Update the guides.

The methodology evolves through real project experience, not theory.

---

## License

Use freely, modify as needed, share improvements. No attribution needed but appreciated.

---

## Credits

**Extracted from:** Quazy Quizzer project patterns
**Philosophy:** "What worked well in practice" > "What sounds good in theory"
**Collaboration:** Human (hobbyist) + AI agents

---

**Next:** Use these guides on your next project and refine based on experience.
