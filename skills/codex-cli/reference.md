# Codex CLI — reference

Dated material and worked recipes behind `SKILL.md`.

## The model family, as of 2026-09-12 (for the record; confirm before use)

The live frontier family was GPT-5.6 in three tiers. The mapping onto Claude
tiers is the useful part; the ids will rot.

| Tier | `-m` string | Reach for it like… | Sweet spot |
|---|---|---|---|
| Sol | `gpt-5.6-sol` | Opus | Hard, ambiguous, high-value: deep reasoning, tricky refactors, security |
| Terra | `gpt-5.6-terra` | Sonnet | The everyday default for delegated work |
| Luna | `gpt-5.6-luna` | Haiku | Fast, cheap, repeatable: extraction, classification, mechanical passes |

Default to Terra, escalate to Sol when the task is genuinely hard, drop to
Luna for volume. Older families stay callable. The common shape is Terra at
medium effort for breadth, Sol at high for the load-bearing judgement.

Effort values accepted by `model_reasoning_effort`: `minimal`, `low`,
`medium`, `high`, `xhigh` (model-dependent). The 0.143.0 changelog added `max`
for 5.6 before the config reference listed it; confirm on your version.

## Recipes

**Read-only analysis to a file (the workhorse):**
```bash
codex exec --ignore-user-config -s read-only -m <id> -o REVIEW.md \
  -c 'model_reasoning_effort="high"' \
  "Read ./src and ./docs/spec.md. List the top 5 mismatches between spec and implementation." \
  < /dev/null
```

**Structured JSON output (mechanical extraction, cheapest tier):**
```bash
codex exec --ignore-user-config -s read-only -m <id> \
  --output-schema schema.json -o result.json \
  "Extract every TODO in ./src as {file, line, text}." < /dev/null
```

**Let it change the repo:**
```bash
codex exec -s workspace-write -o SUMMARY.md \
  "Add type hints to ./util.py and run the tests." < /dev/null
```

**Throwaway smoke test:**
```bash
codex exec --ephemeral --ignore-user-config -m <id> "Reply with exactly: OK" < /dev/null
```

## Detecting the CLI on a box that only has the desktop app

Observed: `~/.codex` present and fully populated, a valid `auth.json` reading
`"auth_mode": "chatgpt"`, `skills/`, `plugins/`, `sessions/`, `config.toml`,
and no CLI anywhere: nothing on PATH, `npm root -g` pointing at a
`node_modules` that doesn't exist. Every signal short of running the binary
said "installed."

Hunting the filesystem then turns up `~/.codex/plugins/.plugin-appserver/codex.exe`.
It runs and honours the same flags, and it is an app-internal path on an alpha
build (`0.146.0-alpha.9.2` while npm shipped stable `0.146.0`) that moves when
the app updates. Fine for a one-off probe; wrong to script against or write
into a doc. `npm i -g @openai/codex` is a six-second two-package install that
inherits the app's login, so there is no `codex login` round-trip.

## The stdin trap, verbatim

`codex exec --help`: *"If not provided as an argument (or if `-` is used),
instructions are read from stdin. If stdin is piped and a prompt is also
provided, stdin is appended as a `<stdin>` block."* So a prompt argument plus
an open pipe with no data and no EOF, the normal situation under automation,
parks the process in a read. Verified 2026-09-12 on 0.144.6: with stdin held
open by a sleeping producer the call hit a 40 s timeout with an empty `-o`
file and `Reading additional input from stdin...` as the last stderr line; the
same call with `< /dev/null` returned in ten seconds.

## Hooks

`SessionStart`, `UserPromptSubmit`, `PreToolUse`, `PostToolUse`, `Stop` and
the rest run your scripts when Codex does something, in both the CLI and the
desktop app. None of them can initiate a run.
