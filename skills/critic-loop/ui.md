# UI hill climb

Use when the remaining question is what a stranger can find, understand or
want to use: a desktop app, web app, game menu, settings screen or dashboard.
Especially useful when several layouts could work and the author has learned
every route. Correctness stays in tests. This mode adds a perceiver to the
search; [SKILL.md](SKILL.md) still owns §0 approval, independence and logging.

**Evidence:** one subject, Bricky's family-game start screen, round logs 0–11
(2026-11-09). The worked example below is measured; transfer to other UIs and
the added walls are proposals to adapt and prove, not twelve independent runs.

## 1. Build the instrument before buying opinions

Make one HTML mockup engine render **every screen and state from data**.
Store options, assets, accepted choices, preview, focus, destinations and
input transitions explicitly. A variant changes data or layout on that
engine. Give each state a stable id and each variant an immutable snapshot.
Use real content and assets where available: short placeholder labels and
empty collections make a layout look cheaper than it will be.

The engine should emit a screen manifest, rendered pictures, route traces
and wall results. Assert the expected screen count and wait for fonts and
images before capture. Hash the pictures actually sent, not just the HTML.
Change something visible in round zero and prove the export changed. Keep
the incumbent's pictures so a later CSS edit cannot silently redraw it.

### Walls — every screen, every variant, before any critic is paid

Specify thresholds and how to measure them in §0. A screenshot of the happy
path is not an all-screen check. Run the state × viewport × supported-input
matrix; an unrun cell is a gap, not a pass.

| Wall | Build the check |
|---|---|
| Layout and overflow | DOM bounds against viewport/safe area; scroll sizes **and text-range bounds** for truncation; clipping and unintended overlap; hit-test action centres to catch occlusion. Render open overlays, long labels, last pages and empty states. |
| Contrast and size at viewing distance | Computed text sizes and contrast against the actual backdrop, including art, focus and selection states; minimum icon, badge and target sizes. For pictures/gradients, sample the render or require a measured backing plate. Calibrate on the target display at its viewing distance; a CSS floor alone does not prove legibility. |
| Input reachability | Replay each supported method separately: mouse hit targets; keyboard focus, activation and escape/back; touch taps, target spacing and scroll; gamepad focus, directions, confirm/back and paging. Traverse the transition graph; reject dead ends, hidden focus and hint/action mismatches. A drawn grid must navigate spatially. Mark unsupported methods in §0. |
| Destination and content coverage | Compare rendered ids **and reachable states** with the authoritative inventory: every destination, option, mode, category and page. Check selected, focused, previewed and returned states; presence in data alone is insufficient. Include a route to the farthest item. |
| Image aspect and crop | Check loaded dimensions, source/render aspect and fit policy, including CSS backgrounds and SVGs. Reject unapproved stretching; inspect crops at every card shape. Composite art with text or rule badges needs protected bounds: `cover` can preserve aspect and still cut the information away. |
| State and fixture integrity | Replay preview → accept → back → return. Browsing must obey the declared commit rule and preserve unrelated choices. Assert fixture population and expected visible items; an empty recent-items bar passes overflow checks while testing nothing. Test its intentional empty state separately. |

These checks precede the subjective lines. Reachability is measurable;
**findability** still needs a stranger. Likewise, passing a size floor does
not prove that a badge reads from a sofa. Any new deterministic defect found
by a critic becomes a wall before another round. Fix known defects in the
free inner loop, then inspect the whole rendered set yourself.

### Task routes — numbers, not “easy to reach”

Choose core tasks with the human: the default action, a changed setup, a
secondary destination, a farthest item, and recovery/back. Record the exact
starting state, including focus and saved choices. Count every click, tap,
key or pad press, including navigation and confirmation. Declare how scroll,
holds or typing are counted. Give shortcut and ordinary routes separately.

| Task / start state | Input | Exact action sequence | Steps | Steps needing reading | Result |
|---|---|---|---:|---:|---|
| <core task, saved state, initial focus> | <mouse / keyboard / touch / pad> | <replayed actions> | N | R | <destination and accepted state> |

Derive counts from the same transitions the mockup uses; replay them and
assert the result. Report them every round. Set hard caps only where the
product needs them; a shorter route can still be harder to discover. The
critic identifies which decisions require reading and why; keep that claim
separate from the measured press count. Never trust a caption's arithmetic.

## 2. Pre-commit the rubric and gate

Adapt these lines to the audience and actual tasks, then freeze the weights.
The questions concern what the user can perceive; the walls prove mechanics.

| Starter line | Weight | What the critic judges |
|---|---:|---|
| Obviousness | 20 | Is the first useful action apparent, and does it promise the right result? |
| Reach | 20 | Can a stranger find the core tasks, secondary destinations and unusual options? |
| Audience fit | 20 | Does the choice structure suit these users' knowledge, reading and attention? |
| Readability at viewing distance | 15 | Can the user distinguish content, state and consequences on the target display? |
| Input fit | 15 | Do focus, hints and spatial layout explain how this input method works? |
| Looks | 10 | Does the visual language belong to this product and carry its hierarchy? |

Keep **want/20** separate: would the intended user want to act on this screen,
shown it alone? Score the existing UI as the floor to beat; a good exemplar
can also calibrate a ceiling. Do not add new questions to the /100 halfway
through. Record a new scale separately if a new quality matters.

**Blind half:** two fresh critics get the UI, without target, brief, rubric,
captions or prior rounds. Ask what it is for, what they would do first and
what would happen. Give a task in user terms without naming its route or
controls; ask for the exact actions and every destination they can find.
Both must produce routes that replay successfully and find the pre-committed
destinations. Name mandatory rare destinations in the private gate, not in a
hint to the critic. Ask confidence, reading-dependent steps and leak channels.

**Informed half:** two other fresh critics get the target, rubric, complete
screen set, factual captions and named changes. Both must report **no
criticals or majors**. Define severity in §0: a critical blocks or misdirects
a core task; a major makes a core route, destination or consequence hard to
find or understand. Preserve disagreement; the author cannot vote a major
away to pass. A stricter gate is valid if agreed before the run.

Both halves must pass. A high total is not a gate verdict.

**Static-flow limit:** ordered pictures can hand the critic a solved route.
Prefer a navigable mockup starting at the first screen when testing discovery.
If only stills are available, include competing destinations and ask where
the route is inferred. Label the result a route read from stills, not observed
usability. Never accept an impossible press sequence because its choices are
right. Model critics are proxies; they do not establish behaviour in real users.

## 3. Search wide, then climb

1. **Round zero:** judge the existing UI on the same instrument. Prove export,
   leak guards, wall matrix and route replay before judging new directions.
2. **Start with 2–4 divergent directions.** Change information structure, not
   just colours. Run the free inner loop on each, then the same critic reads.
   Pre-commit when to prune and the floor each survivor must beat on rubric
   and want. Keep directions distinct long enough to answer their questions.
3. **Put branch points to the human.** Make a side-by-side page with the same
   viewport, all screens available, core routes/counts, per-line vectors,
   gate failures and the actual trade to decide. Keep captions here. Recommend
   a branch; record the ruling and its reason before changing the structure.
   Critic consensus is evidence for that decision, not authority to make it.
4. **Climb one variant at a time.** Freeze the selected branch's best so far.
   Build the next candidate from it plus the critics' ranked top issues,
   priced against the whole rubric. Take a coherent batch; name what changed,
   what was declined and what each change should improve. Run every wall,
   replay routes, inspect every screen, then buy the next round.
5. **Must beat the best, or stop.** Compare the same instrument's mean /100,
   with want, both gate halves and each line beside it. A tie or regression
   ends this climb; keep the incumbent. A failed wall cannot be a winner; a
   new critical or lost blind route blocks promotion even if the total rises.
   Set any minimum improvement/noise margin in §0. Do not keep going because
   the latest loser beats the previous loser. A human may approve a new
   structural trial or a bounded repair exception; log it as such, not a win.
6. **A line stuck for three rounds is a structural question.** Name the
   unchanged deficiency and its limiting cause. Propose a different grouping,
   hierarchy, navigation model, asset or toolkit capability. Put a real trade
   to the human with pictures; if it cannot change, stop with the gap priced.
   Another badge or spacing tweak does not reset the plateau.

Budget the breadth phase and climb explicitly. Four reads per variant means
three directions cost twelve reads, even if the project calls that one round.
Quote expected calls and local cost/time; do not inherit another project's
token estimate. Fix a maximum number of evaluated variants/rounds and the
pruning checkpoint before starting. Lost, contaminated or unreadable reads
are re-run and logged; extensions and restarts need a human ruling. Stop at
the gate, the non-improvement rule, a ceiling or the budget. Never spend the
remaining allowance merely because it exists.

Log **each critic's per-line vector**, mean and spread every round, with
want, gate halves, exact routes/counts, reading steps, wall report, artifact
hashes, ranked issues, author choices and human rulings. Keep incumbent and
candidate side by side. On stopping, deliver the best artifact, comparison
page and priced open list. A final safe fix is unreviewed until checked again;
rerun walls and do not attach the old score to new pixels.

## 4. Codex or any model as critic

Use four independent, fresh contexts: **two blind and two informed reads in
parallel**, with no conversation shared between them. An inherited project
instruction can leak the answer; isolate the critic's working directory and
inputs and verify what context it receives. No source, job file or prior
scores. Neutral numbered images in a content-addressed directory; strip
metadata and assert that paths and wrapper text do not name the variant or
explain its intent. The UI's own labels stay: those are what the user sees.

Captions go **only to informed reads**. They explain states and transitions,
not how good the design is. Remove variant letters, decision ids and computed
route totals; ask the critic to count. Prove the critic can access its inputs
in the actual sandbox. If a caption file is blocked, put its text inline in
the informed prompt. Request tables first and a bounded answer, then ranked
issues, named changes judged matched/short/overshot, and numeric answers to
the hardest route questions. Keep read failures separate from UI failures.

Parallelism is the default protocol; if the launcher cannot safely run calls
concurrently, serialise independent fresh processes and record the limitation.
Keep model, effort and presentation fixed. On an instrument change, re-score
the incumbent before comparing. Scores from different models do not transfer.
The Bricky Codex rounds ran serially; this reference does not claim otherwise.

## 5. Filled harness — Bricky start screen

Compressed from the 2026-11-09 record; a family game, no children's names.

| Parameter | What ran |
|---|---|
| Presentation | Data-driven HTML; static 1920 × 1080 PNGs with pad focus, route set blind, all states plus captions informed. Real ride/place art, fonts and palette. |
| Task | Replay the last game; configure a fire truck in Wreck town at night; find Garage, character, Photos, Build, Options and God mode. Inventory: 53 rides, 16 places plus My map, 4 skies, 5 modes. |
| Rubric | Straight in 20 · Reach 20 · Young user 20 · 10-foot readability 15 · Pad 15 · Looks like the game 10; want/20 separate. |
| Gate | Both blind reads give a working task route and find at least 5/6 destinations, with God mandatory by amendment. Both informed lists have nothing above marginal — stricter than the starter gate. |
| Walls | Text ≥26 px at 1080, labels 32+; contrast 4.5:1 (3:1 at 32 px+ bold); no truncation/occlusion; 3.5% action-safe frame; one lit item; real pad hints; inventory coverage. Press counts reported, not a pass mark. These are this display's thresholds. |
| Budget | Initially four rounds across A/B/C, twelve fresh reads a round. Prune after round 2 if at/below control on rubric or want; stop if top improvement <3. Later trials and climbs authorised separately. |
| Human rulings | Shelves in the island direction's visual language; retain two God routes; later try Change it first, then one step at a time. Mockups for selection before production implementation. |

The search went A/B/C (activities, shelves, islands), D/E/F (three ride
groupings), then G, H, I, J, K, L. Control **46.5**; F **79**; G **75.5**;
H **76**. H's small recovery did not beat F, so that climb stopped and F/H
went to the human. This is the earned stop rule, not an uninterrupted ascent.

Human-authorised trials resumed. On changing to Codex, H was re-read at
**82.5**, rather than comparing I's **83** to H's old **76**. J **82.5** and
K **84** led to L **89**, whose vector was **[20, 17, 16, 12, 14, 10]**;
both informed reads agreed on every line. The control-to-L figures describe
the record, not a calibrated 42.5-point gain across instruments. L still
failed the informed gate on two majors. Readability stayed at 12 for the
last three rounds: a plateau inside an improving total.

L's main route was **12 pad presses, 0 needing a word**:
`Right, A, Down, A, Down, Right, A, A, A, Right, A, A`.
Start on the Night preview made it 11. Replay was 1; the first-screen God
door was 2. Those are separate routes, not interchangeable count claims.

## 6. Failures that should become walls

| Observed failure | Guard to build before repeating it |
|---|---|
| Captions under-counted a ride buried seventh in a shelf (round 3) | Replay transitions; count actions from the graph, not prose. |
| Coverage was complete, but a selected-and-focused sky state had no picture (round 4) | Coverage over states and interactions as well as item ids. |
| Browsing a foreign place changed the accepted game (G) | Assert preview/commit/back invariants and preservation of unrelated choices. |
| A drawn 2×2 grid moved in reading order (K) | Compare directional transitions to rendered geometry; replay Down, not just the scripted happy route. |
| L's banner cropped/stretched composite explosion-and-clock art; every wall passed | Aspect/fit and protected-content checks at each use, then inspect every render. This guard is proposed, not shown passing in the record. |
| M's empty bars — **reported in this job; unverified in supplied logs 0–11 and A–L harness** | Populated fixture assertions and a separately tested empty state. Proposed guard; no M score claimed. |
| Export called the new K “control” and produced old shots (caught before round 10 reads) | Unique variant ids, expected set count, content hashes and a visible export probe. |
| Blind critics traced the supplied walkthrough; informed captions were sandbox-blocked (H/I) | Test discovery from the first state; verify input access before launch. Label still-image inferences. |

Primary record: `docs/.agents/start-screen-110.md`, its `critic/00-round-0.md`
through `11-round-11.md`, `mock.html`, `data.js`, `dir-d.js`, and
`Scripts/probes/screens_critic.ps1` / `codex_critic.ps1` in the source project.
The supplied HTML shell references shared renderer/wall files and assets not
included in this bundle; wall/coverage outcomes above are the logs' reports,
not an independently rerun harness. No private paths or captures are needed
to apply the method.
