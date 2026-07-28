---
name: robustness-audit
description: Find latent runtime bugs in existing code by close reading, without executing it — crashes, swallowed errors, edge cases, resource leaks, races, and auth gaps that pass tests but fail in production. Triggers include robustness audit, hardening pass, defect-class or FMEA-style review, "what could go wrong", "what's likely broken", "this feels brittle", silent or mysterious failures, bugs that pass CI, features that work in tests but not in production, auditing before a release, and assessing a codebase after time away.
---

# Robustness audit

A defect-class audit that surfaces the runtime bugs hiding between unit tests: bad wiring between modules, swallowed errors, resource leaks, race conditions, and contracts that drift between callers and callees. Most of these survive any mocked test suite because the tests mock the very thing that has drifted.

The audit is read-only. It does not execute the code. That is a feature: it works when the user cannot live-test (no hardware, away from their machine, code path requires a GPU/webcam/credentials/etc.).

## When to invoke

Direct user triggers: "robustness audit", "hardening pass", "audit my code", "find runtime bugs", "what could go wrong", "what's likely broken", "FMEA-style review".

Contextual triggers (use proactively): the user just returned to an unfamiliar codebase, just finished a significant refactor, is about to release, says "this feels brittle" or "I keep hitting weird edge cases", or describes a feature that mysteriously stopped working when their tests are all green.

## Not the right tool for

- **Debugging a specific known error.** "I'm getting `TypeError: x.foo is not a function` at line 47" wants systematic-debugging, not a wide audit.
- **Performance** — different smells.
- **Pure security audit** — overlaps but warrants its own dedicated approach with attacker modeling. This skill catches security boundary holes that show up adjacent to other code (auth gap on a write route next to authed reads), not full threat modeling.
- **Architecture review** — this audit is line-level.
- **"Is my code good?"** — too vague to act on. Pin to a concrete concern.

## Why this works

Most real production bugs in dynamic-typed codebases are not algorithmic. They are *boundary* bugs: a function renamed without updating callers, a constructor that started reading a different config shape, a promise that nobody catches, an event listener that nobody removes, a security check that exists at one HTTP verb but not another.

Mocked unit tests do not catch these because the mock embodies the *intended* boundary, not the *current* boundary. A test that calls `mockDetector.detectForVideo(...)` happily passes against a class that only exports `detect()`, because the mock is whatever the test author said it is.

Reading the real callers and the real callees side by side surfaces the drift. The taxonomy below tells the reviewer which mental models to bring to that reading.

## The process

### 1. Map the surfaces (where to look)

Identify 3-5 natural code surfaces. Each surface gets one agent. Typical surfaces for a web/node project: client modules, server, config + hot-reload plumbing, recently-added code (last few commits), security-relevant paths. For each surface, list the files to read in priority order — heaviest-trafficked or most-recently-modified first.

Three to five surfaces is the right number. Fewer wastes parallelism; more produces overlap and noise.

### 2. Dispatch parallel agents (what to look for)

Use the Agent tool with `general-purpose` or a domain reviewer agent, model `sonnet`. Run all agents in one block so they execute in parallel. The agent prompt must include:

- **The taxonomy below**, spelled out — don't say "find bugs"; the categories prime distinct mental models.
- **Files in priority order**, with one-line ownership descriptions.
- **A quality bar, not a quantity cap**: "Demand a concrete failure mode — if you can't say what breaks, it's a nit." That defines what counts as a finding. Do **not** add "only report what you're confident about", "be conservative", or a severity floor: current models follow suppression instructions literally and report less, and the finding they drop is as likely to be real as the one they keep. Ask for everything that clears the quality bar, scored, and filter in step 3.
- **Output format**: file:line, what breaks (in user-visible terms), one-line fix, severity-as-phrase, confidence 0-100. The confidence number is what makes a separate filter pass possible — it is for sorting, not for self-censoring.

While agents work, the main thread can begin verifying any prior known issues or read surrounding context.

### 3. Verify the loud claims, and filter here

**This is the single biggest failure mode of this workflow. Skipping it is how an audit becomes net-negative.** It is also where filtering happens — step 2 deliberately doesn't filter, so this step is what stands between a raw list and a punch list.

> **Don't mistake this for self-verification and delete it.** Current guidance says not to instruct a model to double-check its own work or spawn subagents to verify itself — that's real, and it's not this. Here the main thread checks *another agent's* claims against the source: a writer-verifier split, where the verifier has something the writer didn't (the actual file, and no stake in the finding). Keep it.

Audit agents fabricate findings at a rate worth planning for — on the models this skill was written against, roughly 1 in 3-5 "Critical" claims failed close reading. Newer models fabricate less, so treat that ratio as a reason to check rather than a quota of falsehoods to find. Common fabrication patterns:

- *"Method X doesn't exist"* — agent grepped the wrong file or missed an alias.
- *"This produces NaN forever"* — agent traced control flow incorrectly; the branch they think runs doesn't.
- *"Race condition loses data"* — agent missed that JS variable rebinding doesn't mutate the original array, or that an async function body runs synchronously until its first `await`.
- *"Path traversal"* — agent didn't see the guard one function call up the stack.
- *"Pause/resume is broken"* — agent misread a falsy-or-null guard as truthy.

Before acting on any high-severity or high-confidence finding, use Grep + Read to reproduce the failure mode in the actual code. If the trace doesn't match the agent's claim, mark the finding *verified false* and surface it to the user with a one-line reason. The "verified to be wrong" section is part of the audit's value — it's the calibration that earns trust for the findings you *do* act on.

### 4. Synthesize

Merge findings across agents. Drop duplicates. Group by impact (color-coded — see below). Note which findings were verified true vs. claimed by agent vs. verified false.

### 5. Present the triage menu

Surface the findings and ask one focused question with 4 explicit options. Don't ask "what should we do?" — that's underspecified.

## The defect taxonomy

These six categories cover the overwhelming majority of latent robustness issues. Spell each one out in the agent prompt — the names alone prime distinct searches.

### 1. Crashes / data loss / silent corruption

The user ends up in a broken state they can't recover from. Highest signal — fix first.

**Patterns to read for:**
- APIs that return `T | null` used without a guard (`Array.find()`, `Map.get()`, `JSZip.folder()`, `document.querySelector()`, `results.landmarks[0]`).
- Optional fields on persisted records treated as required (old DB rows, old localStorage shapes).
- Catches that return a sentinel "empty" value (`return []`, `return null`) which the caller can't distinguish from a legitimate empty result — then writes the sentinel back to storage.
- Type assertions hiding nulls (`foo!`, `as Foo`).
- `JSON.parse` of user-provided or AI-provided strings without validation.
- Numeric ops on possibly-NaN values (parsed inputs, `parseInt` failures).
- **Contract drift** — caller passes argument shape A; callee expects shape B. The frame-loop classic: `main.js` calls `this.detector.detectForVideo(...)` when the class only exports `detect()`. Wrapped in a try/catch that logs and continues, the app silently does nothing.

### 2. Error paths that swallow or misreport

The user does something, it fails, but the UI lies about what happened.

**Patterns:**
- `setStatus('error')` (or similar) with no path back to `'idle'`. The UI is gated on status and now permanently locked.
- `setErrorMsg(...)` set but never cleared on retry — stale banner.
- `try { ... } catch (e) { console.error(e); }` — error never reaches the user-visible log/toast.
- `async` functions that throw inside but the caller `await`s and doesn't handle.
- `Promise.all` where one rejection hides the others.
- Error messages that pass through raw API JSON instead of being mapped to user-readable text.
- Loading spinners that depend on a state variable not reset in every code path.
- Try/catch that wraps a *whole frame loop* and continues into broken state silently.

### 3. Edge cases on user input

What happens at the boundaries — empty, huge, malformed, multi.

**Patterns:**
- `files[0]` from a multi-file drop or paste, silently ignoring the rest.
- File handlers branching on `.endsWith('.json')` but accepting other extensions in the UI / MIME allow-list (mismatched contracts).
- MIME type from the browser trusted without sniffing.
- Text inputs with no max length sent to APIs that charge by token.
- Empty-string inputs not rejected before hitting the API.
- "Optimistic" UI updates that don't roll back on failure.
- IndexedDB / localStorage quota / version-block / private-browsing failures.
- HMR / React StrictMode double-renders triggering side effects twice.

### 4. Resource leaks

Slow accumulation that bites on long sessions.

**Patterns:**
- `URL.createObjectURL(...)` without matching `URL.revokeObjectURL(...)`.
- Event listeners added in `useEffect` (or in a constructor) without cleanup return.
- `setInterval` / `setTimeout` with no `clearInterval` / `clearTimeout`.
- `requestAnimationFrame` loops where the frame ID is not stored, so `stop()` can never cancel — each start leaks a fresh loop.
- `new Worker(...)` without `.terminate()`.
- `IDBDatabase` connections opened per-call instead of singleton + reused.
- Three.js / WebGL: `geometry.dispose()`, `material.dispose()`, `texture.dispose()`, `renderer.dispose()` — usually one is missing.
- Modules that subscribe to an event bus but never unsubscribe; subscriptions whose return handles are never stored.

### 5. Concurrency hazards

Race conditions and stale state.

**Patterns:**
- Double-click on a button that triggers an async call: `setStatus('busy')` isn't synchronous, so a fast second click fires before the disabled prop renders. Need a synchronous `useRef<boolean>` guard.
- `setState` after `await` in an async handler — the component may have unmounted. Need `mountedRef` or `AbortController`.
- Two tabs of the same app racing on shared storage (IDB, localStorage).
- Stale closures: handlers defined outside `useCallback` capturing old state.
- Effects with missing dependencies re-running with stale values.
- Optimistic local writes overwritten by a slow server response that finished earlier.
- File watcher fires during a partial write (editor saves) and broadcasts a half-parsed config to all SSE clients.

### 6. Security boundary holes (server / HTTP code only)

Include this category only when a surface includes server code.

**Patterns:**
- Auth middleware applied to read routes but missing on a write route that mutates the same state.
- CORS pattern-matching regex with unescaped metacharacters — `http://localhost:*` matches `http://localhostXcom` if dots aren't escaped.
- Path traversal: any route that constructs a filesystem path from request data, where `startsWith(dir)` without `path.sep` lets `dir_evil/` escape.
- Secrets returned by a config endpoint that serializes the whole YAML, or served as a static file under a public mount.
- `fs.watch` that crashes the process if the watched path is absent at startup.
- `yaml.load` returns `null` for an empty file and does not throw — broadcasting `config: null` to all clients silently breaks them.
- Rate limiter applied by prefix that accidentally throttles long-lived SSE streams.

## Subagent prompt template

```
Perform a robustness audit of <SURFACE> in <PROJECT>. The user cannot
live-test right now; find latent runtime bugs by close reading only.

Working directory: <ABSOLUTE PATH>

## Context

<2-3 sentences: what the project does, the data flow, recent changes
on this surface.>

## Files of interest (in priority order)

1. `<entry point>` — <one-line ownership>
2. `<service layer>` — <ownership>
... (5-10 files max; prioritize by lines-touched in recent commits)

<Out-of-scope notes here, e.g. "the auth module was audited separately —
only flag auth issues if they cause crashes in this surface.">

## What I want

A prioritized list of robustness issues organized by these categories
(don't just say "find bugs" — the categories tell you where to look):

1. **Crashes / data loss / silent corruption** — broken state the user
   can't recover from. Highest signal.
2. **Error paths that swallow or misreport** — places where catches hide
   info, errors aren't surfaced, or async failures leave UI stuck.
3. **Edge cases on user input** — empty / huge / malformed inputs, weird
   API responses, storage quota or version conflicts, HMR re-renders.
4. **Resource leaks** — unrevoked object URLs, dangling listeners,
   uncancelled animation frames, IDB connections, setState after unmount.
5. **Concurrency hazards** — double-clicks during async work, navigation
   mid-stream, multiple tabs, stale closures, file-watcher partial reads.
6. **Security boundary holes** (only if the files include server/HTTP code):
   auth gaps on write routes, CORS regex escape, path traversal, secret
   leakage via config endpoint, missing-file crashes.

For each finding produce:

**N. <Short title>**
`<file>:<line>` (or `<file>:<line-range>`)

<2-4 sentences describing the bug and its user-visible impact.>

Fix: <one-line sketch>
Severity: **<phrase describing what bad thing happens>** (e.g. "UI
permanently stuck after any error", "tab leaks N MB per export")
Confidence: **NN** (0-100)

**Rules of the road:**
- Report every issue that clears the bar below, including ones you are
  unsure about — score them low rather than dropping them. A separate
  pass filters this list; you are not the filter.
- The bar is a concrete failure mode. If you can't say what breaks, it's
  a nit — drop it. No style notes, no "consider doing X".
- There is no target count. However many real bugs you find is the
  answer; don't pad to reach a number and don't stop early to stay under
  one.

Close with a summary table sorted by severity × confidence (highest
first):

| # | File:line | Severity (phrase) | Confidence |
|---|-----------|-------------------|------------|
| 4 | `App.tsx:190` | UI permanently stuck after any error | 100 |
| 2 | `App.tsx:116` | Empty data saved to storage on exec failure | 95 |
```

## Synthesis output to the user

Use this template — the user reads it as a punch list. Match its length to the findings: one line per finding, and let the count of real bugs set the size of the report. A punch list earns its keep by being scannable, so cover every finding but skip the framing paragraphs, restated methodology, and closing summaries that repeat the table above them.

```markdown
## Robustness audit synthesis — <N> parallel agents

**The bombshell:** <one line: the single most consequential finding in plain English. If everything's minor, say so.>

### 🔴 Red — confirmed real, breaks normal use
*(confidence ≥ 90, severity = crash / lock / data loss / security boundary)*

1. **[file:line](file:line) — <Title>.** <One sentence on the failure mode in user-visible terms.> Verified: yes/no. Confidence: NN.

### 🟠 Orange — high confidence, will bite eventually
*(confidence ≥ 80, severity = leak / silent failure / degraded feature)*

...

### 🟡 Yellow — real but lower urgency
*(everything else)*

...

### Verified to be wrong (deliberately not fixed)

- <Agent's claim>: <why it's wrong on close reading>

### The pattern

<One or two sentences naming the meta-issue — "constructor-contract drift", "missing-cleanup in lifecycle methods", "swallowed errors in async event handlers" — so the user can grep for similar elsewhere.>

### Action menu

1. **Fix red now** — single focused commit.
2. **Red + orange in one branch** — multi-commit branch.
3. **All in one push** — knock the whole list.
4. **File them, fix later** — write to a TODO doc.
```

The severity column uses a *phrase* describing what bad thing happens, not a label like "high/medium" — labels are too abstract to act on; phrases trigger "oh shit."

## Worked examples (for prompt-priming)

Include 2-3 of these in the agent prompt when the surface matches, as anchoring examples:

**Crash class:**
> *`main.js:485` calls `this.detector.detectForVideo(...)` but `PoseDetector` only exports `detect()` — every frame throws `TypeError`, caught silently by the try/catch around the frame loop. The app appears to "just not detect anything" but is actually broken at every frame. Severity: app fundamentally doesn't work. Confidence: 100.*

**Error path swallow:**
> *Three async handlers call `setStatus('error')` but no path resets to `'idle'`. UI is gated on `status === 'idle'`, so after any failure the UI is permanently locked. Severity: UI permanently stuck after any error. Confidence: 100.*

**Resource leak:**
> *`DisplayModule.animate()` calls `requestAnimationFrame(() => this.animate())` without storing the frame id, so `stop()` cannot cancel it. After each start/restart cycle a new loop accumulates alongside the old, each firing `render()` per frame. Severity: animation loops compound across sessions, FPS degrades to zero. Confidence: 95.*

**Concurrency:**
> *Double-click on Generate fires two concurrent API requests. `setStatus('busy')` is async — the disabled prop doesn't render before the second click. Severity: duplicate API charges, racing optimistic updates. Confidence: 90.*

**Security boundary:**
> *`POST /api/pose/update` has no `authenticateApiKey` middleware, while `GET /api/pose/current` and `/api/pose/stream` do. An unauth'd caller can flood / poison the pose ring buffer while reads remain locked down. Severity: write surface bypasses configured auth. Confidence: 100.*

## Anti-patterns to avoid

- **Don't run the audit inline in a long-context session.** The reviewer has accumulated assumptions; dispatch to a sub-agent for fresh eyes.
- **Don't ask for "all bugs."** You get nothing (overwhelmed) or everything (noise). The taxonomy bounds the search.
- **Don't accept "this could be improved" findings.** Demand a concrete failure mode. If the reviewer can't say what breaks, it's a nit.
- **Don't fix without confirming with the user first.** Audits surface more than the user wants done in one session. Triage before action.
- **Don't fix mixed concerns in one commit unless the diff genuinely interleaves.** Themed commits are easier to revert.
- **Don't trust the agent's summary — read the actual code.** The agent reports what it intended; verify against the file. This goes for both findings (during synthesis) and fixes (after the commit).

## Trust calibration

The audit's credibility depends on the "verified to be wrong" section being honest, not on it being full. Report the false positives you actually found — that trace is what earns trust for the findings you act on. If a run genuinely produced none, say that; a clean run is a real outcome, and manufacturing a doubt to fill the section is worse than an empty one.
