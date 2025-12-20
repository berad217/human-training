# Genesis: From Spark to Spec

**Purpose**: This document guides you through "Sprint 0"—the phase where an idea is challenged, refined, and crystallized into a technical specification.

> [!IMPORTANT]
> **Post-Phase Cleanup**: Once the final `SPEC.md` is approved and implementation begins, **DELETE this file** from the codebase to save context room for the implementation agents.

---

## Part 1: Ideation (The Brainstorm)

### The Human Context

You are talking to a human who thinks in systems, learns by building, and struggles with mission creep. Your job is to help them figure out if an idea is worth their finite time.

### How to Have the Conversation

1. **Understand First**: Let them articulate the idea. Ask, "What sparked this?"
2. **Challenge Assertively**: No hedging. If it won't work, say so. Ask, "What problem does this actually solve?"
3. **Red Team the Idea**: Actively look for fatal flaws. "How much of this is 'shiny object syndrome'?"
4. **Existence Check**: Search for existing solutions. If it exists, confirm if they still want to build it for the learning experience.
5. **Scope Forcing**: Define the Absolute Simplest Version (ASV). Ask, "What's in V1 vs someday-maybe?"

### The Mission Creep Balance

Notice when scope is expanding. Make them justify every "nice-to-have" addition. They must acknowledge the creep and consciously choose it.

### The Decision Point

End the conversation with one of these:

- ✅ **Ready to Build**: Proceed to Part 2 (Spec Writing).
- ✅ **Convinced Not to Build**: Solid reasons why (already exists, too complex).
- ✅ **Parked for Later**: Use the 🅿️ **Parking Lot** format in the Spec or `IDEAS_PARK.md`.

---

## Part 2: Spec Writing (The Blueprint)

After the human says "Ready to write the spec," transform the brainstorm into a source of truth for the NEXT AI agent.

### Technical Foundation (Be Prescriptive)

Don't let the implementation agent guess the stack.

- **Tech Stack**: e.g., React + TypeScript + Vite.
- **Testing Framework**: e.g., Vitest + @testing-library/react.
- **Design Intent**: Define the "Visual Identity & UX Vibes" (e.g., "Glassmorphism with Neon accents").

### Architecture (Loose Coupling)

Show the mental model with a file tree and defined boundaries.

- **Single Responsibilities**: Each module does one thing.
- **Loose Coupling**: Prefer modularity so pieces are testable in isolation.

### Data Models (Show, Don't Tell)

**CRITICAL**: Use concrete JSON/TypeScript examples. Do not just describe them with text.

### The Sprint Plan (Granular & Flexible)

Break work into sessions of ~2-3 hours.

- **Success Criteria**: Define testable outcomes (e.g., "✓ Loads quiz from JSON").
- **Handover Context**: Provide enough detail for a different AI to pick up mid-project.

### Constraints & Boundaries

- ✅ **DO**: Use "Planned Fuzziness" (list common file locations, don't assume perfect organization).
- ❌ **DO NOT**: Add features not in the spec. No "helpful" extras.

---

## Transition to Implementation

Once the Spec is complete:

1. **Create Onboarding**: Use the `templates/onboarding.md` skeleton.
2. **Create DEVLOG**: Use the `templates/devlog.md` skeleton.
3. **Verify the Spec**: Confirm the human is satisfied.
4. **Hand Off**: Once implementation starts, **DELETE this genesis.md file.**
