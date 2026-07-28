# ⚠️ GENERATED — DO NOT EDIT

Everything in this directory is **build output**. It is deleted and regenerated
from scratch on every build (`rm -rf skills/`), so any edit you make here works,
survives your testing, and is then silently destroyed the next time anyone runs
a build. CI will also fail: `verify-skills.yml` byte-compares this tree against
a fresh build.

**Edit the source instead.** There are two tracks, and which one a skill belongs
to determines where its source lives:

| Track | Skills | Source of truth |
|---|---|---|
| **1 — Generated** | `handover-manager`, `lifecycle-manager`, `onboarding-creator`, `project-genesis`, `workflow-orientation` | Body: `workflow/guides/<source>.md`<br>Frontmatter: the matching entry in **both** `scripts/build-skills.sh` and `scripts/build-skills.ps1` |
| **2 — Session-authored** | everything else | `skills-source/<name>/` — copied through as-is |

The five track-1 skills are the original model-agnostic workflow docs. They ship
to non-Claude agents too, which is why their bodies live in `workflow/guides/`
with the Claude-specific frontmatter synthesized at build time.

**If you change frontmatter (name, description, allowed-tools, assets) you must
change both builders.** They are required to produce byte-identical output;
editing one is guaranteed red CI.

## Rebuild

```bash
./scripts/build-skills.sh      # or ./scripts/build-skills.ps1 on Windows
```

Verify the invariant before pushing:

```bash
OUTPUT_DIR=/tmp/skills-rebuild bash scripts/build-skills.sh
diff -r skills /tmp/skills-rebuild    # must be empty
python scripts/verify-plugin-manifests.py
```

See [`../onboarding.md`](../onboarding.md) for the full pipeline.
