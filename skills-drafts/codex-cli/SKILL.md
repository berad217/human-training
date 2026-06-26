---
name: codex-cli
description: Use when driving OpenAI's Codex CLI non-interactively / headlessly — `codex exec`, running Codex from a script or another agent, capturing its output to a file, or automating a Codex call. Triggers include "call/run codex from the command line", "codex headless / non-interactive", "codex exec", "is there a codex -p", "automate codex", "have Claude/the agent run Codex", "codex hangs / stuck with no output", "capture codex output", "codex in CI". Covers install + auth, the stdin-block footgun (`< /dev/null`), stdout-vs-stderr capture, sandbox/approval safety, model & reasoning-effort flags, and troubleshooting. Do NOT use for the interactive Codex TUI, the Codex desktop GUI app, or for the OpenAI cloud/Responses API or non-Codex tools.
allowed-tools: [Bash, Read, Write, Edit, Grep, Glob, WebFetch]
---

# Codex CLI — headless / non-interactive

Drive OpenAI's Codex CLI from a script or another agent: fire a prompt, capture the answer, keep it safe and
context-lean. `codex exec` is the non-interactive entry point (alias `codex e`) — it runs the agent to
completion and exits, no TUI.

**Verified against `codex-cli 0.142.2`.** Flags drift between versions — confirm with `codex exec --help` on the
target machine. The honesty line matters because this is a skill another agent will trust: re-check, don't assume.

## TL;DR — the rules that keep headless Codex from biting you

1. **Always close stdin.** Append `< /dev/null` (bash) or `'' |` (PowerShell). The #1 footgun — without it the
   call can hang forever (it's blocked *reading stdin*, not working). See [§3](#3-the-stdin-trap).
2. **Capture the answer with `-o FILE`.** stdout carries **only the final message**; stderr carries the banner,
   progress, and reasoning. `-o FILE` writes just the final message — the clean, context-lean capture. Avoid
   `--json` unless you actually want the whole event stream.
3. **The CLI is not the desktop app.** The Codex GUI app can't be driven externally. Install the standalone CLI
   (`npm i -g @openai/codex`); it reuses the app's stored login.
4. **`--ignore-user-config` for a clean, reproducible reader.** Skips `config.toml` (auth still works) so a heavy
   local setup (MCP servers, custom tools) can't perturb or stall the run.
5. **Pick the sandbox deliberately.** `-s read-only` for "read & analyze", `-s workspace-write` only when it
   should edit files. `codex exec` never prompts mid-run.

The canonical call:

```bash
codex exec --ignore-user-config -s read-only \
  -o ANSWER.md \
  -c 'model_reasoning_effort="high"' \
  "Your full prompt here." \
  < /dev/null
```

## 1. The CLI is not the desktop app

`codex exec` is a **command-line** feature. The **desktop app** has no external "run this prompt" entry point —
you can attach *reactive* [hooks](#hooks-are-reactive-not-a-launcher) to it, but a hook fires *when* Codex does
something; it cannot *start* a run. To drive Codex from a script or agent you need the **standalone CLI**,
installed separately from the app. They coexist; both read `$CODEX_HOME` (default `~/.codex`), so the CLI reuses
the app's login.

## 2. Install & auth

```bash
npm i -g @openai/codex      # the `codex` binary (a native build shipped via npm)
codex --version             # confirm
codex login                 # if not already authenticated
codex doctor                # diagnose install / config / auth / runtime health
```

- **Auth reuse:** `codex exec` uses `$CODEX_HOME/auth.json` by default. If the desktop app is logged in, the CLI
  picks it up — no separate login.
- **API-key auth (CI / unattended):** `CODEX_API_KEY=<key> codex exec ...` (env var, per the docs — not a flag).
- **Windows PATH gotcha:** npm's global bin (`%APPDATA%\npm`) is often missing from a non-interactive shell's
  PATH. If `codex` "isn't found," call it by full path (`"$HOME/AppData/Roaming/npm/codex"`) or add that dir.

## 3. The stdin trap

`codex exec`'s prompt argument is documented as:

> *"If not provided as an argument (or if `-` is used), instructions are read from **stdin**. If stdin is piped
> and a prompt is also provided, stdin is appended as a `<stdin>` block."*

So when you pass a prompt **and** stdin is an open pipe with no data and no EOF (the normal situation in
automation), Codex blocks **reading stdin**, waiting for an EOF that never arrives. It looks like a hang; it's a
parked read.

**Fix — hand it immediate EOF:**

```bash
codex exec "prompt" < /dev/null      # bash / Git Bash / WSL — the verified form
```

PowerShell has no `<` redirection — pipe empty input, or run Codex from a bash shell:

```powershell
'' | codex exec "prompt"
```

Using stdin *on purpose* is fine: `echo "long prompt" | codex exec` or `codex exec - < prompt.txt`. The trap
only springs when stdin is left open unintentionally.

## 4. Capturing output (context-lean)

stdout = the agent's **final message only**. stderr = banner, progress, tool activity, reasoning summaries.
That split is what makes Codex scriptable.

| You want | Use |
|---|---|
| Just the final message, in a file | `-o FILE` / `--output-last-message FILE` |
| The full event stream (reasoning, tool calls) as JSONL | `--json` |
| The final message constrained to a JSON shape | `--output-schema SCHEMA.json` |

For "ask a question, read the answer," **`-o FILE` is the right tool** — the file holds exactly the final
message, so a downstream reader pulls in only that. For machine-parseable output, pair `--output-schema` with a
JSON Schema file. Reserve `--json` for when you genuinely need the event log; it's the opposite of lean.

## 5. Safety: sandbox & approval

`codex exec` can run shell commands and edit files. Govern it with the sandbox flag:

| `-s, --sandbox` | The agent may |
|---|---|
| `read-only` | Read the workspace; **no writes, no side-effecting commands**. Right for analysis. |
| `workspace-write` | Read + write within the working dir (and `--add-dir` extras). Right when it must edit. |
| `danger-full-access` | No sandbox — only inside an already-isolated environment. |

- For a pure "read this and answer" task, pass **`-s read-only`**. Capturing with `-o` still works (the *CLI*
  writes that file, not the sandboxed agent), so read-only never blocks your output.
- `codex exec` is **non-interactive** — it does not prompt mid-run (unlike the TUI's `-a/--ask-for-approval`).
  Command failures are returned to the model, not escalated to a human.
- `--dangerously-bypass-approvals-and-sandbox` exists for externally-sandboxed CI. The name is the warning.

## 6. Model, reasoning effort, config

- **`-m, --model MODEL`** — pick the model (e.g. `-m gpt-5.5`). With `--ignore-user-config` you get the CLI
  default.
- **`-c, --config key=value`** — override any `config.toml` value. The value is parsed as **TOML** (falls back
  to a literal string if it doesn't parse), so quote strings: `-c 'model_reasoning_effort="high"'`. Dotted paths
  reach nested keys: `-c shell_environment_policy.inherit=all`.
- **Reasoning effort** — `-c 'model_reasoning_effort="high"'` (levels `minimal`/`low`/`medium`/`high`). The
  startup banner on stderr prints `reasoning effort: <level>` — use it to confirm the override took.
- **`--ignore-user-config`** — skip `config.toml` (auth still works; it lives in `$CODEX_HOME`). The clean-room
  switch for reproducible automation.
- **`--strict-config`** — error on unrecognized config keys (catch drift after upgrades).
- **`-C, --cd DIR`** set the working root · **`--skip-git-repo-check`** run outside a git repo ·
  **`--ephemeral`** don't persist a session file (good for throwaway probes).

## 7. Recipes

**Read-only analysis → file (the workhorse):**
```bash
codex exec --ignore-user-config -s read-only -o REVIEW.md \
  -c 'model_reasoning_effort="high"' \
  "Read ./src and ./docs/spec.md. List the top 5 mismatches between spec and implementation." \
  < /dev/null
```

**Structured JSON output:**
```bash
codex exec --ignore-user-config -s read-only \
  --output-schema schema.json -o result.json \
  "Extract every TODO in ./src as {file, line, text}." < /dev/null
```

**Let it change the repo (use with care):**
```bash
codex exec -s workspace-write -o SUMMARY.md \
  "Add type hints to ./util.py and run the tests." < /dev/null
```

**Throwaway smoke test (writes nothing persistent):**
```bash
codex exec --ephemeral --ignore-user-config "Reply with exactly: OK" < /dev/null
```

**Related subcommands:**
```bash
codex exec review                 # non-interactive code review of the current repo
codex exec resume --last "..."    # continue the most recent session with a new instruction
```

## 8. Troubleshooting

| Symptom | Cause / fix |
|---|---|
| Hangs forever, no output | stdin trap — add `< /dev/null` (bash) or `'' \|` (PowerShell). §3. |
| `command not found: codex` | Not on PATH — call by full path or add npm global bin. §2. |
| Auth errors / login loop | `codex login`; `codex doctor`; confirm `$CODEX_HOME/auth.json` exists. |
| Slow startup / errors loading skills or MCP | Heavy local `config.toml` — add `--ignore-user-config`. |
| Reasoning effort seems wrong | Check the stderr banner; set `-c 'model_reasoning_effort="high"'`. |
| Config key rejected after upgrade | `--strict-config` to surface it, or `codex doctor`. |
| Won't edit files | Default/`read-only` sandbox blocks writes — pass `-s workspace-write`. §5. |

## Hooks are reactive, not a launcher

Codex **hooks** (`SessionStart`, `UserPromptSubmit`, `PreToolUse`, `PostToolUse`, `Stop`, …) run your scripts
**when** Codex does something. They work with both the CLI and the desktop app but are **reactive only** — a
hook cannot *initiate* a run. To start Codex with a prompt, use `codex exec`; to react to one finishing, use a
`Stop` hook.

---

*Provenance: distilled from a real dogfood (driving Codex as a headless cross-vendor consultant from another
agent's shell), verified end-to-end against `codex-cli 0.142.2` (default model `gpt-5.5`). Re-run
`codex exec --help` to confirm flags on any other version.*
