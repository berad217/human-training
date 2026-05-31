---
name: gemini-api
description: Use when writing, reviewing, debugging, or migrating Gemini API code — especially Gemini 3.x (3 Flash, 3.5 Flash, 3.1 Flash-Lite) and Gemma 4 served via the same hosted API (gemma-4-31b-it, gemma-4-26b-a4b-it). Triggers on imports of `google.genai` / `@google/genai`, model strings like `gemini-3-flash`, `gemini-3.5-flash`, `gemini-3.1-flash-lite`, `gemma-4-31b-it`, or `gemma-4-26b-a4b-it`, calls to `generate_content` / `generateContent`, configuration of `GenerateContentConfig` / `ThinkingConfig`, and explicit user requests to wire up Gemini or Gemma for a task (text, image, function calling, structured output, PDF, audio). Use proactively when about to write Gemini/Gemma code so the default patterns reflect current 3.x conventions rather than older training-data defaults. Do NOT use for general LLM-provider comparisons, OpenAI/Anthropic specifics, locally-hosted Gemma open weights (Ollama / HuggingFace / vLLM — this skill covers the hosted API path), or non-Gemini Google Cloud (storage, Vertex unrelated to Gemini, etc.).
allowed-tools: [Read, Write, Edit, Grep, Glob, Bash, WebFetch]
---

# Gemini API (3.x)

A working reference for writing Gemini API code in 2026 and beyond. This skill exists because Gemini 3.x is recent enough that model-default training knowledge will lead you to write code with stale conventions — old SDK package, removed sampling parameters, deprecated thinking config, silent function-call failure modes. Load this before writing or reviewing Gemini code so the patterns Claude produces match the current SDK and current API contract instead of last year's.

The skill owns the **conventions and footguns** (the TL;DR below and `assets/current-conventions.md`). For use-case how-to, see `assets/cookbook.md`. For anything not covered there, Google's official docs are the source of truth — the pointer table at the bottom is your map; `WebFetch` is in the allowed tools so you can pull current pages live.

## TL;DR — load these six facts before writing any Gemini code

1. **Use `google-genai` (Python) or `@google/genai` (JavaScript).** `google-generativeai` is the deprecated Python SDK; any example or Stack Overflow answer using `import google.generativeai as genai` is pre-current and will not match the current client shape. Install: `pip install google-genai` / `npm install @google/genai`.

2. **On Gemini 3.x, don't set `temperature`, `top_p`, or `top_k`.** Google explicitly recommends defaults; the model's reasoning is calibrated against them and setting these actively hurts. If you want deterministic-style output, write a system instruction that constrains the response — that's the current idiom, not low-temperature sampling.

3. **Use `thinking_level` enum, not `thinking_budget` integer.** Values are `"minimal"` / `"low"` / `"medium"` / `"high"`. Default in 3.5 Flash is `"medium"` (was `"high"` in 3 Flash Preview — code calibrated against the old default may need bumping). In JavaScript the values are **uppercase** (`"MEDIUM"`, `"HIGH"`) where Python is lowercase — easy footgun.

4. **For function calling, prefer Python's automatic mode.** Pass the Python function directly in `tools=[my_function]`; the SDK extracts the schema from the signature + docstring and handles the call/response loop. If you must use manual mode (or you're in JavaScript, which has no automatic mode), **every** `FunctionResponse` MUST include `id=` matching the original `FunctionCall.id`. Omitting `id=` causes `finish_reason: STOP` with empty content — a silent failure mode, not an error.

5. **Current 3.x model IDs:** `gemini-3.5-flash` (default for production, GA), `gemini-3.1-flash-lite` (high-volume / latency-sensitive / cost-sensitive), `gemini-3-flash-preview` (only if you need Computer Use, not yet on 3.5). Do NOT hardcode `gemini-pro`, `gemini-1.5-flash`, `gemini-2.5-flash` in new code — those are pre-3.x. Full table in `assets/current-conventions.md`.

6. **Gemma 4 runs on the *same* hosted Gemini API — and has a far higher free-tier limit.** IDs: `gemma-4-31b-it` (dense, 30.7B) and `gemma-4-26b-a4b-it` (MoE, 25.2B total / 3.8B active). Both are multimodal (text + image), 256K context, and support `system_instruction`, function calling, structured JSON output, Google Search grounding, and `thinking_level`. They hit the same `generateContent` endpoint with the same request shape — no separate SDK, no local weights needed. **For high-volume batch work (captioning, judging, eval loops) Gemma 4 is the workhorse**: free-tier requests-per-day run roughly Gemma 4 ≈ 1,500 ≫ `gemini-3.1-flash-lite` ≈ 500 ≫ `gemini-3.5-flash` ≈ 20 (verify current numbers — they shift). **Caveat:** fact 2 (don't set `temperature`) is specific to Gemini 3.x reasoning calibration — Google does NOT document sampling guidance for Gemma, so do not assume the rule transfers to a different model family. See `assets/current-conventions.md` for the Gemma section.

## Setup and first call

Set an env var named `GEMINI_API_KEY` with your key from https://aistudio.google.com/. The SDK reads it implicitly.

### Python

```bash
pip install google-genai
```

```python
from google import genai
from google.genai import types

client = genai.Client()  # reads GEMINI_API_KEY from env

response = client.models.generate_content(
    model="gemini-3.5-flash",
    contents="Explain how parallel agentic execution works in three sentences.",
)
print(response.text)
```

For a system instruction (use this instead of low temperature for deterministic-style behavior):

```python
response = client.models.generate_content(
    model="gemini-3.5-flash",
    contents="Translate to German: Hey, are you down to grab some pizza later?",
    config=types.GenerateContentConfig(
        system_instruction="Output only the translated text, no commentary."
    ),
)
print(response.text)
```

### JavaScript / TypeScript

```bash
npm install @google/genai
```

```typescript
import { GoogleGenAI } from "@google/genai";

const ai = new GoogleGenAI({});  // reads GEMINI_API_KEY from env

async function main() {
  const response = await ai.models.generateContent({
    model: "gemini-3.5-flash",
    contents: "Explain how parallel agentic execution works in three sentences.",
  });
  console.log(response.text);
}
main();
```

System instruction in JS goes inside `config`:

```typescript
const response = await ai.models.generateContent({
  model: "gemini-3.5-flash",
  contents: "Translate to German: Hey, are you down to grab some pizza later?",
  config: {
    systemInstruction: "Output only the translated text, no commentary.",
  },
});
```

Note: system instructions are configured separately from `contents` — they're NOT a `role: "system"` message like in the OpenAI Chat Completions shape. Reusing OpenAI mental models here is its own footgun.

## Image input

For an image under ~20 MB used once, inline the bytes. For larger files or images reused across multiple calls, upload via the Files API.

### Python — inline bytes

```python
with open("photo.jpg", "rb") as f:
    image_bytes = f.read()

response = client.models.generate_content(
    model="gemini-3.5-flash",
    contents=[
        types.Part.from_bytes(data=image_bytes, mime_type="image/jpeg"),
        "Describe what's in this image.",
    ],
)
print(response.text)
```

### JavaScript — inline bytes

```typescript
import * as fs from "fs";

const imagePart = {
  inlineData: {
    data: Buffer.from(fs.readFileSync("photo.jpg")).toString("base64"),
    mimeType: "image/jpeg",
  },
};

const response = await ai.models.generateContent({
  model: "gemini-3.5-flash",
  contents: [imagePart, "Describe what's in this image."],
});
```

For large or reused media, see `assets/cookbook.md` section 6 (Files API). Uploaded files **auto-expire after 48 hours** — production code should handle re-upload on 404.

## Function calling

Two modes in Python: **automatic** (recommended) and **manual** (when you need to inspect/modify args, do async tool execution, or run in JS — which has no automatic mode).

### Python — automatic mode (recommended)

```python
from google import genai
from google.genai import types

def get_current_weather(city: str) -> str:
    """Returns the current weather in a given city."""
    if "boston" in city.lower():
        return "The weather in Boston is 15°C and sunny."
    return f"Weather data for {city} is not available."

client = genai.Client()

response = client.models.generate_content(
    model="gemini-3.5-flash",
    contents="What is the weather in Boston?",
    config=types.GenerateContentConfig(tools=[get_current_weather]),
)
print(response.text)
```

The SDK extracts the schema from the function signature + docstring, handles the call/response loop, and returns the model's final text. **Your type hints and docstring ARE the schema the model sees** — they're not optional decoration.

For manual mode (Python or JS), see `assets/cookbook.md` sections 9 and 10. **In manual mode, `Part.from_function_response(...)` MUST include `id=`** — omitting it silently kills the response. See `assets/current-conventions.md` Footgun 3 for the full pattern.

## For everything else — pointer table

This skill covers setup, main flow, image input, function calling, and the documented 3.x footguns authoritatively. For everything else, fetch Google's current docs page via `WebFetch`:

| Topic | Where to look |
|---|---|
| Streaming (`generate_content_stream`) | https://ai.google.dev/gemini-api/docs/text-generation |
| Async (`client.aio.models.*`) | https://ai.google.dev/gemini-api/docs/text-generation |
| Multi-turn chat (`client.chats.create()`) | https://ai.google.dev/gemini-api/docs/chat |
| Safety filters & `finish_reason` handling | https://ai.google.dev/gemini-api/docs/safety-guidance |
| Structured output (beyond Pydantic basics) | https://ai.google.dev/gemini-api/docs/structured-output |
| Caching | https://ai.google.dev/gemini-api/docs/caching |
| `count_tokens` | https://ai.google.dev/gemini-api/docs/tokens |
| Files API lifecycle (48h expiration, delete) | https://ai.google.dev/gemini-api/docs/files |
| Vertex AI vs Gemini Developer API | https://ai.google.dev/gemini-api/docs/migrate-to-cloud |
| Pricing | https://ai.google.dev/gemini-api/docs/pricing |
| Built-in tools (Search, URL context, code execution) | https://ai.google.dev/gemini-api/docs/tool-combination |
| Models overview | https://ai.google.dev/gemini-api/docs/models |
| Running Gemma 4 via the hosted Gemini API | https://ai.google.dev/gemma/docs/core/gemma_on_gemini_api |
| Gemma 4 model card (variants, params, modalities) | https://ai.google.dev/gemma/docs/core/model_card_4 |

If a URL above 404s, the page was reshuffled — start from https://ai.google.dev/gemini-api/docs and follow the left nav.

## Source of truth

This skill owns the **conventions and footguns** (TL;DR above and `assets/current-conventions.md`). It's tuned to the current SDK and the current 3.x API contract — copy from these without second-guessing your training data.

Google's official docs own the **use-case how-to** for everything in the pointer table — fetch them fresh with `WebFetch` rather than improvising from older knowledge. The Gemini SDK changes fast enough that the "is my mental model current?" check is worth making explicit before writing non-trivial code.
