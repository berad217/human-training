# Robustness audit — reference

The subagent prompt template, the per-category pattern lists, the known
fabrication patterns, and worked examples. `SKILL.md` §2 sends you here at
dispatch time; §3 sends you to the fabrication list at verification time.

## Subagent prompt template

```
Close-read <SURFACE> in <PROJECT> for latent runtime bugs. The user cannot
live-test right now, so this is reading only.

Do this yourself with Read and Grep. Do not invoke any skill and do not
dispatch further agents: you are one surface of a parallel audit, and the
main thread does the verification and synthesis.

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
Evidence: **Cited** or **Traced** — see below

**Rules of the road:**
- Report every issue that clears the bar below, including ones you are
  unsure about — score them low rather than dropping them. A separate
  pass filters this list; you are not the filter.
- The bar is a concrete failure mode. If you can't say what breaks, it's
  a nit — drop it. No style notes, no "consider doing X".
- There is no target count. However many real bugs you find is the
  answer; don't pad to reach a number and don't stop early to stay under
  one.
- **Report the evidence rung for every finding, and never round it up.**
  **Cited** means you have a real `file:line` you actually opened.
  **Traced** means you read the caller and the callee side by side,
  walked the failure path step by step, and looked for the guard that
  would prevent it and found it absent. If you only have the citation,
  say Cited. A confident-sounding write-up on top of an untraced
  citation is the single most expensive thing you can hand back. You
  cannot run the code, so Cited and Traced are the only two rungs
  available to you — there is no shame in Cited, only in mislabelling it.

Close with a summary table sorted by severity × confidence (highest
first):

| # | File:line | Severity (phrase) | Confidence | Evidence |
|---|-----------|-------------------|------------|----------|
| 4 | `App.tsx:190` | UI permanently stuck after any error | 100 | Traced |
| 2 | `App.tsx:116` | Empty data saved to storage on exec failure | 95 | Cited |
```

## Patterns to read for, by category

Include the relevant lists in the agent prompt when the surface matches.

**1. Crashes / data loss / silent corruption**
- APIs that return `T | null` used without a guard (`Array.find()`, `Map.get()`, `JSZip.folder()`, `document.querySelector()`, `results.landmarks[0]`).
- Optional fields on persisted records treated as required (old DB rows, old localStorage shapes).
- Catches that return a sentinel "empty" value (`return []`, `return null`) which the caller can't distinguish from a legitimate empty result, then writes back to storage.
- Type assertions hiding nulls (`foo!`, `as Foo`).
- `JSON.parse` of user-provided or AI-provided strings without validation.
- Numeric ops on possibly-NaN values (parsed inputs, `parseInt` failures).
- Contract drift: `main.js` calls `this.detector.detectForVideo(...)` when the class only exports `detect()`. Wrapped in a try/catch that logs and continues, the app silently does nothing.

**2. Error paths that swallow or misreport**
- `setStatus('error')` with no path back to `'idle'`; the UI is gated on status and now permanently locked.
- `setErrorMsg(...)` set but never cleared on retry.
- `try { ... } catch (e) { console.error(e); }`, error never reaches the user.
- `async` functions that throw inside but the caller `await`s and doesn't handle.
- `Promise.all` where one rejection hides the others.
- Raw API JSON passed through as the error message.
- Loading spinners tied to a state variable not reset in every path.
- Try/catch wrapping a whole frame loop, continuing into broken state.

**3. Edge cases on user input**
- `files[0]` from a multi-file drop or paste, rest silently ignored.
- Handlers branching on `.endsWith('.json')` while the UI accepts other extensions.
- MIME type from the browser trusted without sniffing.
- Text inputs with no max length sent to APIs that charge by token.
- Empty-string inputs not rejected before the API call.
- Optimistic UI updates that don't roll back on failure.
- IndexedDB / localStorage quota, version-block, private-browsing failures.
- HMR / React StrictMode double-renders triggering side effects twice.

**4. Resource leaks**
- `URL.createObjectURL(...)` without `URL.revokeObjectURL(...)`.
- Listeners added in `useEffect` or a constructor without cleanup.
- `setInterval` / `setTimeout` with no clear.
- `requestAnimationFrame` loops where the id is not stored, so `stop()` can't cancel; each start leaks a loop.
- `new Worker(...)` without `.terminate()`.
- `IDBDatabase` opened per call instead of a reused singleton.
- Three.js / WebGL: `geometry`, `material`, `texture`, `renderer` `.dispose()`, usually one missing.
- Event-bus subscriptions never unsubscribed; return handles never stored.

**5. Concurrency hazards**
- Double-click on an async button: `setStatus('busy')` isn't synchronous, so a fast second click fires first. Needs a synchronous ref guard.
- `setState` after `await` in a handler on an unmounted component. Needs a mounted ref or `AbortController`.
- Two tabs racing on shared storage.
- Stale closures: handlers outside `useCallback` capturing old state.
- Effects with missing dependencies re-running with stale values.
- Optimistic local writes overwritten by a slower server response that started earlier.
- File watcher fires during a partial write and broadcasts a half-parsed config to all SSE clients.

**6. Security boundary holes (server / HTTP only)**
- Auth middleware on read routes but missing on the write route that mutates the same state.
- CORS regex with unescaped metacharacters: `http://localhost:*` matches `http://localhostXcom`.
- Path traversal: a filesystem path built from request data, where `startsWith(dir)` without `path.sep` lets `dir_evil/` escape.
- Secrets returned by a config endpoint that serializes the whole YAML, or served under a public static mount.
- `fs.watch` that crashes the process if the path is absent at startup.
- `yaml.load` returns `null` for an empty file without throwing; `config: null` broadcast to all clients.
- A rate limiter applied by prefix that throttles long-lived SSE streams.

## Known fabrication patterns

Seen at roughly one in three to five "Critical" claims on the models this skill
was written against. Check for these first when promoting a finding.

- *"Method X doesn't exist"*: the agent grepped the wrong file or missed an alias.
- *"This produces NaN forever"*: control flow traced wrong; the branch they think runs doesn't.
- *"Race condition loses data"*: missed that JS variable rebinding doesn't mutate the original array, or that an async body runs synchronously until its first `await`.
- *"Path traversal"*: didn't see the guard one call up the stack.
- *"Pause/resume is broken"*: misread a falsy-or-null guard as truthy.

## Worked examples

Include two or three in the agent prompt when the surface matches.

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
