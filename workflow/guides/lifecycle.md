# Lifecycle: The Active Development Protocol

**Purpose**: This is your daily operations manual. Use it for orientation, decision-making, and context management once implementation has begun.

---

## 1. Orientation & Context Hygiene

### Know Your Environment

- **Cursor/Windsurf**: High integration. Use codebase search and terminal tools.
- **Claude Code (CLI)**: Terminal-centric. Use `grep` and `find` aggressively.
- **Web App**: Limited terminal. Focus on high-level design and explicit file reads.

### Context Hygiene

- **Be Lazy**: Don't read a 1000-line file until you need to edit it. Use outlines first.
- **Reference, Don't Copy**: Name files/docs; don't dump their entire content into chat.
- **Orient by relevance**: Read temporal context fully (latest DEVLOG entry, current handover). For large reference docs, pull only the slice you need — your target section of the spec, not the whole file. Reference files are for lookup, not required reading.
- **Watch the proportion, not a line count**: There is no fixed orientation budget — a bigger project legitimately needs more orientation. The warning sign is proportional: if orienting consumes a large share of your context before any work begins, you're treating lookup files as required reading. Read more selectively; never skip context you actually need.

### Joining a "Moving Train"

If you arrive mid-project:

1. **Read `onboarding.md` (if present)**: Use its "Getting Oriented" section as your map for where DEVLOG, handover, spec, and other docs actually live in this project. This is essential in projects bridged to non-canonical layouts; in canonical layouts it just confirms the defaults. If no `onboarding.md` exists, proceed with the defaults below.
2. **Read the latest DEVLOG entry**: At the path from `onboarding.md`, or default: `DEVLOG.md`, `./docs/devlog.md`. Learn the recent technical baggage.
3. **Read the current Handover**: At the path from `onboarding.md`, or default: `HANDOVER.md`, `./docs/.agents/current-handover.md`. Learn what's currently "breaking" or being debated.
4. **Verify the Build**: Run the tests immediately. Don't trust the environment until the terminal proves it.

---

## 2. Decision Making: The Confidence Bar

When faced with ambiguity, use this threshold:

- **HIGH CONFIDENCE**: Routine task, follows spec exactly. -> **Just do it.**
- **MODERATE CONFIDENCE**: Spec is ambiguous, but there's a clear "best" path. -> **Do it, but highlight the choice in the DEVLOG.**
- **LOW CONFIDENCE**: Multiple valid paths with significant tradeoffs, or spec is silent. -> **STOP. Propose 2-3 options to the human and wait for a decision.**

---

## 3. Token-Sparing Execution (Testing)

Testing in an AI-human loop requires efficiency. High-volume output kills the context window.

### Concise Output by Default

- **Rule**: Always run tests with `--reporter=dot` and `--bail` (fail-fast).
- **Automation**: Check `package.json` for agent-optimized scripts (`npm test`).

### Failure Analysis Workflow

1. **Run Concise**: See what failed without the noise.
2. **Log Redirection**: Pipe full output to `test_results.log`.
3. **Targeted Debugging**: Only read the log or run the specific failing test in verbose mode if necessary.

---

## 4. Documentation Rules

### DEVLOG (The Record)

- **Rule**: NEVER paste raw test logs or full coverage tables into the DEVLOG.
- **Do**: Summarize passes/fails, coverage percentages, and critical technical decisions.
- **rationale**: The DEVLOG is a permanent record of *intent* and *progress*, not a terminal dump.

### The Handover (The Bridge)

- **The Ephemeral Delta**: A handover contains ONLY the conversation context that isn't in the files yet.
- **Strict Pruning**: As soon as a decision is committed to code or the Spec, delete it from the handover.
- **The Overwrite Rule**: NEVER delete and recreate the handover file in one turn. **Always overwrite** to avoid IDE synchronization failures.

---

## 5. Context Reset Logic

If the conversation grows long and the IDE starts to lag or hallucinate:

1. **Update the Handover**: Capture the current "in-flight" delta.
2. **Commit Your Work**: Ensure code and DEVLOG are synced.
3. **Ask for Reset**: "I've updated the handover. Should we reset the context to keep things fast?"
