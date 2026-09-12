# Image generation via Codex — reference

Dated facts, field observations and the stories behind the rules in `SKILL.md`.

## Which model, and where that answer lives

The built-in `image_gen` tool is backed by whatever OpenAI currently routes it
to, and that is not named anywhere you can query from the CLI. The authority
is Codex's own runtime image skill at
`$CODEX_HOME/skills/.system/imagegen/SKILL.md`, which the CLI refreshes at
startup (observed: its mtime moved to the minute of the first `codex exec`
of the day) and which the model reads on every image run. Read that file for
the current model names, quality values, size guidance and the transparency
workflow; do not copy them into this skill.

Snapshot on 2026-09-12, for the record only:

- Built-in `image_gen`: the default path, no API key, runs on the ChatGPT
  subscription. Backing model unnamed in the runtime skill.
- CLI fallback (`scripts/image_gen.py`, needs `OPENAI_API_KEY`): defaults to
  `gpt-image-2`; `gpt-image-1.5` only for native transparent output, and the
  runtime skill tells the model to treat switching to it as a downgrade that
  needs the user's say-so.
- On 2026-07-21 this skill said the built-in tool was `gpt-image-2` and the
  fallback was `gpt-image-1.5`. The fallback default has since moved and the
  built-in mapping is no longer stated. That is why the body names neither.

The runtime skill's save-path policy (same snapshot): built-in output lands
under `$CODEX_HOME/generated_images/<session-id>/`, and the model is told to
move or copy the selected image into the workspace before finishing when the
image is for the project. Whether that copy succeeds on Windows is the
harvest question in `SKILL.md`.

## Output files

`$CODEX_HOME/generated_images/<session-id>/exec-<uuid>.png`, 8-bit RGB or
RGBA. Sizes are subject-driven and not yours to control: observed 1024²-ish,
1254², 1536×1024, 1672×941.

**Alpha, 2026-09-12 (n=2):** two runs asking for "plain white background"
came back RGBA with alpha extrema (0, 255), i.e. real transparency, from the
built-in tool with no chroma-key step. One of the two runs then regenerated an
RGB version on its own. On 2026-07-21 this skill stated the built-in tool had
no native transparent output; that was true of the model it was routed to
then, or of the prompt, and is not true now. Do not promise alpha either way;
inspect the file. Asking for 16:9 buys the proportion, not a standard resolution;
resize after harvesting. Edits come back at the input's resolution. An older
naming (`ig_<hex>.png`) exists in a few 2026-05 session folders.

## Fidelity observations

- A precise recolour held every invariant (plate, shadow, highlight, framing).
- An identity-preserve add-glasses edit kept facial identity strongly
  (freckles, eyes, expression, hair, wardrobe, lighting) with minor micro-drift
  in fine hair detail.
- On a stylised CG subject, recolouring only the translucent canopy of a
  toy-brick cockpit left the other translucent parts in frame (red and green
  buttons, listed as do-not-touch) untouched, along with a detailed background
  object, the starfield, framing and exposure. Naming the near-misses in the
  invariant list is what bought that. Practical for A/B look comparisons where
  exactly one variable moves.
- Edits drift cumulatively across rounds. One change per round, repeat the
  invariants every round.

## The wrong session id (0.146.0, n=3)

One run's final message reported `0dee8ef3-…` as the session id. That was the
*calling agent's* session id, scraped from the working-directory path, for a
`generated_images/` folder that did not exist. The real id, `019fccfd-…`, was
in the stderr banner, and the reported PNG path was correct. A wrong id fails
loudly (empty `ls`), so the cost is confusion, not a bad file. That run used
default reasoning effort; the two high-effort runs reported correctly. Three
runs is a hypothesis, not a rule; the banner is free either way.

## Windows and placing the file (0.144.6 and 0.146.0)

Every attempt Codex made to `Copy-Item` the PNG into the workspace was
`rejected: blocked by policy`, including under `-s workspace-write`, and the
banner read `sandbox: read-only` regardless. Suspected Windows execpolicy;
POSIX hosts may differ. Under `read-only` the `-o` file was sometimes only a
preamble with no path; on 0.146.0 all three runs reported an exact, correct
PNG path, so it improved, but "usually right" is not a contract to script
against.

## Edit-intent slugs

`precise-object-edit`, `identity-preserve`, `lighting-weather`,
`background-extraction`, `style-transfer`, `compositing`, `sketch-to-render`,
`text-localization`. Naming one in the prompt steers the model.

## Provenance

Four `codex exec` image runs on 0.144.6 (generate, precise-object edit,
portrait generate, identity-preserve edit), ChatGPT-login auth, Windows /
Git Bash, 2026-07-21. Three more on 0.146.0 on 2026-08-04 (generate,
precise-object edit on a stylised CG subject, post-install smoke probe).
Re-read on 2026-09-12 against the runtime skill refreshed by 0.144.6 that day;
the model-name section above is from that read.
