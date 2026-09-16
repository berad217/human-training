# Handover — human-training

**Session date:** 2026-09-14
**State:** **1.33.0 shipped** - `onboarding-creator` gains a "Messages from other
sessions" block (peer messages are credible, not authoritative), lifted from the
Blendy repo the day it was needed. Before that, on 2026-09-12: **1.29.0 through
1.32.0 shipped** the same day. Five skills
through the trim: `/start` 2,804 → 890 words, `robustness-audit` 4,160 → 1,643,
`antigravity-cli` 3,232 → 1,325 (a rewrite: the stdout bug it documented was
fixed in agy 1.0.15), `codex-cli` 2,770 → 1,250, `image-gen` 2,224 → 1,194 (the
built-in tool's model is no longer named anywhere; it now returns alpha). Each
has a `reference.md` and was probed before and after. Tree clean and in sync.
Nothing in flight.

What shipped is in the release notes; don't restate it here.

---

## The queue is `TASKS.md`

Anything with a next action lives there. This file carries only what is
contested, unproven, or decided-but-not-obvious.

---

## Read this before probing anything

**The verification technique works and it will lie to you if you use it wrong.**
`claude -p --plugin-dir <repo> "<organic prompt>"` loads the working tree's
`skills/` (the **build output**, so rebuild first or you probe the old body).
It found a real UTC bug, proved skill-to-skill chaining, and this session found
a recursion bug. It also once produced a false result that reached a release.

**Rules, all non-optional:**

1. **Pass `--allowedTools Skill Read Glob Grep Bash`**, plus `Agent` for skills
   that dispatch. Without it `Skill` gets denied on some runs and not others,
   and a denied `Skill` call means the agent hand-rolls the task while sounding
   authoritative.
2. **Read outcomes, not requests.** `tool_use` is the model asking; the paired
   `tool_result` is what happened, and that is where a denial sits.
3. **Count `Skill` calls in the stream.** More than one means a subagent
   re-triggered the skill from inside its own prompt. That is how
   `robustness-audit` was fanning out two levels deep on every run since it
   shipped, unnoticed, because nobody had counted.
4. **Run probes from a scratch or downstream directory, never from this repo.**
   `onboarding.md` suppresses `human-training:*` triggers here.
5. **Believe the subject.** When a run says in its own prose that a tool was
   blocked, it was.

**Negative results are weak; positive results are strong.** One run proves a
found bug; "it didn't do X" from one run proves nothing. Two audit runs on the
same project disagreed on the headline finding (a paddle bug one promoted and
the next dismissed as by-design). That is the variance floor.

**Cost.** `/start` probes are ~$1. `robustness-audit` probes are $6–15 because
they dispatch agents. Budget before running a third.

## The delta (not in the files)

- **The trim method, now 2 for 2.** Keep every rule that encodes a fact the
  model cannot see by looking (glob case-sensitivity, catalog refresh
  mechanics, fabrication rates, "don't add suppression instructions"). Fold
  anti-pattern sections into the step they guard. Move templates, pattern
  lists, history and worked examples to `reference.md`, pointed at from the
  step that needs them. Probe before and after. Both times the behaviour was
  set by the interface the model touched (the output template, the subagent
  prompt), not by the rule count.

- **Re-verify the binary before trimming a vendor-CLI skill.** `antigravity-cli`
  was verified against 1.0.13; the machine was on 1.1.27 and self-updated to
  1.2.2 mid-session. Run the tool, read its changelog (`agy changelog`, GitHub
  releases for codex), then decide whether it is a trim or a rewrite.
  `codex-cli` installed is 0.144.6, npm latest 0.154.0, deliberately not
  upgraded here; the skill's first-use nudge covers that.

- **No model ids in skill bodies** (Brad, 2026-09-12; in memory too). Point at
  the discovery command (`agy models`; Codex has none, so the TUI's `/model`),
  put a dated snapshot in `reference.md` marked do-not-copy. `gemini-api` is the last
  skill with ids in the body; it is on the queue.

- **"Dispatch in one block" is moot, not wrong.** All three audit runs
  dispatched one agent per turn. The Agent tool now launches async, so they
  overlapped anyway. Delete the instruction next time `robustness-audit` is
  touched; it is in the body of every skill that dispatches.

- **`/start`'s docs-only contract is contested - one piece decided (1.34.0).**
  Both `/start` probes read source diffs to explain a dirty tree, and it was
  the most useful line in the orientation. Nobody has decided whether to
  loosen the contract to permit `git diff --stat` on a dirty tree. What IS
  decided (Brad, 2026-09-16): `/start` makes exactly one write, the TASKS
  sweep - ticked items out of Active into Done one-liners, because it is the
  reader that pays for a bloated Active and a session open is when culling
  costs no attention. Not probed before shipping: the headless CLI's OAuth
  had expired; the fixture (a TASKS with two ticked items in Active) is
  described in `reference.md`'s sweep section and is a five-line rebuild.

- **`critic-loop` lives in two places on purpose.** `skills-source/` ships;
  `skills-drafts/critic-loop/rounds/` is the evidence log. Don't tidy it.

- **An observation, not a rule (n=4):** a critic marking an item "not safe
  without review" for a reason only the author can resolve, and the author
  taking it as a logged deviation. Honest with a scrupulous author,
  rationalisation with a careless one. Stays in the draft README.

- **`/start` step 2d works. Do not delete it again** (1.25.0 removed it on a
  misread probe; 1.26.0 restored it). The tell is a probe where 2d "silently
  didn't fire": check for a denied `Skill` call first.

- **The evidence ladder does not catch instrument failure.** Both 2026-08-19
  overclaims were a check that ran and was misread. Unresolved. Names shared
  across skills, definitions local; don't fold the rung into confidence.

- **The pstack rejections, so they aren't re-derived:** `poteto-mode`'s router,
  `swarm`, `arena`, `interrogate`, `architect`, `how`/`why`, `recall`,
  `automate-me`. `unslop` would fight this repo's prose; fork, don't adopt.

- **Branch protection is settled.** "Bypassed rule violations" on push is the
  rule working.

## What is now actually verified

Watched running with a sound instrument: **`/start`** (both bodies, same
coverage), **`robustness-audit`** (three runs; the guarded body is the one
that shipped), **`antigravity-cli`** and **`codex-cli`** (old and new bodies,
each producing a working script; the agy claims re-run live on 1.2.2, the
codex claims on 0.144.6), **`leroy-jenkins` → `show-me-your-work`** chaining,
and **`critic-loop`** on itself, twice.

Still assumed: `grill`, `tasks`, `handover-manager`, `project-checkup`, and
everything in `skills-drafts/`.

## Toolchain data point

This machine is on 1.28.0 by install record, and the `human-training`
marketplace `lastUpdated` advanced on its own to 2026-09-12 10:00Z. Whether
the plugin followed the catalog to 1.29.0 and 1.30.0 after a relaunch is the
still-open `TASKS.md` item, and today gives it two fresh releases to test
against. Other machines: unknown.

---

*Ephemeral bridge — prune once absorbed. Durable record: the release notes,
`TASKS.md` for the queue, and the skill bodies themselves.*
