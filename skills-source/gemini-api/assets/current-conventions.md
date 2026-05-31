# Current Gemini 3.x conventions — wrong-way / right-way

These six patterns are documented in Google's 3.5 Flash migration guide. Each
one bites because either (a) older Gemini versions or other LLM APIs used the
opposite convention, or (b) it's a silent-failure mode that wouldn't surface
during casual testing. Code generated from stale training data will get these
wrong by default — that's what this reference is for.

The six footguns are listed in order of likelihood-to-hit when wiring up a
fresh project.

---

## Footgun 1: Sampling parameters on Gemini 3.x

**Why it bites:** Old reflex from earlier Gemini and from other providers (OpenAI, Anthropic). On Gemini 3.x, Google explicitly recommends defaults; the model's reasoning is calibrated against them, and setting these actively hurts. For deterministic-style output, use a system instruction instead.

### Python

```python
# ❌ Wrong — these no longer recommended on 3.x
config = types.GenerateContentConfig(
    temperature=0.7,
    top_p=0.9,
    top_k=40,
)
```

```python
# ✅ Right — let defaults stand; constrain via system instruction
config = types.GenerateContentConfig(
    system_instruction="Respond in JSON. No prose, no markdown fences."
)
```

### JavaScript

Same shape, with camelCase keys (`temperature`, `topP`, `topK`).

```typescript
// ❌ Wrong
const config = { temperature: 0.7, topP: 0.9, topK: 40 };

// ✅ Right
const config = { systemInstruction: "Respond in JSON. No prose." };
```

**Look for:** any of `temperature`, `top_p`/`topP`, `top_k`/`topK` in a `GenerateContentConfig` (Python) or `config` object (JS) for a `gemini-3*` model.

---

## Footgun 2: `thinking_budget` (deprecated) instead of `thinking_level` enum

**Why it bites:** The numeric `thinking_budget` was the pre-3.x API; it's now `thinking_level` taking an enum string. Default in 3.5 Flash changed from `"high"` (3 Flash Preview) to `"medium"` — code calibrated against the old default may need `"high"` to match prior quality. JS uses **uppercase** enum values; Python uses lowercase. Mixing these silently invalidates the config.

### Python

```python
# ❌ Wrong — deprecated numeric budget
config = types.GenerateContentConfig(
    thinking_config=types.ThinkingConfig(thinking_budget=7500),
)
```

```python
# ✅ Right — enum string, lowercase
config = types.GenerateContentConfig(
    thinking_config=types.ThinkingConfig(thinking_level="medium"),
)
# Valid values: "minimal" | "low" | "medium" | "high"
```

### JavaScript

```typescript
// ❌ Wrong — deprecated, or lowercase values
const config = { thinkingConfig: { thinkingBudget: 7500 } };
const config2 = { thinkingConfig: { thinkingLevel: "medium" } };  // wrong case!
```

```typescript
// ✅ Right — UPPERCASE enum value in JavaScript
const config = { thinkingConfig: { thinkingLevel: "MEDIUM" } };
// Valid values: "MINIMAL" | "LOW" | "MEDIUM" | "HIGH"
```

**Look for:** any `thinking_budget` / `thinkingBudget` reference; any lowercase `thinkingLevel` value in JavaScript code; any uppercase `thinking_level` value in Python.

---

## Footgun 3: Function-call `id` / `name` / count strict matching

**Why it bites:** The Interactions API errors loudly on mismatch; the GenerateContent API does NOT — it returns `finish_reason: STOP` with empty `content`. Silent. Worse: the python-genai SDK's manual-function-calling docs in some places omit `id=` in the example — copying those will produce broken 3.x code.

The rule: every `FunctionResponse` must carry `id` matching the original `FunctionCall.id`, `name` matching the original `name`, and the count must match (one response per call, in the same turn).

### Python

```python
# ❌ Wrong — no id; silently returns empty content on 3.x
function_response_part = types.Part.from_function_response(
    name=tool_call.name,
    response={"result": result},
)
```

```python
# ✅ Right — id is non-negotiable on 3.x
function_response_part = types.Part.from_function_response(
    name=tool_call.name,
    response={"result": result},
    id=tool_call.id,
)
```

### JavaScript

In JS, `createPartFromFunctionResponse(id, name, response)` has `id` as the **first positional argument** — the signature forces it. The footgun in JS is hand-rolling the `functionResponse` object literal and forgetting `id`:

```typescript
// ❌ Wrong — id missing from the object literal
const part = {
  functionResponse: {
    name: toolCall.name,
    response: { result },
  },
};
```

```typescript
// ✅ Right — id present
const part = {
  functionResponse: {
    name: toolCall.name,
    id: toolCall.id,
    response: { result },
  },
};
// Or use the helper:
import { createPartFromFunctionResponse } from "@google/genai";
const part = createPartFromFunctionResponse(toolCall.id, toolCall.name, { result });
```

**Look for:** any `Part.from_function_response` (Py) or `functionResponse: { ... }` literal (JS) without `id=` / `id:`. Also: a model issuing 3 function calls but code returning only 2 responses in the next turn.

---

## Footgun 4: Multimodal content INSIDE the function response, not alongside it

**Why it bites:** Common reflex — a function returns an image, and the caller sends the image back as a separate user-role multimodal part following the `FunctionResponse`. The 3.x model expects the image bytes (or other media) to live **inside** the `FunctionResponse.response` dict, not as a sibling part. Putting it outside causes "thought leakage" and lower-quality follow-up responses.

### Python

```python
# ❌ Wrong — image as a separate part after the function response
contents = [
    *previous_contents,
    response.candidates[0].content,
    types.Content(role="user", parts=[
        types.Part.from_function_response(
            name=tool_call.name,
            response={"result": "instrument.jpg"},
            id=tool_call.id,
        ),
        types.Part.from_bytes(data=image_bytes, mime_type="image/jpeg"),  # ❌ separate part
    ]),
]
```

```python
# ✅ Right — image bytes/base64 included as a key in the response dict
contents = [
    *previous_contents,
    response.candidates[0].content,
    types.Content(role="user", parts=[
        types.Part.from_function_response(
            name=tool_call.name,
            response={
                "result": "instrument.jpg",
                "image": base64_image_data,
            },
            id=tool_call.id,
        ),
    ]),
]
```

### JavaScript

```typescript
// ✅ Right — include media inside the response object
const part = {
  functionResponse: {
    name: toolCall.name,
    id: toolCall.id,
    response: {
      result: "instrument.jpg",
      image: base64ImageData,
    },
  },
};
```

**Look for:** a function that produces media (image, audio, PDF), followed by a separate user-role multimodal part in the same content message.

---

## Footgun 5: Inline instructions in function responses as separate Parts

**Why it bites:** Common reflex — append a hint or extra instruction as a separate `Part.from_text(...)` after the `FunctionResponse`. 3.x interprets that as a new user turn; quality drops and thought leakage can occur. Append instructions to the function response text itself, separated by two newlines.

### Python

```python
# ❌ Wrong — separate text part after the function response
parts=[
    types.Part.from_function_response(
        name=tool_call.name,
        response={"result": result_json},
        id=tool_call.id,
    ),
    types.Part.from_text(text="Now summarize this result concisely."),  # ❌
]
```

```python
# ✅ Right — append to the function response text, two newlines as separator
result_text = f"{json.dumps(result)}\n\n<your inline instructions here>"
parts=[
    types.Part.from_function_response(
        name=tool_call.name,
        response={"result": result_text},
        id=tool_call.id,
    ),
]
```

### JavaScript

Same shape — concat into the response text:

```typescript
const resultText = `${JSON.stringify(result)}\n\n<your inline instructions here>`;
const part = {
  functionResponse: {
    name: toolCall.name,
    id: toolCall.id,
    response: { result: resultText },
  },
};
```

**Look for:** any text-only `Part` immediately following a `FunctionResponse` part in the same content message.

---

## Footgun 6: Reconstructing conversation history strips thought signatures

**Why it bites:** Gemini 3.5 Flash preserves intermediate reasoning across turns when **thought signatures** travel inside the conversation history. The SDKs do this for you when you replay `response.candidates[0].content` verbatim. If you manually rebuild `contents` from `{role, text}` pairs out of your own database, the signatures are gone — you lose the preserved-thinking benefit and may regress on multi-step tasks.

### Python

```python
# ❌ Wrong — reconstructing from text only loses thought signatures
contents = [
    {"role": "user", "parts": [{"text": prev_user_msg}]},
    {"role": "model", "parts": [{"text": prev_model_text}]},
    {"role": "user", "parts": [{"text": new_user_msg}]},
]
response = client.models.generate_content(model="gemini-3.5-flash", contents=contents)
```

```python
# ✅ Right — replay the model's previous Content object verbatim
contents = [
    prev_user_content,
    prev_response.candidates[0].content,  # carries thought signatures
    new_user_content,
]
response = client.models.generate_content(model="gemini-3.5-flash", contents=contents)
```

If you must persist conversations to a database, store the full `Content` objects (their serialized form including any `thought_signature` fields), not just `text`. For genuinely simple single-turn queries where multi-turn reasoning isn't needed, you can clear thoughts to reduce token cost — but that's an optimization, not the default.

**Look for:** code that builds `contents` from a database query returning `(role, text)` rows; any code constructing a model-role `Content` with only a `text` part.

---

## Current Gemini 3.x models

| Model | Model code | Input limit | Output limit | Knowledge cutoff | When to pick |
|---|---|---|---|---|---|
| Gemini 3.5 Flash | `gemini-3.5-flash` | 1M tokens | 65k tokens | Jan 2025 | Default for production. GA. Best for agentic and coding workloads. |
| Gemini 3.1 Flash-Lite | `gemini-3.1-flash-lite` | 1M tokens | 65k tokens | Jan 2025 | High-volume, latency-sensitive, cost-sensitive workloads — translation, simple extraction, classifier-as-router. |
| Gemini 3 Flash Preview | `gemini-3-flash-preview` | (legacy) | (legacy) | — | Only if you need Computer Use, which is not yet supported on 3.5. |

Pricing differs by roughly an order of magnitude between Flash and Flash-Lite — verify the current numbers at https://ai.google.dev/gemini-api/docs/pricing before scaling. Knowledge cutoffs may shift as Google ships point releases; verify via the models overview at https://ai.google.dev/gemini-api/docs/models if it matters for your use case.

Pre-3.x model IDs (`gemini-pro`, `gemini-1.5-flash`, `gemini-1.5-pro`, `gemini-2.0-flash`, `gemini-2.5-flash`, etc.) are out of scope for these conventions — if you're maintaining code on those, the migration checklist in https://ai.google.dev/gemini-api/docs/whats-new-gemini-3.5 is the canonical upgrade path.

---

## Gemma 4 on the hosted Gemini API

Gemma 4 (Google's open-weight family, released April 2026, Apache 2.0) is served on the **same** hosted Gemini API as the Gemini-branded models — same `generativelanguage.googleapis.com/v1beta/models/{id}:generateContent` endpoint, same `google-genai` / `@google/genai` SDK, same request shape. You do NOT need to download weights or run a local server to use these via the API. (The smaller on-device variants — E2B, E4B — are open-weights-only and not served on the hosted API; only the two below are.)

| Model | Model code | Arch | Params | Context | Modalities |
|---|---|---|---|---|---|
| Gemma 4 31B | `gemma-4-31b-it` | Dense | 30.7B | 256K | text + image |
| Gemma 4 26B | `gemma-4-26b-a4b-it` | MoE (8 of 128 experts active, 1 shared) | 25.2B total / 3.8B active | 256K | text + image |

**Dense vs MoE — which to pick.** The dense `gemma-4-31b-it` gives predictable full-parameter quality and is the safer default when output *consistency* matters (e.g. a judge/scorer whose outputs you compare across runs). The MoE `gemma-4-26b-a4b-it` is cheaper/faster per token (only ~3.8B params active) and near-31B quality — a good captioner/generator, worth A/B-ing, but the routing makes it a slightly less stable choice for a scoring role. Both share the identical API shape, so supporting both is just two entries in a model list.

**Why Gemma 4 matters for batch work — free-tier RPD.** The free-tier requests-per-day limit is dramatically higher for Gemma than for the Gemini Flash models, which flips the usual default for high-volume jobs (captioning, judging, eval/search loops):

| Model | Approx. free-tier RPD |
|---|---|
| Gemma 4 | ~1,500 |
| `gemini-3.1-flash-lite` | ~500 |
| `gemini-3.5-flash` | ~20 |

At ~20 RPD, `gemini-3.5-flash` cannot complete even one moderate batch (e.g. a 27-item caption + judge pass = 54 requests). For any loop that fans out across a dataset, reach for Gemma 4 first. **Verify current numbers** at https://ai.google.dev/gemini-api/docs/rate-limits — Google adjusts these.

### Supported features (confirmed via Google's "Run Gemma with the Gemini API" page)

- ✅ **`system_instruction` / `systemInstruction`** — fully supported, same as Gemini. (Note: this is a *correction* of a common stale belief that Gemma lacks system-instruction support — older locally-hosted Gemma chat templates folded the system prompt into the first user turn, but the hosted API exposes the real field.)
- ✅ **Image input** — works both ways: inline base64 (`Part.from_bytes` / `inline_data`) AND the Files API (`file_data` + `file_uri`). Google's doc example uses Files API; inline bytes also work, same as Gemini. Use inline for one-shot small images, Files API for large or reused ones.
- ✅ **Function calling**, ✅ **structured JSON output**, ✅ **Google Search grounding**, ✅ **`thinking_level`** (Google's example sets `thinking_level="high"`).

### The one real footgun: sampling parameters

Footgun 1 above (**don't set `temperature` / `top_p` / `top_k`**) is specific to **Gemini 3.x**, whose *reasoning is calibrated against the defaults*. That justification does **not** automatically extend to Gemma — it's a different model family, and Google does **not** publish sampling guidance for Gemma on the API. So:

- Do not blindly apply the "never set temperature" rule to Gemma code, and do not blindly copy a temperature you'd use elsewhere either.
- If you need deterministic-style output, the system-instruction approach (Footgun 1's "right way") is still the safest portable move.
- If you genuinely need sampling control on Gemma, treat it as unverified: test empirically and check the current model card (https://ai.google.dev/gemma/docs/core/model_card_4) rather than assuming.

This asymmetry — a rule that's load-bearing for Gemini 3.x but unverified for Gemma — is exactly the kind of thing that produces subtly wrong code when you pattern-match "it's all the Gemini API" too eagerly.
