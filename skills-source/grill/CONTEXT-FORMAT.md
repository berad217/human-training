# CONTEXT.md format

`CONTEXT.md` is a project's **domain glossary** — a shared language between you
and the agent. It exists to do one thing: let both of you say a lot in few
words. "There's a problem with the materialization cascade" instead of "there's
a problem when a lesson inside a section of a course is given a real spot in the
file system." That concision pays off every session.

It is **not** an `onboarding.md` (the office tour — where things live, how to
work), **not** a `spec.md` (what to build), and **not** a `DEVLOG.md` (what was
decided and why). It is a glossary, and nothing else. Keep implementation
details, plans, and decisions out — the moment they leak in, it stops being a
fast reference and becomes another doc nobody trusts.

Keep it at the project root. Keep it short — a glossary you can read in 30
seconds is one the agent will actually use.

## Structure

```markdown
# Context — [Project Name]

A shared language for this project. Terms defined once, used everywhere —
in conversation, in code (variable/function/file names), in the docs.

## Language

**[Term]**:
[One or two sentences. What it *is*, precisely. Distinguish it from the
nearest concept it gets confused with.]
_Avoid_: [looser synonyms that should not be used for this concept]

**[Term]**:
[definition]
_Avoid_: [synonyms to avoid]

## Relationships

- A **[Term]** holds many **[Term]**
- A **[Term]** carries one **[Term]** at a time
- [the structural facts that the definitions alone don't capture]

## Flagged ambiguities

- "[word]" was used to mean both [X] and [Y] — resolved: [X] is now **[Term]**,
  [Y] is now **[Term]**.
- [open ambiguities not yet resolved, so the next session knows they're live]
```

## Rules

- **Define against confusion.** A good entry says what the term is *and* what it
  is not ("the Customer, not the User"). The contrast is where the value is.
- **`_Avoid_` lists earn their keep.** Naming the loose synonyms you're
  retiring is what stops the language from drifting back.
- **Relationships are first-class.** "An Order holds many Line Items" is the
  kind of fact that keeps naming and reasoning consistent across the codebase.
- **Flag ambiguities you haven't resolved.** A live ambiguity recorded is worth
  more than a clean-looking glossary that hides it.
- **Write lazily.** Add a term only when it's actually load-bearing — when
  getting it wrong would cost you. An exhaustive glossary nobody reads is worse
  than a five-term one everybody does.

## Example

```markdown
# Context — course-video-manager

## Language

**Lesson**:
A single teachable unit. Belongs to exactly one Section. Has draft content
before it is materialized.
_Avoid_: video, clip, page

**Materialization**:
Giving a Lesson a real location in the file system, turning it from a draft
record into on-disk content.
_Avoid_: publishing, exporting, building

## Relationships

- A **Course** holds many **Sections**; a **Section** holds many **Lessons**
- **Materialization** cascades: materializing a Section materializes its Lessons

## Flagged ambiguities

- "real" was used for both "materialized" and "published" — resolved:
  on-disk = **Materialized**; visible to learners = **Published**.
```
