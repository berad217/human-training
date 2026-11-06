---
name: codex-cli
description: Use when driving OpenAI's Codex CLI non-interactively / headlessly — `codex exec`, running Codex from a script or another agent, capturing its output to a file, or automating a Codex call. Triggers include "run codex from the command line", "codex headless / non-interactive", "codex exec", "is there a codex -p", "automate codex", "codex hangs / stuck with no output", "capture codex output", "codex in CI", "resume / message a codex session", "hand a job to a codex worker", "how much codex usage is left". Do NOT use for the interactive Codex TUI, the Codex desktop GUI app, or for the OpenAI cloud/Responses API or non-Codex tools.
allowed-tools: [Bash, Read, Write, Edit, Grep, Glob, WebFetch]
---

# Codex CLI — headless / non-interactive

Drive OpenAI's Codex CLI from a script or another agent. `codex exec` (alias
`codex e`) runs the agent to completion and exits, no TUI. The desktop app has
no external "run this prompt" entry point; you need the standalone CLI
(`npm i -g @openai/codex`), which shares the app's login through `$CODEX_HOME`.
For image generation and editing through Codex's built-in tool, see the
`image-gen` skill, which builds on the mechanics here.

**Verified against `codex-cli 0.166.0` on 2026-11-02** (first written on 0.144.6). Flags and models drift
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
   It also skips any `model =` line there, so the run gets the CLI's own
   default model. That is wanted: leave `-m` out (see Models and effort).
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

**Leave `-m` out by default.** With no `-m` and no `model =` in
`config.toml`, a run gets the CLI's own default, the current flagship for that
CLI version. Keeping the CLI current (the check at the top) is then what keeps
the model current. A pinned id does the opposite: when a better model ships,
the pinned one keeps running at the same price, and nothing says so. The pin
hides in three places: an `-m <id>` in a script, a `model =` line in
`config.toml` (a model picker may have written it, so the user often doesn't
know it is there), and an id copied from a dated document. Pinned ids also get
retired per login: a ChatGPT login refuses an older one outright. If the
user's `config.toml` has a `model =` line they didn't choose on purpose, offer
to delete it, not to update it to today's id.

Pass `-m` only to pick a tier on purpose, a cheaper one for volume, say. No CLI
command lists the ids; the TUI's `/model` picker does, and the tier mapping
against Claude is in `reference.md`, dated. Don't copy an id from a document
older than the CLI. The stderr banner's `model:` line is the model of record,
pinned or not: asked which model it is, the agent often names the wrong one.

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
| Wrong or stale model | Read the banner. A stale model is a pin: `-m` in the call or `model =` in `config.toml`. Drop it. Effort: `-c 'model_reasoning_effort="…"'`. |
| `The '<id>' model is not supported when using Codex with a ChatGPT account` | A retired id pinned in `config.toml` or `-m`. Delete the pin; updating the CLI alone does not fix it. |
| Config key rejected after upgrade | `--strict-config` to surface it, or `codex doctor`. |
| Won't edit files | Sandbox is `read-only`. `-s workspace-write`. |
| A parallel run's output is missing | Shared `-o` path, last writer wins. One path per run. |
| Output opens with a can't-write apology | Read-only agent told to save its own file. Strip it, or scoped `workspace-write`. |
| `thread-store conflict … active writer` on resume | The desktop app has that thread loaded. Use a CLI-owned thread, or quit the app fully. |
| `index.lock: Permission denied` on commit | `.git` is read-only in the sandbox. Commit from the driving agent. |
| `failed to load models cache: missing field …` | CLI older than the desktop app. `npm i -g @openai/codex@latest`. |
| Non-ASCII garbled on Windows | Console encoding. Cosmetic if symmetric; normalise before a machine parse. |

## Driving a worker thread: resume, messages, limits

A run is a thread on disk (`$CODEX_HOME/sessions/**/rollout-*.jsonl`), so an
agent can hold a conversation with one, not just fire one-shots.

- **Talk to it again:** `codex exec resume <thread-id> "msg" -o reply.md < /dev/null`
  appends a turn with its full history. `resume` takes no `-s`; pass
  `-c 'sandbox_mode="workspace-write"'`. The id is the banner's `session id:`.
- **One writer per thread, enforced.** The desktop app holds a writer lock on
  every thread it has *loaded*, open on screen or not, and a resume fails with
  `thread-store conflict: … already has an active writer`. Drive threads you
  started from the CLI, or quit the app fully (tray, not the window close).
  Never resume a thread the human has open.
- **It can't hear you mid-turn,** but it can talk: tell it to drop short notes
  as files in a folder inside its writable root (an outbox), and watch that
  folder. Its final message is the turn's end. A blocked worker writes the
  question and ends its turn; you answer by resuming. Mid-turn steering needs
  the app-server protocol (`turn/steer`), not `exec`.
- **Commits are yours.** Under `workspace-write` the repo's `.git` is
  read-only to the agent, and a linked worktree's metadata lives outside its
  root anyway, so `git commit` fails on `index.lock`. Have it stop at "files
  ready, checks green", rerun its check yourself, and commit for it.
- **No network either:** shell `git fetch`/`push` fail. App-configured
  connectors (a GitHub one) can still work when you don't pass
  `--ignore-user-config`. `-c sandbox_workspace_write.network_access=true`
  should open it (untested here); it is the human's call.
- **Approval is forced to `never`** under `exec`: nothing reaches the human,
  and anything needing escalation just fails back to the model. The sandbox is
  the whole permission story.
- **Usage, without a run:** each turn's rollout carries `token_count` events
  with `rate_limits.primary` (the 300-minute window) and `.secondary` (the
  week): `used_percent` and `resets_at` (epoch). Read the newest rollout before
  you dispatch. The app-server protocol also has `account/rateLimits/read`
  (seen in the generated schema, not exercised). Model and effort per turn are
  in `turn_context`; thread names in `session_index.jsonl`.

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
flags (0.154.0 adds managed worktrees to `exec`, unverified here).
Re-verified 2026-11-02 on 0.166.0 (the app bundled 0.166.0-alpha): resume of a
desktop thread, the writer-lock refusal while the app ran, the read-only `.git`,
no network, forced `approval: never`, and rate limits in the rollout, across two
real jobs handed to fresh CLI threads with outbox notes watched by another
agent. 2026-11-06 on 0.167.0: a `model =` pin in `config.toml` that the user
didn't remember setting was refused by a ChatGPT login and survived the CLI
update. With the pin deleted, the same config's run took the CLI's default
(`gpt-6.1-sol`) and kept the configured effort.*
