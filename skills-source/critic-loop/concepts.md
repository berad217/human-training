# Concepts first: breadth as pictures, then code

Use when the directions you want to compare are expensive to build: a HUD,
a menu, a screen, an icon set, a livery, a layout. Building each variant in
code (or in the [ui.md](ui.md) mockup engine) costs engineering, so breadth
stays narrow and every direction comes out of the author's own habits. A
climb from there polishes a local maximum, however many rounds it runs.

A painted concept costs a minute. Paint the breadth, pick a short list, then
build only the survivors. The `human-training:image-gen` skill is
the tool; this file is the method. [SKILL.md](SKILL.md) still owns §0
approval, independence and logging.

## The steps

1. **Anchor on the real thing.** Attach a capture of the actual screen or view
   (image-gen's Edit, `-i`) so every concept sits in the real composition,
   camera and palette. Name the medium's look in the prompt (a toy-brick game,
   a medical dashboard). Ask for one direction per image, each named by its
   idea ("edge tapes", "twin arcs"), not N variations of one.
2. **The spec is a wall, not a hint.** Write what the concept must show and
   what it must not. The "must not" list matters more: an image model happily
   restores the clutter the human just rejected. The critic checks the list
   before scoring; a concept that adds an unrequested element fails the wall
   whatever it scores.
3. **Critique the pictures blind,** on the rubric lines the build will be held
   to, plus one desirability question asked of a stranger in the role ("would
   this ship in a top-tier product of this kind?"). Advance two or three.
   Revise those by img2img with the critics' fixes. Edits drift cumulatively,
   so cap the concept rounds in §0 (two is plenty) and repeat the invariants
   every round.
4. **Put the short list to the human** side by side (ui.md §3, step 3), each
   with what the still cannot show. A critic pick against the author's eye is
   said on the page, not settled quietly.
5. **Translate before building.** Write the chosen concept down as something
   code can meet: placement as fractions of the viewport, sizes at the
   shipping resolution, palette tokens, every state (idle, active, warning,
   empty), motion intent. List what the picture promised that the toolkit
   can't cheaply do (glows, blurs, invented fonts, garbled numerals) and pick
   the substitute now, not mid-build.
6. **Build, then read fidelity.** Capture the built screen beside the chosen
   concept and run a fidelity read (both side by side, informed) before the
   ordinary climb resumes on the build.

## What a still can't tell you

A concept is never the artifact, and no score a concept earns transfers to the
build. The build's walls still run on the build: the worst-case backgrounds
behind an overlay (bright sky, snow), motion, scale at the shipping
resolution, safe areas and the toolkit's actual rendering. Text in a concept
is decoration; never take wording or numbers from it.

## Coming back for more breadth

A line stuck for three rounds (ui.md §3, step 6) is a structural question, and
a fresh concept round is the cheapest way to look for a different structure.
Run it on the incumbent's capture with the stuck line named in the spec.

## Evidence

One subject: a vehicle-cockpit side HUD in the same family game as ui.md's
start screen (2026-11-15). The first coded direction was rejected by the human as "just a
box with some text". Four painted directions over a real cockpit capture; a
blind critic in the role of a top-tier UI lead advanced two; both were revised,
with throttle-only ground-vehicle versions added; a second blind critic picked
one with three named fixes. The author's eye preferred the runner-up and said
so on the page. Steps 1–4 are observed. Steps 5–6 (translation and the
fidelity read) are proposed guards that have not yet run; the first build
through them rewrites this paragraph.
