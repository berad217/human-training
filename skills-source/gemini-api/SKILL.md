---
name: gemini-api
description: Use when writing, reviewing, debugging, or migrating Gemini API or hosted-Gemma code (Gemini 3.x, Gemma 4). Triggers on imports of `google.genai` / `@google/genai`, model strings like `gemini-3-flash`, `gemini-3.5-flash`, `gemini-3.1-flash-lite`, `gemma-4-31b-it`, `gemma-4-26b-a4b-it`, calls to `generate_content` / `generateContent`, config of `GenerateContentConfig` / `ThinkingConfig`, and requests to wire up Gemini or Gemma for a task. Use proactively before writing Gemini/Gemma code, so defaults reflect current 3.x conventions rather than older training-data ones. Do NOT use for general LLM-provider comparisons, OpenAI/Anthropic specifics, locally-hosted Gemma open weights (Ollama / HuggingFace / vLLM — this covers the hosted API path), or non-Gemini Google Cloud.
allowed-tools: [Read, Write, Edit, Grep, Glob, Bash, WebFetch]
---

# Gemini API (3.x)

Gemini 3.x is recent enough that training-data defaults are wrong: old SDK
package, removed sampling parameters, deprecated thinking config, a silent
function-call failure. This skill owns the **conventions and footguns**.
Runnable how-to is in `assets/cookbook.md`; the wrong-way / right-way pairs,
a dated model and rate-limit snapshot, and the index of Google's docs pages
are in `assets/current-conventions.md`. Read those only when a step points
you there.

---

## Discover, never recall

**Model ids and rate limits change faster than any file, including this one.**
A model id from memory, from a Stack Overflow answer, or from this skill's
assets is a guess. Look, then write:

```python
for m in client.models.list():           # JS: for await (const m of await ai.models.list())
    print(m.name, m.supported_actions)   # e.g. "models/gemini-...", ["generateContent", ...]
```

The same list is `GET https://generativelanguage.googleapis.com/v1beta/models`
with the API key, and the models overview page (index in the reference) has
the per-model context, output limits and knowledge cutoffs. Pick by **role**,
not by name: the current-generation Flash for production default; the
Flash-Lite tier for high-volume, latency- or cost-sensitive work; the hosted
Gemma models for free-tier batch work (below). An id already in the code that
is a generation behind the newest in the live list is stale — flag it.

**Rate limits are per-account and per-model, and the public docs stopped
publishing per-model tables.** Read yours at https://aistudio.google.com/rate-limit,
and treat a 429's `retryDelay` as authoritative. Batch loops pace themselves
against the RPM you actually have. The snapshot in the reference is dated and
marked do-not-copy; it exists so you know the *shape* of the surprise (an
order-of-magnitude spread in free-tier requests per day between tiers), not
the numbers.

---

## The six footguns

1. **SDK: `google-genai` (Python) / `@google/genai` (JavaScript).**
   `google-generativeai` and `import google.generativeai as genai` are the
   deprecated SDK; any example using them predates the current client shape.

2. **On Gemini 3.x, do not set `temperature`, `top_p`, or `top_k`.** The
   model's reasoning is calibrated against the defaults and setting them
   actively hurts. For deterministic-style output, constrain with a system
   instruction. This rule is **Gemini-specific**: Google publishes no sampling
   guidance for Gemma on the API, so do not assume it transfers (or that its
   opposite does) — test.

3. **`thinking_level` enum, not `thinking_budget` integer.** Values
   `minimal | low | medium | high`; **lowercase in Python, UPPERCASE in
   JavaScript.** The default level differs between model versions, so code
   calibrated against one model's default may need re-tuning on the next.

4. **Function calling: Python's automatic mode first** — pass the function
   itself in `tools=[fn]`; the signature and docstring *are* the schema the
   model sees, not decoration. In manual mode (or JavaScript, which has no
   automatic mode) **every `FunctionResponse` must carry `id=` matching the
   `FunctionCall.id`.** Omitting it yields `finish_reason: STOP` with empty
   content — a silent failure, not an error. Media and follow-up instructions
   go *inside* the function response, not as sibling parts; and replay the
   model's previous `Content` verbatim when rebuilding history, or you strip
   the thought signatures. Patterns for all three are Footguns 3–6 in the
   reference.

5. **System instructions are `config`, not a `role: "system"` message.** The
   OpenAI Chat Completions mental model is its own footgun here.

6. **Hosted Gemma is the same endpoint, same SDK, same request shape** — no
   weights, no local server. Two things differ: structured output
   (`response_schema`) is **best-effort, not constrained decoding**, so
   `response.parsed` can be `None` with fenced JSON in `response.text` — parse
   defensively (fallback in the reference); and its free-tier limits have been
   far higher than the Gemini tiers, which is why it is the first reach for
   captioning, judging and eval loops. Empirically, "return null if unsure"
   binds more weakly on Gemma than on Gemini, so keep a downstream verifier.

Also: Files API uploads **expire after 48 hours** — production code re-uploads
on 404. Inline bytes are fine under ~20 MB for a single use.

---

## First call

`GEMINI_API_KEY` in the environment; the client reads it implicitly.

```python
from google import genai
from google.genai import types

client = genai.Client()
MODEL = "..."  # from client.models.list(), not from memory

response = client.models.generate_content(
    model=MODEL,
    contents="Translate to German: are you up for pizza later?",
    config=types.GenerateContentConfig(
        system_instruction="Output only the translated text."
    ),
)
print(response.text)
```

JavaScript mirrors it: `new GoogleGenAI({})`, `ai.models.generateContent({
model, contents, config: { systemInstruction } })`. Images, structured output,
Files API, PDFs and both function-calling modes are in the cookbook.

---

## Everything else

Fetch Google's current page with `WebFetch` rather than improvising from older
knowledge — streaming, async, chat, safety, caching, tokens, pricing, Vertex
migration, built-in tools. The URL index is the last section of
`assets/current-conventions.md`; if a URL 404s the page moved — start from
https://ai.google.dev/gemini-api/docs and follow the left nav.

**Reply:** which model id you chose and how you confirmed it is live, which of
the footguns applied to the code in hand, and any limit or default you could
not verify, where you looked for it, and that you are treating it as unknown.
