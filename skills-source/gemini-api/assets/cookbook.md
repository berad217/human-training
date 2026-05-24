# Gemini API cookbook — current 3.x patterns

Complete, runnable snippets for the most-asked Gemini API use cases. Each
example uses the current SDK (`google-genai` / `@google/genai`) and bakes in
the 3.x conventions from `current-conventions.md`, so it's safe to copy.

Default model in every example: `gemini-3.5-flash`. For latency or cost
sensitivity, swap in `gemini-3.1-flash-lite`.

---

## 1. Text generation with a system instruction

Use a system instruction to set persistent behavior (tone, format, constraints) without putting it in user content every turn. This is the current idiom for "I want deterministic-style output" — not low `temperature`.

### Python

```python
from google import genai
from google.genai import types

client = genai.Client()

response = client.models.generate_content(
    model="gemini-3.5-flash",
    contents="What's the capital of France?",
    config=types.GenerateContentConfig(
        system_instruction="Answer with only the city name, no punctuation, no commentary."
    ),
)
print(response.text)  # -> "Paris"
```

### JavaScript

```typescript
import { GoogleGenAI } from "@google/genai";
const ai = new GoogleGenAI({});

const response = await ai.models.generateContent({
  model: "gemini-3.5-flash",
  contents: "What's the capital of France?",
  config: {
    systemInstruction: "Answer with only the city name, no punctuation, no commentary.",
  },
});
console.log(response.text);
```

**Watch out for:** system instructions go in `config`, not as a `role: "system"` message inside `contents` — reusing the OpenAI Chat Completions mental model here will produce malformed requests.

---

## 2. Translation

A specialization of pattern 1: keep the system instruction parameterless so the same call shape works for any input text.

### Python

```python
text = "Hey, are you down to grab some pizza later? I'm starving!"
target_lang = "German"

response = client.models.generate_content(
    model="gemini-3.5-flash",
    contents=f"Translate the following text to {target_lang}: {text}",
    config=types.GenerateContentConfig(
        system_instruction="Output only the translated text. No explanation, no source, no commentary."
    ),
)
print(response.text)
```

**Watch out for:** putting "translate to X" in the system instruction hardcodes the target language. Keep the system instruction about *format* (output only the translation) and put the language + source text in user content so the call is reusable.

---

## 3. Structured output with Pydantic

Best when you want a typed object on the Python side, not a dict. The response is JSON in `response.text`; you still validate it yourself.

### Python

```python
from pydantic import BaseModel, Field

class ReviewAnalysis(BaseModel):
    aspect: str = Field(description="The feature mentioned (e.g., Price, Comfort, Style, Shipping)")
    summary_quote: str = Field(description="The specific phrase from the review about this aspect")
    sentiment_score: int = Field(description="1 to 5 (1=worst, 5=best)")
    is_return_risk: bool = Field(description="True if the user mentions returning the item")

review = "The boots look amazing and the leather is high quality, but they run way too small. I'm sending them back."

response = client.models.generate_content(
    model="gemini-3.5-flash",
    contents=f"Analyze this customer review: {review}",
    config=types.GenerateContentConfig(
        response_mime_type="application/json",
        response_json_schema=ReviewAnalysis.model_json_schema(),
    ),
)

analysis = ReviewAnalysis.model_validate_json(response.text)
print(analysis.is_return_risk)  # True
```

**Watch out for:** `response.text` is a JSON *string*. You still need `model_validate_json` (or `json.loads` + manual handling) to get a typed object — the SDK doesn't auto-deserialize.

---

## 4. Structured output with a raw JSON schema

For projects without Pydantic, pass a plain JSON schema dict (Python) or object (JS).

### Python

```python
schema = {
    "type": "object",
    "properties": {
        "aspect": {"type": "string"},
        "sentiment_score": {"type": "integer", "minimum": 1, "maximum": 5},
        "is_return_risk": {"type": "boolean"},
    },
    "required": ["aspect", "sentiment_score", "is_return_risk"],
}

response = client.models.generate_content(
    model="gemini-3.5-flash",
    contents="Analyze: The boots run too small, returning them.",
    config=types.GenerateContentConfig(
        response_mime_type="application/json",
        response_json_schema=schema,
    ),
)

import json
data = json.loads(response.text)
```

### JavaScript

```typescript
const schema = {
  type: "object",
  properties: {
    aspect: { type: "string" },
    sentimentScore: { type: "integer", minimum: 1, maximum: 5 },
    isReturnRisk: { type: "boolean" },
  },
  required: ["aspect", "sentimentScore", "isReturnRisk"],
};

const response = await ai.models.generateContent({
  model: "gemini-3.5-flash",
  contents: "Analyze: The boots run too small, returning them.",
  config: {
    responseMimeType: "application/json",
    responseJsonSchema: schema,
  },
});
const data = JSON.parse(response.text);
```

**Watch out for:** large schemas inflate token usage substantially. Keep schemas minimal — the model fills in what it can infer from prompt context, not every field you can imagine.

---

## 5. Image input — inline bytes

For images under ~20 MB used once. For larger or reused images, see section 6.

### Python

```python
with open("photo.jpg", "rb") as f:
    image_bytes = f.read()

response = client.models.generate_content(
    model="gemini-3.5-flash",
    contents=[
        types.Part.from_bytes(data=image_bytes, mime_type="image/jpeg"),
        "What's in this image? List objects visible.",
    ],
)
print(response.text)
```

### JavaScript

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
  contents: [imagePart, "What's in this image? List objects visible."],
});
console.log(response.text);
```

**Watch out for:** mime type must be correct (`image/jpeg`, `image/png`, `image/webp`, `image/heic`, `image/heif`). Wrong mime types fail silently or produce garbage results.

---

## 6. Image input — Files API for large or reused media

Best when the file is over ~20 MB, when you'll reference it across multiple calls, or for video/audio that's typically large. Files **auto-expire after 48 hours** — production code must handle re-upload on 404.

### Python

```python
# Upload once
my_file = client.files.upload(file="long_video.mp4")

# Reference it in one or more generate_content calls
response = client.models.generate_content(
    model="gemini-3.5-flash",
    contents=[my_file, "Summarize what happens in this video."],
)
print(response.text)

# Clean up when done
client.files.delete(name=my_file.name)
```

For typical web/API backends, list/delete patterns matter:

```python
# List active uploads (useful for orphan cleanup)
for f in client.files.list():
    print(f.name, f.create_time, f.expiration_time)
```

**Watch out for:** the 48-hour expiration is silent. A long-running job that uploads a file and references it 50 hours later will fail. Wrap calls in retry logic that re-uploads on `404` / `not found`.

---

## 7. PDF processing — inline bytes

```python
import httpx

doc_data = httpx.get("https://example.com/document.pdf").content

response = client.models.generate_content(
    model="gemini-3.5-flash",
    contents=[
        types.Part.from_bytes(data=doc_data, mime_type="application/pdf"),
        "Summarize this document in three bullet points.",
    ],
)
print(response.text)
```

For PDFs over ~20 MB, use the Files API pattern in section 6 with `mime_type="application/pdf"`.

**Watch out for:** PDF tokens add up fast — a 30-page dense PDF can easily consume 100k+ input tokens. If hitting token limits or paying too much, set `media_resolution_high` lower (see https://ai.google.dev/gemini-api/docs/media-resolution) or extract text upstream with a dedicated library.

---

## 8. Function calling — automatic mode (Python, recommended)

The SDK extracts the schema from your Python function's signature + docstring, handles the model's `function_call` → invoke → return loop internally, and returns the final text. By far the easiest path when it fits.

```python
from google import genai
from google.genai import types

def get_current_weather(city: str) -> str:
    """Returns the current weather in a given city.

    Args:
        city: The city name, e.g. "Boston" or "San Francisco".
    """
    if "boston" in city.lower():
        return "Boston: 15°C, sunny, light wind."
    return f"Weather data for {city} unavailable."

def get_current_time(timezone: str) -> str:
    """Returns the current time in a given IANA timezone.

    Args:
        timezone: IANA timezone string, e.g. "America/New_York".
    """
    from datetime import datetime
    from zoneinfo import ZoneInfo
    return datetime.now(ZoneInfo(timezone)).isoformat()

client = genai.Client()

response = client.models.generate_content(
    model="gemini-3.5-flash",
    contents="What's the weather in Boston, and what time is it in New York?",
    config=types.GenerateContentConfig(
        tools=[get_current_weather, get_current_time],
    ),
)
print(response.text)
```

**Watch out for:** type hints and docstrings ARE the schema the model sees. Missing type hints, missing `Args:` blocks, or vague descriptions degrade function-selection accuracy. Don't skip them.

---

## 9. Function calling — manual end-to-end (Python)

Use when you need to inspect or modify args before executing, do async tool execution, log calls, or otherwise interpose between the model and the tool. Three required pieces: declare → execute → return-with-id.

```python
from google import genai
from google.genai import types

def get_current_weather(city: str) -> dict:
    if "boston" in city.lower():
        return {"city": city, "temp_c": 15, "condition": "sunny"}
    return {"city": city, "temp_c": None, "condition": "unavailable"}

client = genai.Client()

# 1. Declare the tool
weather_decl = types.FunctionDeclaration(
    name="get_current_weather",
    description="Get the current weather for a city.",
    parameters_json_schema={
        "type": "object",
        "properties": {
            "city": {"type": "string", "description": "City name, e.g. 'Boston'."},
        },
        "required": ["city"],
    },
)
weather_tool = types.Tool(function_declarations=[weather_decl])

# 2. First call — model may emit a function_call
user_prompt = "What's the weather in Boston?"
response = client.models.generate_content(
    model="gemini-3.5-flash",
    contents=user_prompt,
    config=types.GenerateContentConfig(tools=[weather_tool]),
)

# 3. If a function call came back, execute it and return the result
if response.function_calls:
    fc = response.function_calls[0]
    result = get_current_weather(**fc.args)

    final = client.models.generate_content(
        model="gemini-3.5-flash",
        contents=[
            types.Content(role="user", parts=[types.Part.from_text(text=user_prompt)]),
            response.candidates[0].content,  # replay model's function_call turn
            types.Content(role="user", parts=[
                types.Part.from_function_response(
                    name=fc.name,
                    response={"result": result},
                    id=fc.id,  # ⚠️ id is NON-NEGOTIABLE on 3.x
                ),
            ]),
        ],
        config=types.GenerateContentConfig(tools=[weather_tool]),
    )
    print(final.text)
else:
    print(response.text)
```

**Watch out for:** (a) **`id=fc.id` is mandatory** — omitting it returns `finish_reason: STOP` with empty content; silent failure. (b) If the model issues multiple parallel function calls (`response.function_calls` has length > 1), you MUST respond to all of them in a single content turn — count mismatch silently fails the same way.

---

## 10. Function calling — manual end-to-end (JavaScript)

JS has no automatic mode — manual is the only path. Same three pieces; same id requirement.

```typescript
import { GoogleGenAI, FunctionDeclaration, createPartFromFunctionResponse } from "@google/genai";

const ai = new GoogleGenAI({});

// 1. Declare the tool
const weatherDecl: FunctionDeclaration = {
  name: "get_current_weather",
  description: "Get the current weather for a city.",
  parametersJsonSchema: {
    type: "object",
    properties: {
      city: { type: "string", description: "City name, e.g. 'Boston'." },
    },
    required: ["city"],
  },
};

function getCurrentWeather(city: string) {
  if (city.toLowerCase().includes("boston")) {
    return { city, tempC: 15, condition: "sunny" };
  }
  return { city, tempC: null, condition: "unavailable" };
}

const userPrompt = "What's the weather in Boston?";

const response = await ai.models.generateContent({
  model: "gemini-3.5-flash",
  contents: userPrompt,
  config: { tools: [{ functionDeclarations: [weatherDecl] }] },
});

if (response.functionCalls && response.functionCalls.length > 0) {
  const fc = response.functionCalls[0];
  const result = getCurrentWeather(fc.args.city as string);

  // ⚠️ createPartFromFunctionResponse REQUIRES id as the first arg
  const responsePart = createPartFromFunctionResponse(fc.id, fc.name, { result });

  const final = await ai.models.generateContent({
    model: "gemini-3.5-flash",
    contents: [
      { role: "user", parts: [{ text: userPrompt }] },
      response.candidates[0].content,
      { role: "user", parts: [responsePart] },
    ],
    config: { tools: [{ functionDeclarations: [weatherDecl] }] },
  });
  console.log(final.text);
} else {
  console.log(response.text);
}
```

**Watch out for:** if you hand-roll the `functionResponse` object literal instead of using `createPartFromFunctionResponse`, it's easy to forget `id`. Use the helper unless you have a specific reason not to.
