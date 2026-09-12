---
name: codex-cli
description: Use when driving OpenAI's Codex CLI non-interactively / headlessly — `codex exec`, running Codex from a script or another agent, capturing its output to a file, or automating a Codex call. Triggers include "run codex from the command line", "codex headless / non-interactive", "codex exec", "is there a codex -p", "automate codex", "codex hangs / stuck with no output", "capture codex output", "codex in CI". Do NOT use for the interactive Codex TUI, the Codex desktop GUI app, or for the OpenAI cloud/Responses API or non-Codex tools.
allowed-tools: [Bash, Read, Write, Edit, Grep, Glob, WebFetch]
---

# Codex CLI — headless / non-interactive

Drive OpenAI's Codex CLI from a script or another agent. `codex exec` (alias
`codex e`) runs the agent to completion and exits, no TUI. The desktop app has
no external "run this prompt" entry point; you need the standalone CLI
(`npm i -g @openai/codex`), which shares the app's login through `$CODEX_HOME`.
For image generation and editing through Codex's built-in tool, see the
`image-gen` skill, which builds on the mechanics here.

**Verified against `codex-cli 0.144.6` on 2026-09-12.** Flags and models drift
between versions; `codex exec --help` on the target machine is the authority.
On first use compare `codex --version` with `npm view @openai/codex version`
and tell the user once if they differ: an agent driving Codex headlessly is
often the only thing positioned to notice a stale CLI, and a stale CLI is the
root of most flag and model errors.

## The posture: Codex fails quietly

It hangs instead of erroring, falls back to a default model without saying so,
misreports which model it is, apologises in-band when a blocked write fails,
and overwrites a reused output path without a word. So every run you depend on
gets three cheap checks: the stderr **banner** (`model:`, `sandbox:`,
`reasoning effort:`), the **`-o` file** (exists, non-empty, no apology on top),
and the **exit code**. Never the agent's prose.

The canonical call:

```bash
codex exec --ignore-user-config -s read-only \
  -m <model-id> \
  -c 'model_reasoning_effort="high"' \
  -o ANSWER.md \
  "Your full prompt here." \
  < /dev/null
```

1. **Close stdin.** `< /dev/null` in bash, `'' |` in PowerShell. Without it a
   call with a prompt and an open, dataless pipe blocks reading stdin for an
   EOF that never comes. It looks like a hang; stderr says
   `Reading additional input from stdin...` and nothing else happens. Using
   stdin on purpose (`codex exec - < prompt.txt`) is fine.
2. **Capture with `-o FILE`.** stdout carries only the final message and
   stderr carries banner, progress and reasoning; `-o` writes the final
   message alone, the context-lean capture. `--output-schema FILE` constrains
   it to a JSON shape. `--json` is the whole event stream; reserve it for when
   you want that.
3. **`--ignore-user-config`** skips `config.toml` so a heavy local setup (MCP
   servers, custom tools) can't perturb or stall the run. Auth still works.
   It also discards your configured model default, so pass `-m` explicitly.
4. **Pick the sandbox deliberately.** `read-only` for read-and-analyse,
   `workspace-write` (plus `--add-dir`) only when it should edit,
   `danger-full-access` only inside something already isolated. `codex exec`
   never prompts mid-run; command failures go back to the model, not to a
   human.

## Reading the capture

`-o` is written by the CLI, not the sandboxed agent, so it lands even when the
agent believes it failed. Under `read-only` the model sometimes tries to write
its own output file, gets blocked, and announces "I couldn't write the file."
That prose is not the outcome; the file and the exit code are.

Two consequences. First, that apology often lands as the first one or two
lines of the `-o` file, ahead of the real answer: strip it on read, or grant
`workspace-write` scoped to the output folder so no apology is generated.
Second, `-o` is a plain overwrite with no lock: two parallel runs sharing a
path leave you with one silently missing result. Template the path off the
run's identity.

## Models and effort

`-m` takes any model id the account can use; there is no CLI command that
lists them, the TUI's `/model` picker does, and the current family with a
tier-to-tier mapping against Claude is in `reference.md`, dated. Don't copy
an id from a document older than the CLI. The stderr banner's `model:` line is
the model of record: asked which model it is, the agent often names the wrong
one.

Reasoning effort is the second dial, `-c 'model_reasoning_effort="high"'`,
confirmed by the banner's `reasoning effort:` line. Spend `high` or above on
the legs whose wrongness is expensive (validation, lock-in, adversarial
checks) and leave generative-breadth legs at default; paying high effort
across many candidates mostly buys latency.

`-c key=value` overrides any config value, parsed as TOML, so quote strings
and use dotted paths for nesting. `--strict-config` errors on keys this
version doesn't know, which catches drift after an upgrade. `-C DIR` sets the
working root, `--skip-git-repo-check` allows a non-repo, `--ephemeral` skips
the session file. `codex exec review` runs a non-interactive review;
`codex exec resume --last "…"` continues the latest session.

## Install and auth

`npm i -g @openai/codex`, then `codex --version`, `codex login` if needed,
`codex doctor` for health. The CLI reuses the desktop app's `auth.json`; for
CI, `CODEX_API_KEY=<key>` in the environment. On Windows the npm global bin
(`%APPDATA%\npm`) is often absent from a non-interactive shell's PATH, so call
by full path.

**Test for the CLI with `codex --version`, never by `~/.codex` existing.** The
desktop app populates that directory fully, auth and all, with no CLI
anywhere, and a working alpha binary sits under `~/.codex/plugins/` that moves
when the app updates. The story is in `reference.md`; the fix is the six-second
npm install, which inherits the login.

## Troubleshooting

| Symptom | Cause / fix |
|---|---|
| Hangs, stderr ends in `Reading additional input from stdin...` | stdin trap. `< /dev/null` or `'' \|`. |
| `command not found: codex` | Not on PATH. Full path, or add npm's global bin. |
| `command not found`, but `~/.codex` has valid auth | The desktop app's dir. Install the CLI with npm; don't script against the bundled exe. |
| Auth errors | `codex login`, `codex doctor`, confirm `$CODEX_HOME/auth.json`. |
| Slow startup, errors loading skills or MCP | Heavy `config.toml`. `--ignore-user-config`. |
| Wrong model or effort | Read the banner. Pass `-m` (required with `--ignore-user-config`) and `-c 'model_reasoning_effort="…"'`. |
| Config key rejected after upgrade | `--strict-config` to surface it, or `codex doctor`. |
| Won't edit files | Sandbox is `read-only`. `-s workspace-write`. |
| A parallel run's output is missing | Shared `-o` path, last writer wins. One path per run. |
| Output opens with a can't-write apology | Read-only agent told to save its own file. Strip it, or scoped `workspace-write`. |
| Non-ASCII garbled on Windows | Console encoding. Cosmetic if symmetric; normalise before a machine parse. |

Hooks (`SessionStart`, `PreToolUse`, `Stop`, …) are reactive: they run when
Codex does something and cannot start a run. To launch, use `codex exec`; to
react to a finish, a `Stop` hook.

---

*Provenance: distilled from driving Codex as a headless cross-vendor consultant
from another agent's shell. Re-verified 2026-09-12 on 0.144.6: `-o` and stdout
both carry the final message, the banner reports model, sandbox and effort,
and an open dataless stdin pipe hangs until timeout with the
`Reading additional input` line. npm's latest that day was 0.154.0; its release
notes to that point mention no change to `exec`'s stdin, capture or sandbox
flags (0.154.0 adds managed worktrees to `exec`, unverified here).*
