# image-gen (draft)

**Status:** genuine draft — no matching `skills-source/image-gen/` yet, so nothing
ships. Iterating on the `SKILL.md` (chiefly its triggering description) before graduation.

**What it is:** advertises + teaches Claude's ability to *generate and edit raster/
photographic images* by driving the Codex CLI's built-in `gpt-image-2` tool (no API key,
on a ChatGPT subscription). Framed as a capability skill, not a CLI skill, so it triggers
on image intent ("make me an image", "edit this photo") rather than CLI intent.

**Design decisions (settled with Brad, 2026-07-21):**
- Its own skill, **not** buried in `codex-cli` — image intent ≠ CLI intent, so a separate
  triggering surface is the whole point.
- **Thick on our delta, not a mirror of OpenAI's skill.** The official `imagegen` skill is
  installed at `$CODEX_HOME/skills/.system/imagegen/SKILL.md` and the model reads it at
  runtime, so we do NOT copy its prompt taxonomy/size tables (staleness trap). We own the
  *headless driving* wisdom: `-i` to attach edit targets, session-id harvest, Windows
  blocked-copy, `-s read-only` default, the no-API-key clarification, the denial nudge.
- **Thin pointer to `codex-cli`** for generic headless rules (stdin trap, `-o`, model
  tiers, install/auth). `codex-cli` gets a one-line cross-ref back (add at graduation).

**Files:**
- `SKILL.md` — the draft, iterated in place.
- `field-notes.md` — the verified dogfood wisdom this skill distills (4 real runs).

## Before graduating to `skills-source/image-gen/`

1. **Triggering check (the risky part).** Its description collides with `canvas-design`
   (png/pdf design via code), `algorithmic-art` (p5.js generative), `dataviz`/charts,
   and `frontend-design`. Validate with **blind subagent judges** (the harness trigger-eval
   is broken on Windows — nested `claude -p` 401s): give N general-purpose agents the
   unlabeled queries + a realistic menu (image-gen + those confusables + "none"), tally
   majority vote vs gold labels. Target: image/photo/edit queries → image-gen; SVG/chart/
   code-art queries → the others.
2. **Add the `codex-cli` cross-ref** ("Codex can also make/edit images — see `image-gen`").
3. **Frontmatter**: confirm `name:` matches the dir, `allowed-tools:` well-formed.
4. Graduate per onboarding workflow #1: move `SKILL.md` → `skills-source/image-gen/`
   (leave `field-notes.md`/this README as residue), build, verify `diff -r` parity,
   bump both plugin manifests (minor — feature add), update README skills table.

## Open empirical gaps (from field-notes §6)
- Multi-image compositing via multiple `-i` (untested).
- Real-photo identity fidelity on a *known* face (synthetic only so far — Brad offered a photo).
- macOS/Linux copy-out behaviour (Windows blocked-copy may be OS-specific).
