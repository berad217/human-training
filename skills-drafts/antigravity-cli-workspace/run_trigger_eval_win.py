#!/usr/bin/env python3
"""Windows-safe trigger evaluation for a skill description.

Faithful re-implementation of skill-creator's run_eval.run_single_query, but
replaces the POSIX-only `select.select()` on a pipe (which throws WinError 10038
on Windows) with `subprocess.communicate(timeout=...)` + full-stream parsing,
and uses threads instead of a process pool. Detection semantics are identical:
a trigger = Claude invokes the `Skill` tool (skill name contains clean_name) or
`Read`s a path containing clean_name, for the uniquely-named proxy command.
"""

import argparse
import json
import os
import re
import subprocess
import sys
import uuid
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path


def parse_frontmatter(skill_md: Path):
    text = skill_md.read_text(encoding="utf-8")
    m = re.search(r"^---\s*\n(.*?)\n---\s*\n", text, re.DOTALL)
    fm = m.group(1) if m else text
    name = re.search(r"^name:\s*(.+)$", fm, re.MULTILINE)
    desc = re.search(r"^description:\s*(.+)$", fm, re.MULTILINE)
    return name.group(1).strip(), desc.group(1).strip()


def run_single_query(query, skill_name, description, project_root, model, timeout):
    unique_id = uuid.uuid4().hex[:8]
    clean_name = f"{skill_name}-skill-{unique_id}"
    commands_dir = Path(project_root) / ".claude" / "commands"
    command_file = commands_dir / f"{clean_name}.md"
    try:
        commands_dir.mkdir(parents=True, exist_ok=True)
        indented = "\n  ".join(description.split("\n"))
        command_file.write_text(
            f"---\ndescription: |\n  {indented}\n---\n\n# {skill_name}\n\n"
            f"This skill handles: {description}\n",
            encoding="utf-8",
        )
        cmd = ["claude", "-p", query, "--output-format", "stream-json", "--verbose"]
        if model:
            cmd += ["--model", model]
        env = {k: v for k, v in os.environ.items() if k != "CLAUDECODE"}
        proc = subprocess.Popen(
            cmd, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL,
            cwd=project_root, env=env,
        )
        try:
            out, _ = proc.communicate(timeout=timeout)
        except subprocess.TimeoutExpired:
            proc.kill()
            out, _ = proc.communicate()
        text = out.decode("utf-8", errors="replace") if out else ""
        for line in text.splitlines():
            line = line.strip()
            if not line:
                continue
            try:
                event = json.loads(line)
            except json.JSONDecodeError:
                continue
            if event.get("type") == "assistant":
                for ci in event.get("message", {}).get("content", []):
                    if ci.get("type") != "tool_use":
                        continue
                    tn = ci.get("name", "")
                    ti = ci.get("input", {}) or {}
                    if tn == "Skill" and clean_name in str(ti.get("skill", "")):
                        return True
                    if tn == "Read" and clean_name in str(ti.get("file_path", "")):
                        return True
        return False
    finally:
        if command_file.exists():
            command_file.unlink()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--eval-set", required=True)
    ap.add_argument("--skill-md", required=True)
    ap.add_argument("--description-file", default=None,
                    help="Override description (plain text file)")
    ap.add_argument("--model", default=None)
    ap.add_argument("--runs", type=int, default=3)
    ap.add_argument("--workers", type=int, default=8)
    ap.add_argument("--timeout", type=int, default=90)
    ap.add_argument("--threshold", type=float, default=0.5)
    ap.add_argument("--out", default=None)
    args = ap.parse_args()

    skill_md = Path(args.skill_md)
    skill_name, description = parse_frontmatter(skill_md)
    if args.description_file:
        description = Path(args.description_file).read_text(encoding="utf-8").strip()

    project_root = skill_md.resolve().parent
    for parent in [project_root, *project_root.parents]:
        if (parent / ".claude").is_dir():
            project_root = parent
            break

    eval_set = json.loads(Path(args.eval_set).read_text(encoding="utf-8"))
    print(f"Skill: {skill_name}  |  project_root: {project_root}", flush=True)
    print(f"Queries: {len(eval_set)} x {args.runs} runs, model={args.model}\n", flush=True)

    tasks = []
    with ThreadPoolExecutor(max_workers=args.workers) as ex:
        fut_to_item = {}
        for item in eval_set:
            for _ in range(args.runs):
                fut = ex.submit(run_single_query, item["query"], skill_name,
                                description, str(project_root), args.model, args.timeout)
                fut_to_item[fut] = item
        triggers = {}
        items = {}
        done = 0
        total = len(fut_to_item)
        for fut in as_completed(fut_to_item):
            item = fut_to_item[fut]
            q = item["query"]
            items[q] = item
            triggers.setdefault(q, [])
            try:
                triggers[q].append(bool(fut.result()))
            except Exception as e:
                print(f"Warning: query failed: {e}", file=sys.stderr, flush=True)
                triggers[q].append(False)
            done += 1
            if done % 5 == 0 or done == total:
                print(f"  ...{done}/{total} runs complete", flush=True)

    results = []
    tp = fp = tn = fn = 0
    for q, tr in triggers.items():
        item = items[q]
        rate = sum(tr) / len(tr)
        should = item["should_trigger"]
        fired = rate >= args.threshold
        passed = (fired == should)
        if should and fired: tp += 1
        elif should and not fired: fn += 1
        elif (not should) and fired: fp += 1
        else: tn += 1
        results.append({"query": q, "should_trigger": should,
                        "trigger_rate": round(rate, 3), "fired": fired, "pass": passed})

    precision = tp / (tp + fp) if (tp + fp) else 0.0
    recall = tp / (tp + fn) if (tp + fn) else 0.0
    accuracy = (tp + tn) / len(results) if results else 0.0
    f1 = (2 * precision * recall / (precision + recall)) if (precision + recall) else 0.0

    print("\n================ RESULTS ================")
    print(f"accuracy={accuracy:.2f}  precision={precision:.2f}  recall={recall:.2f}  f1={f1:.2f}")
    print(f"TP={tp} FP={fp} TN={tn} FN={fn}\n")
    print("FAILURES:")
    any_fail = False
    for r in sorted(results, key=lambda x: (x["pass"], x["should_trigger"])):
        if not r["pass"]:
            any_fail = True
            kind = "FALSE-NEG (should fire, didn't)" if r["should_trigger"] else "FALSE-POS (shouldn't fire, did)"
            print(f"  [{kind}] rate={r['trigger_rate']}  {r['query'][:90]}")
    if not any_fail:
        print("  (none)")
    print("\nPER-QUERY:")
    for r in results:
        tag = "+" if r["should_trigger"] else "-"
        ok = "PASS" if r["pass"] else "FAIL"
        print(f"  {tag} rate={r['trigger_rate']:.2f} {ok}  {r['query'][:80]}")

    payload = {"skill_name": skill_name, "description": description,
               "metrics": {"accuracy": accuracy, "precision": precision,
                           "recall": recall, "f1": f1,
                           "tp": tp, "fp": fp, "tn": tn, "fn": fn},
               "results": results}
    if args.out:
        Path(args.out).write_text(json.dumps(payload, indent=2), encoding="utf-8")
        print(f"\nWrote {args.out}")


if __name__ == "__main__":
    main()
