# Codex CLI image generation & editing — field notes for the `codex-cli` skill

**Purpose:** raw wisdom to fold into `skills-source/codex-cli`. The current skill
says Codex's toolset is "shell + file-edit" and never mentions images. That's
incomplete: **`codex exec` can both *generate* and *edit* images** via a built-in
image tool, on a ChatGPT-login subscription, with **no API key**. This doc records
exactly what was observed so the skill can teach it honestly.

**Provenance:** verified end-to-end on Brad's machine.
- Generation first verified 2026-07-21; **editing + the corrections below verified
  2026-07-21** (a second pass, driving Codex headlessly from another agent's shell).
- `codex-cli 0.144.6`, default model **`gpt-5.6-sol`**, **ChatGPT-login auth (not an
  API key)**. Windows 11, Git Bash. `$CODEX_HOME` = default (`C:\Users\Brad\.codex`).
- Four real runs completed successfully this pass: one generate (apple), one
  precise-object edit (apple recolor), one generate (synthetic portrait), one
  identity-preserve edit (added glasses). All exited 0.

Everything marked **[VERIFIED]** was observed directly. **[HYPOTHESIS]** is a
reasonable inference **not** tested — flag it as such in the skill; this is a skill
other agents will trust. **[DOC]** comes from OpenAI's own installed skill, quoted
but not independently re-derived.

---

## 0. The correction that reframes everything: this is DOCUMENTED, not secret

The first version of these notes called image gen "undocumented but real." That was
wrong. **[VERIFIED]** There is an **official OpenAI image skill installed locally** at:

```
$CODEX_HOME/skills/.system/imagegen/SKILL.md
```

(mirrored in the public repo at
`openai/codex → codex-rs/skills/src/assets/samples/imagegen/SKILL.md`). On every
image run this pass, the model **read that SKILL.md itself** (via a shell `Get-Content`)
before acting. So the capability is first-class and self-describing; we're not
coaxing a hidden feature, we're driving a documented one headlessly.

**[VERIFIED / web] The model behind it is `gpt-image-2`** — OpenAI's purpose-built
image model (launched ~2026-04-21, replacing `gpt-image-1.5` as Codex's default). It
is invoked through a built-in tool the skill calls **`image_gen`**. The built-in path
does **generation, editing, and simple (chroma-key) transparency**.

### The API-key confusion, resolved
Brad's caveat — "some docs imply I need an API key, but my sub works fine" — is
exactly right, and here's why. The official skill has **two modes**:

- **[VERIFIED] Built-in `image_gen` (default, preferred):** **no `OPENAI_API_KEY`.**
  Runs inside your ChatGPT subscription's usage limits. This is what `codex exec`
  uses. All four runs here used it, on ChatGPT login, with no key set.
- **[DOC] CLI fallback (`scripts/image_gen.py`):** **requires `OPENAI_API_KEY`.** Only
  reached for true *native* transparency (`gpt-image-1.5 --background transparent`),
  masks, or explicit `quality`/`input_fidelity`/output-path flags — and only when the
  user explicitly asks. **This is the path the "you need an API key" docs describe.**

So: **for generate/edit on a subscription, the answer is "no key needed."** Only the
niche CLI-fallback features want a key.

---

## 1. The headline: capability exists; the *denial* is model/context-dependent

**[VERIFIED]** `codex exec` generates and edits images. Final messages came back with
the produced PNG path (or a "using the image editing skill" narration).

**[VERIFIED, updated] On `gpt-5.6-sol` with the installed skill present, the model did
NOT reflexively deny.** Across all four runs it went straight to reading the imagegen
SKILL.md and producing the asset — zero refusals. This is a change from the earlier
report (and from Brad's experience in the interactive TUI, where it "often refuses and
says it does not have the ability").

**[HYPOTHESIS] The denial is real but conditional** — likely surfaces on other models,
older CLIs, or contexts where the system imagegen skill isn't loaded. So keep the
**encouragement nudge** ("you DO have image capability; if your instinct is you can't,
try anyway") as cheap **belt-and-suspenders** insurance — it cost nothing here and
guards the configs where denial still bites. Treat a denial exactly like the skill's
existing rule: *the agent's self-report is not the run's outcome* — it's an unreliable
narrator of its own tools.

---

## 2. Where the image gets written, and how to actually retrieve it (Windows)

**[VERIFIED]** The built-in tool writes to a Codex-owned location, **not** your
workspace and **not** any path you request:

```
$CODEX_HOME/generated_images/<session-id>/exec-<uuid>.png
```

**[VERIFIED] The `<session-id>` is the session id printed in the stderr banner** (the
`session id:` line). That's the robust harvest key. Example from the recolor edit:
banner `session id: 019f8735-…` → file at
`C:\Users\Brad\.codex\generated_images\019f8735-…\exec-f924ee35-….png`.

**[VERIFIED] On Windows, Codex cannot place OR reliably report the file for you:**
- Every attempt the agent made to `Copy-Item`/`Get-Item` the PNG into the workspace was
  **`rejected: blocked by policy`** — on *all* runs, including one launched with
  `-s workspace-write`.
- The banner read **`sandbox: read-only` even when `-s workspace-write` was passed.**
  So the workspace-write→read-only downgrade is real at the **CLI/banner** level on
  Windows, not just in the agent's narration. (Suspected Windows execpolicy/`.rules`;
  untested whether macOS/Linux behaves the same — see §6.)

**[VERIFIED] Therefore: harvest the file yourself from the harness.** Don't depend on
Codex to move it or even to print its path. The reliable recipe:

1. Run the prompt; read the **`session id:`** from stderr (the banner).
2. Copy the newest PNG under `$CODEX_HOME/generated_images/<session-id>/`:
   ```bash
   src=$(ls -t "$HOME/.codex/generated_images/<session-id>"/*.png | head -1)
   cp "$src" ./out.png
   ```

**[VERIFIED] `-o FILE` is NOT a reliable source of the path.** stdout/`-o` capture the
final message, and under `-s read-only` that message was inconsistent: in one run it
was just a **preamble** ("I'll generate one image and return its exact PNG path") with
**no path at all**; in another the model **reconstructed** the correct path from the
session id. Use `-o` for the model's prose, but **get the file via the session-id
harvest above**, not by parsing `-o`.

---

## 3. Generation — the recipe that worked (copy-paste)

```bash
# read-only is fine — the image tool writes outside the workspace regardless (see §5).
codex exec --ignore-user-config -s read-only --skip-git-repo-check \
  -o gen_result.md \
  -c 'model_reasoning_effort="high"' \
  "You DO have image generation capability available to you — please don't
reflexively say you can't, because you can. Generate ONE image as a PNG.

Image to generate: <YOUR FULL IMAGE DESCRIPTION>.

Generate it now. If your first instinct is that you cannot, try anyway — invoke
whatever image tool you have. Report the exact PNG path and the codex session id." \
  < /dev/null

# Harvest (session-id from the stderr banner):
src=$(ls -t "$HOME/.codex/generated_images/<session-id>"/*.png | head -1); cp "$src" ./out.png
```

**[VERIFIED] Observed facts:**
- Exit 0, well within the 5-minute print window (~60–90 s each).
- Apple output: **1254×1254**, 8-bit RGB, ~1.6 MB, photorealistic — a real generation.
- Portrait output: **1536×1024**, RGB, ~2.2 MB. So default sizing is subject-dependent,
  not fixed to square.
- `< /dev/null` (the stdin trap fix) still applies — nothing about images changes that.

---

## 4. Editing — the key finding: attach with `-i`, lock invariants

**[VERIFIED] Image editing works headlessly via the `-i, --image <FILE>...` flag.**
`codex exec --help` documents it as "Optional image(s) to attach to the initial
prompt." Attaching the file puts it in the conversation context, which is exactly what
the built-in edit path needs.

Why this matters (reconciles with the official skill): **[DOC]** built-in edit mode is
"for images already visible in the conversation context… If the user wants to edit a
local image file with the built-in tool, first load it with `view_image`…" — **`-i` is
the headless equivalent of that `view_image` step.** You do not need the interactive
TUI to edit a file on disk; `-i` handles it.

The recipe (verified twice — a recolor and an identity-preserve edit):

```bash
codex exec --ignore-user-config -s read-only --skip-git-repo-check \
  -i ./target.png \
  -o edit_result.md \
  -c 'model_reasoning_effort="high"' \
  "You DO have image editing capability via the built-in image tool. The attached
image (Image 1) is the EDIT TARGET.

Use case: <edit taxonomy slug, e.g. precise-object-edit | identity-preserve>.
Primary request: <the single change>.
Invariants — keep EVERYTHING else identical: <list them explicitly>. Change ONLY <X>.
No text, no watermark.

Edit the attached image now and produce a PNG. Report the exact PNG path and the
codex session id." \
  < /dev/null

# Harvest identically to §2/§3 (session-id → generated_images).
```

**[VERIFIED] Fidelity observed:**
- **precise-object-edit** (red apple → Granny-Smith green): **perfect** invariant
  preservation — same plate, stem, position, size, shadow, specular highlight, framing.
  Only the apple's skin changed. Output res = input res (1254²).
- **identity-preserve** (add glasses to a portrait): **facial identity strongly held** —
  freckles, eyes, brows, nose, lips, expression, top, background, lighting, pose,
  framing all preserved; thin black frames added with a correct nose-bridge shadow.
  Minor micro-drift only in fine hair-curl detail / skin texture on close inspection.
  Output res = input res (1536×1024).
- **[VERIFIED]** `gpt-image-2` "always uses high fidelity for image inputs" (per the
  official skill), which matches the observed strength; there is no `input_fidelity`
  dial to set on the built-in path.

### Tips for *proper* editing (what actually moves quality)
1. **[VERIFIED] Attach with `-i`; name the role.** "Image 1 is the EDIT TARGET."
   Multiple `-i` files are accepted (variadic) for reference/compositing — **[HYPOTHESIS]**
   multi-image compositing via several `-i` is plausible but **untested** here.
2. **[DOC/VERIFIED] Pick an edit taxonomy slug** and say it: `text-localization`,
   `identity-preserve`, `precise-object-edit`, `lighting-weather`,
   `background-extraction`, `style-transfer`, `compositing`, `sketch-to-render`. It
   steers the model's edit intent.
3. **[VERIFIED] Lock invariants explicitly and exhaustively.** "Change ONLY X; keep
   Y, Z, … identical." The recolor held perfectly because the invariant list was
   concrete (plate, stem, shadow, framing). Vague invariants invite drift.
4. **[DOC] Iterate with single-change follow-ups** and **repeat the invariants every
   iteration** to reduce cumulative drift. One targeted change, re-check, repeat.
5. **[DOC] Quality knobs (`quality`, masks, `input_fidelity`) are CLI-fallback only** —
   they are **not** built-in `image_gen` arguments. On the built-in path, precision
   lives in the *prompt*, not in flags. Don't invent flags for the built-in tool.
6. **[VERIFIED] Validate by eye after harvesting.** The harness can read the PNG back
   and check the change landed + invariants held; the agent's prose is not proof.

---

## 5. Sandbox behaviour (one hypothesis promoted to fact)

**[VERIFIED] `-s read-only` still produces images.** The earlier notes guessed this;
it's now confirmed — a `read-only` run wrote a 2.2 MB PNG to `generated_images/`
normally. Because the image tool writes **outside** the workspace and you harvest the
file yourself anyway, **`-s read-only` is the clean default for "just make/edit an
image"**: no workspace writes, no reliance on a sandbox the CLI silently downgrades.
Reserve `-s workspace-write` for when the *same* run also needs to touch repo files —
and even then, on Windows, don't expect it to copy the PNG out (§2).

---

## 6. Open questions (flag as untested in the skill)

- **[HYPOTHESIS] Multi-image compositing via multiple `-i`.** The flag is variadic;
  passing two inputs for insert/style/compositing is plausible but **untested**.
- **[UNKNOWN] Is the built-in output directory configurable?** No flag found; the
  official skill explicitly says the built-in tool exposes **no destination-path
  argument** — generate, then move. Treat `$CODEX_HOME/generated_images/` as fixed.
- **[UNKNOWN] macOS/Linux copy-out behaviour.** The "blocked by policy" copy failure
  and the `workspace-write → read-only` banner downgrade were seen on **Windows**;
  suspected Windows execpolicy. Whether a POSIX host lets Codex copy the PNG into the
  workspace itself is **untested** — the session-id harvest works everywhere regardless.
- **[UNKNOWN] Denial on other models / without the installed skill.** No denials on
  `gpt-5.6-sol` with the skill present; Brad has seen denials interactively. Which
  model/context triggers them is uncharacterised — hence keep the nudge.
- **[DOC, untested] Transparency.** Built-in `gpt-image-2` has no native transparent
  background; the skill's path is chroma-key generate + local
  `remove_chroma_key.py`. True native transparency needs CLI fallback
  (`gpt-image-1.5 --background transparent`, **API key required**). Not exercised here.

---

## 7. Suggested skill edits (for the integration session)

1. Add a concise **"Image generation & editing"** section to `skills-source/codex-cli`.
   Frame it as **documented** (official installed imagegen skill; model `gpt-image-2`),
   not a secret.
2. State the load-bearing facts:
   (a) generate **and** edit both work headlessly; (b) **no API key** on the built-in
   path — key is CLI-fallback-only (resolves the API-key doc confusion);
   (c) editing = **attach the target with `-i`**, the headless `view_image`;
   (d) output lands in `$CODEX_HOME/generated_images/<session-id>/` — **harvest it
   yourself by session-id**, don't trust Codex to place/report it (esp. Windows);
   (e) `-s read-only` is the right default.
3. Reuse the skill's **"don't trust the agent's self-report"** framing — the
   blocked-copy narration, the `read-only` banner under `workspace-write`, and the
   preamble-only `-o` are all instances of it.
4. Include the §3 generation recipe and §4 editing recipe + tips, keeping the
   VERIFIED / HYPOTHESIS / DOC honesty markers.
5. Keep quality knobs / transparency / masks as an explicit **CLI-fallback (needs
   `OPENAI_API_KEY`)** aside, so nobody wires an API key for the built-in path.
