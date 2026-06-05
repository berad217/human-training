---
name: handover-manager
description: >-
  Use when the user requests a handover, the context window is getting full or laggy, at a natural pause point (end of sprint or milestone), or when stuck and a fresh perspective is needed. Creates a handover capturing the ephemeral conversation delta not already in the project files. Works with any AI agent.
allowed-tools: [Read, Write, Edit, Grep, Glob]
---

# Handover Guide

**Purpose**: Enable smooth context resets by capturing what's not documented elsewhere. Works with any AI agent (Claude, GPT, Gemini, etc.).

---

## For Outgoing AI: How to Write a Handover

### When User Requests Handover

You're about to hand off to a fresh AI session. Your job: **Capture the "Ephemeral Delta"—the conversation context that doesn't live in the files yet.**

### The Handover Philosophy: Ephemeral Delta

A handover is NOT a status report. It is a bridge.

- **Record**: Files, Spec, DEVLOG, Tests (Permanent).
- **Bridge**: Handover (Temporary).

**Rule**: If it is in a file, it does NOT belong in the handover.
**Rule**: Once a decision is committed to a file, DELETE it from the handover.

---

### Step 1: Inventory What Exists

**Don't assume documentation exists.** Check what's actually in the project:

```bash
# What docs are present?
- [ ] onboarding.md (how to work with this human)
- [ ] docs/.agents/global-preferences.md (communication style) — legacy aliases: `.agents/global-preferences.md`, `.claude/global-preferences.md`
- [ ] SPEC.md or similar (what to build)
- [ ] DEVLOG.md (what was built and why)
- [ ] Code (actual implementation)

**If paths are unclear, search these common locations:**
- onboarding: `onboarding.md`, `./docs/onboarding.md`, `./docs/.agents/onboarding.md`, `.agents/onboarding.md`, `.claude/onboarding.md`
- global preferences: `./docs/.agents/global-preferences.md`, `.agents/global-preferences.md`, `.claude/global-preferences.md`
- handover: `HANDOVER.md`, `./docs/.agents/current-handover.md`, `.agents/current-handover.md`, `.claude/current-handover.md`, `./docs/handover.md`
- spec: `spec.md`, `SPEC.md`, `./docs/spec.md`, `./documentation/spec.md`
- devlog: `DEVLOG.md`, `./docs/DEVLOG.md`, `./docs/devlog.md`
```

**Adapt your handover based on what's missing.**

### Step 2: Understand What to Capture

Different docs serve different purposes:

| Document | What It Contains | What It DOESN'T Contain |
|----------|------------------|-------------------------|
| Spec | What to build (decisions made) | Decisions still in flight |
| DEVLOG | What was built + rationale | Current discussions, unsolved problems |
| Code | Implementation | Why we chose this approach over alternatives we discussed |
| **Handover** | **Conversation state** | Nothing - handover is ephemeral |

**Handover captures the discussion, not just the state.**

### Step 3: Write the Handover

Use this lean template. If a section is already covered by a file, **delete the section.**

---

## Handover Template

### 1. Orientation (2 Sentences Max)

```markdown
New AI: Oriented via onboarding.md. We are in Implementation Phase, Sprint 4.
```

### 2. The Delta (Conversation Context)

**Strictly what is NOT in the files:**

- **Active Debates**: "We are choosing between X and Y. User leans Z but is worried about [Tradeoff]."
- **Failed Paths**: "Approach A failed because [Reason]. Don't try it again."
- **In-Flight Issues**: "Extracting the engine logic but stopped at the event handler. Code is currently broken in `engine.ts`."

### 3. Next Steps (Specific)

1. [Next immediate task]
2. [Task following that]

---

### Step 4: The Overwrite Rule

**CRITICAL**: NEVER delete and recreate the handover file in the same turn. Many IDEs will fail to process the new file.

1. **Always overwrite** the existing `HANDOVER.md` or `current-handover.md`.
2. Do not change the filename unless the user explicitly requests it.
3. If no file exists, create it. If it exists, edit it.

### Step 5: Context Hygiene & Pruning

As soon as a task is done and the DEVLOG is updated:

1. **Wipe the handover clean** or reduce it to the next immediate "in-flight" thought.
2. The goal is to keep the handover under 200 tokens whenever possible.
3. **Draft the Handover**: Tell the user you've prepared it, summarize the "Delta", and save/overwrite the file.

---

## For Incoming AI: How to Use a Handover

### Step 1: Trust the Files, then the Handover

1. `onboarding.md` - Your map.
2. `SPEC.md` / `DEVLOG.md` - Your history and destination.
3. **Handover** - Your "live" radio feed of what's happening *right now*.

### Step 2: Context Reset Hygiene

If the handover mentions an "In-Flight" issue that you have now fixed:
**DELETE the mention from the handover at the end of your session.**
Do not let old "Delta" context linger once it has become "Record" (code/docs).

### Step 3: Immediate Feedback on Bloat

If an outgoing agent left you a "novel" instead of a "delta", tell the user. "The handover was too long and duplicated the spec. I've pruned it to keep the session lean."

---

## Anti-Patterns

❌ **Duplicating the Spec/DEVLOG** - If it's in a permanent doc, keep it out of the handover.
❌ **Keeping "Zombie" Context** - Leaving a "Decision in Flight" in the handover after the decision was made.
❌ **Delete-then-Create** - Deleting the handover file instead of overwriting it (breaks IDE toolchains).
❌ **The Novel** - Writing more than 3-4 paragraphs. Keep it a bridge, not a book.
❌ **Missing Failed Paths** - Not warning the next agent about what *didn't* work.

**For Outgoing AI:**

❌ **Assuming docs exist** - Check first
❌ **Writing a novel** - Keep it lean, reference other docs
❌ **Only stating facts** - Capture the discussion and uncertainty
❌ **Vague next steps** - Be specific and actionable
❌ **Skipping red flags** - Warn about known issues

**For Incoming AI:**

❌ **Skipping the handover** - Read it first
❌ **Asking questions answered in handover** - User will notice
❌ **Not providing feedback** - If handover was bad, say so
❌ **Diving straight into code** - Orient yourself first

---

## Example: Good Handover

```markdown
# Handover - Quiz App

## 1. Orientation
New AI: Oriented via onboarding.md. We are in Implementation, midway through Sprint 3.

## 2. The Delta
- **Active Debate**: Extracted the `QuizEngine` (src/quiz/engine.ts). User is unsure if a pure class is too disconnected from React state. We are weighing a `Zustand` store as an alternative but haven't started.
- **Failed Path**: Tried lifting state to the `App` component; it caused a render loop. Do not revert to that.
- **In-Flight**: Engine logic is extracted but tests are currently failing on the transition from Q1 to Q2.

## 3. Next Steps
1. Debug `engine.test.ts` question transition failure.
2. Discuss if `Zustand` is preferred over the current class approach.
```

**Why this is good:**

- Points to other docs without duplicating them
- Captures the refactoring discussion (not in docs yet)
- Shows what was tried (ephemeral context)
- Flags the decision that needs making
- Specific next steps
- Warns about known issue

---

## Remember

**Handover is about the conversation, not just the state.**

Capture what a new AI needs to pick up the discussion where you left off, not just know what's been done.

If incoming AI has to ask "why did we choose X?" or "what have we tried?", the handover failed.

---

## First-Agent Bootstrap (no docs exist yet)

- Create `onboarding.md` with doc locations, workflow, and how to write handovers.
- Create `DEVLOG.md` skeleton and note initial sprint.
- If global preferences are provided, save to `./docs/.agents/global-preferences.md` (or `.agents/...` / `.claude/...` if already used).
- If no spec is needed (meta project), say so explicitly; otherwise create `spec.md`.
- Write a minimal `HANDOVER.md` capturing what you set up and any open decisions.

## Fresh-Context Pickup (later agents)

- Read `onboarding` → `handover` → `spec` → `DEVLOG`.
- Verify the build immediately.
- **Prune the handover**: If the handover context is now obsolete because of your first tool call, update it.
- **Reset Context**: If the conversation gets too long, ask the user: "Should I write a fresh handover and reset our context to keep things fast?"

---

**Continuous improvement:** Incoming AIs should provide feedback if handover was inadequate. This guide evolves based on what actually works.
