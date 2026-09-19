# Handover — reference

Lookup material for the handover guide. Nothing here is required reading; each
section is pointed at from the step that needs it.

## Where docs usually live (Step 1)

When `onboarding.md` has a map, the map wins. Otherwise glob for these:

- onboarding: `onboarding.md`, `docs/onboarding.md`, `docs/.agents/onboarding.md`,
  `.agents/onboarding.md`, `.claude/onboarding.md`
- handover: `HANDOVER.md`, `docs/.agents/current-handover.md`,
  `.agents/current-handover.md`, `.claude/current-handover.md`, `docs/handover.md`
- spec: `spec.md`, `SPEC.md`, `docs/spec.md`, `documentation/spec.md`
- context: `CONTEXT.md`, `docs/CONTEXT.md`
- devlog: `DEVLOG.md`, `docs/DEVLOG.md`, `docs/devlog.md`
- global preferences (legacy): `docs/.agents/global-preferences.md`,
  `.agents/global-preferences.md`, `.claude/global-preferences.md`

## What each doc holds (Step 2)

| Document | Contains | Does not contain |
|---|---|---|
| Spec | what to build, decisions made | decisions still in flight |
| DEVLOG | what was built and why | current discussions, unsolved problems |
| Code | the implementation | why this approach over the ones discussed |
| CONTEXT.md | the project's vocabulary | plans, decisions, implementation |
| **Handover** | **conversation state** | anything the above already hold |

## Example: a good handover

```markdown
# Handover - Quiz App

## 1. Orientation
New AI: Oriented via onboarding.md. We are in Implementation, midway through Sprint 3.

## 2. The Delta
- **Active Debate**: Extracted the `QuizEngine` (src/quiz/engine.ts). User is unsure
  if a pure class is too disconnected from React state. Weighing a `Zustand` store
  as an alternative; not started.
- **Failed Path**: Lifting state to the `App` component caused a render loop. Don't.
- **In-Flight**: Engine extracted but tests fail on the Q1 -> Q2 transition.

## 3. Next Steps
1. Debug `engine.test.ts` question transition failure.
2. Decide Zustand vs the class approach.
```

Points at docs without duplicating them; captures the discussion and what was
tried; flags the decision that needs making; specific next steps; names the
known breakage.

## Example: the handover that looked perfect and wasn't (Step 0)

A real one. It is the reason Step 0 exists.

```markdown
## 1. Orientation
Clean stop - nothing in flight, all work committed in both repos
(Blendy `22e36f1`, Blocky `6854e21` at time of writing).
```

Accurate. Precise. Cited SHAs. **Both SHAs were unpushed local tips.** Eight
commits across two repos lived on a single disk for a day, found only because
a later session ran `git push` for an unrelated reason and watched a
four-commit range fly past.

Nothing was *false*. The failure is that a confident, specific claim of safety
**stops the next agent from checking**. A vague handover would have prompted a
look; this one guaranteed nobody would. With Step 0 the line would have read
`**Durability:** Blendy ahead 4, Blocky ahead 4 — NOT pushed.` and the work
would have been safe within the minute.

The word "committed" is the trap: in prose it means "written down"; in git it
means "on this disk". The guide's rule is phrased as "lands in a file" for that
reason.

## First-agent bootstrap (no docs exist yet)

- Create `onboarding.md` with doc locations, workflow, and how to write handovers.
- Create a `DEVLOG.md` skeleton and note the initial sprint.
- If global preferences are provided, save them where the project already keeps
  agent docs (`docs/.agents/`, else `.agents/`).
- If no spec is needed (meta project), say so explicitly; otherwise create `spec.md`.
- Write a minimal `HANDOVER.md` capturing what you set up and any open decisions.

## Fresh-context pickup (later agents)

- Read `onboarding` → `handover` → `spec` → `DEVLOG`.
- Verify the build immediately.
- Prune the handover if your first tool call made part of it obsolete.
- When the conversation gets long, offer: "Should I write a fresh handover and
  reset our context to keep things fast?"

## History

- 2026-07-24: Step 0 (durability) added after the Blendy/Blocky incident above.
- 2026-09-19: guide trimmed 2,348 → ~1,150 words. Anti-pattern lists folded
  into the steps they guard; examples, path lists and checklists moved here.
  Two additions from the queue: the `wip:` commit is mandated before writing,
  and the incoming section now says a pickup is an inheritance — verify the
  build, don't re-derive the decisions.
