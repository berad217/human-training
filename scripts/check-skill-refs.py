#!/usr/bin/env python3
"""Check that cross-skill references and the manifest description stay honest.

Written as the rung-4 proof for a blast-radius run on commit 74abd58, the
show-me-your-work extraction. It failed on first run: 1.23.0 shipped without
adding the new skill to plugin.json's hardcoded description. Kept because the
gap it covers is invisible to verify-plugin-manifests.py.

The safety fact under test: a `human-training:<skill>` reference written in one
shipped skill resolves to a skill the reader actually has, because every skill
ships from one skills/ directory as a unit.

Exits non-zero and names the offender if the fact is false. Re-runnable.
"""
import io
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

SKILLS = ROOT / "skills"
REF = re.compile(r"human-training:([a-z0-9-]+)")

failures = []

# --- Fact 1: every cross-reference resolves to a shipped skill -------------
shipped = {d.name for d in SKILLS.iterdir() if (d / "SKILL.md").is_file()}
refs = {}
for skill_md in SKILLS.glob("*/SKILL.md"):
    text = io.open(skill_md, encoding="utf-8").read()
    for target in set(REF.findall(text)):
        refs.setdefault(target, set()).add(skill_md.parent.name)

for target, sources in sorted(refs.items()):
    if target not in shipped:
        failures.append(
            f"DANGLING REF: '{target}' referenced by {sorted(sources)} but "
            f"skills/{target}/SKILL.md does not exist"
        )

# --- Fact 2: no skill references itself (a rewrite that lost its target) ---
for target, sources in sorted(refs.items()):
    if target in sources and len(sources) == 1:
        failures.append(f"SELF-REF: skills/{target} references itself and nothing else")

# --- Fact 3: plugin.json's hardcoded skill list matches what ships ---------
import json
desc = json.loads(io.open(ROOT / ".claude-plugin" / "plugin.json", encoding="utf-8").read())["description"]
source_skills = {d.name for d in (ROOT / "skills-source").iterdir() if (d / "SKILL.md").is_file()}
unlisted = sorted(s for s in source_skills if s not in desc)
if unlisted:
    failures.append(
        "STALE DESCRIPTION: .claude-plugin/plugin.json description omits "
        f"session-authored skill(s): {unlisted}"
    )

# --- Report ----------------------------------------------------------------
print(f"shipped skills:        {len(shipped)}")
print(f"cross-references:      {sum(len(v) for v in refs.values())} across {len(refs)} targets")
for t, s in sorted(refs.items()):
    mark = "ok " if t in shipped else "DANGLING"
    print(f"  {mark}  human-training:{t}  <- {', '.join(sorted(s))}")
print()

if failures:
    print(f"FAIL ({len(failures)}):")
    for f in failures:
        print(f"  - {f}")
    sys.exit(1)

print("PASS: every cross-reference resolves and the manifest description is current.")
