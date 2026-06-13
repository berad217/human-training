# human-training

Workflow rails for hobby projects where a human and an AI build software together. You bring the taste and the questionable ideas; the agent brings the typing speed and the bottomless patience. This repo keeps you both pointed the same way — and yes, it's a sibling of [`markdown_reticulator`](https://github.com/berad217/markdown_reticulator), so it reticulates the occasional spline too.

It's called *human*-training. After a few sprints you stop being sure who's training whom.

**Key trick:** the workflow lives in plain markdown that works with *any* AI (Claude, GPT, Gemini, Cursor, whatever). The Claude Code and Codex skills are generated from that same source — so the docs and the skills never drift apart.

> **🤖 AI agent that just landed in this repo: read [onboarding.md](onboarding.md) first.**
> This repo *builds* the plugin — its relationship to its own skills is upside-down
> from a normal project. Five minutes of onboarding saves you from a whole genre
> of sensible-looking mistakes.

---

## Two ways to use this repo

This is really two repos wearing one trench coat:

**You just want some skills.** That's most people. Point your coding agent at
this repo and say *"read through this, tell me what's useful, and take it"* — or
skim [the skills table](#the-skills) and lift the folder you want. Everything
past that table (the build pipeline, the two source tracks, the CI invariant) is
**not your problem**. That machinery is what makes the repo *look* complicated;
as a consumer you can cheerfully ignore all of it.

**You want to add your own skills.** *Now* the pipeline matters — and yes, it's
the fiddly bit. It's written up under [How the repo is wired](#how-the-repo-is-wired)
and [Shipping a change](#shipping-a-change-to-your-other-machines). Come back for
it when you're actually building a skill; until then it's just noise you can
scroll past.

---

## Quick start

### Any AI tool (the model-agnostic path)

1. Copy the contents of `workflow/` into your project's `docs/.agents/`.
2. Tell your AI: *"Read `docs/.agents/onboarding-guide.md` and help me create onboarding.md."*
3. Start working: *"Read onboarding.md and let's begin Sprint 1."*

No plugin, no install, no lock-in. It's just markdown your agent reads.

### Claude Code (the comfortable path)

The skills ship as a Claude Code **plugin**. Once per machine, inside Claude Code:

```
/plugin marketplace add berad217/human-training
/plugin install human-training@human-training
```

After install, everything is namespaced under `human-training:` —
`/human-training:project-genesis`, `/human-training:start`,
`/human-training:lifecycle-manager`, and friends (full roster below).

Hacking on *this* repo itself? Skip the marketplace entirely and load the plugin
straight off disk:

```
claude --plugin-dir .
```

Optionally run `./scripts/setup-machine.ps1` to also symlink the global CLAUDE.md.

### Codex

The same built `skills/` tree is exposed through `.codex-plugin/plugin.json`.
Wire it up as a Codex local/personal plugin pointing at this checkout. Codex
reads the exact same `skills/` output Claude Code does; the Codex manifest just
describes the package to Codex. Keep the two manifests on the same `version` —
CI checks.

---

## The skills

Twelve of them. The first five are generated from model-agnostic workflow docs
(Track 1); the rest are session-authored Claude skills (Track 2). What that
distinction means is two sections down — for now, just grab the one you need.

| Skill | Track | What it does | Reach for it when |
|-------|-------|--------------|-------------------|
| **project-genesis** | workflow/guides/ | Sprint 0: pressure-tests an idea, then turns it into a real spec | You've got an idea and it needs challenging, scoping, and writing down |
| **lifecycle-manager** | workflow/guides/ | The day-to-day build loop: orient → implement → test → log → assess | You're actually building |
| **handover-manager** | workflow/guides/ | Captures the ephemeral delta before a context reset | The context window's filling up, or you're switching sessions |
| **onboarding-creator** | workflow/guides/ | Writes a project's onboarding.md — the office tour, not the policy manual | Setting up a new project |
| **workflow-orientation** | workflow/guides/ | Retrofits this whole workflow onto a project that doesn't have it yet | Adopting the sprint scaffold in an existing repo |
| **start** | skills-source/ | One-keystroke session opener: reads the temporal docs + TASKS Active, proposes the next move. Read-only, never touches code | The very first prompt of a fresh session |
| **tasks** | skills-source/ | Per-project `TASKS.md` (Active / Someday / Done) plus a guardrail that offers to park tangents in Someday | Tracking todos; stopping a shiny tangent from hijacking the task in hand |
| **grill** | skills-source/ | Adversarial pre-build alignment — pokes holes in the plan against your own docs *before* you write code | Right before building, to find out why it won't work while it's still cheap |
| **robustness-audit** | skills-source/ | Defect-class audit of existing code (reads it carefully, doesn't run it) | Back in a codebase after a while; a pre-release "what's likely broken?" pass |
| **project-checkup** | skills-source/ | State-aware health check: orientation + robustness audit + next-move + friction inventory | Re-entering a dormant or half-abandoned hobby project |
| **leroy-jenkins** | skills-source/ | Autonomy-biased mode that turns about-to-expire token quota into useful work, logging its calls to the DEVLOG | You've got quota about to reset and nothing queued. *(Name is a warning, not an accident.)* |
| **gemini-api** | skills-source/ | Current Gemini-API working reference so the agent stops defaulting to stale 3.x patterns | Writing, reviewing, or migrating Gemini code |

---

## How the repo is wired

Two manifests (`.claude-plugin/` for Claude Code, `.codex-plugin/` for Codex)
point at the *same* built `skills/` tree and must carry the same `version`. CI
runs `scripts/verify-plugin-manifests.py` to keep them honest.

```
human-training/
├── .claude-plugin/
│   ├── plugin.json              # Plugin manifest (name, version)
│   └── marketplace.json         # Single-plugin marketplace catalog (source: "./")
├── .codex-plugin/
│   └── plugin.json              # Codex manifest — same skills/, same version
│
├── workflow/                    # SOURCE OF TRUTH (model-agnostic)
│   ├── guides/                  # Track 1 skill bodies (genesis, lifecycle, …)
│   ├── templates/               # Starter docs shipped to downstream projects
│   └── claude-code.md           # Global CLAUDE.md template — customize this!
│
├── skills-source/               # Track 2: ready-to-ship session-authored skills
│   ├── start/  tasks/  grill/   #   each a complete SKILL.md (+ assets/evals),
│   ├── robustness-audit/        #   copied through to skills/ byte-for-byte
│   ├── project-checkup/  leroy-jenkins/
│   └── gemini-api/
│
├── skills-drafts/               # In-progress ideas. Tracked in git, NEVER shipped.
│   └── <idea>/                  #   the messy workshop; research, half-baked drafts
│
├── skills/                      # BUILD OUTPUT — do not hand-edit
│   ├── project-genesis/  …      #   5 generated from workflow/guides/
│   └── start/  tasks/  …        #   7 copied from skills-source/
│
├── scripts/
│   ├── build-skills.ps1         # Windows builder
│   ├── build-skills.sh          # Linux/Mac builder (and what CI runs)
│   ├── verify-plugin-manifests.py
│   └── setup-machine.ps1        # Link the global CLAUDE.md
│
├── update-plugin.bat            # One-click "pull the latest plugin on this machine"
│
└── .github/workflows/
    └── verify-skills.yml        # CI: committed skills/ must match a fresh build
```

---

## The three workspaces

Skills grow up in three places: a messy workshop, and two source tracks that
feed the build. Only the two tracks ship.

```
┌──────────────────────────────────────────────────────────────┐
│  skills-drafts/<idea>/          (THE WORKSHOP — never ships)  │
│  Raw research, half-formed SKILL.md drafts, footgun notes,    │
│  candidate eval queries. Be as messy as you like. Both        │
│  builders ignore it; CI doesn't watch it. A draft physically  │
│  cannot leak into the plugin.                                 │
│                    ↓ graduate to one of the two tracks        │
└──────────────────────────────────────────────────────────────┘

┌──────────────────────────────────────────────────────────────┐
│  workflow/guides/*.md           (TRACK 1 — GENERATED)         │
│  Model-agnostic markdown. The source of truth for the         │
│  sprint-workflow skills, and usable on its own by any AI.     │
│  Frontmatter lives in $skillDefinitions inside both           │
│  build-skills scripts.                                        │
│                    ↓ build-skills  →  skills/<name>/SKILL.md   │
├──────────────────────────────────────────────────────────────┤
│  skills-source/<name>/          (TRACK 2 — PASS-THROUGH)      │
│  Fully-formed Claude skills. Drop them in complete            │
│  (SKILL.md + any assets/evals).                               │
│                    ↓ build-skills (copy)  →  skills/<name>/    │
│                       (byte-identical to the source)          │
└──────────────────────────────────────────────────────────────┘
```

**Workshop (`skills-drafts/`)** — raw material or a SKILL.md you're still wrestling with.

**Track 1 (`workflow/guides/`)** — the skill body is genuinely model-agnostic and you also want a standalone doc GPT/Gemini/Cursor can read.

**Track 2 (`skills-source/`)** — the skill is Claude-specific (subagents, Claude Code tooling) and was authored in a session. The SKILL.md *is* the artifact, not a translation of a generic doc.

CI (`verify-skills.yml`) rebuilds `skills/` on every push and fails if the
committed tree is stale or the two manifests disagree on version. Translation:
if you hand-edit `skills/`, the robots will tattle.

---

## Shipping a change to your other machines

This is the part everyone trips on, so read it twice.

When you change anything that ends up in the plugin:

```powershell
# edit workflow/ files or drop a skill into skills-source/, then:
./scripts/build-skills.ps1
# bump "version" to the SAME value in BOTH plugin manifests
python scripts/verify-plugin-manifests.py
git add . && git commit -m "Update workflow"
git push
```

A push is **not** instantly live. `autoUpdate` only refreshes the marketplace
catalog at Claude Code *startup*, and it's flaky — so each other machine has to
be told, explicitly:

```bash
claude plugin marketplace update human-training      # refresh the catalog (the step everyone forgets)
claude plugin update human-training@human-training   # install the new version
# then fully quit + relaunch Claude Code
```

Skip that first line and `plugin update` cheerfully reports "you're on the
latest" while sitting versions behind — the single most common way to lose an
afternoon to this plugin. (Codex installs may also need a reinstall/cache
refresh and a fresh thread.)

**Shortcut:** [`update-plugin.bat`](update-plugin.bat) at the repo root runs both
commands for you — run it on any machine, then relaunch. It pulls from GitHub, so
it works even where this repo isn't cloned. One catch: `plugin update` keys off
the **version number, not the content**, so the shortcut is only reliable if you
bump `version` on every skills change. Forget the bump and the new content
silently stays home.

### Adding a session-authored skill (Track 2)

When a session produces a workflow worth keeping:

1. Have that session package it into a complete `<skill-name>/` folder: `SKILL.md`
   with valid frontmatter (`name:` matches the dir, `description:` tuned for
   trigger accuracy) plus any `assets/` or `evals/`.
2. Drop the folder into `skills-source/<skill-name>/`.
3. Open a session in this repo: *"I dropped a new skill in skills-source — wire it in."*
4. It'll validate the frontmatter, run the build, bump both manifests, and commit.
5. On each machine: `update-plugin.bat` (or the two commands above), then restart.

### Developing a skill here from scratch (Track 1 or the workshop)

No session with perfect context lying around? Build it here:

1. Make `skills-drafts/<idea-name>/` and dump in whatever you've got — research,
   API references, footgun notes, transcripts.
2. Iterate on `skills-drafts/<idea-name>/SKILL.md` in place. Nothing here ships,
   so make a mess.
3. When it's ready, **graduate** it — move it to `skills-source/<idea-name>/`
   (dropping research you don't want shipped), then follow the Track 2 steps. Or,
   if the body is truly model-agnostic, promote it to a `workflow/guides/` doc +
   a definition in both build scripts.

See `skills-drafts/README.md` for the workshop convention.

---

## The workflow itself

### Phase 0 — idea to spec

1. **Brainstorm** with `/human-training:project-genesis` — it challenges
   assumptions, red-teams the idea, checks whether the thing already exists, and
   forces you to define scope.
2. **Write the spec** with the same skill (ideation flows straight into speccing)
   — concrete JSON examples, not hand-wavy prose.
3. **Create onboarding** with `/human-training:onboarding-creator` — the office
   tour for whatever AI shows up next.

### Phase 1–N — implementation

Follow `/human-training:lifecycle-manager`:

1. **Orient** — onboarding → handover → spec → DEVLOG (`/human-training:start` does this for you)
2. **Implement** — a feature from the spec
3. **Test** — immediately; tests are part of "done," not a someday-chore
4. **Document** — DEVLOG the decisions *and the reasoning*
5. **Assess** — use the Confidence Bar to pick the next move

### Context management

Reach for `/human-training:handover-manager` when the context window's filling,
you're stuck and want a fresh perspective, or you've hit a natural pause.

**The Ephemeral Delta** is the key idea: a handover captures only what's *not in
the files yet*. The moment a decision lands in code or docs, delete it from the
handover. Keep it lean — a couple hundred tokens beats a wall of text nobody
re-reads.

---

## Customization

### Your communication style

Edit `workflow/claude-code.md` (the global CLAUDE.md template) so it reflects how
*you* actually work — the **About This Human** section covers communication,
background, learning style, feedback preferences, and what you value. Run
`./scripts/setup-machine.ps1` afterward to install your version to
`~/.claude/CLAUDE.md`.

> **Note:** older versions shipped a separate `workflow/global-preferences.md`.
> It's been folded into `claude-code.md` — one source of truth, fewer files to
> keep in sync.

### Project-specific overrides

Any project can keep its own `.claude/` folder that wins over the globals:
project CLAUDE.md beats global CLAUDE.md, project skills beat global skills, and
project `docs/.agents/` docs are used preferentially.

---

## Design principles

1. **Conversational, not prescriptive** — office tour, not a compliance binder.
2. **Planned fuzziness** — missing docs and odd file locations are expected, not errors.
3. **The AI codes *and* tests** — same agent implements and verifies.
4. **Examples over descriptions** — show the JSON, don't describe it.
5. **Honest assessment** — no sugarcoating; a DEVLOG concern is an action item.
6. **Model-agnostic first** — works with any AI; Claude Code is the optional comfort layer.

---

## FAQ

**Q: Do I need Claude Code to use this?**
A: No. The workflow docs are plain markdown and work with any AI. The Claude Code and Codex skills are an optional convenience.

**Q: What if I switch AI tools mid-project?**
A: Fine. `spec.md`, `DEVLOG.md`, and `onboarding.md` are plain markdown — any agent can pick up where the last one left off.

**Q: How do I update skills after editing workflow docs?**
A: Run `./scripts/build-skills.ps1`, bump `version` in *both* manifests, commit, push. Then on each machine run `update-plugin.bat` (or `claude plugin marketplace update human-training` → `claude plugin update human-training@human-training`) and restart. It is not automatic — see "Shipping a change" above.

**Q: Can I add my own skills?**
A: Yes, two ways. **Track 1:** add a `workflow/guides/<name>.md` plus a matching definition in *both* build scripts — use this when the body is model-agnostic and you want a standalone doc too. **Track 2:** drop a complete `<name>/` folder into `skills-source/` — use this for Claude-specific skills where the SKILL.md *is* the artifact.

---

## Philosophy

**It's a partnership.** The human designs at the top level, the AI implements, and communication is the whole game.

**It's for hobby projects.** Optimized for non-professional developers who'd rather hand the technical complexity to an agent and stay in the driver's seat on direction.

**It should evolve.** These guides aren't scripture. When you find a better pattern, update them.

---

## Credits

The `grill` skill is adapted from [Matt Pocock's skills](https://github.com/mattpocock/skills)
(MIT, © 2026 Matt Pocock) — his `grill-me` and `grill-with-docs`, merged into a
single docs-aware skill. The `CONTEXT.md` glossary idea comes from the same
place. If the adversarial-alignment flavor lands for you, the original is well
worth a star.

---

## License

Use freely, modify as needed, share improvements.

---

**Next:** install the plugin, then start your next project with `/human-training:project-genesis`. Or, if you're returning to one that's gone quiet, `/human-training:project-checkup`.
