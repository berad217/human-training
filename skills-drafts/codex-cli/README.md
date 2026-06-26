# codex-cli — draft notes

A skill for driving the OpenAI **Codex CLI** non-interactively (`codex exec`) from a script or another agent.

## Scope

- **In:** install/auth, the headless contract (stdin/stdout/stderr), output capture (`-o` / `--json` /
  `--output-schema`), sandbox + approval safety, model & reasoning-effort/config flags, recipes, troubleshooting,
  and the hooks-are-reactive clarification.
- **Out:** the interactive Codex TUI, the desktop GUI app's normal use, the OpenAI cloud/Responses API, and
  non-Codex tooling. (These are the negative-scope clauses in the `description:`.)

## Footguns captured (the reasons this skill exists)

1. **stdin block** — `codex exec` reads stdin to append a `<stdin>` block; an open pipe with no EOF hangs it.
   Fix: `< /dev/null` (bash) / `'' |` (PowerShell). This is the headline footgun.
2. **CLI vs desktop app** — the app can't be launched externally; you need the standalone CLI (it shares auth).
3. **stdout vs stderr** — final message on stdout, reasoning/progress on stderr; `-o` captures cleanly; `--json`
   is the opposite of lean.
4. **`--ignore-user-config`** — a clean-room reader, immune to a heavy local `config.toml` (MCP/tools) that can
   stall or pollute a run.
5. **Sandbox defaults** — `read-only` vs `workspace-write`; pick deliberately.

## Provenance

Distilled from a live dogfood: an agent drove Codex as a **headless cross-vendor consultant** from its own
shell (fire prompt → capture `-o` file → harvest), verified end-to-end against `codex-cli 0.142.2`
(default model `gpt-5.5`). Every flag in SKILL.md was taken from that version's `codex exec --help`.

## Graduation TODO (before moving to `skills-source/codex-cli/`)

- [ ] Run a trigger eval against `eval-queries.md`; tune `description:` for precision/recall.
- [ ] Re-verify the flag set against the **latest** Codex CLI (note the version in the appendix line).
- [ ] Decide whether to ship any `research/` (none needed yet — SKILL.md is self-contained).
- [ ] Confirm `name:` (`codex-cli`) matches the dir name, then move the folder to `skills-source/codex-cli/`,
      `./scripts/build-skills.ps1`, bump `version` in both plugin manifests, commit, `/plugin update`.
