# Workflow Orientation — reference

Lookup material for the workflow-orientation guide. Nothing here is required
reading; each section is pointed at from the step that needs it.

## Candidate locations for canonical docs (§1)

- `onboarding.md`: project root, `docs/onboarding.md`, `docs/.agents/onboarding.md`
- `DEVLOG.md`: project root, `docs/devlog.md`, `docs/DEVLOG.md`
- Handover: `HANDOVER.md`, `docs/.agents/current-handover.md`,
  `.agents/current-handover.md`, legacy `.claude/current-handover.md`
- Global preferences: `docs/.agents/global-preferences.md`, legacy
  `.agents/global-preferences.md`
- Project memory: `memory/MEMORY.md`, `docs/memory/MEMORY.md`
- Folders worth noting: `docs/.agents/`, `docs/`, `.claude/`, `memory/`

## DEVLOG skeleton (Empty state)

````markdown
# Development Log - <Project Name>

## Sprint 0 - Genesis

**Status:** Not yet started.

---

<!-- Sprint entries accumulate below as work proceeds. Each entry: Summary, Decisions, Testing, Concerns/Risks, Next Sprint. -->
````

For a *Code, no workflow* project the first entry is instead a "Pre-skill
history" note: prior work is not captured here because git pre-dates the
workflow.

## Gap report (Partial state)

| Doc | Status | Recommended action |
|---|---|---|
| `onboarding.md` | present / present-but-incomplete / missing | propose patch / propose creation / skip |
| `DEVLOG.md` | same | same |
| Handover doc | same | same |
| `docs/.agents/` meta-guides | check each | propose copy from plugin assets |

One confirmation per row.

## Template completeness (drift check, signal 4)

- `onboarding.md`: a top-level project heading; a "Getting Oriented" section
  with doc-location pointers; an "About This Human" section or a reference to
  `global-preferences.md`; a "How We Work" / workflow section.
- `DEVLOG.md`: at least one sprint entry with Summary, Decisions, Testing,
  Concerns/Risks, Next Sprint.
- Handover (if used): Orientation, The Delta, Next Steps, plus a Durability
  line whenever work is unpushed. A "what we accomplished" section is a status
  report that belongs in the DEVLOG; its absence is correct, not a gap.

## Discussion summary (§3)

```
**Project state:** <state> (confidence: <high|medium|low>)

**Key findings:**
- <observation>
- <observation>

**Proposed actions:**
- <action 1>
- <action 2>
```

## Memory migration boilerplate (§6)

The `CLAUDE.md` pointer, at the project root:

```markdown
## Memory is repo-local
Project memory lives in `memory/`, indexed in `memory/MEMORY.md`. Never write
memory to `~/.claude/` — it does not travel between machines. If your harness
hands you a global memory directory, override it and write here instead.
```

The tombstone that replaces the global `MEMORY.md`:

```markdown
# Moved
This project's memory now lives in `<repo path>/memory/`, indexed in
`memory/MEMORY.md`. Read it there. Do not write memory here — it does not
travel between machines.
```

Host note: the global path above is Claude Code's. Codex has no per-project
memory directory of this shape; in a Codex session §6 reduces to "is there a
stranded Claude directory for this cwd, and is the repo private?" — the
migration itself is the same six steps.

## History

- 2026-05-23: skill designed (`docs/specs/2026-05-23-workflow-orientation-design.md`).
- 2026-07-24: §6 (memory placement) added after a solo developer's memory
  silently failed to travel between two machines.
- 2026-09-19: guide trimmed 2,501 → ~1,480 words. Anti-patterns folded into the
  step each guards; templates, path lists and boilerplate moved here; `Reply:`
  contract added. Section numbers kept — `start` and `genesis` cite §6 by number.
