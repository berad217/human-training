---
name: ollama
description: Use when writing, reviewing, or debugging code that hits a local Ollama daemon — imports of `ollama` (Python) or `'ollama'` (JS), HTTP requests to `localhost:11434` / `/api/generate` / `/api/chat` / `/api/embed`, OpenAI-SDK code with `base_url="http://localhost:11434/v1/"`, or model strings like `qwen3:*`, `qwen3-vl:*`, `llama3*:*`, `gemma3:*`, `gpt-oss:*`, `deepseek-*`, `embeddinggemma`, `all-minilm`. Use proactively before writing the first Ollama call so the model picked is one the user actually has installed and so sampling/format defaults reflect Ollama's recommendations rather than carryover from other APIs. Do NOT use for hosted-API code (Claude, Gemini, OpenAI cloud) or non-LLM tooling.
allowed-tools: [Read, Write, Edit, Grep, Glob, Bash, WebFetch]
---

# Ollama

Defensive playbook for writing code against a local Ollama daemon. Ollama's API is small and friendly on the surface but has real footguns around model selection (hallucinated model names), structured outputs (two `format` modes that behave very differently), vision payloads (model-family-specific bugs), thinking models (`gpt-oss` accepts an enum, others accept a bool), and sampling defaults that you should usually leave alone. This skill keeps those straight.

The skill teaches **discovery-first** model selection (never assume a model is installed; ask `/api/tags` first), Ollama's recommended **sampling defaults** (and which knobs to leave at default), the **two structured-output modes** and when each is the right call, and a small catalog of **verified vision-pipeline bugs** taken from real production usage.

## TL;DR — eight rules before writing any Ollama code

1. **Discover models before naming them.** Hit `GET http://localhost:11434/api/tags` (or `ollama list`) FIRST. Never hardcode a model string that hasn't been verified against the user's installed list. If the task needs vision/embed/tools, intersect the requirement with what's installed and *propose*; don't guess. Common hallucination: writing `llama3.3` or `llama3` when only `llama3.2:latest` is pulled.

2. **Set `temperature: 0` for any deterministic / evaluable task** (structured output, judging, reproducible benchmarks, anything you'll grade). Otherwise leave sampling defaults alone. Ollama's defaults are `temperature: 0.8`, `top_p: 0.9`, `top_k: 40`, `min_p: 0.0`, `repeat_penalty: 1.1` — these are the maintainers' calibration, not arbitrary numbers. Don't tune `top_p` / `top_k` unless you have a measured reason; defaults are fine.

3. **Structured output: prefer JSON Schema over the legacy `"json"` string.** Two modes:
   - `format: <JSON-schema-object>` — modern, deterministic. Use `Country.model_json_schema()` (Pydantic) or `zodToJsonSchema(...)` (Zod). **This is the upstream-recommended path** and works with vision models (gemma3 + images example in docs).
   - `format: "json"` — legacy. Requires you to also instruct the model to use JSON in the prompt; otherwise it produces whitespace. Avoid on vision models (see Footgun §1).
   - Always also include the schema in the prompt for grounding — the format field alone isn't always enough.

4. **Thinking models: `think: true/false`, except gpt-oss which expects `"low"|"medium"|"high"`.** Supported families: qwen3, deepseek-v3.1, deepseek-r1, gpt-oss. Passing `true` to gpt-oss is silently ignored. Reasoning trace lands in `message.thinking` (chat) / `thinking` (generate); the answer is still in `message.content` / `response`. Thinking is on by default in CLI+API for supported models.

5. **Use `/api/embed` not `/api/embeddings`.** The plural is deprecated. `/api/embed` accepts `input` as a string or array (batches in one call), returns `embeddings: [[...]]` (always nested even for single input). **Vectors are L2-normalized** — cosine similarity equals dot product. Use the same model for indexing and querying.

6. **Vision: `images: [<base64 | path | bytes>]` on the message.** Same `/api/chat` or `/api/generate` endpoint; no special vision endpoint. SDKs accept paths/URLs/bytes; raw REST requires base64. **Model-specific vision bugs exist** — see Footgun §1 and §2 below before relying on `format` or `num_predict` with images.

7. **`num_predict` is per-task, not global.** Default is `-1` (unlimited). Set a positive integer to cap output tokens — useful for predictable cost, harmful on some vision-model + image combinations (see Footgun §2). Don't set it as a "safety net" by default; only when you actually want a hard token cap.

8. **`keep_alive` controls model lifecycle, not request behavior.** Default is 5 min after last use. Pass `keep_alive: -1` to pin a model in memory (e.g., between bench iterations); `keep_alive: 0` to unload immediately. Useful for predictable cold-start timing; irrelevant to generation quality.

## Step 0: Discover what's installed (do this every time)

Never write a model string the user doesn't have. The discovery endpoints are cheap and definitive.

### From the CLI

```powershell
ollama list                                # what's installed
ollama ps                                  # what's loaded in memory now
ollama show <model-name>                   # capabilities, template, parameters
```

### From code (no SDK needed)

```python
import requests

tags = requests.get("http://localhost:11434/api/tags", timeout=5).json()
for m in tags["models"]:
    print(f"{m['name']:<40} {m['details']['parameter_size']:<6} {m['details']['family']}")
```

Output looks like:

```
qwen3-vl:8b                              8.3B   qwen3vl
qwen3-vl:4b                              4.1B   qwen3vl
llama3.2:latest                          3.2B   llama
embeddinggemma:latest                    0.3B   gemma
```

### Capability check before role assignment

`/api/show` returns `capabilities: ["completion", "vision", "tools", "embedding", "thinking"]`. Use it to pick the right model for the role:

```python
import requests

def model_has(name: str, cap: str) -> bool:
    r = requests.post("http://localhost:11434/api/show",
                      json={"model": name}, timeout=10)
    return cap in r.json().get("capabilities", [])

# pick a vision model from what's installed
tags = requests.get("http://localhost:11434/api/tags", timeout=5).json()
vision_models = [m["name"] for m in tags["models"]
                 if model_has(m["name"], "vision")]
print("Vision models available:", vision_models)
```

If the requested role has no installed match, **stop and tell the user**. Don't fall back to a model that doesn't exist (`llama3.3`, `gpt-4`, etc.). Suggest `ollama pull <name>` if the user wants to install something specific.

## Endpoint cheatsheet

```
POST /api/generate     single-prompt completion. Streaming default true.
                       Body: {model, prompt, [images], [format], [options], [think]}

POST /api/chat         multi-turn. Streaming default true.
                       Body: {model, messages: [...], [tools], [format], [options], [think]}

POST /api/embed        embeddings. Returns L2-normalized vectors.
                       Body: {model, input: <string | string[]>}

GET  /api/tags         list installed models
GET  /api/ps           list loaded models (with VRAM usage and expiry)
POST /api/show         model details + capabilities

POST /api/copy         {source, destination}
DELETE /api/delete     {model}
POST /api/pull         {model}                  # download from registry

POST /v1/chat/completions    OpenAI-compatible shim
POST /v1/responses           OpenAI Responses-API shim
                             api_key='ollama' (required but ignored)
                             base_url='http://localhost:11434/v1/'
```

**Streaming defaults differ by surface:** REST is streaming-on-by-default; SDKs are streaming-off-by-default. Pass `stream=True` to the SDK call if you want chunks. When streaming, accumulate partial `thinking`, `content`, and `tool_calls` chunks — you have to pass the full accumulated message back on the next turn or the model loses state.

**Durations in API responses are nanoseconds.** Tokens per second = `eval_count / eval_duration * 1e9`.

## Options reference — defaults and when to override

Source: [modelfile.mdx](https://github.com/ollama/ollama/blob/main/docs/modelfile.mdx#valid-parameters-and-values).

| Option           | Default | Override when                                                    |
|------------------|---------|------------------------------------------------------------------|
| `temperature`    | 0.8     | Set to `0` for structured/deterministic/eval work. Otherwise leave. |
| `top_p`          | 0.9     | Leave. Moot when `temperature: 0`.                               |
| `top_k`          | 40      | Leave. Moot when `temperature: 0`.                               |
| `min_p`          | 0.0     | Leave unless you've measured a benefit.                          |
| `seed`           | 0       | Set to a fixed int for reproducibility across runs.              |
| `repeat_penalty` | 1.1     | Bump to ~1.15 if you see repetition loops on small models. Don't go above 1.3 — distorts prose. |
| `repeat_last_n`  | 64      | Leave. `-1` = num_ctx; `0` = disabled.                           |
| `num_ctx`        | 2048 (model) / 4096 (server) | Bump if your prompt + expected output approaches the cap. Costs VRAM linearly. |
| `num_predict`    | -1 (unlimited) | Set when you need a hard token cap. **Skip on vision calls — see Footgun §2.** |
| `stop`           | model-specific | Add custom stop sequences. Untested with vision; probe first.   |

The server-wide context default (4096) can be raised globally via `OLLAMA_CONTEXT_LENGTH`. Per-request `num_ctx` overrides it. Note the multiplier in faq.mdx: required VRAM scales by `OLLAMA_NUM_PARALLEL × OLLAMA_CONTEXT_LENGTH`.

## Structured outputs — the two modes

This is the single highest-friction area in Ollama. Get it right.

### Mode A: `format: <JSON Schema object>` — preferred

Pass a real JSON Schema. The daemon constrains generation to match. Works for arbitrary shapes; works with vision models.

```python
from ollama import chat
from pydantic import BaseModel

class Country(BaseModel):
    name: str
    capital: str
    languages: list[str]

response = chat(
    model='qwen3:8b',
    messages=[{'role': 'user', 'content': 'Tell me about Canada.'}],
    format=Country.model_json_schema(),
    options={'temperature': 0},
)
country = Country.model_validate_json(response.message.content)
```

**Always also paste the schema (or its key fields) into the prompt.** The `format` field alone doesn't always ground the model strongly enough; mentioning the field names in the prompt closes the gap. Source: [structured-outputs.mdx](https://github.com/ollama/ollama/blob/main/docs/capabilities/structured-outputs.mdx).

JavaScript equivalent uses Zod:

```javascript
import ollama from 'ollama'
import { z } from 'zod'
import { zodToJsonSchema } from 'zod-to-json-schema'

const Country = z.object({ name: z.string(), capital: z.string(), languages: z.array(z.string()) })

const response = await ollama.chat({
    model: 'qwen3:8b',
    messages: [{ role: 'user', content: 'Tell me about Canada.' }],
    format: zodToJsonSchema(Country),
})
const country = Country.parse(JSON.parse(response.message.content))
```

### Mode B: `format: "json"` — legacy

The string form. Less precise (no schema), and **requires the prompt to ask for JSON** or the model emits whitespace ([api.md:79](https://github.com/ollama/ollama/blob/main/docs/api.md)).

```python
response = chat(
    model='qwen3:8b',
    messages=[{'role': 'user',
               'content': 'Return JSON with keys name and capital for Canada.'}],
    format='json',
)
```

**Use this only when you don't have a schema and just need *some* JSON.** Don't use it on vision models — see Footgun §1.

### Mode C: OpenAI-compatible shim

If you're already using the OpenAI SDK, the shim supports `response_format`:

```python
from openai import OpenAI
client = OpenAI(base_url='http://localhost:11434/v1/', api_key='ollama')

resp = client.chat.completions.create(
    model='qwen3:8b',
    messages=[{'role': 'user', 'content': '...'}],
    response_format={'type': 'json_schema', 'json_schema': {'name': 'Country', 'schema': <schema>}},
)
```

## Thinking models

Set `think` on the request. Most models: bool. **gpt-oss: enum** (`"low" | "medium" | "high"`). Passing the wrong type is silently ignored.

```python
from ollama import chat

# qwen3, deepseek-r1, deepseek-v3.1: bool
r = chat(model='qwen3:8b',
         messages=[{'role': 'user', 'content': 'What is 17 × 23?'}],
         think=True)
print('Reasoning:', r.message.thinking)
print('Answer:', r.message.content)

# gpt-oss: enum
r = chat(model='gpt-oss:20b',
         messages=[{'role': 'user', 'content': 'Draft a headline.'}],
         think='low')
```

The trace lives on `message.thinking` (chat) or `thinking` (generate). To use a thinking model without rendering the trace, just discard `.thinking` and use `.content`. CLI flag: `--hidethinking`.

When streaming, thinking chunks arrive before content chunks. Switch your UI from "thinking" → "answer" when the first `message.content` chunk appears (pattern in [thinking.mdx](https://github.com/ollama/ollama/blob/main/docs/capabilities/thinking.mdx)).

## Tool calling

OpenAI-shaped `tools` array on `/api/chat`. Python SDK auto-derives schema from the function signature + docstring — pass the function directly:

```python
from ollama import chat

def get_temperature(city: str) -> str:
    """Get the current temperature for a city.

    Args:
      city: The name of the city
    """
    return {"New York": "22°C", "London": "15°C"}.get(city, "Unknown")

messages = [{'role': 'user', 'content': 'What is the temperature in New York?'}]
response = chat(model='qwen3:8b', messages=messages,
                tools=[get_temperature], think=True)

messages.append(response.message)
if response.message.tool_calls:
    for call in response.message.tool_calls:
        result = get_temperature(**call.function.arguments)
        messages.append({'role': 'tool',
                         'tool_name': call.function.name,
                         'content': str(result)})
    final = chat(model='qwen3:8b', messages=messages, tools=[get_temperature])
    print(final.message.content)
```

For a multi-turn agent loop, wrap the above in a `while True:` and break when `response.message.tool_calls` is empty (pattern at [tool-calling.mdx:425](https://github.com/ollama/ollama/blob/main/docs/capabilities/tool-calling.mdx)).

**Streaming + tools:** accumulate `tool_calls` chunks across the stream into one list before executing. Pass the full assistant message (with accumulated `thinking`, `content`, `tool_calls`) back as the next message before the tool responses, or the model loses state.

## Vision

Same endpoints; pass `images` on the message:

```python
from ollama import chat

response = chat(
    model='gemma3',
    messages=[{
        'role': 'user',
        'content': 'What is in this image?',
        'images': ['/abs/path/to/image.jpg'],   # SDK accepts paths
    }],
)
```

Raw REST requires base64:

```python
import base64, requests
b64 = base64.b64encode(open('image.jpg', 'rb').read()).decode()
r = requests.post('http://localhost:11434/api/chat', json={
    'model': 'gemma3',
    'messages': [{'role': 'user', 'content': '...', 'images': [b64]}],
    'stream': False,
})
```

Structured output + vision works on `gemma3` (upstream example). Other vision models may have footguns — see below.

## Embeddings

```python
import ollama

# single
r = ollama.embed(model='embeddinggemma', input='The quick brown fox.')
vec = r['embeddings'][0]   # ALWAYS nested, even for single input

# batch
r = ollama.embed(model='embeddinggemma', input=['first', 'second', 'third'])
vecs = r['embeddings']     # list of 3 vectors
```

Vectors are L2-normalized → cosine similarity is just a dot product:

```python
import numpy as np
a, b = np.array(vec_a), np.array(vec_b)
similarity = float(a @ b)   # in [-1, 1]
```

Use the **same model for indexing and querying**. Switching models mid-pipeline silently produces garbage similarity scores. Recommended models: `embeddinggemma`, `qwen3-embedding`, `all-minilm`.

## OpenAI-compatible shim

Point any OpenAI SDK at Ollama by changing two things — `base_url` and `api_key`:

```python
from openai import OpenAI

client = OpenAI(
    base_url='http://localhost:11434/v1/',
    api_key='ollama',     # required by SDK; ignored by daemon
)

r = client.chat.completions.create(
    model='qwen3:8b',
    messages=[{'role': 'user', 'content': 'Hello'}],
)
```

Useful when you want to keep existing OpenAI-shaped code and swap the backend. Also supports `client.responses.create(...)` and `response_format` for structured output. Source: [openai-compatibility.mdx](https://github.com/ollama/ollama/blob/main/docs/api/openai-compatibility.mdx). Anthropic-shaped shim exists too at `/v1/messages` (see [anthropic-compatibility.mdx](https://github.com/ollama/ollama/blob/main/docs/api/anthropic-compatibility.mdx)).

## Model lifecycle and concurrency

- **Default `keep_alive` is 5 min.** Override per-request: duration string (`"10m"`, `"24h"`), seconds (`3600`), `-1` (pin), `0` (unload immediately). Global default via `OLLAMA_KEEP_ALIVE`.
- **Preload a model:** `POST /api/generate {"model": "..."}` with no prompt loads it without generating.
- **`OLLAMA_NUM_PARALLEL`** (default 1) — parallel requests per model. **Memory cost multiplies: required VRAM scales by `OLLAMA_NUM_PARALLEL × OLLAMA_CONTEXT_LENGTH`.**
- **`OLLAMA_MAX_LOADED_MODELS`** (default 3 × num_GPUs).
- **`OLLAMA_MAX_QUEUE`** (default 512) — over this, requests get 503.
- **`OLLAMA_FLASH_ATTENTION=1`** can reduce VRAM-vs-context cost on supported models.

## Footgun catalog

These are real bugs verified in production, not theoretical. Lift them as case studies, not universal rules.

### §1 — `format: "json"` (legacy string) + `images: [...]` → empty response

**Verified May 2026 on qwen3-vl:4b and qwen3-vl:8b.** With the legacy string-form `format`, the daemon returns HTTP 200 with `eval_count > 0` (tokens *were* generated) but `response: ""`. The JSON-grammar filter discards everything.

**Workaround:** use Mode A (JSON Schema object) instead of Mode B (`"json"` string) on vision calls. The schema form was demonstrated working with `gemma3` + images in the upstream docs. If you don't need a schema, omit `format` entirely and parse JSON out of the response text with a tolerant parser (strip markdown fences, extract first balanced `{...}`).

Source: `skills-drafts/ollama/ollama-playbook.md` Bug 1 (caption_lab project, qwen3-vl, May 2026).

### §2 — `num_predict: <positive int>` + `images: [...]` → empty response

**Verified May 2026 on qwen3-vl:4b.** Same failure mode as §1 — `eval_count` exactly hits the cap, response is empty. `num_predict: -1` (unlimited) and absent are both fine. Verified matrix from the playbook:

| Options                              | eval_count | response chars |
|--------------------------------------|------------|----------------|
| (none)                               | 4730       | 698 (works)    |
| `{temperature: 0.0}`                 | 2384       | 839 (works)    |
| `{num_predict: 400}`                 | 400        | **0 (BROKEN)** |
| `{num_predict: -1}` (unlimited)      | 1066       | 585 (works)    |

**Workaround:** don't cap output via `num_predict` on vision calls. Bound at the application layer after the response comes back (slice the string). If you need to abort runaway generation, switch to streaming and close the connection client-side after N tokens.

Source: `skills-drafts/ollama/ollama-playbook.md` Bug 2.

### §3 — high-detail images spiral past context limit

**Model-behavior bug, not a daemon bug.** Some images deterministically cause vision models (verified on qwen3-vl:4b/8b) to enter a runaway descriptive loop, generating tokens until the 32k context limit. Wall clock: >300s per image. `temperature` and `repeat_penalty` don't help. `num_predict` doesn't help (see §2). Triggering image traits: high-detail line art, many discrete elements inviting enumeration, high-contrast graphical content.

**Workaround:** accept the timeout cost with a sane HTTP timeout (60-120s) and `max_attempts` retry budget; flag affected images for review. Real fix is streaming + client-side abort after N tokens.

Source: `skills-drafts/ollama/ollama-playbook.md` Bug 3.

### §4 — `gpt-oss` ignores `think: true/false`

Passing a bool to `gpt-oss` is silently ignored — it always thinks unless you give it `"low"|"medium"|"high"`. Trace cannot be fully disabled on gpt-oss; pick `"low"` if you want minimal thinking. Source: [thinking.mdx:71](https://github.com/ollama/ollama/blob/main/docs/capabilities/thinking.mdx).

### §5 — `/api/embeddings` (plural) is deprecated; use `/api/embed`

Both still work, but the plural form returns a different shape (`embedding: [...]` instead of `embeddings: [[...]]`) and won't get new features. Source: [api.md:1813](https://github.com/ollama/ollama/blob/main/docs/api.md).

### §6 — model name hallucination

When asked to "use Ollama for X," it's tempting to write `llama3.3` or `gpt-4` without checking. Every Ollama call against an uninstalled model returns 404. **Always run discovery first** (§0). Common mismatches: writing `llama3` when only `llama3.2:latest` is pulled; writing `qwen3-vl` (no tag) when only `qwen3-vl:8b` is pulled.

## Diagnostic recipe — when something looks wrong

Don't loop on the live application. Probe the daemon directly. Each takes <1 minute.

### "The response is empty"

```python
import requests, base64
b64 = base64.b64encode(open("path/to/image.png", "rb").read()).decode()
for opts in [None, {}, {"temperature": 0.0}, {"num_predict": 400}]:
    body = {"model": "qwen3-vl:4b", "prompt": "Describe this image.",
            "images": [b64], "stream": False}
    if opts is not None:
        body["options"] = opts
    r = requests.post("http://localhost:11434/api/generate",
                      json=body, timeout=120)
    d = r.json()
    print(f"opts={opts}  eval={d.get('eval_count')}  len={len(d.get('response',''))}")
```

If `eval_count > 0` but `response == ""`, you've hit a vision-pipeline bug like §1 or §2. Vary one option at a time.

### "Calls are slow"

Time a single call. >30s for a single non-detailed image on the captioner role = the model is probably spiraling (§3). Check the raw response for repetition or going past the prompt's target length.

### "Model isn't loading"

```powershell
ollama ps                              # what's currently loaded
ollama show <model>                    # confirm it's installed and check capabilities
ollama pull <model>                    # if missing
```

If a model never appears in `ps` after a request, restart the daemon (`ollama serve` in a separate terminal on Linux/Mac, or restart the Ollama service on Windows).

### "It worked before"

Read this skill. Revert the last option change. If your option isn't in the safe-defaults table above, you owe a one-call probe before claiming it works.

## When stuck — searching the docs

The upstream Ollama docs are MIT-licensed and live at `github.com/ollama/ollama/docs/`. Cite this URL pattern in answers so users can verify:

```
https://github.com/ollama/ollama/blob/main/docs/<file>
```

**Local docs speedup (optional).** If the user has cloned the repo, they can set `OLLAMA_DOCS_DIR` to enable Grep over a local copy:

```powershell
# PowerShell, persistent
[System.Environment]::SetEnvironmentVariable(
    "OLLAMA_DOCS_DIR",
    "C:\path\to\ollama\docs",
    "User"
)
```

When `$env:OLLAMA_DOCS_DIR` is set and the path exists, prefer `Grep` over the local copy for searches. Otherwise, use `WebFetch` against the upstream URL.

### High-value docs (where to look first)

- `api.md` — REST endpoint reference. Search for endpoint name.
- `modelfile.mdx` — every PARAMETER option with defaults.
- `faq.mdx` — `keep_alive`, context length, concurrency, env vars, GPU detection.
- `capabilities/structured-outputs.mdx` — both `format` modes with examples.
- `capabilities/tool-calling.mdx` — single/parallel/streaming/agent-loop patterns.
- `capabilities/thinking.mdx` — `think` field and gpt-oss enum.
- `capabilities/vision.mdx` — `images` field on messages.
- `capabilities/embeddings.mdx` — `/api/embed` usage.
- `api/openai-compatibility.mdx` — `/v1/` shim.
- `api/anthropic-compatibility.mdx` — `/v1/messages` shim.
- `troubleshooting.mdx` — platform-specific GPU detection issues.
- `context-length.mdx` — `num_ctx` and `OLLAMA_CONTEXT_LENGTH`.

## Out of scope

- **Modelfile authoring** (custom models with `FROM`, `TEMPLATE`, `SYSTEM`). Refer to [modelfile.mdx](https://github.com/ollama/ollama/blob/main/docs/modelfile.mdx) when needed.
- **Importing GGUF / Safetensors models.** See [import.mdx](https://github.com/ollama/ollama/blob/main/docs/import.mdx).
- **Hosted Ollama Cloud features.** This skill targets local daemons (`localhost:11434`).
- **Other LLM providers.** For Gemini, use the `gemini-api` skill. For Claude API, use `claude-api`. For OpenAI direct, neither — but the OpenAI shim against local Ollama is in scope here.
