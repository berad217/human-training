---
name: robustness-audit
description: Find latent runtime bugs in existing code by close reading, without executing it — crashes, swallowed errors, edge cases, resource leaks, races, and auth gaps that pass tests but fail in production. Triggers include robustness audit, hardening pass, defect-class or FMEA-style review, "what could go wrong", "what's likely broken", "this feels brittle", silent or mysterious failures, bugs that pass CI, features that work in tests but not in production, auditing before a release, and assessing a codebase after time away.
---

# Robustness audit

A defect-class audit that surfaces the runtime bugs hiding between unit tests:
contract drift between callers and callees, swallowed errors, resource leaks,
races. Most survive a mocked test suite because the mock embodies the *intended*
boundary, not the *current* one. Reading the real caller and the real callee
side by side is what surfaces the drift; the taxonomy tells the reader which
mental models to bring.

**The audit is read-only.** It does not execute the code, which is what makes it
work when the user cannot live-test (no hardware, away from their machine, a
path that needs a GPU or credentials).

**Not the right tool for:** a specific known error (debug it); performance;
a full security audit with attacker modelling (this catches the auth gap on a
write route next to authed reads, not a threat model); architecture review;
"is my code good?" (too vague; pin to a concern first).

## The evidence ladder

A finding that *sounds* right reads as convincing whether or not it is true,
and a confidence score doesn't fix that: an agent can be 95% confident in a
trace it got wrong. So every finding carries a second, independent field.

| Rung | Name | What it means |
|------|------|---------------|
| 1 | **Asserted** | The agent says so. Never ships. |
| 2 | **Cited** | A real `file:line` that exists and contains what the finding claims. |
| 3 | **Traced** | Caller and callee read together, the failure path walked, the guard that would prevent it looked for and found absent. |
| 4 | **Executed** | A script that calls the real code and fails loud if the claim is wrong. |
| 5 | **Reproduced** | Observed in the running app. |

This audit ceilings at rung 3 by design. Get each finding as far as is cheap,
report where it stopped, and **never round up**: restating a Cited finding in
confident prose does not make it Traced; the rung only moves when you open the
files. Confidence and rung are separate axes. Confidence is how sure the agent
feels; the rung is what it checked. 95-confident at rung 2 is the combination
worth catching.

Other skills in this plugin use the same five names in the same order, with
their own local definition of each rung. Keep the names aligned; don't share
the definitions.

## The process

**1. Map the surfaces.** Three to five natural code surfaces, one agent each:
client, server, config and hot-reload plumbing, recently-changed code,
security-relevant paths. For each, list files in priority order, heaviest
traffic or most recently modified first. Fewer than three wastes parallelism;
more than five produces overlap.

**2. Dispatch parallel agents.** Agent tool, `general-purpose` or a domain
reviewer, model `sonnet`, all in one block so they run in parallel. Don't run
the audit inline in a long session; the reviewer has accumulated assumptions.
The prompt template is in `reference.md`; open it and fill it in. Non-negotiable
contents:

- The instruction that the agent reads the files itself and invokes no skill
  and no further agents. Without it, a prompt that says "robustness audit"
  triggers this skill inside the subagent, which then fans out again: two
  levels deep and double the cost, observed on both runs that lacked the line.
- The six taxonomy categories, spelled out. "Find bugs" primes nothing.
- Files in priority order, one-line ownership each.
- A quality bar, not a quantity cap: "demand a concrete failure mode; if you
  can't say what breaks, it's a nit." Do **not** add "only report what you're
  confident about" or a severity floor. Current models follow suppression
  instructions literally and report less, and the finding they drop is as
  likely to be real as the one they keep. Filter in step 3, not here.
- Output per finding: `file:line`, what breaks in user-visible terms, a
  one-line fix, severity as a phrase, confidence 0-100, and evidence rung.

**3. Promote the loud claims, and filter here.** This is the step that keeps
an audit from being net-negative, and it is not self-verification: the main
thread checks *another agent's* claims against the source, with the actual file
and no stake in the finding. Keep it. On the models this was written against,
roughly one in three to five "Critical" claims failed close reading (patterns
in `reference.md`); newer models fabricate less, so treat that as a reason to
check, not a quota. For every high-severity or high-confidence finding, Grep
and Read the failure path. Three outcomes, all of them results:

- The trace holds: promote to **Traced**.
- The trace contradicts the claim: **verified false**, with a one-line reason.
- Unsettled: leave it at **Cited** and say so.

Where two surface agents independently flag the same boundary, that is the
strongest signal the run produces: the surfaces are different files, so genuine
overlap is where contract drift lives. Record the agreement.

**4. Synthesize.** Merge across agents, group by severity colour, carry the
rung through, and give every surviving finding a disposition. Two agents
reaching the same finding is a confidence signal: merge into one entry and note
it, don't drop the duplicate.

**5. Triage.** Present the synthesis and one focused question with four
options. Don't fix anything before the user chooses; audits surface more than
one session wants done. You are the lead reviewer, not an aggregator: the
agents saw one surface each and you have the project's goals and stage.

## The defect taxonomy

Six categories. Spell each out in the agent prompt; the names prime distinct
searches. The full pattern lists per category are in `reference.md`.

1. **Crashes, data loss, silent corruption.** The user ends up in a state they
   can't recover from. Nullable returns used unguarded, optional persisted
   fields treated as required, catches that return a sentinel the caller can't
   distinguish from real data, and contract drift: the caller passes shape A,
   the callee expects B, and a try/catch around the loop hides it forever.
2. **Error paths that swallow or misreport.** It failed and the UI lies:
   status set to error with no path back to idle, `catch (e) { log(e) }`,
   `Promise.all` hiding all but one rejection.
3. **Edge cases on user input.** Empty, huge, malformed, multiple: `files[0]`
   from a multi-drop, extension checks that disagree with the MIME allow-list,
   storage quota and private-browsing failures, double-rendered effects.
4. **Resource leaks.** Object URLs never revoked, listeners without cleanup,
   intervals and animation frames whose ids were never stored, workers never
   terminated, GPU resources never disposed.
5. **Concurrency hazards.** Double-click during async work, setState after
   unmount, two tabs on shared storage, stale closures, a file watcher firing
   on a half-written file.
6. **Security boundary holes** (server or HTTP surfaces only). Auth on reads
   but not the write that mutates the same state, CORS regex with unescaped
   dots, path traversal past a `startsWith(dir)` check, secrets in a serialized
   config, `yaml.load` returning null for an empty file.

## Synthesis output

Use this template. One line per finding; the count of real bugs sets the
length. No framing paragraphs, no restated method, no closing summary.

```markdown
## Robustness audit synthesis — <N> parallel agents

**The bombshell:** <one line: the single most consequential finding. If everything's minor, say so.>

### 🔴 Red — confirmed real, breaks normal use
*(confidence ≥ 90, severity = crash / lock / data loss / security boundary)*
1. `[act on]` **[file:line](file:line) — <Title>.** <One sentence, user-visible failure.> Evidence: Traced. Confidence: NN. <"Raised independently by 2 agents." when true.>

### 🟠 Orange — high confidence, will bite eventually
*(confidence ≥ 80, severity = leak / silent failure / degraded feature)*

### 🟡 Yellow — real but lower urgency

### Dismissed (shown so you can overrule me)
- **Verified false** — <claim>: <why it's wrong on close reading>.
- **Valid, not actionable** — <finding>: <why it doesn't earn a fix now>.

### The pattern
<One or two sentences naming the meta-issue so the user can grep for it elsewhere.>

### Action menu
1. **Fix red now** — single focused commit.
2. **Prove the reds first** — a script per red that fails loud if the bug is real, promoting it to Executed before any code changes. Only if you can run the code.
3. **Red + orange in one branch** — multi-commit, themed so each is revertable.
4. **File them, fix later** — TASKS.md or a TODO doc.
```

**Colour is severity; the disposition tag is what to do about it,** and the tag
is yours as lead reviewer: `[act on]` (would block a release), `[consider]`
(legitimate, cost may not be worth it now, the user's call), `[noted]` (valid,
not actionable at this stage). Severity is a phrase naming what bad thing
happens, never a label like "high"; phrases trigger "oh shit", labels don't.

**Show the dismissals, honestly sized.** A filter the user can't see is one
they can't overrule, and your dismissals are the judgements most likely to be
wrong. But don't manufacture doubt to fill the section: a clean run is a real
outcome. The same goes for rungs. A report where everything is Traced is either
unusually thorough or dishonest, and the user can't tell which, so an inflated
rung costs the credibility of the real ones. A red labelled Cited, with a note
on what stopped the trace, is worth more than the same finding dressed up.
