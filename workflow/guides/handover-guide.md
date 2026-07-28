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
**Rule**: Once a decision is written to a file, DELETE it from the handover.

> **Word warning**: "committed" in the sentence above is the *prose* sense —
> written down to a doc. It is NOT `git commit`. The two senses collide, and the
> collision is how a handover ends up asserting that work is safe when it is
> sitting unpushed on one laptop. See Step 0.

---

### Step 0: Durability Check (do this before anything else)

The Record/Bridge split above has an unstated axiom: **"in a file = safe."** On a
local disk that is false. A file is one disk away from gone, and a commit that was
never pushed is invisible to every other machine and every future session.

So before you write a word of handover, establish whether the work is actually
**durable**.

**Which repos to check.** A session often spans more than one repo (sibling
projects, a library plus its consumer). Check, in order:

1. The repo you are working in.
2. Any sibling repos named in `onboarding.md` or in the current handover.
3. If you are not sure the session was confined to those, **ask the user** —
   "did we touch any repo besides X today?" is one question and it closes the gap.

**The check**, run in each repo:

```bash
git status -sb
```

Read the **first line**, and specifically the `[ahead N]` / `[behind N]` marker —
not just the list of modified files. The file list tells you about *uncommitted*
work. The marker tells you about *undurable* work. Those are different failures
and only one of them is obvious.

| First line shows | What it means | What to write |
|---|---|---|
| `## main...origin/main` (no marker) | Committed **and** pushed | Nothing — a clean stop is genuinely clean |
| `## main...origin/main [ahead 4]` | 4 commits exist **only on this disk** | Say so, and **offer to push** |
| `## main` (no upstream) | No remote or no tracking branch | Say it plainly — "committed" is the ceiling here |
| Modified / untracked files listed | Uncommitted work in flight | Ordinary Delta material (§2) |

**Never push on your own.** Report the state and offer; the user decides. Pushing
unasked trades a visibility bug for a consent bug — and the remote may be shared.

If you cannot run commands at all (no shell access in your environment), say so
explicitly: *"Push state unverified — I can't run git here."* An honest unknown is
useful. A confident wrong "all work committed" is what this step exists to prevent.

---

### Step 1: Inventory What Exists

**Don't assume documentation exists.** Check what's actually in the project:

```bash
# What docs are present?
- [ ] onboarding.md (how to work with this human)
- [ ] docs/.agents/global-preferences.md (communication style) — legacy aliases: `.agents/global-preferences.md`, `.claude/global-preferences.md`
- [ ] SPEC.md or similar (what to build)
- [ ] CONTEXT.md (the project's glossary / shared language)
- [ ] DEVLOG.md (what was built and why)
- [ ] Code (actual implementation)

**If paths are unclear, search these common locations:**
- onboarding: `onboarding.md`, `./docs/onboarding.md`, `./docs/.agents/onboarding.md`, `.agents/onboarding.md`, `.claude/onboarding.md`
- global preferences: `./docs/.agents/global-preferences.md`, `.agents/global-preferences.md`, `.claude/global-preferences.md`
- handover: `HANDOVER.md`, `./docs/.agents/current-handover.md`, `.agents/current-handover.md`, `.claude/current-handover.md`, `./docs/handover.md`
- spec: `spec.md`, `SPEC.md`, `./docs/spec.md`, `./documentation/spec.md`
- context: `CONTEXT.md`, `./docs/CONTEXT.md`
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
| CONTEXT.md | The project's shared vocabulary (glossary) | Plans, decisions, implementation — those live in spec/DEVLOG |
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

**Durability line — include ONLY when something is not pushed.** Omit it entirely
when every repo is committed and in sync; a clean stop needs no line, and the
handover has a 200-token budget to protect.

```markdown
**Durability:** Blendy ahead 4, Blocky ahead 4 — committed but NOT pushed.
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
4. **Flush the glossary**: If any domain terms got sharpened or coined this session, land them in `CONTEXT.md` now (if the project keeps one). Terms are Record, not Delta — they belong in the glossary, not the handover.

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

**Durability (see Step 0):**

❌ **Declaring work safe because it is committed** - Committed ≠ pushed. Verify with `git status -sb`, or say the state is unverified.
❌ **Citing commit SHAs as evidence of safety** - A SHA proves a commit exists *on this disk*. It proves nothing about the remote, and its precision makes the claim more convincing, not more true.
❌ **Checking only the current repo when the session spanned several** - A sibling repo strands work just as easily, and nobody thinks to look there.
❌ **Pushing on your own initiative** - Surface and offer. The remote is usually shared; consent is not yours to assume.

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

## Example: The Handover That Looked Perfect And Wasn't

This is a real one. It is the reason Step 0 exists.

```markdown
## 1. Orientation
Clean stop - nothing in flight, all work committed in both repos
(Blendy `22e36f1`, Blocky `6854e21` at time of writing).
```

Accurate. Precise. Cited SHAs. **Both SHAs were unpushed local tips.** Eight
commits across two repos lived on a single disk for a day, and were found only
because a later session happened to run `git push` for an unrelated reason and
watched a four-commit range fly past.

Note what went wrong: nothing was *false*. The work genuinely was committed. The
failure is that a confident, specific claim of safety **stops the next agent from
checking**. A vague handover would have prompted a look; this one guaranteed
nobody would.

The fix is one command before you write. If Step 0 had run, the line would have
read `**Durability:** Blendy ahead 4, Blocky ahead 4 — NOT pushed.` and the work
would have been safe within the minute.

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
