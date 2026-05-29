# Ollama skill — research notes

Notes and pointers for drafting `skills-drafts/ollama/SKILL.md`. Nothing
here ships in the plugin; `skills-drafts/` is excluded by the build scripts.

## Portability principle

The published skill must work on any machine, with or without a local
copy of the Ollama docs. Therefore the skill SHALL:

- Cite upstream URLs (`https://github.com/ollama/ollama/blob/main/docs/<file>`
  or `https://raw.githubusercontent.com/ollama/ollama/main/docs/<file>`) as
  the canonical reference. `WebFetch` reaches these on any machine.
- Treat any local copy as an optional speedup via the `OLLAMA_DOCS_DIR`
  environment variable. If set and the path exists, prefer it for
  `Grep`/`Read`. If unset, fall back to `WebFetch`.
- Never hardcode an absolute filesystem path.

## Brad's local clone (this machine)

Sparse-checkout of `github.com/ollama/ollama` (MIT) at
`P:\software_projects\ollama-docs\`. Refresh with:

```powershell
cd P:\software_projects\ollama-docs
git pull
```

To activate the local-docs speedup for this skill, set:

```powershell
# PowerShell session
$env:OLLAMA_DOCS_DIR = "P:\software_projects\ollama-docs\docs"

# Or permanently
[System.Environment]::SetEnvironmentVariable("OLLAMA_DOCS_DIR", "P:\software_projects\ollama-docs\docs", "User")
```

Other machines without the clone: leave `OLLAMA_DOCS_DIR` unset — the
skill will WebFetch.

## File map (high-value docs)

Paths are relative to `<ollama-repo>/docs/`:

- `api.md` — REST API reference. Endpoints and request/response shapes.
- `openapi.yaml` — full OpenAPI schema (machine-readable).
- `modelfile.mdx` — every `PARAMETER` option (temperature, top_p, num_ctx,
  num_predict, repeat_penalty, ...) with defaults and meaning.
- `faq.mdx` — runtime behavior, keep_alive, context length, env vars.
- `capabilities/`
  - `structured-outputs.mdx` — `format` field (legacy `"json"` string and
    JSON Schema object). NOTE: caption_lab playbook documents a vision-
    pipeline bug with the `"json"` string form on `qwen3-vl` (May 2026);
    the JSON Schema form is the upstream-recommended path.
  - `tool-calling.mdx` — tool/function calling conventions.
  - `thinking.mdx` — thinking-model knobs (`think: true/false`; gpt-oss
    uses `"low"|"medium"|"high"`).
  - `vision.mdx` — multimodal payloads.
  - `embeddings.mdx` — `/api/embed` usage.
  - `streaming.mdx` — `stream: true` semantics.
- `api/openai-compatibility.mdx` — `/v1/chat/completions` shim. Lets any
  OpenAI SDK target a local Ollama.
- `api/anthropic-compatibility.mdx` — Anthropic-compatible endpoint.
- `troubleshooting.mdx` — common failure modes from the maintainers.
- `context-length.mdx` — `num_ctx` and how to set it.
- `gpu.mdx` — VRAM and offload behavior.

## Drafting workflow

When writing a section of SKILL.md, open the upstream doc and verify the
facts. Quote URLs as `https://github.com/ollama/ollama/blob/main/docs/<file>`
in the skill so future readers can follow the source.

The May 2026 caption_lab playbook at `../ollama-playbook.md` is the
case-study source for vision-pipeline footguns. Lift specific bugs into
SKILL.md as labeled, dated examples — don't overclaim them as universal.
