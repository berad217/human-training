# gemini-api skill — Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Author the `gemini-api` skill (SKILL.md + two assets + evals), drop it into `skills-drafts/` for iteration, graduate it to `skills-source/`, bump the plugin to 1.3.0, and ship a single commit.

**Architecture:** Track 2 (session-authored) skill, pass-through compiled by both build scripts into `skills/gemini-api/`. SKILL.md is the trigger surface and TL;DR; `assets/current-conventions.md` is the six-footgun reference (Py + JS wrong/right pairs); `assets/cookbook.md` is the use-case examples; `evals/trigger-eval.json` matches the robustness-audit eval shape.

**Tech stack:** Markdown + JSON only. No code to test traditionally; verification is build-pipeline correctness (`diff -r skills /tmp/skills-rebuild` empty) plus structural validation of frontmatter and JSON.

**Source of truth for content:** `skills-drafts/gemini-api/research/whats-new-gemini-3.5.md` (six footguns + 3.5 Flash quickstart) and `skills-drafts/gemini-api/research/gemini-3.1-flash-lite.md` (use cases: translation, transcription, structured output, PDF, model routing). Context7-fetched current docs for `google-genai` (Python) and `@google/genai` (JS) for setup, image input, and function-calling end-to-end. See [docs/specs/2026-05-24-gemini-api-skill-design.md](../specs/2026-05-24-gemini-api-skill-design.md) for the full design.

**Commit cadence:** Two intermediate commits (draft landed in skills-drafts/, then graduation to skills-source/ + version bump) plus the design doc as part of commit 1. No pushes; user pushes when ready.

---

## Task 1: Create skill directory scaffold in skills-drafts/

**Files:**
- Create: `skills-drafts/gemini-api/assets/` (directory)
- Create: `skills-drafts/gemini-api/evals/` (directory)

Existing: `skills-drafts/gemini-api/research/` (don't touch — research stays in drafts).

- [ ] **Step 1: Create the two new subdirectories**

```powershell
New-Item -ItemType Directory -Force -Path "D:\Coding_projects\human-training\skills-drafts\gemini-api\assets" | Out-Null
New-Item -ItemType Directory -Force -Path "D:\Coding_projects\human-training\skills-drafts\gemini-api\evals" | Out-Null
```

- [ ] **Step 2: Verify directory structure**

```powershell
Get-ChildItem "D:\Coding_projects\human-training\skills-drafts\gemini-api" -Directory | Select-Object Name
```

Expected output: three directories — `assets`, `evals`, `research`.

---

## Task 2: Draft SKILL.md

**Files:**
- Create: `skills-drafts/gemini-api/SKILL.md`

**Reference for content:** design doc section "SKILL.md structure (the spine)". 7 sections, ~150-180 lines total.

- [ ] **Step 1: Write the file with the seven sections**

Frontmatter:
```yaml
---
name: gemini-api
description: Use when writing, reviewing, debugging, or migrating Gemini API code — especially Gemini 3.x (3 Flash, 3.5 Flash, 3.1 Flash-Lite). Triggers on imports of `google.genai` / `@google/genai`, model strings like `gemini-3-flash` or `gemini-3.5-flash`, calls to `generate_content` / `generateContent`, configuration of `GenerateContentConfig` / `ThinkingConfig`, and explicit user requests to wire up Gemini for a task (text, image, function calling, structured output, PDF, audio). Use proactively when about to write Gemini code so the default patterns reflect current 3.x conventions rather than older training-data defaults. Do NOT use for general LLM-provider comparisons, OpenAI/Anthropic specifics, or non-Gemini Google Cloud (storage, Vertex unrelated to Gemini, etc.).
allowed-tools: [Read, Write, Edit, Grep, Glob, Bash, WebFetch]
---
```

Section 1: `# Gemini API (3.x)` with a one-paragraph framing that the skill exists because Gemini 3.x is recent and Claude's training-data defaults are stale.

Section 2: `## TL;DR — load these five facts before writing any Gemini code` — bulleted, in this order:
1. Use the `google-genai` (Python) or `@google/genai` (JavaScript) package. `google-generativeai` is the deprecated Python SDK; old code/examples using it will mislead.
2. On Gemini 3.x: **don't set `temperature` / `top_p` / `top_k`**. Google explicitly recommends defaults; reasoning is calibrated against them. For deterministic-style output, write a system instruction.
3. Use `thinking_level` enum (`"minimal"` / `"low"` / `"medium"` / `"high"`), **not** the deprecated `thinking_budget` integer. Default in 3.5 is `"medium"` (was `"high"` in 3 Flash Preview — code calibrated against the old default may regress).
4. For function calling: prefer Python automatic mode (pass the Python function directly in `tools=[]`; the SDK extracts schema from the signature and docstring). If you use manual mode, **every** `FunctionResponse` MUST include `id=` matching the original `FunctionCall.id` — omitting it causes `finish_reason: STOP` with empty content (silent failure).
5. Current model IDs and quick "which to pick" — see model-reference section in `assets/current-conventions.md`. Don't hardcode `gemini-pro` or `gemini-1.5-flash` in new code; those are pre-3.x.

Section 3: `## Setup and first call` — install commands for both languages, client construction, first call, system_instruction example. Use the patterns context7 surfaced (e.g., `client = genai.Client()` reads from env var; `const ai = new GoogleGenAI({apiKey: process.env.GEMINI_API_KEY})` for JS). Add a note on env var name (`GEMINI_API_KEY` is standard, sometimes `GOOGLE_API_KEY`).

Section 4: `## Image input` — short overview, then point to `assets/cookbook.md` entries 5 and 6. Inline the minimal pattern for both Py (`types.Part.from_bytes(data=image_bytes, mime_type='image/jpeg')`) and JS (`{ inlineData: { data: base64String, mimeType: '...' } }`). Decision rule: inline bytes for < 20 MB / single-use; Files API for ≥ 20 MB or multi-call reuse; Files API uploads expire in 48 hours.

Section 5: `## Function calling` — recommend Python automatic mode (1 paragraph + 8-line snippet). For manual mode and the JS equivalent (which has no automatic mode), point to `assets/cookbook.md` entries 8-10. Highlight the `id=` invariant in bold.

Section 6: `## For everything else — pointer table` — markdown table with columns `Topic | Where to look`. Rows:
- Streaming → `https://ai.google.dev/gemini-api/docs/text-generation#streaming`
- Async → `https://ai.google.dev/gemini-api/docs/text-generation` (SDK supports `client.aio.models.*`)
- Multi-turn chat → `https://ai.google.dev/gemini-api/docs/chat`
- Safety filters / `finish_reason` → `https://ai.google.dev/gemini-api/docs/safety-guidance`
- Structured output (beyond Pydantic basics) → `https://ai.google.dev/gemini-api/docs/structured-output`
- Caching → `https://ai.google.dev/gemini-api/docs/caching`
- count_tokens → `https://ai.google.dev/gemini-api/docs/tokens`
- File API lifecycle → `https://ai.google.dev/gemini-api/docs/files`
- Vertex AI vs Gemini Developer API → `https://ai.google.dev/gemini-api/docs/migrate-to-cloud`
- Pricing → `https://ai.google.dev/gemini-api/docs/pricing`
- Built-in tools (Search, URL context, code execution) → `https://ai.google.dev/gemini-api/docs/tool-combination`

Section 7: `## Source of truth` — two lines:
> This skill owns the **conventions and footguns** (sections 2 and `assets/current-conventions.md`). Google's official docs own the **use-case how-to** — fetch fresh via `WebFetch` if you need anything not in the pointer table.

Reference URL: `https://ai.google.dev/gemini-api/docs`.

- [ ] **Step 2: Verify the frontmatter parses and `name:` matches the directory**

```powershell
$content = Get-Content "D:\Coding_projects\human-training\skills-drafts\gemini-api\SKILL.md" -Raw
$frontmatterMatch = $content -match '(?s)^---\s*\n(.*?)\n---'
if (-not $frontmatterMatch) { Write-Error "Frontmatter not parseable" }
if ($content -notmatch 'name:\s*gemini-api') { Write-Error "name does not match directory" }
Write-Host "OK: frontmatter parses, name matches"
```

Expected: `OK: frontmatter parses, name matches`.

- [ ] **Step 3: Verify all seven sections are present**

```powershell
$content = Get-Content "D:\Coding_projects\human-training\skills-drafts\gemini-api\SKILL.md" -Raw
$required = @('# Gemini API', '## TL;DR', '## Setup', '## Image input', '## Function calling', '## For everything else', '## Source of truth')
foreach ($h in $required) {
    if ($content -notmatch [regex]::Escape($h)) { Write-Error "Missing section: $h" }
}
Write-Host "OK: all seven sections present"
```

Expected: `OK: all seven sections present`.

---

## Task 3: Draft `assets/current-conventions.md`

**Files:**
- Create: `skills-drafts/gemini-api/assets/current-conventions.md`

**Reference for content:** design doc section "`assets/current-conventions.md` structure". Six footgun sections, each ~30-40 lines, in this order: sampling-params → thinking_budget → function-call id matching → multimodal-in-function-response → inline-instructions-placement → thought-preservation.

- [ ] **Step 1: Write the file**

Header:
```markdown
# Current Gemini 3.x conventions — wrong-way / right-way

These six patterns are documented in Google's 3.5 Flash migration guide. Each
one bites because either (a) older Gemini versions/other LLM APIs used the
opposite convention, or (b) it's a silent-failure mode that wouldn't surface
during casual testing. Code generated from stale training data will get these
wrong by default.
```

Then six `## Footgun N: <name>` sections. Each section:
- `**Why it bites:** ...` one line.
- `### Python` — wrong-way code block (~5-10 lines) → right-way code block (~5-10 lines).
- `### JavaScript` — same structure if the shape differs meaningfully; one-line note "Same shape, just camelCase keys — `topP`, `topK`, `thinkingConfig.thinkingLevel`" otherwise.
- `**Look for:** <pattern>` — short hint for code review.

Concrete content per footgun:

**Footgun 1 — Sampling parameters on Gemini 3.x.**
Why: Old habit from earlier Gemini and other providers (OpenAI, Anthropic). On Gemini 3.x, Google explicitly recommends defaults; the model's reasoning is calibrated against them. Setting these actively hurts.
Wrong (Py): `config = types.GenerateContentConfig(temperature=0.7, top_p=0.9, top_k=40)`.
Right (Py): `config = types.GenerateContentConfig()` and add a system instruction if deterministic-style output is needed.
JS: same, with `temperature`, `topP`, `topK` keys in the `config` object.
Look for: any of `temperature`, `top_p`/`topP`, `top_k`/`topK` in a `GenerateContentConfig` for a `gemini-3*` model.

**Footgun 2 — `thinking_budget` (deprecated) instead of `thinking_level` enum.**
Why: Numeric budget was the old API; replaced by an enum (`minimal` / `low` / `medium` / `high`). Default changed from `high` to `medium` in 3.5 Flash.
Wrong (Py): `thinking_config=types.ThinkingConfig(thinking_budget=7500)`.
Right (Py): `thinking_config=types.ThinkingConfig(thinking_level="medium")`.
JS: `thinkingConfig: { thinkingLevel: "HIGH" }` — note the **uppercase** values in JS where Python uses lowercase. This is its own footgun.
Look for: any `thinking_budget` / `thinkingBudget` reference; any lowercase `thinkingLevel` value in JS.

**Footgun 3 — Function-call `id` / `name` / count strict matching.**
Why: The Interactions API errors on mismatch; the GenerateContent API does NOT — it returns `finish_reason: STOP` with empty content. Silent. The Python SDK's manual-function-calling examples in current docs sometimes omit `id=` — copying them will break.
Wrong (Py): `Part.from_function_response(name=tool_call.name, response={'result': result})` — no `id`.
Right (Py): `Part.from_function_response(name=tool_call.name, response={'result': result}, id=tool_call.id)`.
JS: use `createPartFromFunctionResponse(id, name, response)` — id is the first positional arg, required by signature.
Look for: any `from_function_response` / `functionResponse` construction without `id`. Also: count mismatch (model issued 3 function calls, code returns 2 responses).

**Footgun 4 — Multimodal content INSIDE the function response, not alongside it.**
Why: Common pattern: a function returns an image, and the caller sends the image back to the model as a separate user-role multimodal part. The 3.x model expects the image bytes *inside* the `FunctionResponse.response` dict.
Wrong: separate user-role message with the image after the function response.
Right (Py): include the image bytes/base64 as a key in the response dict: `Part.from_function_response(name=..., response={"result": "...", "image": base64_image_data}, id=...)`.
JS: same shape — `response: { result: "...", image: base64ImageData }`.
Look for: function results that produce media, followed by a separate user-role multimodal part.

**Footgun 5 — Inline instructions in function responses as separate Parts.**
Why: Common pattern: append a hint or instruction as a separate `Part` after the `FunctionResponse`. 3.x interprets that as a new turn; quality drops, "thought leakage" can occur.
Wrong: two parts — `[FunctionResponse(...), Part.from_text("Now also do X")]`.
Right (Py): `result_text = f"{json.dumps(result)}\n\n<inline instructions here>"`, then `Part.from_function_response(name=..., response={"result": result_text}, id=...)`.
JS: same shape — concat into the response text.
Look for: any `Part.from_text` / `{ text: ... }` immediately following a `FunctionResponse` in the same content message.

**Footgun 6 — Reconstructing conversation history strips thought signatures.**
Why: 3.5 Flash preserves intermediate reasoning across turns when thought signatures travel with conversation history. If you manually rebuild `contents` from just `{role, text}` pairs (e.g., copying from your own DB), the signatures are gone and you lose the preserved-thinking benefit. SDKs handle this when you replay `response.candidates[0].content` directly.
Wrong: `contents=[{"role": "user", "parts": [{"text": user_msg}]}, {"role": "model", "parts": [{"text": prev_model_text}]}]` — model text only, no signature.
Right: replay the model's previous `Content` object verbatim: `contents=[user_prev, response_prev.candidates[0].content, user_next]`.
Look for: code that reconstructs history from a database of message text rather than persisting the SDK's `Content` objects.

Tail section — model reference table:

```markdown
## Current Gemini 3.x models

| Model | Model code | Input | Output | Knowledge cutoff | When to pick |
|---|---|---|---|---|---|
| Gemini 3.5 Flash | `gemini-3.5-flash` | 1M tokens | 65k tokens | Jan 2025 | Default for production agentic and coding workloads. GA. |
| Gemini 3.1 Flash-Lite | `gemini-3.1-flash-lite` | 1M tokens | 65k tokens | Jan 2025 | High-volume, latency-sensitive, cost-sensitive workloads (translation, simple extraction, classifier-as-router). |
| Gemini 3 Flash Preview | `gemini-3-flash-preview` | (legacy) | (legacy) | — | Only if you need Computer Use, which is not yet supported on 3.5. |

Pricing changes between Flash and Flash-Lite by an order of magnitude — verify before scaling.
```

- [ ] **Step 2: Verify section count and structure**

```powershell
$content = Get-Content "D:\Coding_projects\human-training\skills-drafts\gemini-api\assets\current-conventions.md" -Raw
$footgunCount = ([regex]::Matches($content, '## Footgun \d')).Count
if ($footgunCount -ne 6) { Write-Error "Expected 6 footgun sections, found $footgunCount" }
if ($content -notmatch '## Current Gemini 3.x models') { Write-Error "Missing model reference table" }
Write-Host "OK: 6 footguns + model table"
```

Expected: `OK: 6 footguns + model table`.

---

## Task 4: Draft `assets/cookbook.md`

**Files:**
- Create: `skills-drafts/gemini-api/assets/cookbook.md`

**Reference for content:** design doc section "`assets/cookbook.md` structure". Ten use cases, each ~25-35 lines with one-sentence intro + complete code block + ≤2-line watch-out.

- [ ] **Step 1: Write the file**

Header:
```markdown
# Gemini API cookbook — current 3.x patterns

Complete, runnable snippets for the most-asked Gemini API use cases. Each
example uses the current SDK (`google-genai` / `@google/genai`) and bakes in
the 3.x conventions from `current-conventions.md` so it's safe to copy.

Default model in every example: `gemini-3.5-flash`. For latency/cost
sensitivity, swap in `gemini-3.1-flash-lite`.
```

Ten sections, in order:

1. **Text generation with a system instruction** — Py + JS. Show `config=GenerateContentConfig(system_instruction="...")` pattern. Watch-out: system instruction is configured separately from `contents`, not as a `role: "system"` message like OpenAI.

2. **Translation** — Py only (research has it). System_instruction constrains output to "only the translated text"; then user content is the source text + target language. Watch-out: don't ask for "translate to X" in the system instruction — put the source text in user content so the model can be reused for different inputs.

3. **Structured output with Pydantic** — Py only. `response_mime_type="application/json"` + `response_json_schema=MyModel.model_json_schema()`. Watch-out: the response is JSON in `response.text` — you still need to `MyModel.model_validate_json(response.text)` to get a typed object.

4. **Structured output with a raw JSON schema** — Py + JS (for projects without Pydantic). `response_mime_type="application/json"` + `response_json_schema={...}` (Py) or `responseMimeType` + `responseJsonSchema` (JS). Watch-out: keep schemas small; large schemas inflate token usage.

5. **Image input — inline bytes** — Py + JS.
   - Py: `with open(path, 'rb') as f: image_bytes = f.read()` → `types.Part.from_bytes(data=image_bytes, mime_type='image/jpeg')`.
   - JS: `Buffer.from(fs.readFileSync(path)).toString("base64")` → `{ inlineData: { data: base64, mimeType: 'image/jpeg' } }`.
   - Watch-out: this is best under ~20 MB. For larger files or images reused across calls, use the Files API (next entry).

6. **Image input — Files API for large or reused media** — Py. `my_file = client.files.upload(file='video.mp4')` → pass `my_file` in `contents`. Cleanup: `client.files.delete(name=my_file.name)`. Watch-out: uploads auto-expire in 48 hours; production code should handle re-upload on 404.

7. **PDF processing — inline** — Py. `types.Part.from_bytes(data=pdf_bytes, mime_type='application/pdf')`. Watch-out: PDF tokens can be heavy; for very dense documents consider `media_resolution` config (see Google's media-resolution docs).

8. **Function calling — automatic mode (Py)** — recommended path. Just pass a Python function in `tools=[]`; the SDK extracts the schema from the signature + docstring and handles the call/response loop. Watch-out: type hints and docstrings are not optional — they ARE the schema the model sees.

9. **Function calling — manual end-to-end (Py)** — for cases where you need to inspect/modify args before executing, or where automatic mode isn't appropriate (e.g., async tool execution). Show: `FunctionDeclaration` with `parameters_json_schema`, wrapped in `Tool(function_declarations=[fn])`, passed in `config.tools=[tool]`. Read `response.function_calls[0]`, execute locally, return via `Part.from_function_response(name=fc.name, response={"result": result}, id=fc.id)`. **The `id=fc.id` is non-negotiable.** Watch-out: if the model issues multiple parallel function calls, you must respond to all of them in a single content turn — count mismatch silently fails.

10. **Function calling — manual end-to-end (JS)** — equivalent for JavaScript. `FunctionDeclaration` with `parametersJsonSchema`, passed via `config.tools: [{ functionDeclarations: [decl] }]`. Read `response.functionCalls`, execute, return via `createPartFromFunctionResponse(toolCall.id, toolCall.name, { result })`. Watch-out: JS has no automatic mode — manual is the only path.

Each section format:
```markdown
## N. <Title>

<one-sentence intro>

### Python
\`\`\`python
<complete code block>
\`\`\`

### JavaScript
\`\`\`javascript
<complete code block>
\`\`\`

**Watch out for:** <≤2-line subtle trap, if any>
```

(JS block omitted where the section is Python-only.)

- [ ] **Step 2: Verify section count**

```powershell
$content = Get-Content "D:\Coding_projects\human-training\skills-drafts\gemini-api\assets\cookbook.md" -Raw
$secCount = ([regex]::Matches($content, '## \d+\.')).Count
if ($secCount -ne 10) { Write-Error "Expected 10 cookbook sections, found $secCount" }
Write-Host "OK: 10 cookbook sections present"
```

Expected: `OK: 10 cookbook sections present`.

---

## Task 5: Draft `evals/trigger-eval.json`

**Files:**
- Create: `skills-drafts/gemini-api/evals/trigger-eval.json`

**Reference for content:** design doc section "`evals/trigger-eval.json`". 4 should-trigger + 4 should-NOT-trigger entries, format matches `skills-source/robustness-audit/evals/trigger-eval.json`.

- [ ] **Step 1: Write the JSON file**

```json
[
  {
    "query": "I want to wire up Gemini for image classification in my Python script. The model needs to read a JPEG from disk and return a category label.",
    "should_trigger": true
  },
  {
    "query": "Migrate this code from gemini-pro to gemini-3.5-flash. Right now it sets temperature=0.7 and uses thinking_budget=4000.",
    "should_trigger": true
  },
  {
    "query": "My Gemini function call keeps returning an empty response with finish_reason STOP. The model is supposed to call my get_weather function, but nothing happens. What am I doing wrong?",
    "should_trigger": true
  },
  {
    "query": "Help me set up structured JSON output with Gemini using a Pydantic model. I need to extract product names and prices from a review.",
    "should_trigger": true
  },
  {
    "query": "Compare Gemini, GPT-4, and Claude for code generation tasks. Which one is best for refactoring?",
    "should_trigger": false
  },
  {
    "query": "How do I authenticate to Google Cloud Storage from a Python service account? I need to read objects from a bucket.",
    "should_trigger": false
  },
  {
    "query": "Write OpenAI function-calling code for a weather tool. Use the chat completions API with the tools parameter.",
    "should_trigger": false
  },
  {
    "query": "Generate a Python script that reads a CSV file and computes the mean of one of the columns. No AI needed.",
    "should_trigger": false
  }
]
```

- [ ] **Step 2: Verify JSON parses and has the expected shape**

```powershell
$json = Get-Content "D:\Coding_projects\human-training\skills-drafts\gemini-api\evals\trigger-eval.json" -Raw | ConvertFrom-Json
if ($json.Count -ne 8) { Write-Error "Expected 8 eval entries, found $($json.Count)" }
$trueCount = ($json | Where-Object { $_.should_trigger -eq $true }).Count
$falseCount = ($json | Where-Object { $_.should_trigger -eq $false }).Count
if ($trueCount -ne 4 -or $falseCount -ne 4) { Write-Error "Expected 4+4 split, got $trueCount+$falseCount" }
Write-Host "OK: 4 should-trigger + 4 should-not-trigger entries"
```

Expected: `OK: 4 should-trigger + 4 should-not-trigger entries`.

---

## Task 6: Intermediate commit — draft landed in skills-drafts/

- [ ] **Step 1: Stage the draft files + the design and plan docs**

```bash
git add skills-drafts/gemini-api/SKILL.md \
        skills-drafts/gemini-api/assets/current-conventions.md \
        skills-drafts/gemini-api/assets/cookbook.md \
        skills-drafts/gemini-api/evals/trigger-eval.json \
        docs/specs/2026-05-24-gemini-api-skill-design.md \
        docs/plans/2026-05-24-gemini-api-skill.md
```

- [ ] **Step 2: Commit**

```bash
git commit -m "$(cat <<'EOF'
Draft gemini-api skill in skills-drafts/

Skill body (SKILL.md), two assets (current-conventions for the six 3.x
footguns; cookbook for ten common use cases), and a trigger eval.

Spec and plan committed alongside under docs/specs/ and docs/plans/.

Skill is not yet graduated to skills-source/ — will move and build in a
follow-up commit after iteration in the drafts workspace.

Co-Authored-By: Claude Opus 4.7 (1M context) <noreply@anthropic.com>
EOF
)"
```

- [ ] **Step 3: Verify commit landed**

```bash
git log -1 --stat
```

Expected: commit message visible; 6 files in the stat list.

---

## Task 7: Graduate to skills-source/

**Files:**
- Move: `skills-drafts/gemini-api/SKILL.md` → `skills-source/gemini-api/SKILL.md`
- Move: `skills-drafts/gemini-api/assets/` → `skills-source/gemini-api/assets/`
- Move: `skills-drafts/gemini-api/evals/` → `skills-source/gemini-api/evals/`
- Leave: `skills-drafts/gemini-api/research/` (does NOT graduate; stays in drafts)

- [ ] **Step 1: Create the destination directory**

```powershell
New-Item -ItemType Directory -Force -Path "D:\Coding_projects\human-training\skills-source\gemini-api" | Out-Null
```

- [ ] **Step 2: git-mv the three skill artifacts**

Using `git mv` so history is preserved:

```bash
cd "D:/Coding_projects/human-training"
git mv skills-drafts/gemini-api/SKILL.md skills-source/gemini-api/SKILL.md
git mv skills-drafts/gemini-api/assets skills-source/gemini-api/assets
git mv skills-drafts/gemini-api/evals skills-source/gemini-api/evals
```

- [ ] **Step 3: Verify the move**

```powershell
Get-ChildItem "D:\Coding_projects\human-training\skills-source\gemini-api" -Recurse | Select-Object FullName
Get-ChildItem "D:\Coding_projects\human-training\skills-drafts\gemini-api" -Recurse | Select-Object FullName
```

Expected: `skills-source/gemini-api/` has SKILL.md, assets/{current-conventions.md, cookbook.md}, evals/trigger-eval.json. `skills-drafts/gemini-api/` has only `research/` with the two `.md` files.

---

## Task 8: Run build + verify CI invariant

- [ ] **Step 1: Run the PowerShell build**

```powershell
& "D:\Coding_projects\human-training\scripts\build-skills.ps1"
```

Expected output ends with:
```
  Generated skills: 5
  Session-authored skills: 2
```

And `skills/gemini-api/` should now exist with the same structure as `skills-source/gemini-api/`.

- [ ] **Step 2: Run the sh build into a temp dir and diff against the committed skills/**

```bash
cd "D:/Coding_projects/human-training"
rm -rf /tmp/skills-rebuild
OUTPUT_DIR=/tmp/skills-rebuild bash scripts/build-skills.sh > /dev/null 2>&1
diff -r skills /tmp/skills-rebuild
echo "Diff exit code: $?"
```

Expected: no diff output, exit code 0.

If diff output is non-empty, fix the source files in `skills-source/gemini-api/` so both builders produce identical output. Common cause: line-ending differences in the JSON file or trailing whitespace.

- [ ] **Step 3: Verify SKILL.md ended up at the expected output location**

```powershell
Test-Path "D:\Coding_projects\human-training\skills\gemini-api\SKILL.md"
Test-Path "D:\Coding_projects\human-training\skills\gemini-api\assets\current-conventions.md"
Test-Path "D:\Coding_projects\human-training\skills\gemini-api\assets\cookbook.md"
Test-Path "D:\Coding_projects\human-training\skills\gemini-api\evals\trigger-eval.json"
```

Expected: all four return `True`.

---

## Task 9: Bump plugin version

**Files:**
- Modify: `.claude-plugin/plugin.json`

- [ ] **Step 1: Bump 1.2.0 → 1.3.0 (minor: new skill = feature add)**

Read [.claude-plugin/plugin.json](.claude-plugin/plugin.json), then change:
```json
"version": "1.2.0",
```
to:
```json
"version": "1.3.0",
```

Also update the description if it still says "plus session-authored skills like robustness-audit" — change to "plus session-authored skills (robustness-audit, gemini-api)."

- [ ] **Step 2: Verify the version**

```powershell
Get-Content "D:\Coding_projects\human-training\.claude-plugin\plugin.json" | Select-String '"version"'
```

Expected: `"version": "1.3.0",`

---

## Task 10: Update README skills table

**Files:**
- Modify: `README.md` (the "Available Skills" table)

- [ ] **Step 1: Add a row for `gemini-api`**

Find the table at `## Available Skills (Claude Code)` and add this row (after the `robustness-audit` row):

```markdown
| **gemini-api** | skills-source/ | Current-Gemini-API working reference | Writing/reviewing/migrating Gemini 3.x code; preventing the training-data-default stumble when wiring up Gemini for text/image/function calling |
```

- [ ] **Step 2: Verify the row landed**

```powershell
Get-Content "D:\Coding_projects\human-training\README.md" -Raw | Select-String 'gemini-api'
```

Expected: at least one match (the new row).

---

## Task 11: Final build verification + commit

- [ ] **Step 1: Run the round-trip verification one last time**

```bash
cd "D:/Coding_projects/human-training"
rm -rf /tmp/skills-rebuild
OUTPUT_DIR=/tmp/skills-rebuild bash scripts/build-skills.sh > /dev/null 2>&1
diff -r skills /tmp/skills-rebuild && echo "BUILD OK"
```

Expected: `BUILD OK` (no diff output, exit code 0).

- [ ] **Step 2: Show staged changes**

```bash
git status --short
```

Expected mix of staged moves (from Task 7's `git mv`) and modifications (plugin.json, README.md, possibly skills/).

- [ ] **Step 3: Stage all skill-related changes**

```bash
git add skills-source/gemini-api/ \
        skills-drafts/gemini-api/ \
        skills/ \
        .claude-plugin/plugin.json \
        README.md
```

- [ ] **Step 4: Commit**

```bash
git commit -m "$(cat <<'EOF'
Graduate gemini-api skill to skills-source/, ship in plugin 1.3.0

Moves SKILL.md, assets/, and evals/ from skills-drafts/ to skills-source/
(research/ stays in drafts as reference material; does not ship). Rebuild
populates skills/gemini-api/.

Plugin version 1.2.0 -> 1.3.0; README skills table updated.

Co-Authored-By: Claude Opus 4.7 (1M context) <noreply@anthropic.com>
EOF
)"
```

- [ ] **Step 5: Confirm clean working tree**

```bash
git status
```

Expected: `nothing to commit, working tree clean` (or only untracked files unrelated to this work).

---

## Self-review checklist (planner running before handoff)

1. **Spec coverage** — every section of the design doc maps to a task:
   - SKILL.md spine → Task 2
   - current-conventions.md → Task 3
   - cookbook.md → Task 4
   - evals → Task 5
   - Graduation → Task 7
   - Build + CI invariant → Task 8
   - Version bump → Task 9
   - README update → Task 10
   - Pointer-table URLs are spelled out in Task 2 (Section 6).

2. **Placeholder scan** — no TBDs, no "implement later", no "similar to Task N." Every content step lists exact content or references a specific design-doc section that does.

3. **Type / name consistency** — all paths use `gemini-api` (matches the dir name); all model strings use `gemini-3.5-flash` / `gemini-3.1-flash-lite` / `gemini-3-flash-preview` consistently across tasks; all references to `Part.from_function_response` use that exact spelling.

4. **Pointer-table URLs** — listed once in Task 2 Section 6. Treated as a known minor staleness risk; mitigated by including `WebFetch` in `allowed-tools`.

5. **Test analogue** — for markdown artifacts, verification is structural (sections present, JSON parses, build diff empty). Tasks 2/3/4/5 each include a verification step; Tasks 8 and 11 each include the round-trip build check.

---

## Execution handoff

Plan complete and saved to `docs/plans/2026-05-24-gemini-api-skill.md`. Two execution options:

**1. Subagent-Driven (recommended)** — Dispatch a fresh subagent per task, review between tasks, fast iteration. Best when content tasks (2, 3, 4) might surface issues during drafting; each can be inspected before moving on.

**2. Inline Execution** — Execute tasks in this session using executing-plans, batch execution with checkpoints. Best when you want minimal context-switching and trust the plan to need few adjustments.

Which approach?
