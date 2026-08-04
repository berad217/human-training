---
name: image-gen
description: "Use when the user wants to CREATE or EDIT a raster/photographic image — 'generate an image', 'make a photo/logo/hero/mockup/sprite/icon-art', 'edit this picture', 'change/add/remove/replace X in this image', img2img, style or background swaps, identity-preserving edits, upscale-style redo. Claude CAN do this (like ChatGPT/DALL·E) by driving the Codex CLI's built-in gpt-image-2 tool — no API key, runs on a ChatGPT subscription. Do NOT use for code-native or vector visuals (SVG icons, charts/dataviz, CSS/HTML/canvas UI, algorithmic/generative art) — those have their own skills; and do NOT use for the OpenAI image API directly (this is the subscription/CLI path)."
allowed-tools: [Bash, Read, Write, Glob]
---

# Image generation & editing — via the Codex CLI

**Yes, you can generate and edit images.** Not by calling an API you don't have a key
for — by driving the **Codex CLI**, which ships a built-in image tool (`image_gen`,
backed by OpenAI's **`gpt-image-2`**). It runs inside the user's **ChatGPT
subscription** with **no `OPENAI_API_KEY`**. Text→image *and* image→image (editing) both
work headlessly. Output is genuine photorealistic quality, not placeholders.

This skill is the **image capability**; the Codex CLI is just the delivery mechanism.
For the generic headless-Codex rules it builds on (the stdin trap, `-o` capture, model
tiers, install/auth), see the **`codex-cli`** skill — this skill only re-states the
image-specific parts.

**Verified against `codex-cli 0.144.6` and re-verified on `0.146.0`, default model
`gpt-5.6-sol`, ChatGPT-login auth, on Windows (Git Bash).** Every flag below is unchanged
across those versions — but flags do drift, so confirm with `codex exec --help`.

## TL;DR — the five things that make this work

1. **You can do it; say so in the prompt.** Codex's model sometimes *reflexively denies*
   it can make images (more so in older CLIs / other models / when its installed image
   skill isn't loaded). Open your prompt with an explicit "you DO have image capability;
   if your instinct is you can't, try anyway." Cheap insurance; harmless when unneeded.
2. **No API key.** The built-in path runs on the ChatGPT sub. A key is only for the CLI
   *fallback* (true native transparency, masks) — see [Auth](#auth--the-api-key-myth).
3. **Edit by attaching the target with `-i FILE`.** That puts the image in Codex's
   context — the headless equivalent of the interactive `view_image` step. Variadic:
   `-i a.png -i b.png` for reference/compositing.
4. **Harvest the output yourself.** Codex writes the PNG to
   `$CODEX_HOME/generated_images/<session-id>/exec-*.png` and — at least on Windows —
   **cannot** copy it into your workspace. Read the `session id:` off the stderr banner
   and copy the file out. Take that id from the **banner**, never from the model's prose —
   it has been observed reporting a confidently wrong one (§4).
5. **`-s read-only` is the right default.** The image tool writes outside the workspace
   regardless, and you're harvesting yourself — so no write sandbox is needed.

## 1. Prereqs (one-time)

- **Codex CLI installed and logged in** (`npm i -g @openai/codex`; `codex login`). Install
  and auth details live in the `codex-cli` skill. If `codex` isn't on PATH in a
  non-interactive shell, call it by full path (Windows: `"$HOME/AppData/Roaming/npm/codex"`).
- **Detect the CLI with `codex --version`, never by checking for `~/.codex`.** The Codex
  *desktop app* creates that directory — auth included — with no CLI installed, so
  "`~/.codex` exists and has a valid `auth.json`" is not evidence you can run anything.
  If `codex` turns out to be missing, `npm i -g @openai/codex` takes seconds and inherits
  the app's existing login. Full trap (including the bundled binary you'll find in there
  and shouldn't use) in **`codex-cli` §2**.
- **No `OPENAI_API_KEY` required** for anything in the main path below.
- Confirm the capability is live with a cheap probe before a big job if unsure.

## 2. Generate an image

```bash
codex exec --ignore-user-config -s read-only --skip-git-repo-check \
  -o gen_result.md \
  -c 'model_reasoning_effort="high"' \
  "You DO have image generation capability available to you — please don't reflexively
say you can't, because you can. Generate ONE image as a PNG.

Image to generate: <FULL DESCRIPTION — subject, scene, style, composition, lighting>.

Generate it now. If your first instinct is that you cannot, try anyway — invoke whatever
image tool you have. Report the exact PNG path and the codex session id." \
  < /dev/null
```

Then **harvest** (see [§4](#4-harvest-the-output-the-load-bearing-step)). Typical run:
exit 0, ~60–90 s, well inside Codex's 5-minute print window. Output is 8-bit RGB PNG at a
**subject-driven size you don't control and shouldn't predict** — observed 1024²-ish
square, 1536×1024, and 1672×941. Asking for "16:9" gets you the *proportion*, not a
standard resolution. If you need exact pixels, resize after harvesting.

> `< /dev/null` closes stdin — without it `codex exec` hangs forever (the `codex-cli`
> stdin trap). PowerShell has no `<`; use `'' | codex exec ...` instead.

## 3. Edit an existing image (img2img)

Attach the target with **`-i`** and lock invariants hard. The single highest-leverage
move is an **exhaustive "change ONLY X; keep everything else identical"** list.

```bash
codex exec --ignore-user-config -s read-only --skip-git-repo-check \
  -i ./target.png \
  -o edit_result.md \
  -c 'model_reasoning_effort="high"' \
  "You DO have image editing capability via the built-in image tool. The attached image
(Image 1) is the EDIT TARGET.

Use case: <edit slug — see below>.
Primary request: <the single change>.
Invariants — keep EVERYTHING else identical: <list them: subject identity, pose,
background, lighting, framing, colors, text…>. Change ONLY <X>. No text, no watermark.

Edit the attached image now and produce a PNG. Report the exact PNG path and the codex
session id." \
  < /dev/null
```

**Edit-intent slugs** (name one; they steer the model): `precise-object-edit` (add/
remove/replace an element), `identity-preserve` (lock a face/body/pose — try-on,
add glasses), `lighting-weather` (time-of-day/season only), `background-extraction`
(cutout), `style-transfer`, `compositing` (merge multiple inputs), `sketch-to-render`,
`text-localization`.

**Observed fidelity (verified):** a precise recolor held every invariant perfectly
(plate, shadow, highlight, framing untouched); an `identity-preserve` add-glasses edit
kept facial identity strongly (freckles, eyes, expression, hair, wardrobe, lighting),
with only minor micro-drift in fine hair detail. Output resolution matched the input.
`gpt-image-2` always uses high input fidelity — there's no dial to set on this path.

**It holds on stylized/CG subjects too, not just photographs** — and it can tell
near-identical materials apart when you name them. A `precise-object-edit` recolouring
*only* the translucent canopy of a CG toy-brick cockpit left the other translucent parts
in the same frame (red and green buttons, explicitly listed as do-not-touch) completely
untouched, along with a detailed background object's geometry, the starfield, framing and
exposure. **Naming the near-misses in the invariant list is what buys that** — "change the
translucent canopy" alone invites collateral damage to every other translucent thing on
screen. This makes it a practical way to produce A/B look comparisons where exactly one
variable moves.

**Iterate with single-change follow-ups**, and **repeat the invariants each round** —
edits drift cumulatively. One change, harvest, eyeball it, next change.

## 4. Harvest the output (the load-bearing step)

Codex saves the image to a Codex-owned path, **not** your workspace and **not** any path
you asked for:

```
$CODEX_HOME/generated_images/<session-id>/exec-<uuid>.png
```

`<session-id>` is the **`session id:` line in the stderr banner** — that's your key.

```bash
# after the run, with the session id read from the banner:
SID=<session-id>
src=$(ls -t "${CODEX_HOME:-$HOME/.codex}/generated_images/$SID"/*.png | head -1)
cp "$src" ./out.png
# then view it back to confirm the result actually landed:
```
Then **Read `out.png`** to verify the change — the agent's prose is not proof.

**Take the id from the banner, never from the model's prose.** This is the whole rule, and
it survives the model *appearing* to tell you the answer:

> **[verified, 0.146.0] Codex reported a confidently wrong session id.** The final message
> gave `0dee8ef3-0330-4bdf-babd-7ec061d4a626` — which was the **calling agent's** session
> id, scraped out of the working-directory path, for a `generated_images/` folder that does
> not exist. The real id was `019fccfd-…`, in the stderr banner, and the reported *PNG
> path* was correct. A wrong id fails loudly (empty `ls`), so the cost is only confusion —
> but do not "fix" it by trusting the prose over the banner. That run used **default**
> reasoning effort; the two `high`-effort runs reported correctly. n=3, so treat that as a
> hypothesis, not a rule — the banner is free either way.

**Why you must harvest, not delegate:**
- **[Windows, verified] Codex can't place the file for you.** Every attempt it made to
  `Copy-Item` the PNG into the workspace was `rejected: blocked by policy`, even under
  `-s workspace-write` — and the banner read `sandbox: read-only` regardless. Suspected
  Windows execpolicy; POSIX hosts may differ, but the session-id harvest works either way.
- **`-o` is unreliable for the path.** It captures the final message, which under
  read-only was sometimes just a preamble ("I'll generate one image…") with no path. On
  0.146.0 all three runs *did* report an exact, correct PNG path — so it has improved, but
  "usually right" is not a contract you can script against. Use `-o` for the model's prose;
  get the file via the session-id harvest.

Grab the id mechanically rather than eyeballing it — redirect stderr and grep it:

```bash
codex exec ... 2> run_stderr.txt < /dev/null
SID=$(grep -m1 '^session id:' run_stderr.txt | awk '{print $3}')
```

## Auth — the API-key myth

Some docs imply you need `OPENAI_API_KEY`. You don't, for this. The official image skill
has two modes:

- **Built-in `image_gen` (what everything above uses): NO key.** Runs inside the ChatGPT
  subscription's usage limits.
- **CLI fallback (`scripts/image_gen.py`): needs a key.** Only for true *native*
  transparency (`gpt-image-1.5 --background transparent`), masks, or explicit
  `quality`/output-path flags — and only when the user explicitly asks for it. **This is
  the path the "you need an API key" docs describe.** Don't wire a key for normal work.

> **Transparency note:** built-in `gpt-image-2` has no native transparent background. For
> simple subjects the official skill generates on a flat chroma-key background and removes
> it locally (its bundled `remove_chroma_key.py`). True native transparency is the
> key-required CLI fallback above — ask the user before going there.

## Prompt quality — let the runtime skill do the heavy lifting

Codex has an **installed image skill** (`$CODEX_HOME/skills/.system/imagegen/SKILL.md`,
mirrored in the public `openai/codex` repo) that the model **reads on every image run** —
it injects the full gpt-image-2 prompt taxonomy, size table, and best-practices for you.
So **don't paste all that here**; just compose a clear request and let Codex's own skill
refine it. What actually helps from your side:

- **Structure:** scene/backdrop → subject → details → constraints.
- **Be specific** if you're specific; if generic, add only detail that materially helps.
- **Quote exact text verbatim** and specify placement (image models mangle text).
- **For edits, list invariants explicitly and repeat them every iteration** (§3).
- **Multiple inputs:** reference them by index ("Image 1 is the target, Image 2 the
  style reference").

## Sandbox, model, and the generic CLI rules

- **`-s read-only`** is the default for pure make/edit. Use `-s workspace-write` only if
  the *same* run also edits repo files (and even then, harvest the PNG yourself).
- **Model/effort:** the default `gpt-5.6-sol` worked well; `-c 'model_reasoning_effort=
  "high"'` for careful edits. Model tiers and the effort dial are covered in `codex-cli`.
- Everything generic — the stdin trap, `-o` vs `--json`, `--ignore-user-config`, install,
  auth, Windows PATH — lives in the **`codex-cli`** skill. This skill assumes it.

## Troubleshooting

| Symptom | Cause / fix |
|---|---|
| "I can't generate images" refusal | Add the explicit "you DO have image capability… try anyway" opener. §TL;DR. |
| Run hangs, no output | stdin trap — add `< /dev/null` (bash) or `'' \|` (PowerShell). See `codex-cli`. |
| Image made, but not in my folder | Expected — it's at `$CODEX_HOME/generated_images/<session-id>/`. Harvest by session id. §4. |
| `-o` file has prose but no path | Normal under read-only. Get the file via session-id harvest, not `-o`. §4. |
| `ls` on the session dir finds nothing | You used the id from the model's prose. It reports a wrong one occasionally. Use the stderr banner's `session id:`. §4. |
| `codex: command not found`, but `~/.codex` exists with valid auth | The desktop app made that dir; the CLI was never installed. `npm i -g @openai/codex` — it inherits the login. §1. |
| Codex says "blocked by policy" copying the PNG | Windows sandbox can't write your workspace; copy the file yourself from the harness. §4. |
| Asked for transparent PNG, got opaque | Built-in gpt-image-2 has no native alpha; chroma-key workflow or key-required CLI fallback. See Auth. |
| Edit changed too much | Invariants too vague — enumerate everything to keep; one change per iteration. §3. |
| Wants an API key | Only the CLI fallback needs one; the built-in path doesn't. Don't set a key for normal work. |

---

*Provenance: distilled from a verified dogfood (four `codex exec` image runs — generate
+ precise-object edit + portrait generate + identity-preserve edit) on `codex-cli 0.144.6`,
`gpt-5.6-sol`, ChatGPT-login auth, Windows/Git Bash, 2026-07-21. Re-verified 2026-08-04 on
`codex-cli 0.146.0` (three more runs — generate, precise-object edit on a stylized CG
subject, and a post-install smoke probe); every flag held, and that pass added the install
detection trap (§1), the non-standard output sizes (§2), the stylized-subject fidelity note
(§3), and the wrong-session-id finding (§4). Re-run `codex exec --help` to confirm flags on
any other version. Full field notes: the image-gen field-notes doc.*
