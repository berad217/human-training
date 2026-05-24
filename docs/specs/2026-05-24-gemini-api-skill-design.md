# Design — `gemini-api` skill

**Date:** 2026-05-24
**Status:** Design (pre-implementation)
**Lives at:** `skills-drafts/gemini-api/` while iterating; graduates to
`skills-source/gemini-api/` when ready.

---

## Purpose

A current-Gemini-API working reference that Claude loads when writing or
reviewing Gemini code. It exists because Gemini 3.x is recent enough that
Claude's training data still defaults to older conventions (pre-3.x
sampling-parameter habits, deprecated `thinking_budget`, the wrong SDK
package name) and to other-LLM-API conventions (OpenAI-shaped function
calling, "set `temperature` for determinism" reflex).

The skill prevents the predictable initial stumble when wiring Gemini into
a project, then points Claude at Google's official docs for any use case
the skill doesn't cover authoritatively.

## Non-goals

- Not an encyclopedic Gemini API reference. Streaming, async, multi-turn
  chat, safety filter handling, caching, token counting, Vertex AI distinction:
  pointer-link only.
- Not a migration tool. The skill is forward-looking — "how to write
  Gemini code today" — even though the *reason* for its existence is that
  training data lags reality.
- Not a guide to choosing between providers (Gemini vs OpenAI vs Anthropic).
  Triggers only when Gemini is already the target.

## Scope

Authoritatively covered:
1. **Setup** — install command, client construction, API key conventions.
2. **Main flow** — one-shot text generation; system instructions.
3. **Image input** — inline bytes vs Files API; both Python and JS.
4. **Function calling end-to-end** — Python automatic mode (preferred) and
   manual mode (with the 3.x `id` requirement baked in); JS manual mode.
5. **Current 3.x conventions** — six footguns from Google's 3.5 migration guide:
   - Don't set `temperature` / `top_p` / `top_k`
   - Use `thinking_level` enum, not `thinking_budget`
   - Function-call `id`/`name`/count strict matching
   - Multimodal content INSIDE function responses
   - Inline instructions appended to function response text
   - Thought preservation: pass full unmodified history
6. **Model reference table** — current 3.x model IDs with capability matrix
   and "use this when" guidance, plus pricing-page link.

Pointer-only (no reproduction, just one-line + URL):
- Streaming (`generate_content_stream` / async iteration)
- Async (`client.aio.models.*`)
- Multi-turn chat (`client.chats.create()`)
- Safety filters / `finish_reason` handling
- Structured output (the basic Pydantic pattern IS reproduced; advanced
  schema features are pointer-linked)
- File API lifecycle (48h expiration, `client.files.delete`)
- Caching, count_tokens
- Vertex AI vs Gemini Developer API distinction
- Code execution, URL context, Google Search grounding (3.x built-in tools)

## Languages

**Python is primary.** Most Google examples are Python-first; the SDK
migration was Python-side; the user's primary language.

**JavaScript/TypeScript is secondary** — included for the surfaces where
the shape genuinely differs (camelCase config keys, `inlineData` vs
`Part.from_bytes`, `parametersJsonSchema` vs `parameters_json_schema`). No
blind doubling of every snippet.

REST is not covered. The 3.5 migration doc has REST examples; if needed,
pointer-link.

## File layout

```
skills-source/gemini-api/                  (after graduation)
├── SKILL.md                ~150-180 lines  trigger + TL;DR + setup +
│                                           main flow + pointer table
├── assets/
│   ├── current-conventions.md ~200-250 lines  six 3.x footguns,
│   │                                          wrong/right pairs in Py + JS
│   └── cookbook.md            ~250-350 lines  end-to-end examples:
│                                              text + system_instruction,
│                                              image input (inline + Files API),
│                                              function calling end-to-end
│                                              (Py auto, Py manual, JS),
│                                              structured output (Pydantic),
│                                              PDF processing
└── evals/
    └── trigger-eval.json   ~8 candidate queries (4 should-trigger,
                            4 should-NOT-trigger)
```

The `research/` directory in `skills-drafts/gemini-api/` does NOT graduate —
it stays in drafts as reference for future skill maintenance.

## SKILL.md structure (the spine)

1. **Frontmatter.** `name: gemini-api`, `description` tuned for:
   - "write me Gemini code", "wire up Gemini for X", "use Gemini 3.x"
   - imports of `google.genai` / `@google/genai`
   - model strings matching `gemini-3*`, `gemini-3-flash`, `gemini-3.5-flash`, `gemini-3.1-flash-lite`
   - mentions of `generate_content`, `generateContent`, `GenerateContentConfig`, `ThinkingConfig`
   - DOES NOT trigger on: general LLM discussion, non-Gemini Google Cloud, OpenAI/Anthropic specifics
   - `allowed-tools: [Read, Write, Edit, Grep, Glob, Bash, WebFetch]` (WebFetch so future-Claude can follow the pointer links live).

2. **TL;DR (~40 lines).** Five facts ordered by load-bearing weight, each
   one or two lines:
   - Use `google-genai` package, NOT `google-generativeai` (deprecated).
   - On Gemini 3.x: don't set `temperature` / `top_p` / `top_k`. Use system instructions for deterministic-style behavior.
   - Use `thinking_level` enum (`"minimal"`/`"low"`/`"medium"`/`"high"`), NOT `thinking_budget` (deprecated).
   - For function calling: prefer Python automatic mode. In manual mode, EVERY `FunctionResponse` must include `id` matching the original `FunctionCall` — or you get silent empty responses.
   - Current model IDs and quick "which to pick" decision.

3. **Setup & first call (~30 lines).**
   - Install command (Py + JS).
   - Client construction (env var convention + how to override).
   - Minimum viable text call.
   - System instruction usage.

4. **Image input (~20 lines).**
   - Inline bytes pattern (Py + JS).
   - When to use Files API instead (≥20MB or reused across calls).
   - Files API upload + cleanup, with the 48h expiration noted.

5. **Function calling (~30 lines).**
   - Python automatic mode example. Plus: "this is the recommended path."
   - "When you need manual control" — pointer to cookbook.md for full manual example.

6. **For everything else (~25 lines).** Pointer table:
   - Streaming → `assets/cookbook.md` + Google docs URL
   - Async → Google docs URL
   - Chat (multi-turn) → Google docs URL
   - Safety / finish_reason → Google docs URL
   - Structured output → `assets/cookbook.md` + Google docs URL
   - Caching → Google docs URL
   - count_tokens → Google docs URL
   - Vertex AI distinction → Google docs URL

7. **Source of truth.** Two-line note: skill owns the conventions/footguns;
   Google's docs own use-case how-to. Link to `https://ai.google.dev/gemini-api/docs`.

## `assets/current-conventions.md` structure

Six sections, one per footgun, each ~30-40 lines:

Each section format:
- `## Footgun N: <name>`
- One-line "Why it bites:" (training-data drift, silent failure mode, etc.)
- `### Python` block: wrong-way → right-way code pair (~5-10 lines each).
- `### JavaScript` block: wrong-way → right-way code pair if it differs meaningfully; otherwise note "same shape, with camelCase keys."
- "Look for:" — one-line pattern to spot in code (e.g., `temperature=` in a `GenerateContentConfig`).

The six footguns, in order of likelihood-to-hit:
1. `temperature` / `top_p` / `top_k` set on 3.x (most reflexive habit).
2. `thinking_budget=N` instead of `thinking_level="..."`.
3. `Part.from_function_response()` missing `id=` (silent fail — `finish_reason: STOP`, empty content).
4. Multimodal content provided alongside function response instead of inside it (quality degradation, "thought leakage").
5. Inline instructions in function responses as separate Parts instead of appended text.
6. Manual conversation history reconstruction stripping thought signatures (loses preserved reasoning context).

Tail: model ID reference table (3 Flash, 3.5 Flash, 3.1 Flash-Lite) with
columns: model_code, token-limit input/output, knowledge cutoff, when-to-pick.

## `assets/cookbook.md` structure

Ten use cases, each a complete runnable snippet:

1. **Text + system instruction** (Py + JS) — the "follow system_instruction to constrain output" pattern from the translation example.
2. **Translation** (Py) — direct from research material.
3. **Structured output with Pydantic** (Py) — `response_mime_type` + `response_json_schema` + Pydantic model. Direct from research.
4. **Structured output without Pydantic** (Py + JS) — raw JSON schema variant for projects without Pydantic.
5. **Image input — inline bytes** (Py + JS) — from context7 results.
6. **Image input — Files API for large files** (Py) — from context7 results; includes the `client.files.delete()` cleanup line.
7. **PDF processing — inline** (Py) — direct from research material.
8. **Function calling — automatic (Py)** — from context7 results. Pass Python function directly in `tools=[]`.
9. **Function calling — manual end-to-end (Py)** — declare `FunctionDeclaration`, parse `response.function_calls[0]`, execute locally, return via `Part.from_function_response(name=..., response=..., id=...)`. The example always shows `id=` set (never omitted) so that pattern is what Claude copies, baking in the 3.x convention.
10. **Function calling — manual end-to-end (JS)** — equivalent shape using `createPartFromFunctionResponse(id, name, response)`.

Each cookbook entry: one-sentence intro, complete code block, ≤2-line "watch out for" note if there's a subtle trap. No padding.

## `evals/trigger-eval.json`

Format matches `skills-source/robustness-audit/evals/trigger-eval.json`:
array of `{query, should_trigger}` objects.

Should-trigger candidates (4):
- "I want to wire up Gemini for image classification in my Python script."
- "Migrate this code from gemini-pro to gemini-3.5-flash."
- "My Gemini function call keeps returning an empty response, finish_reason STOP. What am I doing wrong?"
- "Help me set up structured JSON output with Gemini using Pydantic."

Should-NOT-trigger candidates (4):
- "Compare Gemini, GPT-4, and Claude for code generation tasks." (model comparison, not coding-with-Gemini)
- "How do I authenticate to Google Cloud Storage from a service account?" (non-Gemini Google Cloud)
- "Write OpenAI function-calling code for a weather tool." (other provider)
- "Generate a Python script that reads a CSV." (unrelated)

## Trigger description tuning

The `description` field is what Claude's skill-loader matches against the
current conversation. Tune it to enumerate concrete triggers explicitly,
modeled on `robustness-audit`'s description style. Example draft:

> Use when writing, reviewing, debugging, or migrating Gemini API code —
> especially Gemini 3.x (3 Flash, 3.5 Flash, 3.1 Flash-Lite). Triggers on
> imports of `google.genai` / `@google/genai`, model strings like
> `gemini-3-flash` or `gemini-3.5-flash`, calls to `generate_content` /
> `generateContent`, configuration of `GenerateContentConfig` /
> `ThinkingConfig`, and explicit user requests to wire up Gemini for a
> task (text, image, function calling, structured output, PDF, audio).
> Use proactively when about to write Gemini code so the default patterns
> reflect current 3.x conventions rather than older training-data defaults.
> Do NOT use for general LLM-provider comparisons, OpenAI/Anthropic
> specifics, or non-Gemini Google Cloud (storage, Vertex unrelated to
> Gemini, etc.).

The `allowed-tools` line includes `WebFetch` so the pointer-table URLs
remain useful — future-Claude can fetch the live Google docs page when
the skill defers to it.

## Success criteria

1. A session writing Gemini code from scratch produces code that:
   - imports from `google.genai` (not `google.generativeai`)
   - does NOT set `temperature` / `top_p` / `top_k` for 3.x models
   - uses `thinking_level` if thinking config is needed
   - on manual function calling, includes `id=` on every `FunctionResponse`
2. A session reviewing existing Gemini code spots the same patterns when
   they're wrong.
3. When asked about a use case the skill doesn't cover authoritatively
   (e.g., streaming), the session follows the pointer rather than
   improvising from stale knowledge.
4. The skill description triggers correctly on the should-trigger
   queries and does NOT trigger on the should-not-trigger queries from
   the evals.
5. The build pipeline accepts the skill as a Track 2 (skills-source/)
   skill without changes: drop the graduated folder into
   `skills-source/gemini-api/`, run `./scripts/build-skills.ps1`, verify
   `diff -r skills /tmp/skills-rebuild` is empty, bump plugin version,
   commit.

## Open questions

None blocking. Two minor calls during implementation:

1. **Pointer-table URL stability.** Google's docs URLs are reasonably
   stable, but `ai.google.dev/gemini-api/docs/<topic>` paths sometimes
   reshuffle. We accept the staleness risk; this is what `WebFetch` in
   the allowed-tools list mitigates.
2. **Auto vs manual function-calling emphasis.** Python SDK supports both;
   automatic is strictly easier and has fewer footguns. SKILL.md TL;DR
   recommends automatic; cookbook covers both. If the user expresses a
   different preference during implementation, swap order.

## Out-of-scope considerations (documented for future revisions)

- **Diagnostic skill** for "my Gemini call is misbehaving — debug it"
  was considered (Approach C in brainstorming) but deferred. Build this
  skill first; if a diagnostic split turns out to be needed, it's its
  own skill session.
- **Vertex AI** is mentioned only in passing. If a future project needs
  Vertex-side conventions, a separate `gemini-vertex` skill is the right
  shape — different auth, different deployment context.
- **Live updates** to the skill from Google's docs (e.g., a script that
  refreshes `current-conventions.md` from upstream) is overkill for now.
  Keep manual; revisit if the skill rots within 6 months.
