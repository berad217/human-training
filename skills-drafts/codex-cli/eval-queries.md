# codex-cli — candidate trigger queries

For the eventual `trigger-eval.json`. **Positive** = the skill should fire; **negative** = it must NOT.

## Positive (should trigger)

- "How do I call Codex from the command line without opening the app?"
- "Is there a `codex -p` to run a prompt headless?"
- "Run Codex non-interactively and save the output to a file."
- "Have Claude/the agent run Codex on this folder and bring back the answer."
- "Automate a Codex call in a script / in CI."
- "My `codex exec` just hangs with no output — what's wrong?"
- "Capture only Codex's final answer, not all the reasoning."
- "Use Codex as a cross-vendor reviewer from the command line."
- "How do I make Codex edit files vs just read them when scripting it?"
- "Set Codex's reasoning effort / model when running it headless."
- "codex exec stuck / blocked / frozen"
- "Drive the Codex CLI from another agent."

## Negative (must NOT trigger)

- "Help me use the Codex chat in the desktop app." (GUI app, interactive)
- "Walk me through the Codex TUI." (interactive, not headless)
- "Write code against the OpenAI Responses API / cloud API." (not the Codex CLI)
- "Call the Anthropic / Gemini / Ollama API." (other providers — other skills)
- "What model should I pick for my ChatGPT subscription?" (not CLI automation)
- "Set up GitHub Copilot in VS Code." (unrelated tool)

## Notes for tuning

- The strongest disambiguator vs. cloud-API skills is **"command line / CLI / headless / `codex exec` /
  automate / script"** + the word **Codex**. Keep those in `description:`.
- The strongest disambiguator vs. the **desktop app** is **"without the app / from a script / non-interactive."**
- "codex hangs / stuck with no output" should fire — the stdin trap is a top reason someone reaches for this.
