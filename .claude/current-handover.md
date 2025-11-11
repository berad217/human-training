# Handover - Human-Training Workflow Project

## Quick Start

New AI: Start by reading `.claude/global-preferences.md` (communication style), then come back here.

## Project Context

**Project**: Human-Training - Standardized workflow templates for AI-human hobby project collaboration

**Purpose**: Create reusable templates and guidance docs that optimize the workflow from idea → spec → implementation for projects where a non-professional developer works with AI coding agents.

**Phase**: Core documentation complete - foundational guides finished, cleaned up old docs, ready to tackle implementation/testing guidance

**No spec for this project** - This is a meta-project about creating the workflow itself. We're building the templates that future projects will use.

## Where We Are

**NEW foundational docs in `.claude/` folder (COMPLETE):**
- ✅ `global-preferences.md` - User's cognitive and communication preferences
- ✅ `ideation-protocol.md` - How to conduct brainstorming conversations
- ✅ `spec-writing-guide.md` - How to write specs (updated to create onboarding.md + DEVLOG)
- ✅ `handover-guide.md` - How to write/use handover documents
- ✅ `onboarding-guide.md` - How to write onboarding docs (NEW this session)
- ✅ `current-handover.md` - This document

**Cleaned up docs:**
- ✅ `templates/best-practices-ai-human-collab.md` - Removed Phase 1 & 3, kept Phase 2 (Implementation) & Phase 4 (Iteration)
- ✅ Deleted: `sidequest-collaboration-stack.md`, `handover-template.md`, `patterns-extracted.md`, `onboarding.md`, `templates/ai-onboarding-template.md`

**Still to review/refine:**
- ⏳ `templates/testing-standards.md` - Not yet reviewed
- ⏳ `templates/sprint-checklist.md` - Not yet reviewed
- ⏳ `templates/devlog-entry-template.md` - Not yet reviewed
- ⏳ `templates/project-spec-template.md` - Complements NEW spec-writing-guide
- ⏳ `templates/best-practices-ai-human-collab.md` - Phase 2 & 4 content still there

**Git status**: All work committed and pushed to branch `claude/read-handover-notes-011CUzhvRDartRA4AZt6hf39`

## This Session's Accomplishments

**Major breakthrough: Onboarding as universal entry point**

Created `.claude/onboarding-guide.md` which reframes onboarding completely:
- Not "how to work with this human on this project"
- Instead: "Single reliable entry point that works in chaos"
- Works across ANY environment (Claude Code, Cursor, GPT in VS Code, Claude.ai with MCP, etc.)
- Uses "planned fuzziness" for document locations (handles real-world messiness)
- Embeds handover instructions (since every agent needs to know how to hand off)
- "Office tour" style - conversational, practical, not formal

**Updated spec-writing-guide.md:**
- Step 4: Now explicitly creates onboarding.md + DEVLOG.md skeleton
- Added "Supporting Documents" section explaining why onboarding is separate from spec
- Spec = WHAT to build (technical), Onboarding = HOW to get started (navigation + process)

**Cleaned up old documents:**
1. Deleted `sidequest-collaboration-stack.md` - Original vision doc, now implemented
2. Deleted `handover-template.md` - Conflicted with NEW lean/adaptive handover philosophy
3. Deleted `patterns-extracted.md` - Lessons extracted, refined into NEW guides
4. Deleted `onboarding.md` and `templates/ai-onboarding-template.md` - Superseded by onboarding-guide

**Continued cleaning best-practices:**
- Already removed Phase 1 (Idea to Spec) and Phase 3 (Context Management) earlier
- What remains: Phase 2 (Implementation), Phase 4 (Iteration), Common Pitfalls, Success Metrics

## Key Insights This Session

**The "office tour" framing for onboarding:**
User shared great analogy: Onboarding is like your first day at work when someone walks you around the office. Shows you the lunchroom, tells you about the Monday meetings that sometimes happen on other days, explains that Bob expects a knock-knock joke with deliverables, warns you about Brenda who will gossip. Document control is on 3rd floor, just take the elevator and you'll figure it out from there.

This is DIFFERENT from the employee handbook (spec Section 11):
- Employee handbook = formal policies
- Office tour = how things really work, with personality and fuzziness

**Onboarding handles real-world chaos:**
Agents get summoned into messy scenarios:
- Different IDE (Cursor vs VS Code vs Claude Code)
- Different agent (GPT-5 vs Claude)
- Maybe no handover was written
- Documents in random locations
- User just says "read onboarding.md and let's go"

Onboarding needs to work in ALL these scenarios, so it has:
- Fuzzy document locations ("look for spec.md in ./docs or ./ or ./spec/")
- Instructions for missing docs ("if DEVLOG doesn't exist, create it")
- Embedded handover instructions (every agent reads onboarding, not every agent writes spec)

**Separation of concerns achieved:**

| Document | Purpose | Audience | Stability |
|----------|---------|----------|-----------|
| global-preferences.md | Who the human is | All agents, all projects | Very stable |
| onboarding.md | How to work on THIS project | All agents, this project | Semi-stable, refined after Sprint 1-2 |
| spec.md Section 11 | Technical constraints | Implementation agents | Stable but living |
| handover.md | Current conversation state | Next agent | Ephemeral, changes every session |

## Design Patterns Reinforced

**Context management philosophy:**
- Human controls timing based on "open loops" not token counts
- AI doesn't suggest when to reset
- Opportunistic resets at natural pause points
- User said: "I need to be in the habit of making context management my responsibility"

**Spec-writing delivers THREE documents:**
1. spec.md - What to build
2. onboarding.md - How to get started
3. DEVLOG.md skeleton - Where sprint notes go

**Onboarding structure:**
1. Welcome / purpose
2. Document locations (fuzzy)
3. About this human
4. Workflow (sprints, testing, DEVLOG)
5. If you're first agent (creating docs)
6. Writing handovers (embedded, adapted from handover-guide)
7. Project-specific notes

**Communication style:**
- Direct, no hedging
- Challenge assumptions
- "That won't work because X" > "That's interesting..."
- Humor when it reveals insight
- Precise when it matters, casual when it doesn't

## What's Left to Build

**Still need to review/refine existing templates:**
1. `templates/testing-standards.md` - Review for useful content
2. `templates/best-practices-ai-human-collab.md` Phase 2 & 4 - Implementation and iteration guidance
3. `templates/sprint-checklist.md` - May inform implementation guidance
4. `templates/devlog-entry-template.md` - Template for DEVLOG entries

**Process for remaining work:**
- Review existing template docs
- Extract useful patterns
- Either keep/refine templates OR integrate into guides
- Delete anything that's redundant/conflicting

**Future work (lower priority):**
- Create README or quick-start guide as entry point for this meta-project
- Possibly create an actual onboarding.md for THIS meta-project to dogfood the concept

## Important Context

**Mid-session context glitch (first session):**
- Lost access to beginning of conversation where we did "rounds 1, 2, 3" review
- User pasted it back - handover process proved resilient to disruption
- The rounds were about what to delete from best-practices (all rejected as covered by NEW docs)

**Git workflow learning:**
- User learning git/GitHub
- Created PR and merged to main
- Now working on branch `claude/read-handover-notes-011CUzhvRDartRA4AZt6hf39`
- Can't push directly to main (403 error) - must use claude/* branches

**Best-practices document status:**
- User manually edited (linter change noted by system)
- Phase 1 & 3 removed (covered by NEW docs)
- Phase 2 (Implementation) & 4 (Iteration) still present
- Common Pitfalls and Success Metrics still there
- These sections haven't been reviewed yet - that's upcoming work

## Next Steps

**Immediate (in next session):**
1. New AI: Read `.claude/global-preferences.md` and this handover
2. Review remaining template docs:
   - `templates/testing-standards.md`
   - `templates/best-practices-ai-human-collab.md` (Phase 2 & 4)
   - `templates/sprint-checklist.md`
   - `templates/devlog-entry-template.md`
3. Decide: Keep/refine/delete/integrate each one

**Then:**
4. Create implementation guidance (or extract from best-practices Phase 2)
5. Create testing guidance (or refine existing testing-standards.md)
6. Final cleanup of any remaining old docs
7. Eventually: Create README for this meta-project as entry point

## Red Flags / Warnings

None for this project. It's documentation, low technical risk.

**Git note:** Remember to use claude/* branches, not main directly.

## Meta Notes

**This is the third handover using the guide we created.**

Handover process continues to work well:
- Survived context glitch (first session)
- Captured complex session with major insights (this session)
- User comfortable with opportunistic resets based on "open loops"

The onboarding work this session was significant - it's the universal entry point that ties the whole workflow together.

Incoming AI: The onboarding-guide.md is a substantial piece of work. It reframes onboarding from "project-specific preferences" to "universal entry point that handles chaos." This is a key architectural piece of the whole system.

---

**Resume point:** User will start fresh session to review remaining template docs and decide what to keep/refine/integrate/delete.
