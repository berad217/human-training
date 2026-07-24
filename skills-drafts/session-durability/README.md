# session-durability — change-set spec

**Status:** genuine draft (no `skills-source/session-durability/` — this is not a
skill, it's a **cross-cutting change-set** for existing skills).
**Filed:** 2026-07-24, from a real incident (below).
**Target release:** 1.17.0.

> This folder is a spec, not a skill. Nothing here ships. When the changes land in
> `workflow/guides/` + the builders, delete this folder.

---

## 1. The incident (why this exists)

Two sibling repos, `Blendy_McBlendface` + `blocky-mcblockface`, worked in a joint
session. Session closed via `handover-manager`. The handover it produced said:

> *"Clean stop - nothing in flight, all work committed in both repos
> (Blendy `22e36f1`, Blocky `6854e21` at time of writing)."*

Accurate, precise, cited SHAs — **and both named SHAs were unpushed local tips.**
A full session's work (4 commits in each repo, 8 total) lived on one disk for a
day. Discovered only because a later session happened to run `git push` for an
unrelated reason and saw a 4-commit range fly by.

Nothing was lost. The failure mode is that **the handover asserted safety and was
believed.** A vague handover would have prompted a check; a confident wrong one
did not.

---

## 2. Root cause — three findings, all verified

### 2.1 `handover-manager` is structurally incapable of checking

`skills/handover-manager/SKILL.md:5` (generated — see §3):

```
allowed-tools: [Read, Write, Edit, Grep, Glob]
```

**No `Bash`.** The one skill whose entire job is closing a session safely cannot
run `git status`. It could not verify push state even if instructed to.

For contrast, these already have `Bash`: `lifecycle-manager`, `workflow-orientation`,
`project-checkup`, `start`, `robustness-audit`, `pdf-toc-splitter`.

### 2.2 A word collision hides the bug

`handover-guide.md` mentions "commit" exactly **once**:

> *"Once a decision is committed to a file, DELETE it from the handover."*

That is "committed" in the **prose** sense. The skill's whole ontology is
**Record (files, permanent) vs Bridge (handover, ephemeral)**, and it treats
*written to a file* as the terminal durable state. The unstated axiom is
**"in a file = safe."** On a local disk that is false.

Because git's verb and the skill's verb are the same word, an agent writes
"all work committed" and it is simultaneously true (skill sense) and misleading
(git sense). Nothing in the text forces the distinction.

### 2.3 Push is absent from the entire plugin

Grep of every shipped `SKILL.md` for push/remote/durability discipline:

| Skill | Closest existing text | Gap |
|---|---|---|
| `lifecycle-manager` | *"**Commit Your Work**: Ensure code and DEVLOG are synced."* | Stops at commit. "Synced" = code↔DEVLOG, not local↔remote. |
| `project-checkup` | Runs `git status -sb` — framed as *"uncommitted? unstashed? not on main?"* | Runs the exact command that prints `[ahead N]` and never names ahead/behind as a thing to read. |
| `start` | Has `Bash`, docs-only contract | Never touches git; wouldn't catch drift at session open. |
| `handover-manager` | — | No git awareness at all. |

**Zero occurrences of `git push` anywhere in any skill.** This is not "under-promoted";
durability is a category the plugin's model does not contain.

---

## 3. The `skills/` vs `skills-source/` question — ANSWERED

**These five are in `skills/` but not `skills-source/`:**
`handover-manager`, `lifecycle-manager`, `onboarding-creator`, `project-genesis`,
`workflow-orientation`.

**This is not a bug or a migration gap.** There are **two source tracks**, both
documented in `scripts/build-skills.sh`'s own header comment and in
`skills-drafts/README.md:40-42`:

| Track | Source of truth | Which skills |
|---|---|---|
| **1 — Generated** | `workflow/guides/<file>.md` (body) + a `build_skill` call in **both** builders (frontmatter) | The 5 above |
| **2 — Session-authored** | `skills-source/<name>/` copied through as-is | All 11 others |

The five "missing" ones are exactly the original workflow-doc set — they predate
`skills-source/` and are model-agnostic guides that ship to non-Claude agents too,
which is *why* they stayed in `workflow/guides/`.

### ⚠️ The landmine this creates

`scripts/build-skills.sh:32`:

```bash
# Start clean so skills removed from the build definitions don't linger.
rm -rf "$OUTPUT_DIR"
```

**`skills/` is wiped and regenerated on every build.** Editing
`skills/handover-manager/SKILL.md` directly appears to work, survives testing, and
is silently destroyed on the next build. Any fix MUST go to the track-1 source.

### Recommended follow-up (separate from this change-set)

The two-track split is legitimate but under-signposted at the point of confusion.
Consider a `skills/README.md` (or a header comment in the generated `SKILL.md`)
saying *"GENERATED — do not edit; source is `workflow/guides/<x>.md` +
`scripts/build-skills.{sh,ps1}`"*. That is where someone lands when they go
looking, and there is currently nothing there to redirect them.

---

## 4. Changes required

### 4.1 `handover-manager` — add durability to the close ritual

**PRIMARY FIX.** Three files, all must change together.

**(a) `workflow/guides/handover-guide.md`** — body edits:

1. **New step, before writing the handover** (suggest as "Step 0: Durability
   check", or fold into Step 1 Inventory):

   > Before writing anything, establish whether the work is actually durable.
   > For **each repo touched this session** (a session may span siblings):
   >
   > ```bash
   > git -C <repo> status -sb | head -1
   > ```
   >
   > Read the `[ahead N]` / `[behind N]` marker, not just the file list.
   > - `ahead N` → N commits exist only on this disk. **Say so in the handover
   >   and offer to push.** Do not push unless the user says yes.
   > - No upstream / no remote → say that plainly; "committed" is the ceiling.
   > - Clean and in sync → *then* a clean stop is a clean stop.

2. **Disambiguate the word "committed"** at its one occurrence (§2.2). Suggested:
   *"Once a decision is written to a file (note: 'committed' here means written
   to the doc, NOT `git commit` — see the durability check)…"*

3. **Handover template** — the Orientation/Delta template should carry a
   durability line when non-clean, e.g.:
   `**Durability:** Blendy ahead 4, Blocky ahead 4 — NOT pushed.`
   Suppress the line entirely when everything is in sync (keeps the ≤200-token goal).

4. **New anti-patterns** in the Anti-Patterns section:
   - ❌ **Declaring work safe because it is committed.** Committed ≠ pushed.
     Verify with `git status -sb`, or say the state is unverified.
   - ❌ **Citing commit SHAs as evidence of safety.** A SHA proves a commit
     exists locally and nothing more. (This is precisely what made the 2026-07-23
     handover convincing and wrong.)
   - ❌ **Checking only the cwd repo when the session spanned several.**

**(b) `scripts/build-skills.sh:92-95`** — add `Bash` to allowed-tools:

```bash
build_skill "handover-guide.md" "handover-manager" \
    "<description unchanged>" \
    "Read, Write, Edit, Grep, Glob, Bash" \
    "handover.md"
```

**(c) `scripts/build-skills.ps1:53-58`** — the same change, or CI fails:

```powershell
"handover-guide.md" = @{
    name = "handover-manager"
    description = "<unchanged>"
    allowedTools = @("Read", "Write", "Edit", "Grep", "Glob", "Bash")
    assets = @("handover.md")
}
```

> `verify-skills.yml` byte-compares the output of both builders against committed
> `skills/`. Changing one builder only = red CI.

**(d) `workflow/templates/handover.md`** — mirror the durability line if the
template is meant to stay in lockstep with the guide's template section.

### 4.2 `start` — the cheap safety net (RECOMMENDED)

`start` already has `Bash` in `allowed-tools`; no builder change needed. It is
track 2 (`skills-source/start/SKILL.md`).

Add one read-only command to the orient sequence and one line to the output:

```bash
git status -sb | head -1
```

Output line, shown **only when non-clean** (keep the tight format otherwise):

```
**Durability:** 4 commits unpushed on master — want me to push?
```

**Why this earns its place:** it would have caught the incident a full session
earlier, at the cost of one command, and it is squarely inside `start`'s existing
contract (read-only, docs-only, no writes, no tests). Reading git state is not a
build or a test.

**Decision needed:** does this violate the "docs-only" contract in spirit?
Recommendation: **no** — the contract exists to prevent *writes and side effects*,
and `git status` is strictly read-only. But it is Brad's call.

### 4.3 `lifecycle-manager` — extend "Commit Your Work" (SMALL)

Track 1: body in `workflow/guides/lifecycle.md`. Already has `Bash`, so **no
builder change**.

Current: *"**Commit Your Work**: Ensure code and DEVLOG are synced."*
Extend to name the second half: commit, then verify the commit is pushed (or
state explicitly that it is not), so "done" means durable rather than merely
recorded.

### 4.4 `project-checkup` — name the ahead/behind field (TINY)

Track 2: `skills-source/project-checkup/SKILL.md`. Already runs `git status -sb`
and already has `Bash`. It just doesn't tell the agent to *read* the ahead/behind
marker. Add unpushed-commit count to the health table and to the friction audit
("work stranded locally" is exactly the dormant-project failure this skill exists
to surface).

---

## 5. Design constraint — surface and offer, never auto-push

`onboarding.md:246` already lists as an anti-pattern:

> *"Running `git commit`/`git push` without being asked. This is a shared remote.
> Stage changes, show the user, let them push."*

Every change above must therefore **report and offer**, never push autonomously.
The bug being fixed is a *silent false assurance*, not a missing automation. Do not
"fix" it by making agents push on their own — that trades a visibility bug for a
consent bug.

---

## 6. Verification checklist

Build integrity:

- [ ] `./scripts/build-skills.sh` runs clean
- [ ] `./scripts/build-skills.ps1` runs clean
- [ ] Both produce byte-identical `skills/` (this is what `verify-skills.yml` enforces)
- [ ] `git diff skills/` shows the expected regenerated output and **nothing unexpected deleted** (remember `rm -rf` — confirm all 16 skills still exist)
- [ ] `skills/handover-manager/SKILL.md` frontmatter now reads `[Read, Write, Edit, Grep, Glob, Bash]`

Behavioural (the real test — the build passing proves nothing about behaviour):

- [ ] In a repo with deliberately unpushed commits, request a handover → agent runs the check, reports `ahead N`, and **offers** to push
- [ ] In a clean in-sync repo → no durability line appears; handover stays lean (≤200 tokens)
- [ ] In a repo with **no remote configured** → agent says so rather than erroring or claiming safety
- [ ] Multi-repo session (Blendy + Blocky is the live regression case) → **both** repos checked, not just cwd
- [ ] `/start` in a drifted repo surfaces the unpushed count at orient
- [ ] No agent pushes without explicit user approval

Regression guard:

- [ ] Re-read the 2026-07-23 Blendy handover wording. The new guide must make
      *"all work committed (SHA, SHA)"* impossible to write without a push check.

---

## 7. Release steps

1. Land the edits (guides + both builders + template).
2. Run **both** build scripts; confirm byte-identical output.
3. Bump `version` in **both** `.claude-plugin/plugin.json` and
   `.codex-plugin/plugin.json` (currently `1.16.0` → `1.17.0`).
4. Update the repo `HANDOVER.md`.
5. Commit, push, tag, release.
6. `/plugin update human-training@human-training`, then verify
   `handover-manager` actually has Bash at runtime.
7. Delete `skills-drafts/session-durability/` (this folder).

---

## 8. Open questions for the implementing session

1. **`start` scope** (§4.2) — accept the git read inside a docs-only skill? *Rec: yes.*
2. **Multi-repo discovery** — how does the agent know which repos a session touched?
   Options: (a) ask the user, (b) check cwd + siblings named in onboarding/handover,
   (c) cwd only and say so. *Rec: (b), degrade to (a).* The Blendy/Blocky bridge is
   the motivating case and is discoverable from onboarding.
3. **Is `handover-manager` the right home at all**, or should durability be a
   tiny shared checklist that `handover-manager` + `lifecycle-manager` +
   `project-checkup` all reference? *Rec: inline in handover-manager now (one
   place, real bug); extract only if it starts drifting between skills.*
4. **`skills/README.md` redirect** (§3) — do it in this release or file separately?
