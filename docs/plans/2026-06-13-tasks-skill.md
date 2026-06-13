# tasks skill (+ start integration) — Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Author the `tasks` skill (a per-project `TASKS.md` forward queue with a mission-creep guardrail), wire it into the existing `start` skill so Active tasks surface at session open, ship in plugin 1.11.0, in a single implementation commit.

**Architecture:** Track 2 (session-authored) skill, auto-copied by both build scripts into `skills/tasks/`. The SKILL.md is the whole artifact — no `workflow/guides/` source, no `$skillDefinitions` build-script edit. Two pragmatic refinements vs the design doc, both narrowing scope: (1) author directly in `skills-source/tasks/` rather than `skills-drafts/` → graduate, because nothing needs to stay in a drafts scratchpad (the design lives in `docs/specs/`); (2) inline the 8-line `TASKS.md` starter into SKILL.md instead of a separate `assets/TASKS-template.md`, avoiding an asset file and relative-path resolution. The `start` integration is a content-only edit to the existing `skills-source/start/SKILL.md`.

**Tech stack:** Markdown + JSON only. No code to unit-test; verification is build-pipeline correctness (`diff -r skills /tmp/skills-rebuild` empty), manifest validity/alignment (`scripts/verify-plugin-manifests.py`), and structural checks (frontmatter parses, sections present, JSON parses, `start` references TASKS).

**Source of truth for content:** [docs/specs/2026-06-13-tasks-skill-design.md](../specs/2026-06-13-tasks-skill-design.md). Full SKILL.md, eval, and `start` edits are inlined below — no need to re-derive from the spec.

**Commit cadence:** One implementation commit at the end (new skill + start edit + rebuilt `skills/` + both manifests + README + this plan doc). The design doc is already committed (`c00d9f6`). **No pushes** — surface staged changes; the user pushes when ready, then runs `update-plugin.bat` + restart to load it.

---

## Task 1: Scaffold `skills-source/tasks/`

**Files:**
- Create: `skills-source/tasks/evals/` (directory)

- [ ] **Step 1: Create the skill + evals directories**

```powershell
New-Item -ItemType Directory -Force -Path "D:\Coding_projects\human-training\skills-source\tasks\evals" | Out-Null
```

- [ ] **Step 2: Verify**

```powershell
Test-Path "D:\Coding_projects\human-training\skills-source\tasks\evals"
```

Expected: `True`.

---

## Task 2: Write `skills-source/tasks/SKILL.md`

**Files:**
- Create: `skills-source/tasks/SKILL.md`

**Reference:** design doc "SKILL.md structure (the spine)". The template block is inlined here (no separate asset).

- [ ] **Step 1: Write the file verbatim**

````markdown
---
name: tasks
description: Use when managing a project's task list / todos — adding, reviewing, or completing tasks, or parking a tangent or "I should also…" idea so it doesn't derail current work. Maintains a per-project TASKS.md (Active / Someday / Done). Triggers on /tasks, "add a task", "what's on my list", "park that for later", "what was I going to do next". Offers to capture commitments and tangents mid-work, always confirming first. Do NOT use for recording decisions or rationale (that's the DEVLOG) or for workplace contact/jargon memory.
allowed-tools: [Read, Write, Edit, Glob]
---

# /tasks — Per-project forward queue

A lightweight task list for the current project that doubles as a mission-creep
guardrail. It holds what's **next** and what's **parked**, so a tangent gets
captured instead of derailing the task in hand.

It complements the DEVLOG, it does not duplicate it: **DEVLOG is
backward-looking** (decisions made and why); **TASKS is forward-looking** (what's
queued, parked, done). Don't put rationale here; don't put todos there.

## The file

One file per project: `TASKS.md` at the project root (fall back to
`./docs/TASKS.md` if the project keeps working docs under `docs/`). Three
sections. If the file is absent when you need it, create it from this template:

```markdown
# Tasks

## Active
<!-- current + next-up work -->

## Someday
<!-- the parking lot: tangents, "I should also…", deferred ideas -->

## Done
<!-- completed, newest first -->
```

Line format:
- Open task: `- [ ] **Short title** — one-line context (for what / blocked on what)`
- Done task: `- [x] ~~Short title~~ (YYYY-MM-DD)`

## Managing tasks

Invoked explicitly with `/tasks`, or in natural language ("add a task to…",
"what's on my list?", "mark X done").

- **Show** (default, no verb): summarize **Active**, and flag anything that reads
  stale or overdue. Don't dump Someday or Done unless asked.
- **Add**: insert into **Active** (or **Someday** for a parked idea) with a
  one-line context. Confirm the wording if it's ambiguous.
- **Done**: tick the checkbox, strike the title, append `(today's date)`, move it
  under **Done** (newest first).

## Notices & offers (the guardrail)

While this skill is loaded in a session, watch for the user voicing a tangent, a
fresh idea, or a commitment mid-work ("oh, I should also refactor X", "we need to
handle Y eventually"). When you spot one, **offer** to capture it:

> "Want me to park that in Someday so we stay on \<current Active item\>?"

Rules:
- **Always confirm before writing. Never auto-add a task.**
- Default a tangent to **Someday** (a parking lot, not a new priority); only put
  it in Active if the user says it's the next thing.
- This watching only works while the skill's instructions are in context — a
  session where `/tasks` or `/start` has loaded it. There is no background
  capture; that's by design.

## Anti-patterns

- **Turning Done into a changelog.** Done is a checkbox + date. The *why* of a
  decision goes in the DEVLOG, not here.
- **Surfacing Someday unprompted.** The parking lot stays parked until asked.
  Showing it during normal work re-introduces the exact distraction it exists to
  prevent.
- **Auto-adding.** Always offer and confirm. The user's list is the user's.
- **Recording decisions or workplace/jargon memory here.** Wrong tool — that's
  the DEVLOG and the memory system respectively.
````

- [ ] **Step 2: Verify frontmatter parses and `name:` matches the directory**

```powershell
$content = Get-Content "D:\Coding_projects\human-training\skills-source\tasks\SKILL.md" -Raw
if ($content -notmatch '(?s)^---\s*\n(.*?)\n---') { Write-Error "Frontmatter not parseable" }
if ($content -notmatch 'name:\s*tasks') { Write-Error "name does not match directory" }
Write-Host "OK: frontmatter parses, name matches"
```

Expected: `OK: frontmatter parses, name matches`.

- [ ] **Step 3: Verify all sections present**

```powershell
$content = Get-Content "D:\Coding_projects\human-training\skills-source\tasks\SKILL.md" -Raw
$required = @('# /tasks', '## The file', '## Managing tasks', '## Notices & offers', '## Anti-patterns')
foreach ($h in $required) { if ($content -notmatch [regex]::Escape($h)) { Write-Error "Missing: $h" } }
Write-Host "OK: all sections present"
```

Expected: `OK: all sections present`.

---

## Task 3: Write `skills-source/tasks/evals/trigger-eval.json`

**Files:**
- Create: `skills-source/tasks/evals/trigger-eval.json`

**Reference:** design doc "evals/trigger-eval.json". Shape matches `skills-source/robustness-audit/evals/trigger-eval.json`.

- [ ] **Step 1: Write the JSON verbatim**

```json
[
  { "query": "add a task to wire up the retry logic in the fetch client", "should_trigger": true },
  { "query": "park that streaming-parser idea for later so I don't lose it", "should_trigger": true },
  { "query": "what's on my list — what was I going to do next here?", "should_trigger": true },
  { "query": "mark the backoff util task as done", "should_trigger": true },
  { "query": "log in the devlog why we chose exponential backoff over a fixed delay", "should_trigger": false },
  { "query": "remember that the staging API key rotates every 90 days", "should_trigger": false },
  { "query": "what does this parseResponse function actually do?", "should_trigger": false },
  { "query": "create a handover for the next session before I stop", "should_trigger": false }
]
```

- [ ] **Step 2: Verify JSON parses and 4+4 split**

```powershell
$json = Get-Content "D:\Coding_projects\human-training\skills-source\tasks\evals\trigger-eval.json" -Raw | ConvertFrom-Json
if ($json.Count -ne 8) { Write-Error "Expected 8 entries, found $($json.Count)" }
$t = ($json | Where-Object { $_.should_trigger -eq $true }).Count
$f = ($json | Where-Object { $_.should_trigger -eq $false }).Count
if ($t -ne 4 -or $f -ne 4) { Write-Error "Expected 4+4, got $t+$f" }
Write-Host "OK: 4 should-trigger + 4 should-not-trigger"
```

Expected: `OK: 4 should-trigger + 4 should-not-trigger`.

---

## Task 4: Wire `TASKS.md` into the `start` skill

**Files:**
- Modify: `skills-source/start/SKILL.md`

Four edits. Each is an exact old→new replacement. Do NOT touch `skills/start/SKILL.md` — it's build output, regenerated in Task 5.

- [ ] **Step 1: Edit A — add TASKS.md to the locate list (§1)**

Old:
```markdown
- **Handover**: `./HANDOVER.md` → `./docs/.agents/current-handover.md` → `.agents/current-handover.md` → legacy `.claude/current-handover.md`
```
New:
```markdown
- **Handover**: `./HANDOVER.md` → `./docs/.agents/current-handover.md` → `.agents/current-handover.md` → legacy `.claude/current-handover.md`
- **TASKS.md**: project root → `./docs/TASKS.md`
```

- [ ] **Step 2: Edit B — read the Active section (§2)**

Old:
```markdown
- **Current handover, in full** — this is the ephemeral delta: what was
  in-flight, breaking, or being debated. Read all of it (it's short by design).
```
New:
```markdown
- **Current handover, in full** — this is the ephemeral delta: what was
  in-flight, breaking, or being debated. Read all of it (it's short by design).
- **TASKS.md — Active section only, if present** — the forward queue. Read the
  **Active** items (not Someday, the parking lot; not Done). Skip silently if
  there's no TASKS.md.
```

- [ ] **Step 3: Edit C — surface Active in the orientation template (§3)**

Old:
```markdown
**Last DEVLOG entry:** <date + one-line summary>

**Next:** I'd suggest <X> because <Y>. 1) <X> (recommended). 2) <alt>. 3) Stop / set your own direction.
```
New:
```markdown
**Last DEVLOG entry:** <date + one-line summary>
**Active tasks:** <top 1–3 from TASKS.md Active — omit this line entirely if there's no TASKS.md>

**Next:** I'd suggest <X> because <Y>. 1) <X> (recommended). 2) <alt>. 3) Stop / set your own direction.
```

- [ ] **Step 4: Edit D — let the next move draw from Active**

Old:
```markdown
Keep it tight. The point is to remove inertia, not to produce a report. If the
handover or DEVLOG names a concrete unfinished task, that *is* the recommended
next move — don't invent alternatives just to fill the list.
```
New:
```markdown
Keep it tight. The point is to remove inertia, not to produce a report. If the
handover, DEVLOG, or TASKS Active names a concrete unfinished task, that *is* the
recommended next move — don't invent alternatives just to fill the list.
```

- [ ] **Step 5: Edit E — add an anti-pattern guarding the Active-only rule**

Old:
```markdown
- **Reading everything.** Latest DEVLOG entry, not the whole log. Onboarding
  map, not the whole file. Temporal context only.
```
New:
```markdown
- **Reading everything.** Latest DEVLOG entry, not the whole log. Onboarding
  map, not the whole file. From TASKS, the **Active** section only — never
  surface Someday or Done at orient. Temporal context only.
```

- [ ] **Step 6: Verify the five edits landed**

```powershell
$content = Get-Content "D:\Coding_projects\human-training\skills-source\start\SKILL.md" -Raw
$markers = @('TASKS.md**: project root', 'Active section only', 'Active tasks:', 'or TASKS Active', 'surface Someday or Done')
foreach ($m in $markers) {
    if ($content -notmatch [regex]::Escape($m)) { Write-Error "Missing edit marker: $m" }
}
Write-Host "OK: all five start edits present"
```

Expected: `OK: all five start edits present`.

---

## Task 5: Build + verify the CI invariant

- [ ] **Step 1: Run the PowerShell build**

```powershell
& "D:\Coding_projects\human-training\scripts\build-skills.ps1"
```

Expected: completes without error; `skills/tasks/` is created and `skills/start/SKILL.md` reflects the edits.

- [ ] **Step 2: Confirm the new + edited outputs exist**

```powershell
Test-Path "D:\Coding_projects\human-training\skills\tasks\SKILL.md"
Test-Path "D:\Coding_projects\human-training\skills\tasks\evals\trigger-eval.json"
(Get-Content "D:\Coding_projects\human-training\skills\start\SKILL.md" -Raw) -match 'Active tasks:'
```

Expected: `True`, `True`, `True`.

- [ ] **Step 3: Run the sh build into a temp dir and diff against committed `skills/`**

```bash
cd "D:/Coding_projects/human-training"
rm -rf /tmp/skills-rebuild
OUTPUT_DIR=/tmp/skills-rebuild bash scripts/build-skills.sh > /dev/null 2>&1
diff -r skills /tmp/skills-rebuild && echo "DIFF-CLEAN"
```

Expected: `DIFF-CLEAN` (no diff output). If non-empty, the usual cause is line endings/trailing whitespace in the new files — fix in `skills-source/tasks/` (the builders normalize to LF/no-BOM) and re-run.

---

## Task 6: Bump both plugin manifests 1.10.1 → 1.11.0

**Files:**
- Modify: `.claude-plugin/plugin.json`
- Modify: `.codex-plugin/plugin.json`

New skill = feature add = minor bump. **Both manifests must match** (`verify-plugin-manifests.py` checks alignment).

- [ ] **Step 1: Bump `.claude-plugin/plugin.json` version + add `tasks` to the description**

Change:
```json
  "version": "1.10.1",
```
to:
```json
  "version": "1.11.0",
```
And in the `description`, change the session-authored list ending `…project-checkup, leroy-jenkins).` to `…project-checkup, leroy-jenkins, tasks).`

- [ ] **Step 2: Bump `.codex-plugin/plugin.json` version**

Change:
```json
  "version": "1.10.1",
```
to:
```json
  "version": "1.11.0",
```
(The codex description is generic — no list to update.)

- [ ] **Step 3: Verify versions aligned**

```powershell
python "D:\Coding_projects\human-training\scripts\verify-plugin-manifests.py"
```

Expected: ends with `Plugin manifests are valid and version-aligned.` and exit code 0.

---

## Task 7: Add `tasks` to the README skills table

**Files:**
- Modify: `README.md`

- [ ] **Step 1: Read the skills table to match its exact column order**

```powershell
Get-Content "D:\Coding_projects\human-training\README.md" -Raw | Select-String -Pattern '(?s)## Available Skills.*?\n\n' | ForEach-Object { $_.Matches.Value }
```

- [ ] **Step 2: Add a row for `tasks`, matching the columns you just saw**

Cells to use (reorder to match the table's actual columns):
- **name:** `**tasks**`
- **source:** `skills-source/`
- **what:** `Per-project TASKS.md forward queue (Active/Someday/Done) + mission-creep guardrail`
- **when:** `Managing project todos; parking tangents so they don't derail current work; Active items surface at session start via /start`

- [ ] **Step 3: Verify the row landed**

```powershell
Get-Content "D:\Coding_projects\human-training\README.md" -Raw | Select-String 'tasks.*forward queue'
```

Expected: one match.

---

## Task 8: Final verification + commit

- [ ] **Step 1: Re-run the round-trip build check + manifest check**

```bash
cd "D:/Coding_projects/human-training"
rm -rf /tmp/skills-rebuild
OUTPUT_DIR=/tmp/skills-rebuild bash scripts/build-skills.sh > /dev/null 2>&1
diff -r skills /tmp/skills-rebuild && echo "DIFF-CLEAN"
```
```powershell
python "D:\Coding_projects\human-training\scripts\verify-plugin-manifests.py"
```

Expected: `DIFF-CLEAN`, then `Plugin manifests are valid and version-aligned.`

- [ ] **Step 2: Stage everything**

```bash
git add skills-source/tasks/ \
        skills-source/start/SKILL.md \
        skills/ \
        .claude-plugin/plugin.json \
        .codex-plugin/plugin.json \
        README.md \
        docs/plans/2026-06-13-tasks-skill.md
```

- [ ] **Step 3: Show staged changes for review**

```bash
git status --short
```

Expected: new `skills-source/tasks/*` and `skills/tasks/*`; modified `skills-source/start/SKILL.md`, `skills/start/SKILL.md`, both manifests, `README.md`; new plan doc.

- [ ] **Step 4: Commit**

```bash
git commit -m "$(cat <<'EOF'
Add tasks skill (per-project TASKS.md) + surface Active tasks in /start

New Track 2 skill: a per-project TASKS.md forward queue (Active / Someday /
Done) that doubles as a mission-creep guardrail — offers to park tangents in
Someday (always confirming) so they don't derail the Active task. Complements
the DEVLOG (backward-looking decisions) rather than duplicating it.

start now reads TASKS.md Active at orient and lets it inform the proposed next
move; degrades to current behavior when no TASKS.md exists.

Plugin 1.10.1 -> 1.11.0 (both manifests); README skills table updated.

Co-Authored-By: Claude Opus 4.8 (1M context) <noreply@anthropic.com>
EOF
)"
```

- [ ] **Step 5: Confirm working tree clean**

```bash
git status
```

Expected: `nothing to commit, working tree clean`. **Do not push** — leave that to the user.

---

## Self-review (planner, before handoff)

1. **Spec coverage:**
   - SKILL.md spine → Task 2. evals → Task 3. start integration (locate/read/next-move) → Task 4. Build + CI invariant → Tasks 5, 8. Version bump (both manifests) → Task 6. README → Task 7. Non-goals (no dashboard/sync/decoding/Waiting-On) are realized by absence — nothing to implement.
   - Two spec deviations, both narrowing and flagged in the Architecture note: direct-to-`skills-source/` (no drafts dance), and template inlined into SKILL.md (no `assets/TASKS-template.md`). The design doc's `assets/` line is intentionally dropped.

2. **Placeholder scan:** none. SKILL.md, eval JSON, and all five `start` edits are inlined verbatim. The only "read first" step (Task 7 Step 1) is to match an existing table's columns, with the exact cell content provided.

3. **Type/name consistency:** `tasks` used for skill name and every path; `TASKS.md` capitalization consistent; section names Active/Someday/Done consistent across SKILL.md, the start edits, and the design doc; version `1.11.0` in both manifests.

4. **Test analogue:** structural checks per draft task (frontmatter, sections, JSON shape, start-edit markers) + the round-trip build diff and manifest verify (Tasks 5, 8). The `trigger-eval.json` is created as a future-use artifact; running it is not part of this plan (consistent with the gemini-api plan).

---

## Execution handoff

Plan complete and saved to `docs/plans/2026-06-13-tasks-skill.md`. Two execution options:

**1. Subagent-Driven (recommended)** — Dispatch a fresh subagent per task, review between tasks. Good here because Task 2 (SKILL.md voice) and Task 4 (start edits) benefit from a look before moving on.

**2. Inline Execution** — Execute in this session via executing-plans, batched with checkpoints. Good if you want minimal context-switching; the plan is concrete enough to run start-to-finish.

Which approach?
