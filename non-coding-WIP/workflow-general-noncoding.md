# AI-Assisted Non-Coding Workflow: General Framework

A distilled workflow framework for large-scale non-coding projects developed with AI assistance. Extracted from real project experience, stripped of project-specific details.

**Use this for**: Books, research papers, course curricula, technical documentation, policy frameworks, any structured knowledge work spanning multiple AI sessions.

---

## The Core Problem

Writing a large structured document (50+ pages) across multiple AI sessions over weeks/months creates these risks:

- **Conceptual drift**: Same term means different things in different sections
- **Tone drift**: Voice changes across sessions or AI tools
- **Example inconsistency**: Same scenario used differently in different places
- **Lost context**: Next session doesn't know what previous session decided
- **Dependency confusion**: Writing Section 5 before Section 2, which it depends on

**Solution**: Adapt software development workflow patterns to writing projects.

---

## The Five-Document Foundation

### 1. SPEC.md — What to Build

**Purpose**: Complete outline with success criteria and dependencies.

**Contains**:
- Section-by-section outline with status (todo/in-progress/done)
- Success criteria for each section ("reader can DO X afterward")
- Dependency map (which sections must exist before others)
- Recommended writing order with phases

**Why it matters**: Prevents "what should I work on next?" paralysis. Ensures logical build order. Makes "done" measurable.

---

### 2. onboarding.md — Agent Entry Point

**Purpose**: Philosophy, tone, and session workflow instructions.

**Contains**:
- Project overview (problem solved, core approach)
- Document philosophy (what this is and is NOT)
- Tone guidelines with concrete examples
- Session-specific workflows (new section, revision, continuity check, handover)
- Key concepts to understand before writing

**Why it matters**: Any AI agent can orient in 5 minutes. Prevents tone drift. Works across all AI tools.

---

### 3. HANDOVER.md — Session-to-Session Context

**Purpose**: Temporal context that changes each session.

**Contains**:
- What just happened (last session summary)
- Current project state
- What's next (recommended focus)
- Open questions or blockers

**Why it matters**: Keeps required reading small and fresh. Separates "what's always true" (onboarding) from "what's current" (handover).

**Critical**: Keep under 100 lines. This is read every session.

---

### 4. voice-samples.md — Tone Reference Library

**Purpose**: Show-don't-tell guide for consistent voice.

**Contains**:
- GOOD examples with "why this works" analysis
- BAD examples with "why this fails" analysis
- Key phrases to use consistently
- Section templates that have proven effective

**Why it matters**: "Be direct" is useless instruction. "Like Example A, not Example B" is actionable. Library grows with project—later sections calibrate against earlier best work.

**Usage**: Read first 5-10 examples during orientation. Reference during writing. Add strong passages after each section.

---

### 5. examples-bank.md — Canonical Examples Tracker

**Purpose**: Ensure same scenario used consistently across sections.

**Contains**:
- Canonical formulation of each major example
- Where example is used (cross-reference)
- Allowed variations
- Notes on what makes it work

**Why it matters**: If your core example appears in 5 sections, it must be identical (or deliberately varied). Prevents contradictions.

**Usage**: Reference during writing, not during orientation.

---

## Lean Reading Protocol

**The trap**: Reference files grow. If agents read everything, orientation consumes 50-70% of context before writing begins.

**The rule**: Reference files are for LOOKUP, not required reading.

**Orientation reading (target ~400 lines)**:
1. onboarding.md (evergreen context)
2. HANDOVER.md (what's current)
3. Your target section from SPEC.md (~30 lines, not whole file)
4. First 5-10 voice examples (~150 lines)

**Skip during orientation** (reference during writing only):
- Full SPEC.md
- Full voice-samples.md
- examples-bank.md
- Previous sections
- DEVLOG.md (HANDOVER summarizes it)

---

## Writing Order: Spiral Development

Don't write linearly (Section 1 → 2 → 3). Write in conceptual phases:

**Phase 1: Foundation**
- Core concepts, first examples
- Establishes voice for everything that follows
- Goal: "Now we know how to write the rest"

**Phase 2: Practical Utility**
- Immediately useful content
- Rich examples across contexts
- Goal: Make it useful before making it complete

**Phase 3: Theoretical Depth**
- Theory can now reference concrete examples from Phase 2
- Goal: Explain why it works

**Phase 4: Specialized Applications**
- Apply framework to specific contexts
- Goal: Context-specific guidance

**Phase 5: Polish**
- Fill remaining sections
- Cross-reference verification
- Consistency pass

---

## Session Protocol

Every session follows the same pattern:

**1. ORIENT (5 min)**
- Read HANDOVER.md
- Read target section from SPEC.md
- Skim first 5 voice examples

**2. CONTEXT (as needed)**
- Read prerequisite sections if writing depends on them
- Check examples-bank.md if reusing examples

**3. WRITE (main work)**
- Draft the section
- Test against success criteria from SPEC.md

**4. DOCUMENT (5-10 min)**
- Update SPEC.md section status
- Update HANDOVER.md for next session
- Add strong passages to voice-samples.md
- Add reusable examples to examples-bank.md

---

## Key Patterns

### Pattern 1: Success Criteria > Word Count

Not "write 2000 words" but "reader can DO X afterward." Makes quality measurable.

### Pattern 2: Template Reuse

Once a template works for one section, replicate exactly for similar sections. Extract proven templates to onboarding.md.

### Pattern 3: Symptom-Based Navigation

Don't organize by features (what the tool does). Organize by symptoms (what pain the user feels). Users search for their problem, not your solution.

### Pattern 4: Strategic Frameworks > Prescriptive Rules

"When X matters, do A; when Y matters, do B" beats "always do A." Acknowledge trade-offs. Give judgment tools, not just rules.

### Pattern 5: Separate Static from Temporal

onboarding.md = always true. HANDOVER.md = what's current. Don't mix them. Static content bloats required reading.

### Pattern 6: Build Systems for Non-Code

Source files (markdown) are for maintainers. Compiled outputs (PDF) are for consumers. Build script bridges the gap. Include timestamps and source-of-truth notices in outputs.

### Pattern 7: Multiple Output Formats

Different audiences need different formats:
- PDF: print, share, offline
- HTML: browser reading with navigation
- Source files: AI navigation, contributions
- ZIP: bulk download

One source, multiple outputs.

---

## Anti-Patterns

### Anti-Pattern 1: Starting Without Structure

Impulse: "Just start writing."
Reality: Without SPEC.md, you don't know what Section 1 needs to accomplish or what depends on it.
Fix: Infrastructure first, content second. 30 min setup saves hours later.

### Anti-Pattern 2: Abstract Style Guidance

Impulse: "Be direct and precise."
Reality: Different people/AIs interpret "direct" differently.
Fix: Concrete GOOD/BAD examples in voice-samples.md.

### Anti-Pattern 3: Reading Entire Reference Files

Impulse: "Read voice-samples.md" (1000+ lines)
Reality: Consumes context window, leaves no room for writing.
Fix: "Read first 10 examples from voice-samples.md" (~150 lines).

### Anti-Pattern 4: Mixing Static and Temporal Content

Impulse: Put session context in onboarding.md
Reality: onboarding.md grows, must be read every session, eventually strangles productivity.
Fix: Separate onboarding.md (evergreen) from HANDOVER.md (current).

---

## Minimal Viable Workflow

If full framework feels like overkill, start here:

**3 files, 30 min setup**:

1. **outline.md**: Numbered sections with brief success criteria
2. **style.md**: 2-3 GOOD examples, 2-3 BAD examples
3. **log.md**: Session template (what was done, decisions, next steps)

**Each session (5 min overhead)**:
- Read last log entry
- Check outline for target section
- Write
- Log what was done

**Scale up as needed**:
- Getting complex? Add dependency map
- Multiple tools? Add onboarding.md
- Reusing examples? Add examples-bank.md

---

## Cross-Tool Compatibility

This workflow works across AI tools because it lives in markdown files:

- Claude (Code, Desktop, web)
- ChatGPT
- Cursor / Windsurf
- Any tool that reads markdown

**Tool-specific notes**:
- Claude Code: Best for file-heavy workflows
- Desktop Claude: Good for long writing sessions
- Web interfaces: Manual file upload; use for one-off sessions
- ChatGPT: Weaker at sustained multi-file context; best for single sections

---

## Metrics for Success

**Working well**:
- New session productive in <10 min
- Tone consistent across weeks
- No contradictions found in polish phase
- Can hand off to different AI tool without re-explaining

**Warning signs**:
- 30+ min re-orienting each session
- Contradictions discovered late
- AI asking questions answered in onboarding.md
- Tone drifts between sections

---

## Evolution Path

**Stage 1**: outline.md + log.md
**Stage 2**: Add style.md with examples
**Stage 3**: Full SPEC.md with dependencies, voice-samples.md
**Stage 4**: Add onboarding.md, HANDOVER.md for multi-tool work
**Stage 5**: Build system, multiple output formats

Scale workflow to project complexity. Stage 5 infrastructure is overkill for Stage 2 projects.

---

**Status**: First-pass extraction from real project. Ready for second pass with coding workflow integration.
