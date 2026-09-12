---
name: antigravity-cli
description: Use when driving Google's Antigravity CLI (`agy`) non-interactively / headlessly — `agy -p`/`--print`, running it from a script or another agent, or automating a Gemini-backed agent call from the terminal. Triggers include "run agy from the command line", "antigravity headless / non-interactive", "agy -p", "is there an antigravity exec/print mode", "automate antigravity", "agy prints nothing / empty output / no stdout", "pick the agy model", and using agy/Gemini as a cross-vendor consultant or reviewer over files. Do NOT use for the interactive `agy` TUI, the Antigravity IDE (Electron app), Antigravity 2.0 desktop, the Antigravity SDK (Python), or the hosted Gemini API (that's the gemini-api skill).
allowed-tools: [Bash, Read, Write, Edit, Grep, Glob, WebFetch]
---

# Antigravity CLI (`agy`) — headless / non-interactive

Drive Google's Antigravity CLI from a script or another agent: `agy -p "..."`
runs one prompt to completion and exits. The CLI is a standalone Go binary,
separate from the Antigravity IDE, Antigravity 2.0 and the Python SDK; it shares
login with the IDE through the OS keyring but is installed on its own.

**Start every session with `agy --version`, and treat this file as dated.** The
binary self-updates silently, including mid-session: on 2026-09-12 it reported
1.1.27, replaced itself in the same minute, and every later run was 1.2.2.
Everything below was verified on that day, on 1.2.2 unless marked. The skill was first written against 1.0.13, when `-p` wrote nothing
to a redirected stdout and the answer had to be dug out of a transcript. That
bug was fixed in 1.0.15 and the whole recovery dance is now legacy
(`reference.md` keeps it, with the changelog map of what changed when). If a
build newer than 1.2.2 behaves differently from this file, believe the build,
and `agy changelog` says why.

## The canonical call

```bash
AGY="$LOCALAPPDATA/agy/bin/agy.exe"     # full path: a fresh install is not on an already-open shell's PATH
OUT=$("$AGY" -p "What is 17 times 3? Reply with just the number." \
        --output-format json --print-timeout 90s < /dev/null)
ANSWER=$(printf '%s' "$OUT" | python -c 'import sys,json; print(json.load(sys.stdin)["response"].strip())')
```

`--output-format json` returns one object: `conversation_id`, `status`
(`SUCCESS` or not), `response` (the text), `duration_seconds`, `num_turns`,
`usage` (input, output, thinking, cache-read, total tokens), and, when the
run wanted a tool it wasn't allowed, `denied_actions`. Plain `-p` prints the
text alone; `stream-json` streams events. `--json-schema <schema-or-path>`
enforces structured output on the final result.

**Judge a run by `status`, `denied_actions`, the exit code and what it
touched, never by the prose.** A run that wanted to run a command it couldn't
returns `SUCCESS` with an empty `response` and a stderr line that names the
denied permission. Exit codes reflect failures of the run itself, not benign
tool denials.

## What still bites

- **PATH lag.** The installer writes the user PATH but not the shell you are
  in. Call by full path or open a new shell. This is the usual "command not
  found."
- **Close stdin** (`< /dev/null` in bash). Subcommands hung on an inherited
  open pipe until 1.1.23; keep the hygiene, it is free.
- **The startup log lies for about 100 ms.** Every run sprays dozens of
  `You are not logged into Antigravity` lines while the backend prewarms
  before the keyring loads. Harmless if `silent auth succeeded` follows. Grep
  the outcome, not the first lines.
- **First-ever auth is interactive.** No `login` subcommand; run bare `agy`
  once and complete the browser flow, or be logged into the IDE, which
  shares the keyring. After that `-p` auths silently. A `GEMINI_API_KEY` with
  `modelProvider: "gemini"` in settings is the sign-in-free alternative.
- **`--print-timeout` defaults to 5 minutes.** Set it to seconds for probes.
  Headless runs no longer stall on permission prompts (auto-denied since
  1.1.3) or plan approval (1.1.28), so the timeout now mostly bounds a slow
  model, and on expiry the CLI returns partial output with a stderr warning.

## Permissions and safety

Under default settings a headless run that wants a tool it isn't allowed gets
the tool auto-denied, finishes with `denied_actions` filled in, and touches
nothing. Verified: a write request under defaults left the directory untouched
and reported `{"action":"command","display_name":"RunCommand"}`. Three ways to
let it act, in order of blast radius:

1. **`--mode plan`**: the agent writes a plan into its own brain directory and
   asks to proceed. Nothing in your tree changes. Good for "what would you do."
2. **`permissions.allow` rules in `settings.json`**, which headless runs honour
   since 1.1.5, scoped to the tool and target you want. `--sandbox` restricts
   terminal commands under OS confinement. `--add-dir .` makes the cwd part of
   the workspace; without it the agent may treat its own scratch directory as
   the working location.
3. **`--dangerously-skip-permissions`**: approves everything. At 1.0.13 a run
   with this flag walked out of the cwd, searched other projects, and wrote a
   fabricated report into an unrelated repo. That incident has not been
   re-tested on a newer build, deliberately. Use only in a throwaway directory
   with nothing else reachable, and check the transcript afterwards.

For the common "read these files and report" job, skip all three: read the
files yourself, inline their contents into the prompt, and run tool-free. The
model sees exactly the bytes you chose and nothing else, and the answer comes
back as a clean `response`. Bound by the prompt budget, so distil first for a
large repo.

## Models

Never hardcode a model id; the list changes faster than this file. `agy models`
prints the current ids with their labels, tab-separated, and works under
redirect. Pass one with `--model <id>`; an id that doesn't resolve fails
non-zero and lists the valid ones (1.1.2). `--effort low|medium|high` sets
reasoning effort where the model supports it. The default resolves at run
time; the log line `Propagating selected model override … label="…"` says
which one you got. Third-party models appear in the list alongside Gemini.

## Session and config

`-c`/`--continue` resumes the latest conversation, `--conversation <id>` a
specific one. `--input-format stream-json` with `--output-format stream-json`
keeps one session open and runs a turn per NDJSON line on stdin, for a driver
that wants state across calls. `--project`/`--new-project` scope the session.
`--log-file` overrides the per-run log, which is where the conversation id and
model label are printed.

Config home is `~/.gemini/antigravity-cli/` (`brain/<id>/` transcripts and
plans, `conversations/`, `cache/`, `log/`, `builtin/` skills); shared
permission rules sit in `~/.gemini/config/config.json`. `settings.json` in the
config home holds `permissions`, model, provider and sandbox choices, and is
absent until something is changed. Read-only slash commands answer
non-interactively (`-p "/help"`, `/config`, `/permissions`, `/model`,
`/changelog`) without spending quota; `agy update` updates the CLI by hand.

## Troubleshooting

| Symptom | Cause / fix |
|---|---|
| `command not found: agy` after install | Stale shell PATH. Full path, or a new shell. |
| `status: SUCCESS`, empty `response`, stderr names a permission | The run wanted a tool headless mode can't prompt for. Read `denied_actions`; add an allow rule, or inline the files and go tool-free. |
| Log says "not logged into Antigravity" | Startup prewarm. Look for a later `silent auth succeeded`; if absent, auth once interactively. |
| Empty stdout on a redirect | Fixed in 1.0.15. If it recurs on a newer build, `reference.md` has the transcript recovery. |
| Wrong or unexpected model | `agy models`, then `--model <id>`. The log's `label=` line says what ran. |
| Behaviour differs from this file | `agy --version`, then `agy changelog`. The binary moved; update the skill. |

---

*Provenance: live runs on Windows 11 / Git Bash on 2026-09-12. The session
opened on 1.1.27; the self-updater installed 1.2.2 within the first minute and
the verifications ran on that. Verified that day: `-p` prints
to a redirected stdout, `--output-format json` shape, `agy models` under
redirect, the default-permission auto-deny with `denied_actions`, `--mode plan`
leaving the tree untouched, keyring silent auth after the noisy startup log.
Version attributions come from `agy changelog`. Not re-verified: PowerShell
capture (stalled at 1.0.13), the skip-permissions roaming incident, and the
`--json-schema` and `stream-json` paths. Original 1.0.13 dogfood is in
`reference.md`.*
