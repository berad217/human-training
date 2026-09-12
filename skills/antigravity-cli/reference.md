# Antigravity CLI — reference

History and legacy recipes behind `SKILL.md`. Open this when a build behaves
like an older one, or to see which version changed what.

## Headless fixes by version (from `agy changelog`)

| Version | Change |
|---|---|
| 1.0.5 | `--model` flag and `models` subcommand added. |
| 1.0.6 | `--sandbox` honoured in print mode. |
| 1.0.15 | **Windows: print-mode output no longer discarded in non-TTY contexts.** The empty-stdout bug the original skill was built around. |
| 1.1.1 | Print mode no longer exits 0 with empty output on a server-side failure. |
| 1.1.2 | Unresolvable `--model` hard-fails and lists valid ids instead of silently downgrading. |
| 1.1.3 | Headless runs soft-deny tools that need a permission prompt instead of hanging or auto-approving. |
| 1.1.5 | Headless runs honour `settings.json` policies: permissions, file access, sandbox. |
| 1.1.8 | `--output-format text|json|stream-json` for print mode. |
| 1.1.9 | Slash-command and skill expansion in print mode (`-p "/my-skill …"`). |
| 1.1.10 | `--model` and `--effort` were being ignored; fixed. |
| 1.1.12 | `--mode accept-edits|plan` honoured headless; `models`/`agents` gain `--output-format`; read-only slash commands answer non-interactively; the agent settles its own choices instead of stalling on a question. |
| 1.1.15 | `--input-format stream-json` for a persistent driver session. |
| 1.1.18 | Dropped agent stream no longer reported as a clean empty success. |
| 1.1.20 | Exit codes reflect run-level failures only; benign tool denials are not fatal. |
| 1.1.23 | `models`/`agents` no longer hang on an inherited unclosed stdin. |
| 1.1.24 | Piped stdout/stderr no longer hang on exit. |
| 1.1.27 | Denied tool actions are named in a notice and as `denied_actions` in JSON. |
| 1.1.28 | Fatal errors on stderr with a stable `error:` marker; truncation note; plan approval no longer stalls headless runs; `--print-timeout` expiry returns partial output and exits 0 with a warning. |

## JSON output shape (1.1.27)

```json
{"conversation_id":"…","status":"SUCCESS","response":"51\n",
 "duration_seconds":1.09,"num_turns":1,
 "usage":{"input_tokens":13112,"output_tokens":54,"thinking_tokens":52,"cache_read_tokens":0,"total_tokens":13166}}
```

With a denied tool, `response` is empty and the object gains
`"denied_actions":[{"action":"command","display_name":"RunCommand"}]`, and
stderr carries one line explaining which permission headless mode could not
prompt for and how to allow it.

## The four surfaces

| Surface | What it is | Driveable headlessly? |
|---|---|---|
| Antigravity CLI (`agy`) | Go binary, terminal agent | Yes, this skill. |
| Antigravity IDE | Electron app, VS Code fork | No external "run this prompt" entry point. |
| Antigravity 2.0 | Desktop orchestration app | No. |
| Antigravity SDK | Python library | Yes, but that is code, not a CLI. |

The IDE and `agy` are separate installs that share auth through the keyring.
Finding the IDE installed says nothing about whether `agy` is.

Install: `irm https://antigravity.google/cli/install.ps1 | iex` (Windows) or
`curl -fsSL https://antigravity.google/cli/install.sh | bash`. The installer
verifies the binary's SHA512, drops it in `%LOCALAPPDATA%\agy\bin`, registers
PATH via `agy install`, and arms a background self-updater.

## Legacy: transcript recovery (builds before 1.0.15)

Every run writes a JSONL transcript. The final answer of a tool-free run is the
last `PLANNER_RESPONSE` step from `MODEL`:

```bash
"$AGY" -p "What is 17 times 3? Reply with just the number." \
  --print-timeout 60s --log-file ./run.log < /dev/null >/dev/null 2>&1
CID=$(grep -oE 'conversation=[0-9a-f-]+' run.log | head -1 | cut -d= -f2)
TRANSCRIPT="$HOME/.gemini/antigravity-cli/brain/$CID/.system_generated/logs/transcript.jsonl"
grep '"type":"PLANNER_RESPONSE"' "$TRANSCRIPT" | tail -1 \
  | python -c "import sys,json; print(json.loads(sys.stdin.read())['content'])"
```

`--log-file` is the reliable handle on the conversation id; the alternative,
`cache/last_conversations.json`, maps workspace dir to latest id and is racy
across concurrent runs from one directory. On agentic runs the last
`PLANNER_RESPONSE` was frequently empty, which was the second reason to keep
consultant runs tool-free. Still a reasonable fallback in a script: if
`response` comes back empty with no `denied_actions`, look here.

## The 1.0.13 dogfood

Fresh install, silent keyring auth inherited from the IDE, default model
Gemini 3.5 Flash. Empty stdout reproduced across three Git Bash runs;
PowerShell stalled rather than returning empty, so capture there was never
pinned down. The transcript recipe above was verified end to end (17×3 → 51).

The consultant pattern was run two ways against a folder with a planted
spec-vs-code inconsistency. Tool-free with the files inlined: the model found
the inconsistency, quoted both values, zero tool calls, zero access outside
the cwd. Agentic with `--dangerously-skip-permissions`: the run left the cwd,
walked `P:\software_projects\`, matched another project's identically named
task file, and wrote a fabricated report into that unrelated repo. Collateral
was reverted. That incident is why `SKILL.md` ranks the flag last and says to
check the transcript for out-of-tree paths, and why it has not been re-run.

Model list on 2026-09-12, for the record only: Gemini 3.6, 3.7 and 3.8 Flash at
low/medium/high, Gemini 3.1 Pro at low/high, Claude Sonnet 4.6 and Opus 4.6
(thinking), GPT-OSS 120B. Default label that day: "Gemini 3.8 Flash (High)".
Do not copy any of these into a script; run `agy models`.
