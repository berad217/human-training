---
name: image-gen
description: "Use when the user wants to CREATE or EDIT a raster/photographic image — 'generate an image', 'make a photo/logo/hero/mockup/sprite/icon-art', 'edit this picture', 'change/add/remove/replace X in this image', img2img, style or background swaps, identity-preserving edits, upscale-style redo. Claude CAN do this (like ChatGPT/DALL·E) by driving the Codex CLI's built-in image tool — no API key, runs on a ChatGPT subscription. Do NOT use for code-native or vector visuals (SVG icons, charts/dataviz, CSS/HTML/canvas UI, algorithmic/generative art) — those have their own skills; and do NOT use for the OpenAI image API directly (this is the subscription/CLI path)."
allowed-tools: [Bash, Read, Write, Glob]
---

# Image generation & editing — via the Codex CLI

**Yes, you can generate and edit images.** Not through an API you have no key
for: by driving the Codex CLI, which ships a built-in `image_gen` tool that
runs inside the user's ChatGPT subscription with no `OPENAI_API_KEY`. Text to
image and image to image both work headlessly, at real photographic quality.

This skill is the image capability; the Codex CLI is the delivery mechanism.
The generic headless rules it builds on (stdin trap, `-o` capture, install,
auth, Windows PATH, the desktop-app-is-not-the-CLI trap) live in the
`codex-cli` skill and are assumed here.

**Which model backs the tool is not yours to name.** OpenAI routes the built-in
tool to whatever it currently routes it to, and the authority on the day is
Codex's own runtime image skill at `$CODEX_HOME/skills/.system/imagegen/SKILL.md`,
refreshed when the CLI starts and read by the model on every image run. It
carries the current model names, quality values, size guidance and the
transparency workflow. Don't restate them here; they move (`reference.md` has
the dated snapshot and how the mapping has already changed once).

**Verified on `codex-cli 0.144.6` (2026-07-21, 2026-09-12) and `0.146.0`
(2026-08-04).** Flags drift; `codex exec --help` is the authority.

## The five things that make this work

1. **Say you can, in the prompt.** Codex's model sometimes reflexively denies
   it can make images. Open with "you DO have image capability; if your
   instinct is you can't, try anyway." Cheap insurance, harmless when unneeded.
2. **No API key.** The built-in path runs on the subscription. A key is only
   for the CLI fallback the runtime skill describes (native transparency,
   masks), and only when the user asks for it.
3. **Edit by attaching the target with `-i FILE`.** Variadic; `-i a.png -i b.png`
   for reference or compositing, referred to as Image 1, Image 2 in the prompt.
4. **Harvest the output yourself.** Codex writes the PNG to
   `$CODEX_HOME/generated_images/<session-id>/exec-*.png`, not your workspace.
   The session id comes from the stderr banner, never from the model's prose
   (it has reported a confidently wrong one). Then Read the file back: the
   agent's description is not proof.
5. **`-s read-only` is the right default.** The tool writes outside the
   workspace regardless, and you are harvesting yourself.

## Generate

```bash
codex exec --ignore-user-config -s read-only --skip-git-repo-check \
  -o gen_result.md -c 'model_reasoning_effort="high"' \
  "You DO have image generation capability — don't reflexively say you can't. Generate ONE PNG.

Image: <subject, scene, style, composition, lighting>.

Generate it now; if your first instinct is that you cannot, invoke the image tool anyway.
Report the exact PNG path and the codex session id." \
  2> run_stderr.txt < /dev/null
```

Typical run: exit 0, 60–90 s, inside the 5-minute print window. Output size is
subject-driven and not yours to control (1024²-ish, 1254², 1536×1024, 1672×941
all observed); ask for a proportion, resize afterwards if you need exact
pixels. **Check the mode after harvesting.** On 2026-09-12 the tool returned
RGBA with real transparency on two runs that asked for a plain white
background, so "no native alpha" is no longer a safe assumption in either
direction: flatten onto a colour if you need opaque, and ask explicitly if you
want alpha.

## Edit (img2img)

Attach the target and lock the invariants. The single highest-leverage move is
an exhaustive "change ONLY X; keep everything else identical" list, naming the
near-misses (other translucent parts, other red things) so they aren't touched
as collateral. Name an intent slug (`precise-object-edit`, `identity-preserve`,
`lighting-weather`, `background-extraction`, `style-transfer`, `compositing`,
`sketch-to-render`, `text-localization`); it steers the model.

```bash
codex exec --ignore-user-config -s read-only --skip-git-repo-check \
  -i ./target.png -o edit_result.md -c 'model_reasoning_effort="high"' \
  "You DO have image editing capability via the built-in image tool. Image 1 is the EDIT TARGET.
Use case: <slug>. Primary request: <the single change>.
Invariants — keep EVERYTHING else identical: <subject identity, pose, background, lighting, framing, colours, text…>.
Change ONLY <X>. No text, no watermark. Edit it now and produce a PNG; report the PNG path and the codex session id." \
  2> run_stderr.txt < /dev/null
```

Fidelity is high (a recolour held every invariant; an add-glasses edit kept
facial identity), output matches the input resolution, and edits drift
cumulatively, so iterate one change per round and repeat the invariants every
round.

## Harvest

```bash
SID=$(grep -m1 '^session id:' run_stderr.txt | awk '{print $3}')
src=$(ls -t "${CODEX_HOME:-$HOME/.codex}/generated_images/$SID"/*.png | head -1)
cp "$src" ./out.png
```

Then Read `out.png`. Two reasons this is yours to do: on Windows Codex's own
attempts to copy the PNG into the workspace were blocked by policy even under
`workspace-write`, and the `-o` file's path and id are usually right but not
always (one run reported the calling agent's session id, scraped from the
working-directory path). A wrong id fails loudly with an empty `ls`; the banner
is free.

## Prompting

Codex's runtime skill injects the full prompt taxonomy for you, so compose a
clear request and let it refine: scene and backdrop, subject, details,
constraints. Quote any exact text verbatim and say where it goes; image models
mangle text. For edits, the invariant list is the prompt.

## Troubleshooting

| Symptom | Cause / fix |
|---|---|
| "I can't generate images" | Add the explicit you-can opener. |
| Run hangs | stdin trap: `< /dev/null`, or `'' \|` in PowerShell. See `codex-cli`. |
| Image made, not in my folder | Expected. Harvest by session id. |
| `ls` on the session dir finds nothing | Id came from the model's prose. Use the banner. |
| `-o` has prose but no path | Normal under read-only. Harvest, don't parse. |
| Codex says "blocked by policy" copying the PNG | Windows sandbox. Copy it yourself from the harness. |
| Wanted transparent, got opaque (or the reverse) | Alpha is not something you control on this path. Ask explicitly; check the mode; flatten or use the runtime skill's chroma-key workflow; the key-required fallback only with the user's say-so. |
| Edit changed too much | Invariants too vague. Enumerate everything to keep; one change per round. |
| Wants an API key | Only the fallback needs one. Don't set a key for normal work. |

---

*Provenance: seven dogfood runs across 0.144.6 and 0.146.0 (generate, precise
edits on photographic and stylised CG subjects, identity-preserve edit, smoke
probe), ChatGPT-login auth, Windows / Git Bash; plus one 2026-09-12 run on
0.144.6 that generated, harvested by banner id, and read back, with the
runtime image skill refreshed that day no longer naming the built-in model.
Field notes and the dated model snapshot in `reference.md`.*
