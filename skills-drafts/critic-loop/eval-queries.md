# Candidate triggers — critic-loop

For the eventual `trigger-eval.json`. Mark expected: **fire** / **no-fire**.

## Should fire

- "Does this actually read as an A-10 or am I too close to it?" — fire
- "I've stared at this README so long I can't tell if it makes sense. Can I get fresh eyes?" — fire
- "Run a critic round on the landing page" — fire
- "Would a stranger know what this screen is for?" — fire
- "Set up a review loop for the pitch deck — I want to iterate against someone who hasn't seen it" — fire
- "Is this spec persuasive? I can't judge it anymore" — fire
- "/critic-loop" — fire
- "I keep flipping on whether the nacelles are too high. Can we get a blind read?" — fire
- "This build is supposed to look like the reference image — how faithful is it, honestly?" — fire (fidelity read)

## Should not fire

- "Review this PR for bugs" — no-fire (test-shaped; code-review / robustness-audit)
- "Do the tests pass?" — no-fire (has a test)
- "Is the overlap count zero?" — no-fire (has a wall)
- "Grill me on this plan before I build it" — no-fire (grill)
- "Summarise the feedback from the last round" — no-fire (reading, not running)
- "Write a rubric for grading essays" — no-fire (the rubric is an input to the loop, not the loop)
- "Which of these three logos is better?" — no-fire on its own; ambiguous — selection among samples is §5's cherry-pick guard, not a round. Ask whether they want a loop or a pick.

## Ambiguous — decide

- "Get a second opinion on this design" — probably fire if "design" is a visual/prose artifact
  with no test; no-fire if it is an architecture decision (that is a discussion, not a loop).
- "Does this look good?" — the unfalsifiable gate the skill exists to replace. Fire, and the
  first thing the skill does is restate the question as identity / function / fidelity.
