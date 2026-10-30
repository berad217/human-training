---
name: coordinator
description: One session coordinates several working sessions ("workers") for one human. It plans and queues the work, routes every question into one decision list, merges through an integration round and keeps the shift's state on disk. Two roles. The COORDINATOR role runs only when the human selects it explicitly, via /human-training:coordinator (Claude Code) or $human-training:coordinator (Codex). When the human says they are leaving while workers are running, offer it in one line and run it only on a yes. The WORKER role: invoke this skill whenever you are told that another session is your coordinator, or that you are a worker (or lane) in a coordinated shift, and read only worker.md.
---

# Coordinator

This skill has two roles. Read the file for yours and nothing else.

- **You run point.** The human selected this skill to coordinate other sessions.
  Read [coordinator.md](coordinator.md). It links reference.md and evidence.md
  for when you need them.
- **Another session runs point.** The human, your brief or your project's memory
  says another session is your coordinator, or that you are a worker (older
  briefs say "lane"). Read [worker.md](worker.md) only. It is short on purpose:
  the coordinator's dials, budget and round mechanics are its job, not yours.

Not sure which you are? You are a worker unless the human asked *you* to
coordinate.
