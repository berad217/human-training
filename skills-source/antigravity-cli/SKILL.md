---
name: antigravity-cli
description: Use when driving Google's Antigravity CLI (`agy`) non-interactively / headlessly — `agy -p`/`--print`, running Antigravity from a script or another agent, capturing its answer, or automating a Gemini-backed agent call from the terminal. Triggers include "call/run agy from the command line", "antigravity headless / non-interactive", "agy -p", "is there an antigravity exec/print mode", "automate antigravity", "have Claude/the agent run agy", "agy prints nothing / empty output / no stdout", "drive Antigravity CLI from a script", "use agy/Gemini as a cross-vendor consultant or reviewer over files", "pick the agy model". Covers install + the keyring auth shared with the IDE, the **empty-stdout-under-pipe** footgun and the transcript-recovery workaround, the 5-minute print timeout, permission/sandbox safety (including the **cwd-escape** footgun when letting agy read files itself), model selection (`--model`), the tool-free file-reading **consultant pattern**, and troubleshooting. Do NOT use for the interactive `agy` TUI, the Antigravity IDE (Electron app), Antigravity 2.0 desktop, the Antigravity SDK (Python), or the hosted Gemini API (that's the gemini-api skill).
allowed-tools: [Bash, Read, Write, Edit, Grep, Glob, WebFetch]
---

# Antigravity CLI (`agy`) — headless / non-interactive

Drive Google's **Antigravity CLI** from a script or another agent: fire a prompt at a Gemini-backed agent and
recover the answer. `agy -p "..."` (aka `--print` / `--prompt`) is the non-interactive entry point — it runs one
prompt to completion and exits, no TUI.

**Verified against `agy 1.0.13` on Windows / Git Bash, default model `gemini-3.5-flash`
("Gemini 3.5 Flash (Medium)").** `agy` is young and self-updates silently — re-confirm with `agy --help` on the
target machine. This skill is one another agent will trust, so the honesty matters: `agy` is **TUI-first**, and
its headless path has a real, easy-to-miss output bug (below). Re-test, don't assume.

**Check `agy --version` at the start of a session — it self-updates silently.** `agy` arms a background updater
(§2), so unlike a manually-managed CLI the build can change *underneath you* between runs. There's no `npm`-style
"latest" to diff against and no manual upgrade to nudge the user toward — so the check serves the *opposite*
purpose of the codex-cli one: not "you're stale, go update," but **catch silent drift in this skill's own
assumptions.** If the running build is newer than the `1.0.13` verified here, the version-specific workarounds
below — above all the empty-stdout capture bug (§4) — may no longer hold. Re-test the load-bearing behavior before
trusting it, and tell the user what changed: a silent update that *fixes* the stdout bug collapses the whole
transcript-recovery dance into `ANSWER=$("$AGY" -p "..." < /dev/null)`.

## TL;DR — the rules that keep headless `agy` from biting you

**The meta-rule: `agy` degrades *quietly*.** Its headline failure mode is *success with no output* — exit 0, the
model answered, stdout empty (rule 1). The same quiet character runs through the rest: the startup log cries "not
logged in" then silently auths anyway (§2), an agentic run's final answer comes back *blank* (§4), and
`--dangerously-skip-permissions` walks out of your cwd and writes elsewhere *without a word* (rule 5). So the
posture is **assume-degraded-until-verified** — the same one the [codex-cli](../codex-cli/SKILL.md) skill spells
out: judge every leg by the recovered **transcript** + **exit code** + what the run actually *touched*, never by
stdout or the agent's own narration.

1. **`agy -p` prints NOTHING to a redirected/piped stdout (v1.0.13).** The #1 footgun. The run succeeds (exit 0),
   the model answers, but **stdout is empty whenever it isn't a real terminal** — i.e. every script, subprocess,
   pipe, or agent call. It works when *you* test it by hand in a terminal, then silently returns nothing in
   automation. **Recover the answer from the conversation transcript** ([§4](#4-getting-the-answer-out-the-key-workaround)).
2. **The CLI is not the IDE.** The Antigravity **IDE** (`Antigravity.exe`, an Electron app) and **`agy`** (a Go
   binary) are separate installs. Having the IDE does *not* give you `agy`. They *do* share login via the system
   keyring — install `agy` separately, but you usually won't re-auth. [§1](#1-the-cli-is-not-the-ide-or-20-or-the-sdk)
3. **Auth can't bootstrap headlessly the first time.** `agy` has no `login` subcommand; first-ever auth needs an
   interactive browser (run `agy` once, press Enter, paste the code) — or just be already logged into the IDE.
   After that, `-p` silently reuses the keyring token. [§2](#2-install--auth)
4. **`--print-timeout` defaults to 5 minutes.** A headless run that stalls (e.g. an agentic task that needs a tool
   permission it can't get) burns up to 5 min, then exits. Set it low for probes. [§5](#5-the-print-timeout)
5. **`--dangerously-skip-permissions` is NOT confined to the cwd — it can roam your whole filesystem.** The
   nastiest footgun, worse than the stdout bug. In a dogfood it searched all of `P:\`, found another project's
   identically-named task file, and **wrote a fabricated report into that unrelated repo.** There's no per-call
   `read-only` flag; safety is governed by `toolPermission`/`allowNonWorkspaceAccess` in `settings.json` and the
   `--sandbox` flag — coarser than Codex's sandbox, and skip-permissions overrides the workspace boundary. For a
   consultant that reads files, **don't let agy read them itself — inline the contents into the prompt** ([§9](#9-the-consultant-pattern-read-files--report)). [§6](#6-safety-permissions--sandbox)

The canonical headless call (Git Bash) — run it, then harvest the transcript:

```bash
AGY="$LOCALAPPDATA/agy/bin/agy.exe"   # full path: install rarely lands on an active shell's PATH
"$AGY" -p "Your full prompt here." \
  --print-timeout 90s \
  --log-file ./agy-run.log \
  < /dev/null                          # stdin closed defensively (see §3)
# stdout is empty — recover the answer from the transcript (see §4)
```

## 1. The CLI is not the IDE (or 2.0, or the SDK)

Antigravity ships as four surfaces. Only one is this skill:

| Surface | What it is | Driveable headlessly? |
|---|---|---|
| **Antigravity CLI** (`agy`) | Go binary, terminal agent | **Yes — this skill.** TUI-first, thin `-p` mode. |
| **Antigravity IDE** | Electron app (`Antigravity.exe`), VS Code fork | No external "run this prompt" entry point. |
| **Antigravity 2.0** | Desktop orchestration app | No. |
| **Antigravity SDK** | Python library | Yes, but that's code, not a CLI — different skill. |

The IDE and `agy` are **separate binaries** but **share auth** through the OS keyring. On this machine the IDE
lives at `…\Programs\Antigravity\Antigravity.exe` (220 MB, bundles a Codeium `language_server.exe`); `agy` is a
standalone ~few-MB Go binary at `%LOCALAPPDATA%\agy\bin\agy.exe`. Finding the IDE installed tells you nothing
about whether `agy` is installed — check `agy --version` explicitly.

## 2. Install & auth

```bash
# Windows (PowerShell):
irm https://antigravity.google/cli/install.ps1 | iex
# macOS / Linux:
curl -fsSL https://antigravity.google/cli/install.sh | bash
agy --version            # confirm (binary at %LOCALAPPDATA%\agy\bin\agy.exe on Windows)
```

The installer fetches a platform manifest, downloads the binary, **verifies its SHA512**, drops it in
`%LOCALAPPDATA%\agy\bin`, runs `agy install` to register PATH, and arms a background self-updater.

- **PATH lag (Windows):** the installer writes the User PATH registry var but **does not update the *active*
  shell**. A session opened before install won't see `agy` — open a new shell, or call it by full path
  (`"$LOCALAPPDATA/agy/bin/agy.exe"`). This is the #1 "command not found."
- **Auth = system keyring → Google Sign-In.** No `login`/`whoami`/`logout` subcommand; the only sign-out is
  `/logout` *inside the TUI*. **First-ever auth is interactive:** run `agy` (bare TUI), press `Enter`, complete
  the browser OAuth, paste the code back. After that, `agy -p` does **silent keyring auth** — it logs
  `Print mode: not authenticated, trying silent auth` → `keyringAuth: loaded token` → `silent auth succeeded`.
- **Already in the IDE? You're already authed for `agy`** — the keyring entry is shared. (Verified: a fresh `agy`
  install silent-authed as the IDE's logged-in Google account with no browser.)
- **The startup log lies for ~100 ms.** On every run the language-server backend prewarms its caches *before* the
  keyring loads, spraying `You are not logged into Antigravity` errors into the log. They're harmless if a later
  `silent auth succeeded` line appears. Don't trust the early lines — grep for the *outcome*.

## 3. stdin

`agy -p` takes the prompt as an argument, so it doesn't *need* stdin. Whether it blocks on an open, dataless pipe
the way `codex exec` does is **unverified** — every test here ran with stdin closed (`< /dev/null`) as hygiene.
Keep doing that in bash; it costs nothing and removes a whole class of hang. PowerShell has no `<` redirection —
pass `'' |` or just call `agy` directly (it reads the prompt from the argument).

## 4. Getting the answer out (the key workaround)

**The problem.** With stdout redirected/piped (all automation), `agy -p` writes **0 bytes** to stdout and exits
0 — verified on v1.0.13 in Git Bash; treat *every* non-TTY context as affected. (Under PowerShell the same call
went the other way and *stalled* with no output rather than returning empty — capture there is at least as
unreliable; pin down which before depending on it.) The model genuinely answers (the log shows
`streamGenerateContent` → `Stream completed`); the result is just **persisted, not emitted**. There is **no
`--output-format` / `--json` / `-o` flag** to fix this — the Go flag set has none, and Google's first-party
codelab documents `-p` for "quick answers" while giving **no way to capture its output in a script**. So this
isn't a missing sanctioned path — there isn't one. `agy models` is suppressed the same way. (Output presumably
renders only to an interactive TTY; this looks like a print-mode bug, not a design.)

**The fix — read the conversation transcript.** Every run writes a JSONL transcript on disk. The final answer is
the last step of `type` `PLANNER_RESPONSE` from `source` `MODEL`:

```bash
AGY="$LOCALAPPDATA/agy/bin/agy.exe"
"$AGY" -p "What is 17 times 3? Reply with just the number." \
  --print-timeout 60s --log-file ./run.log < /dev/null >/dev/null 2>&1

# 1) get the conversation id this run created (from the log we forced)
CID=$(grep -oE 'conversation=[0-9a-f-]+' run.log | head -1 | cut -d= -f2)

# 2) read the model's final answer from that conversation's transcript
TRANSCRIPT="$HOME/.gemini/antigravity-cli/brain/$CID/.system_generated/logs/transcript.jsonl"
grep '"type":"PLANNER_RESPONSE"' "$TRANSCRIPT" | tail -1 \
  | python -c "import sys,json; print(json.loads(sys.stdin.read())['content'])"
# -> 51
```

- **Why `--log-file`:** it's the reliable per-run handle on the conversation id (the log prints
  `Print mode: conversation=<uuid>, sending message`). Without it you'd have to guess.
- **Alternate id source:** `~/.gemini/antigravity-cli/cache/last_conversations.json` maps **workspace dir →
  latest conversation id**. Fine for a single run per dir; racy if you fire several from the same dir.
- **Transcript shape:** JSONL, one step per line. `USER_INPUT` (your prompt, wrapped in `<USER_REQUEST>`),
  `PLANNER_RESPONSE` (model text — *this is the answer for a no-tool Q&A run*), plus `CONVERSATION_HISTORY` /
  `CHECKPOINT` bookkeeping. **Reliable only for the pure-Q&A path.** In an **agentic** run (tool steps like
  `VIEW_FILE` / `LIST_DIRECTORY` / `RUN_COMMAND`) the *last* `PLANNER_RESPONSE` is frequently **empty** — the
  synthesized answer doesn't land as a clean final text step. That's a second reason to keep consultant runs
  tool-free ([§9](#9-the-consultant-pattern-read-files--report)).
- **Re-test on upgrade.** If a newer `agy` actually prints to stdout, this whole dance collapses to
  `ANSWER=$("$AGY" -p "..." < /dev/null)`. Check first; the bug may not survive.
- **The agent's self-report ≠ the run's outcome.** Don't conclude failure from empty stdout — or, on an agentic
  run, from the model narrating *"I couldn't write the file."* The captured artifact is authoritative: judge by
  the recovered transcript + exit code, not agy's prose. (Codex driven headlessly has the identical trap, where
  `-o` captures the answer despite a read-only-sandbox "I couldn't write it" — see codex-cli §4.)

## 5. The print timeout

`--print-timeout` (default **5m0s**) bounds how long print mode waits. A simple Q&A returns in seconds, so the
default rarely bites — but an **agentic** task that wants to run a tool or edit a file under the default
`request-review` permission mode **can't get approval non-interactively**, so it stalls until the timeout, then
exits (often with nothing useful). Two consequences:

- For quick probes, set it low (`--print-timeout 30s`) so a stall fails fast.
- For real headless agentic work, remove the thing it stalls on: grant permission up front ([§6](#6-safety-permissions--sandbox)).

## 6. Safety: permissions & sandbox

`agy` can read/write files and run commands. Unlike Codex there's **no per-invocation `read-only` switch**.
Control comes from two places:

- **Flags:** `--dangerously-skip-permissions` (auto-approve *everything* — the name is the warning) and
  `--sandbox` (run terminal commands under OS restrictions).
- **`settings.json` → `toolPermission`** (`~/.gemini/antigravity-cli/settings.json`): `request-review` (default —
  prompts, which **hangs headless runs**, see §5), `strict`, `always-proceed`, `proceed-in-sandbox`.

Practical guidance:

- **Read-only Q&A / analysis:** the default is fine — a question that needs no tools never triggers a permission
  prompt, and the transcript-recovery path still works.
- **Let it edit/run headlessly — danger zone:** it *will* stall on `request-review`, and the "fix"
  (`--dangerously-skip-permissions`) **removes the cwd boundary**. Dogfod evidence: with skip-permissions agy ran
  shell commands that walked `P:\software_projects\`, matched another project's `consultant_task.md`, and wrote a
  report into that unrelated repo — `allowNonWorkspaceAccess` defaults to `false` but **skip-permissions
  overrides it.** `--sandbox` stops the roaming shell, but then `request-review` blocks the file reads and it does
  nothing. There is currently **no clean flag combo for "let agy edit, but only here."** If you must, do it inside
  a throwaway/containerized dir with nothing else reachable, and verify the transcript didn't touch outside paths.
  For the common "read files and report" case, **don't go agentic at all — use [§9](#9-the-consultant-pattern-read-files--report).**

## 7. Model, session, config

- **`--model MODEL`** — override the model (default `gemini-3.5-flash`). `agy models` *lists* them but its output
  is TTY-suppressed like §4; in the TUI use `/model`.
- **`--continue` / `-c`** resume the most recent conversation · **`--conversation <ID>`** resume a specific one ·
  **`-i` / `--prompt-interactive`** seed a prompt then drop into the TUI (not headless).
- **`--add-dir DIR`** (repeatable) add a workspace dir · **`--project` / `--new-project`** scope the session ·
  **`--log-file PATH`** the handle you need for §4.
- **Config home:** `~/.gemini/antigravity-cli/` — `settings.json` (model, `toolPermission`, `enableTerminalSandbox`,
  `allowNonWorkspaceAccess`, `trustedWorkspaces`, telemetry…), `conversations/<id>.db` (SQLite), `brain/<id>/…`
  (transcripts), `cache/`, `log/`. Shared `~/.gemini/config/config.json` holds global permission rules.

## 8. Recipes

**Headless Q&A → variable (the workhorse, with recovery):**
```bash
AGY="$LOCALAPPDATA/agy/bin/agy.exe"
"$AGY" -p "Summarize ./README.md in 3 bullets." --print-timeout 90s --log-file ./run.log < /dev/null >/dev/null 2>&1
CID=$(grep -oE 'conversation=[0-9a-f-]+' run.log | head -1 | cut -d= -f2)
ANSWER=$(grep '"type":"PLANNER_RESPONSE"' "$HOME/.gemini/antigravity-cli/brain/$CID/.system_generated/logs/transcript.jsonl" \
  | tail -1 | python -c "import sys,json; print(json.loads(sys.stdin.read())['content'])")
echo "$ANSWER"
```

**Let it modify a repo (use with care — re-read [§6](#6-safety-permissions--sandbox) first; this can roam):**
```bash
"$AGY" -p "Add type hints to ./util.py." --dangerously-skip-permissions --sandbox \
  --add-dir . --print-timeout 5m --log-file ./run.log < /dev/null
# then diff the repo / harvest the transcript for the summary
```

**Smoke test the install/auth (does it answer at all?):**
```bash
"$AGY" -p "Reply with exactly: OK" --print-timeout 30s --log-file ./smoke.log < /dev/null
CID=$(grep -oE 'conversation=[0-9a-f-]+' smoke.log | head -1 | cut -d= -f2)
grep -oE '"content":"[^"]*"' "$HOME/.gemini/antigravity-cli/brain/$CID/.system_generated/logs/transcript.jsonl" | tail -1
```

## 9. The consultant pattern (read files → report)

The headline use case: drive `agy` as a Gemini consultant that reads source files and writes back an analysis —
the cross-vendor "cold outside read" (cf. OpenAI Codex driven the same way). **Do NOT do this by letting `agy`
read the files itself** — that's the agentic path, which is flaky (empty final message) and unsafe (roams the
filesystem, [§6](#6-safety-permissions--sandbox)). Instead, **the driver (you/Claude) reads the files and inlines
their contents into the prompt, and `agy` runs tool-free.** This is *safer and more faithful*: agy sees exactly
the bytes you hand it and nothing else — the same "the information boundary IS the methodology" discipline the
Codex consultant pattern relies on.

```bash
AGY="$LOCALAPPDATA/agy/bin/agy.exe"
MODEL="gemini-3.5-flash"                       # <-- model selection: swap per call

# 1) Driver gathers the exact context (you control the boundary — omit anything off-limits)
PROMPT="You are a cold outside reviewer. Analyse the files below and <the task>.
=== spec.md ===
$(cat spec.md)
=== client.py ===
$(cat client.py)
Deliver your complete analysis as your final message."

# 2) agy analyses, TOOL-FREE (no --dangerously-skip-permissions, no --add-dir → it cannot read/roam)
"$AGY" -p "$PROMPT" --model "$MODEL" --print-timeout 90s --log-file ./run.log < /dev/null >/dev/null 2>&1

# 3) Recover the report from the transcript (stdout is empty — §4) and write it where you want
CID=$(grep -oE 'conversation=[0-9a-f-]+' run.log | head -1 | cut -d= -f2)
grep '"type":"PLANNER_RESPONSE"' "$HOME/.gemini/antigravity-cli/brain/$CID/.system_generated/logs/transcript.jsonl" \
  | tail -1 | python -c "import sys,json; print(json.loads(sys.stdin.read())['content'])" > REPORT.md
```

- **Verified:** Gemini 3.5 Flash, fed two files inline, correctly found the planted spec-vs-code inconsistency
  (quoting both conflicting values) with **zero tool calls and zero out-of-cwd access** — the clean, safe result
  the agentic path never produced.
- **Model selection** is just `--model <id>` (default `gemini-3.5-flash`; the run resolves a label like
  "Gemini 3.5 Flash (Medium)" in the log — grep `selected model override` to confirm). The full id list comes
  from `agy models`, but its output is TTY-suppressed ([§4](#4-getting-the-answer-out-the-key-workaround)); read
  it in the TUI (`/model`) if you need names beyond the default.
- **Large inputs:** inlining is bounded by the prompt/context budget. For a big repo, have the *driver* select
  and summarise the relevant files first (it's the one with safe file access), then hand agy the distilled packet
  — don't reach for the agentic path to save a `cat`.

## 10. Troubleshooting

| Symptom | Cause / fix |
|---|---|
| `agy -p` exits 0 but **no output** | The print-mode stdout bug. Expected under any pipe/redirect. Recover from the transcript. §4. |
| `agy` touched/modified files **outside** the cwd | `--dangerously-skip-permissions` removed the workspace boundary — it can roam and write anywhere. Don't use it for read tasks; use the tool-free consultant pattern. §6, §9. |
| Agentic run read files but final answer is **empty** | The last `PLANNER_RESPONSE` is often blank on tool-using runs. Use the tool-free consultant pattern (inline the files). §9. |
| `command not found: agy` right after install | Active shell's PATH is stale. New shell, or call `"$LOCALAPPDATA/agy/bin/agy.exe"`. §2. |
| Log says "You are not logged into Antigravity" | Usually just startup cache prewarm. Look for a later `silent auth succeeded`. If absent, auth interactively once (`agy` → Enter → browser) or log into the IDE. §2. |
| Run hangs ~5 min then exits empty | Agentic task stalled on `request-review` it can't satisfy headlessly. Add `--dangerously-skip-permissions` (+`--sandbox`) or lower `--print-timeout`. §5–6. |
| Wrong / unexpected model | Pass `--model`; default is `gemini-3.5-flash`. §7. |
| Can't find the answer's conversation id | You didn't pass `--log-file`. Add it, or read `cache/last_conversations.json`. §4. |
| `agy models` prints nothing | Same TTY-suppression as §4. Model list isn't available headlessly; use `--model` blind or check the TUI. |

## TUI-first, headless-second

Google's own on-disk reference (`…/antigravity-cli/builtin/skills/antigravity_guide/references/cli.md`) documents
the **TUI** — slash commands (`/model`, `/resume`, `/logout`, `/copy`, …), keyboard nav, and `settings.json` — and
**doesn't mention `-p` at all**. Headless is a real but second-class path. If a task is genuinely interactive,
that's the TUI (`agy`), which this skill doesn't cover. For "fire a prompt, get the answer back in a script,"
`agy -p` + transcript recovery is the route — eyes open about the output bug.

---

*Provenance: live dogfood on Windows 11 — fresh `irm | iex` install of `agy 1.0.13`, silent keyring auth inherited
from the Antigravity IDE (account `white.brad@gmail.com`), default model Gemini 3.5 Flash. The empty-stdout
behavior was reproduced across three Git Bash runs (PowerShell stalled rather than returning, so capture there is
unverified); the transcript-recovery recipe was verified end-to-end (`17×3` → `51`). The **consultant pattern**
([§9](#9-the-consultant-pattern-read-files--report)) was dogfooded against a writey-style `consult/` folder with a
planted spec-vs-code inconsistency: the **tool-free inline-context run** (Gemini 3.5 Flash) nailed it cleanly,
while the **agentic** variant (`--dangerously-skip-permissions`) escaped the cwd, walked `P:\software_projects\`,
and wrote a report into an unrelated repo — the cwd-escape footgun ([§6](#6-safety-permissions--sandbox)) is from
that incident (collateral was reverted). Flags taken verbatim from `agy --help`; settings from Google's bundled
`cli.md`. First-party corroboration: Google's `antigravity-cli-hands-on` codelab documents `-p` and
`--dangerously-skip-permissions` and confirms no output-capture flag exists. Re-run `agy --help` and re-test the
stdout + cwd-confinement behavior on any newer version.*
