# Ollama Playbook

> Rules of engagement with Ollama for caption_lab. Written after a session where we burned ~30 minutes of GPU time rediscovering Ollama vision-pipeline footguns the hard way. Read this before touching any captioner / judge / mutation code that hits Ollama, and before running any bench/tune/evolve command. Everything here is **verified against qwen3-vl:4b and qwen3-vl:8b on a local Ollama daemon, May 2026**. Other vision models may behave differently; assume nothing about ministral or other text-only models from this doc.

---

## TL;DR — the five rules

1. **Never set `format: "json"` with `images: [...]`**. Ollama silently returns an empty response. Tokens are generated; the response field is empty.
2. **Never set `num_predict` to a positive integer with `images: [...]`**. Same failure mode. `num_predict: -1` (unlimited) is fine; absent is fine.
3. **Always set `temperature: 0.0` for reproducible work.** Bench/tune/evolve depend on stable scores across runs.
4. **Always set `repeat_penalty: 1.1` on small vision models.** Mitigates the repetition-loop tendency without distorting prose.
5. **Don't run a full 27-image bench to verify a fix. Use `--limit 5` first.** A bad config can peg the GPU for 15+ minutes; cap your loss with `--limit` until you trust the change.

---

## The vision-pipeline bugs (verified reproducible)

These are real Ollama bugs, not caption_lab bugs. They affect any HTTP client hitting `/api/generate` with `images: [...]`.

### Bug 1: `format=json` + images → empty response

```python
# BROKEN. Returns 200, eval_count=57, response="".
{
    "model": "qwen3-vl:8b",
    "prompt": "...",
    "images": [<b64>],
    "format": "json",     # <-- this kills it
}
```

**Verified May 2026 on qwen3-vl:8b.** The model generates tokens (we see `eval_count > 0`) but the JSON-grammar filter discards them. Reproduce with the diagnostic script in `tests/` or just curl the daemon.

**Workaround:** Don't set `format`. The model emits valid JSON anyway because the prompt asks for it; caption_lab's parser strips markdown fences, preamble, and trailing prose, then extracts the first balanced `{...}`. See `caption_lab/judge/ollama.py::parse_judge_response`.

### Bug 2: `num_predict: <positive int>` + images → empty response

```python
# BROKEN. eval_count exactly hits the cap, response="".
{
    "model": "qwen3-vl:4b",
    "prompt": "...",
    "images": [<b64>],
    "options": {"num_predict": 400},   # <-- any positive int kills it
}
```

**Verified matrix** (qwen3-vl:4b + BFL image + lora_style prompt):

| Options                              | eval_count | response chars |
|--------------------------------------|------------|----------------|
| (none)                               | 4730       | 698 (works)    |
| `{temperature: 0.0}`                 | 2384       | 839 (works)    |
| `{repeat_penalty: 1.1}`              | 3119       | 698 (works)    |
| `{num_predict: 400}`                 | **400**    | **0 (BROKEN)** |
| `{num_predict: 800}`                 | **800**    | **0 (BROKEN)** |
| `{num_predict: -1}` (unlimited)      | 1066       | 585 (works)    |

**Workaround:** Don't bound output via `num_predict` on vision calls. Bound at the application layer via `Strategy.apply_post_process(max_chars=...)` after the response comes back. Or, if you need to abort a runaway, switch to the streaming endpoint and close the connection client-side after N tokens (not yet implemented; Sprint 9 candidate).

### Bug 3: high-detail images can spiral past context limit

This is a model-behavior bug, not a daemon bug, but it interacts with the above.

Some images deterministically cause qwen3-vl (both 4b and 8b) to enter a runaway descriptive loop, generating tokens until they hit the 32k context limit. Observed on `GFX_IMP_003.png` in the BFL reference set — a stylized scorpion illustration with high articulated detail (segmented legs, glowing red accents on a black background).

Reproducing characteristics so far:
- High-detail line art / illustration style
- Many discrete visual elements that invite enumeration
- High-contrast graphical content (not photographic)

**Single-image timing for the spiral case:** >300 seconds wall-clock, regardless of `temperature` or `repeat_penalty`. Both 4b and 8b affected. Converting RGBA → RGB does not help. We cannot cap via `num_predict` because of Bug 2.

**Workaround for now:** Accept the timeout cost. With the current captioner config (`timeout=120, max_attempts=3`), a stuck image costs ~6 minutes (3 retries × 120s) and shows up as a `failure_count` row in `bench.html`. Other images in the same run are unaffected.

**Real fix:** streaming with client-side abort after N tokens. Tracked as Sprint 9 candidate.

---

## Safe options reference

This is what caption_lab currently sets and **why each option is safe**:

```python
# OllamaCaptioner (src/caption_lab/captioner/ollama.py)
"options": {
    "temperature": 0.0,      # Reproducible captions across bench runs
    "repeat_penalty": 1.1,   # Mild; prevents loops without distorting prose
    # DO NOT add num_predict here. See Bug 2.
}

# OllamaJudge (src/caption_lab/judge/ollama.py)
"options": {
    "temperature": 0.0,      # Consistent scoring across bench runs
    "repeat_penalty": 1.1,   # Same as captioner
    # DO NOT add num_predict here. See Bug 2.
}
# Also: judge payload deliberately omits "format": "json". See Bug 1.
```

### Options we have NOT tested but are probably safe

- `seed: <int>` — deterministic across runs. Untested with images but no reason to expect a problem.
- `top_p`, `top_k`, `min_p` — sampling controls. Largely moot when `temperature=0.0`.
- `stop: [...]` — stop sequences. Untested; may interact with vision pipeline. Probe before relying on it.
- `keep_alive: <duration>` — controls how long the model stays loaded. Not a generation knob; safe.

### Options we have NOT tested and might be risky

- `format: <json_schema>` — newer Ollama feature for grammar-constrained JSON. Bug 1 was the legacy `format: "json"` string; the schema variant may behave differently. **Test in isolation before using.**
- `mirostat`, `mirostat_eta`, `mirostat_tau` — alternative sampling. Unknown interaction with vision.

---

## Performance and budget

Typical inference times for current models (RTX 3090, no concurrent load):

| Operation | Model | Image size | Mean | Range |
|---|---|---|---|---|
| Caption | qwen3-vl:4b | 2752×1536 (BFL) | ~11s | 6-25s |
| Caption | qwen3-vl:8b | 2752×1536 (BFL) | ~8s | 5-15s (after warm) |
| Judge | qwen3-vl:8b | 2752×1536 (BFL) | ~8s | 5-17s |
| Stuck image (spiral) | either | high-detail | timeout | >180s, capped by HTTP timeout |

**Both qwen3-vl:4b (9.4 GB) and qwen3-vl:8b (12 GB) fit simultaneously in 24 GB VRAM.** No swap penalty between captioner and judge calls if both stay loaded — verify with `ollama ps`. Default `keep_alive` should hold them for 5 minutes after last use.

### Budget math for bench/tune/evolve

- `bench`: 27 BFL × (1 caption + 1 judge) = 54 inferences. Expect ~10 min total, plus ~6 min wasted on any spiral image. Real wall-clock: 10-20 min.
- `tune`: 27 BFL × N variants × 2 calls = 54N. With 2 shipped variants, that's 108 inferences ≈ 20-30 min.
- `evolve -g 3 -p 4`: 3 generations × 4 pool × 27 × 2 = 648 inferences. ≈ 90-120 min including spiral overhead.

**If you're running these to validate code changes, always start with `--limit 5` for bench. The full sets are for actual evaluation runs, not for "did my patch work."**

---

## Pre-flight checklist

Before any real-VLM run:

1. **Confirm daemon health.** `ollama ps` should respond quickly. If it hangs, restart the daemon (`ollama serve` in a separate terminal, or restart the Ollama service).
2. **Confirm target models are installed.** `caption-lab list-backends` lists everything. If a model is missing, `ollama pull <name>` first.
3. **Confirm nothing else is using the GPU heavily.** Caption_lab assumes exclusive 3090. If a LoRA training run is happening in another window, expect timeouts.
4. **For bench/tune/evolve specifically:** start with `--limit 5` if you're testing a change. Full 27-image runs are for evaluation, not validation.
5. **Watch the log output as it runs.** If the captioner takes >60s on a single non-detailed image, something is wrong — kill the run and investigate.

### Watching progress without buffering

This bit caused real confusion in our session. `bash | tail -N` buffers everything until the pipe closes:

```powershell
# BAD: blank output until completion. Looks like the process is frozen.
caption-lab bench --backend ... --judge ... 2>&1 | tail -20

# GOOD: live progress visible.
caption-lab bench --backend ... --judge ...
```

If you need to capture output to a file, use a tee:

```powershell
caption-lab bench --backend ... --judge ... 2>&1 | Tee-Object bench-run.log
```

---

## When something looks wrong — diagnostic recipe

Don't loop on the live bench command. Probe the daemon directly. Each of these is ~1 minute of GPU time at most.

### "The response is empty"

```python
# minimal probe: vary one option at a time.
import requests, base64
b64 = base64.b64encode(open("path/to/image.png", "rb").read()).decode()
for opts in [None, {}, {"temperature": 0.0}, {"num_predict": 400}]:
    body = {"model": "qwen3-vl:4b", "prompt": "Describe this image.",
            "images": [b64], "stream": False}
    if opts is not None:
        body["options"] = opts
    r = requests.post("http://localhost:11434/api/generate", json=body, timeout=120)
    d = r.json()
    print(f"opts={opts}  eval={d.get('eval_count')}  len={len(d.get('response',''))}")
```

If `eval_count > 0` but response is empty, you've hit a vision-pipeline bug like Bug 1 or 2.

### "Calls are slow"

Time a single call. If a single image takes >30s for the captioner, the model is probably spiraling. Look at the raw response — if it's repeating phrases or going beyond the prompt's target length, that's the spiral. Document the offending image.

### "Model isn't loading"

`ollama ps` shows what's currently loaded. If a model is "loading" in `ollama show <name>` but never appears in `ps`, the daemon may need a restart. Cold-start the 8b model: ~4s. Cold-start the 4b: ~0.2s.

### "I changed an option and now everything is broken"

Read this doc. Revert. If your option isn't in the safe list above, you owe a one-image probe before claiming it works.

---

## Model selection guide

For caption_lab roles:

| Role | Current default | Why |
|---|---|---|
| Captioner | `qwen3-vl:4b` | Fast, decent quality. Smaller model is fine for descriptive captioning. |
| Judge | `qwen3-vl:8b` | Slightly more reliable structured JSON output. Cost: 3× slower than 4b but worth it for score quality. |
| Mutation | text-only (`ministral-3:14b-instruct-2512-q8_0` recommended) | No image; just rewrites prompts. Any decent instruct model works. |

If you want to try a different captioner, run the diagnostic recipe above on 3-5 sample images first. Don't burn 30 min on a full bench.

Untested model families that may or may not have the same vision-pipeline bugs: `gemma3:*-it-qat`, `huihui_ai/qwen3-vl-abliterated:*`. Probe before trusting.

---

## Out of scope for this playbook

- **Gemini.** See the `gemini-api` skill in `human-training`. Different API, different footguns (Gemini 3.x: don't set temperature/top_p/top_k; use `thinking_level` enum). `KNOWN_VISION_MODELS` in `captioner/gemini.py` lists current IDs.
- **Other Ollama endpoints.** Only `/api/generate` is covered here. `/api/chat` may behave differently for vision payloads.
- **Concurrent requests.** caption_lab is single-stream by design (per project rule "quality > speed; no async until proven bottleneck"). If you change this, re-verify everything.

---

## Maintenance

When a new vision-pipeline footgun is found:

1. **Reproduce in isolation** with a minimal HTTP probe (not via bench). Log the eval_count vs response length.
2. **Add to the bug section above** with the verification table.
3. **Add to the TL;DR if it's a hard "never do X"**.
4. **Update the safe-options reference** if a new safe lever is found.
5. **DEVLOG entry** referencing this doc, not duplicating it.

The Sprint 8 hotfix entries in DEVLOG are the canonical place for *when* and *why*; this doc is the canonical place for *what to do*.
