# Handover — human-training

**Session date:** 2026-07-22
**State:** Plugin bumped to **1.16.0**, both manifests aligned. **New skill `image-gen`
graduated and built** (5 generated + 11 session-authored). `diff -r` byte-identical,
`verify-plugin-manifests.py` green — **CI will pass**. **NOT yet committed or pushed** —
working tree has the changes staged for review. This was workflow #2 (build a skill in
`skills-drafts/`) → graduate to `skills-source/` → workflow #1 (wire + version bump).

---

## Recent work (this session)

1. **New capability skill `image-gen` (1.16.0).** Claude can now **generate *and* edit
   photorealistic images** by driving Codex's built-in `image_gen` tool (model
   **`gpt-image-2`**) — **on a ChatGPT sub, no `OPENAI_API_KEY`**. Verified end-to-end
   this session with four real `codex exec` runs (generate apple → recolor edit;
   generate synthetic portrait → identity-preserve add-glasses edit). Fidelity was
   excellent (recolor held every invariant; identity edit held the face, minor hair
   micro-drift).
2. **Framed as a *capability* skill, not a CLI skill** — deliberately. Image intent
   ("make me an image", "edit this photo") never says "codex", so burying it in
   `codex-cli` would make it fire on the wrong surface. Its frontmatter description
   advertises the capability so Claude discovers it from image-shaped asks.
3. **Thick-on-delta, not a mirror of OpenAI's skill.** The official `imagegen` skill is
   installed at `$CODEX_HOME/skills/.system/imagegen/SKILL.md` and the model **reads it
   at runtime** on every image call — so `image-gen` does NOT copy its prompt taxonomy/
   size tables (staleness trap). It owns the *headless-driving* delta: `-i` to attach edit
   targets, session-id harvest, the Windows blocked-copy gotcha, `-s read-only` default,
   the no-API-key clarification, the denial nudge. Thin pointer to `codex-cli` for the
   generic CLI mechanics; `codex-cli` got a one-line cross-ref back.
4. **Triggering validated** — blind subagent judges (harness eval 401s on Windows), 3×20
   queries, **unanimous 10/10 both directions**, zero collisions with `canvas-design` /
   `algorithmic-art` / `dataviz` / `frontend-design`. Caveat: queries were clean-cut;
   borderline "logo/icon/illustration" phrasings weren't stressed.
5. **README skills table de-drifted** — it had silently dropped `codex-cli` and
   `antigravity-cli` (shipped in prior sessions). Added those two + `image-gen`; count
   12→16; tree counts fixed (8→11 session-authored).

## The delta (not in the files)

- **Full image field notes live in `skills-drafts/image-gen/field-notes.md`** (the
  renamed `CODEX_IMAGE_GEN_WISDOM.md` Brad had dropped at repo root — moved into the
  draft folder as research residue). Read it for the VERIFIED/HYPOTHESIS/DOC-marked
  details behind the skill. `skills-drafts/image-gen/README.md` records the design
  decisions + a graduation checklist.
- **The API-key confusion is resolved (Brad's original caveat):** the built-in path needs
  **no key**; a key is only for the **CLI fallback** (`scripts/image_gen.py`, true native
  transparency via `gpt-image-1.5`, masks). That fallback path is what the "need an API
  key" docs describe. Don't wire a key for normal image work.
- **Windows harvest reality (verified):** the image tool writes to
  `$CODEX_HOME/generated_images/<session-id>/exec-*.png` regardless of `-s`, and Codex
  **cannot** copy it into the workspace ("blocked by policy" every time; banner reads
  `sandbox: read-only` even under `-s workspace-write`). Harvest it yourself via the
  `session id:` from the stderr banner. `-o` is unreliable for the path (sometimes just a
  preamble). `-s read-only` still generates fine — it's the clean default.
- **Test images** from this session live only in the session scratchpad (not committed —
  repo shouldn't carry test PNGs).

## Parked / carried

- **PUSH IS PENDING.** Nothing committed. Brad pushes (admin → direct to `main`;
  `enforce_admins=false`, and the `gh` token here can't do PRs — see
  [[gh-token-cannot-do-prs]]). After push: `update-plugin.bat` + full relaunch per machine.
- **Open empirical gaps** (from field-notes §6, flagged HYPOTHESIS/UNKNOWN in the skill):
  - Real-photo identity fidelity on a *known* face — only synthetic tested (Brad offered a photo).
  - Multi-image compositing via multiple `-i` — flag is variadic; untested.
  - macOS/Linux copy-out — the Windows blocked-copy may be OS-specific execpolicy.
  - Adversarial triggering round on borderline "logo/icon/illustration" queries.
- **`ollama`** — still a live, low-priority draft; graduate when it earns it.
- Branch protection on `main` remains enabled (required checks `verify-bash` +
  `verify-powershell`, PR required with 0 approvals, `enforce_admins=false` so admins push
  directly).

---

*Ephemeral bridge — prune once absorbed. Durable record: the shipped `image-gen` skill
(`skills-source/image-gen/SKILL.md`), its field notes + README in
`skills-drafts/image-gen/`, the `codex-cli` cross-ref, and the 1.16.0 manifests.*
