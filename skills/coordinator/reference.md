# coordinator — reference

Lookup material for [coordinator.md](coordinator.md). Nothing here is required
reading. Each section is pointed at from the rule that needs it.

## Where the shift files live

Put them in the project repo, so a coordinator on another machine finds them
once they're pushed. Use `docs/coordinator/` if the project keeps working docs
under `docs/`, otherwise `coordinator/` at the root. Onboarding's map overrides
both.

| File | Holds |
|---|---|
| `<date>-order.md` | The shift order |
| `<date>-log.md` | The shift log, append-only |
| `decisions.md` | The live decision list. There is one, across shifts |
| `<date>-return.md` | Each return brief. A new one marks the last one superseded |
| `workers/<worker>.md` | Worker notes |
| `skill-feedback.md` | The skill-feedback list, across runs |

Worker trails follow `show-me-your-work` and stay on each worker's branch.

## Preset checklists

### Night

**Pre-flight.** Send one message with every item already filled in with a
default. The human answers in one reply ("ok", or corrections), and the answers
go to the shift order.

- [ ] The dials, one line each.
- [ ] **Queue:** what's authorized, in priority order, with what done means for
      each; what's out of scope; and what happens when it runs dry. With
      headroom, the queue must outlast the night, so add the machine queue and
      the burn backlog. Without headroom, stop spending when it runs dry.
- [ ] **Grants:** the standing ones confirmed from memory, not asked again;
      this shift's changes written out.
- [ ] **Human-only steps:** find them and probe each dependency now. Can origin
      be reached? Each share? Can a session start where one is needed? Does a
      no-op build run? Does the package step raise an elevation prompt? Each
      "no" is settled before the human goes, or its work moves to their
      return.
- [ ] **Roles:** every worker the night could need is open now, including a
      spare with only a queue. Workers on other machines are opened by the
      human as native sessions.
- [ ] **The machine:** name the gate. Main goes first, gates take the hold
      first, and workers leave gaps. On the human's own box: headless, idle
      priority, a memory floor.
- [ ] **Budget:** the dial's position, the cap, the measured burn rate.
- [ ] **Stop conditions:** the queue is done; the cap is reached; everything
      left waits on the human; the gate goes red twice on the same thing (stop
      fixing forward and park it); the return time arrives.
- [ ] **Return time and the wake-me bar.** The default is never. At most, a
      machine emergency (disk full, runaway memory) or data at risk.
- [ ] **Compaction.** Offer, since these are settings and so the human's call:
      a `# Compact instructions` section naming the shift files, and a
      `SessionStart` hook on `compact` that prints the shift order and the
      log's tail. Leave auto-compact and idle compaction on. Check that
      `autoContinueAtUsageLimit` is on.

**Running.**

- [ ] Wait on events, not the clock: worker reports, background tasks finishing,
      and one long wake-up as a fallback.
- [ ] Write at most one line per event to the transcript. The return brief is
      the real output.
- [ ] Grow the decision list as items appear, so the brief is assembled, not
      reconstructed.
- [ ] Run the review of each round's diff as part of the round.
- [ ] When the token queue ends early, run a machine-bound job of known length
      as the night's tail.
- [ ] Wind down a couple of points before the cap.

**Stopping.**

- [ ] Each worker runs `leroy-jenkins`' pause protocol, or writes its worker
      note.
- [ ] Write the return brief as a file. Post it as the coordinator's first
      message when the human appears.
- [ ] Add up to three skill deltas (coordinator.md §9).

### Away day

- [ ] The check-in times are in the shift order. Time the decision list for
      them.
- [ ] Worker queues are two jobs deep, and veto in play is on.
- [ ] Send at most one push between check-ins, for a ten-second answer that
      unblocks real work. The blocking tier can be answered from a phone, so
      *ask* where a night would *park*.
- [ ] The burn backlog (reviews, docs, audits, jobs for another pool) is ready
      as the day's filler, so workers don't run dry when only the human's calls
      are left.
- [ ] Post the return brief at each check-in, carrying the open asks forward.

### Burn

- [ ] Measure the burn rate: two usage readings an hour apart, with the fleet in
      its working shape. Compute what can actually be spent, and size the
      fan-out to that headroom, not to the backlog.
- [ ] Start the token-bound backlog first. Machine-bound work doesn't absorb
      tokens.
- [ ] Propose and start the burn's sessions while the human is present.
- [ ] Accept big contexts, rewarms and high effort. The waste being avoided is
      expiring quota, not tokens.
- [ ] Leave the output reviewable: drafts, docs, findings and proposals, merged
      after the human's look or a green round, never straight into a release.
- [ ] Send docs-only work to another budget pool if one exists.

### Thrift

- [ ] Run few workers. Compact every idle context while it's warm, or retire
      it.
- [ ] Machine-bound work goes first. Mechanical workers get a cheaper model or
      a lower effort.
- [ ] The coordinator wakes rarely, in batches.
- [ ] Put "thrift" in the first line of each report, so the human knows why
      things are slower.

### Attended day

- [ ] Questions are still batched into the decision list, and veto in play
      still runs.
- [ ] Report the weekly figure, and flag a big spend before starting it. Don't
      pause on the cap alone.
- [ ] Before the human leaves, offer the away or night preset (coordinator.md,
      the invocation line).

## Templates

### Shift order

```markdown
# Shift order: <date>, <preset>

**Attention:** <watching | around | away until <time>> · **Check-ins:** <times, or the return time>
**Budget:** <position, one line> · used <x%> of the week, resets <when> · cap <88% unless the human said otherwise> · measured burn <y% an hour> · plan for the week: <...>
**Machine:** <the gated resource, its gate, who goes first> · **Wake-me bar:** <never | machine emergency or data at risk | blocking tier, one push per gap>

## Queue (priority order)
1. <item>: done means <...>. Worker <name>.
2. ...
**Out of scope:** <...>
**When it runs dry:** <machine queue | burn backlog items | stop spending>

## Grants
<Standing grants confirmed from memory, and this shift's changes. The full table is in the skill's reference.>

## Human-only
<Each step: settled now, or moved to the return with the work that depends on it.>

## Roster
| Worker | Session id | Machine | Branch / worktree | Model, effort | Queue |
|---|---|---|---|---|---|

## Stop conditions
Queue done · cap reached · everything left waits on the human · the gate red twice on the same thing · <return time>.
```

### Worker brief

```markdown
You are worker <name> in a coordinated shift. Coordinator: <session id>.
Invoke /human-training:coordinator; you are a worker.
Read the shift order at <path> first, and again after any compaction.

**Queue** (in order):
1. <item>. Done means <...>.
2. <item>. Done means <...>.
3. <item>. Done means <...>.

**The gate:** <the command that takes the hold, and the one that gives it back>.
**Never, in this project:** <the project's never-list>.
**Branch:** <branch>. **Worker note:** <path>.
**Trail:** <path>, per `show-me-your-work`; decisions under `leroy-jenkins`' overlay.
```

Everything else a worker needs (whose word counts, never waiting, reports, what
goes up) is in worker.md, which the invoke line loads. Don't restate it here.

### Worker note

```markdown
# Worker <name>: note, <date>
**Branch:** <branch> @ <sha> · merged to main: <yes, at <sha> | no>
**Stopped at:** <one line>
**First step on resume:** <one concrete action>
**Knows that isn't in the code:** <gotchas, failed paths, half-made decisions>
**Waiting on:** <decision list item, or nothing>
```

Under a page. This is handover-manager's ephemeral delta scoped to one worker.
If it is in a file already, it doesn't belong here.

### Decision list

```markdown
# Decisions (live; updated <date time>)
Answer by number: "1 yes, 2b, rest as recommended".

## While you're here (needs you in person or your credentials)
- W1. <action>. Needed for <what it unblocks>.

## Blocking (a worker or a release waits)
1. <question>. **Recommend <X>**, because <Y>. Else <Z>. Unblocks <worker or item>.

## The recommendation stands if you say nothing (reversible)
2. <question>. **Recommend <X>**. Settles at <the next check-in>.

## When you like
3. <question>. **Recommend <X>**.

## Changed, veto in play
- <what changed>. Restore with <the switch, or the revert>.
```

Number by what each answer unblocks, with waiting workers first. Mark an item
carried over from an earlier brief as *(open since <date>)*. Prune an item the
moment it is answered or lands.

### Return brief

```markdown
# Return brief: <date time> (supersedes <previous brief>)

**Waiting on you:** while-you're-here items first, then blocking decisions by number. Carried-over asks are marked (open since <date>). The full list is at <path>.
**Landed:** <merges and pushes with SHAs; each round's result in one line>
**Verified, and not:** <results with numbers; anything done but unproven, said plainly>
**In flight:** <one line per worker: where it stopped, its first step on resume>
**Went wrong:** <each failure, and what was done about it>
**Spend:** <weekly x% to y% against the cap; machine time per worker if the box was the bottleneck>
**Cleanup offers:** <items for the trash, awaiting approval>
**Skill deltas:** <up to three, or "none this run">. Feedback list: <path>
```

The human should be able to act on it in two minutes. Keep it to one screen.
Give paths and SHAs, not diffs. Don't re-explain decisions the human already
made, but do flag anything that changed in their world while they were away (a
build ready to copy, a disk filling up). Publish a page per worker only when
there are many workers.

### Roster report

```markdown
## Roster, <time> (<shift start | mid-shift | close | asked>)

**<this machine>**
| Worker | State | Job | Next job | Last report |
|---|---|---|---|---|
| <name> | working / idle / waiting on <X> | <job> | <job, or **none**> | <time> |

**<another machine>**
| <name> | <state> | <job> | <job, or **none**> | per its <HH:MM> report |

**<sub-coordinator name>**, per its <HH:MM> report: its own roster, as one block.

Not managed: <a session the coordinator didn't start or doesn't run, one line each>.
```

- **Build it from the host's listings, not from memory:** the linked-sessions
  list for this machine, `ListAgents` for other machines, and each branch tip
  against the last SHA the coordinator expected. A moved tip is a report the
  coordinator may have missed.
- **A row from another machine says where it came from.** The coordinator sees
  that session's run state, not its work.
- **Idle with no next job is the row to act on.** Give it work, or retire it.
- **Sessions the coordinator doesn't run** (another project, a machine it
  didn't know about) get one line under the table, never a row: listed, not
  managed.
- In a return brief, the roster replaces the **In flight** line.

### Skill-feedback list

```markdown
| # | When | What happened | The rule it suggests | Scope |
|---|---|---|---|---|
| 1 | <date, preset> | <one line, scrubbed> | <one line> | general / preset:<name> / project |
```

The scope test: *general* would hold on a project with no heavy machine, no
second machine, or another host. A *project* row stays in the project and is
never proposed to the skill.

### Skill delta

```markdown
**Delta <n>:** <coordinator.md, worker.md or reference.md>, <section>
**Old:** "<the exact text>"
**New:** "<the exact text>"
**Evidence:** feedback row <#> (<date>): <a scrubbed phrase>. Seen <once | in N runs>.
**Would have saved:** <what, roughly>
```

## Grants

The defaults when the human is away. Grants are per action and per repo. Read
standing grants from project memory and confirm them; don't ask again.

| Action | Default | Notes |
|---|---|---|
| Commit to worker branches | yes | one branch or worktree per worker |
| Merge worker branches into main | after the worker's own checks and a green round | never into a running round |
| Push main | only if granted, standing or for this shift | scan the range for secrets and private material first |
| Push other branches, or anything in **another repo** | no, unless granted for that repo | a grant for one repo doesn't cover another |
| Publish, send, or any other outward-facing action | only from the session holding the human's request | workers stage; the coordinator ships |
| Start sessions | while the human is present | in their absence: existing workers, or background subagents |
| Releases, tags, deploys, packages for others | no | at the human's return |
| Delete | to the trash only, for items pre-listed in the shift order | anything else is a cleanup offer; discarding uncommitted work counts as a delete |
| Messages to people, purchases, accounts, settings, credentials, permissions, elevation | never | |

When the harness refuses something a grant allows: report it, park it, and move
on. Never route the action through another session or tool.

## The worker lifecycle options

Costs are relative to a warm wake of a 400K context. "Small" means a wake after
a compaction to about 50K.

| Option | Cost now | Cost at the next job | Loses | Host mechanism |
|---|---|---|---|---|
| Keep idle, woken within the hour | none | 1 (warm) | nothing | |
| Keep idle, woken after the hour | none | about 40 (cold) | nothing | |
| Idle compaction | a warm read plus a summary | small, about 5 | detail | `idleCompaction`, on by default: the summary is written about 55 minutes into an idle stretch and applied at the next wake |
| `/compact` while warm | a warm read plus a summary | small | detail | typed by the human; a worker can't type it. Untested: whether one sent by message runs as a command |
| `/compact` after the hour | a cold read plus a summary | small | detail | the costly way round |
| Worker note, then clear | one warm turn | a fresh start plus re-learning | everything not in the note | `clear_session` on an idle session this one started. Refused for a session serving Remote Control, a pinned one, or one open on screen |
| Worker note, then archive | one warm turn | a fresh session, on the human's turn only | everything not in the note | `archive_session` |
| A background subagent per job, no worker | the job only | none | its context, since only its summary returns | `Agent` with worktree isolation, startable on any turn |

## The standing burn backlog

This is work that is ready, token-bound and safe to run without the human,
kept as a short list in TASKS. It is pre-approved. One pre-reset burn
used four fresh sessions on the first four items below, and the ideas they
produced became the next week's queues.

- a docs and agent-navigation map, checked path by path;
- a memory index, regrouped;
- a TASKS sweep;
- an ideas document for the project's next areas;
- `robustness-audit` over a recently changed area;
- an independent code review of the week's merges;
- test-gap hunting;
- a DEVLOG read for zombie decisions.

Docs-only items suit a separate budget pool. New findings become proposals for
the human, not new work.

## Workers on other machines

- **Liveness is only half visible.** `ListAgents` shows such a worker as
  running, idle or offline, so check it before sending: a message to an offline
  one won't land. An idle one still sends no turn notes or read receipts.
- **Ask for a "started" line with a deadline** (say 15 minutes). A missed
  deadline means unreachable: tell the human if they're around, otherwise
  reassign.
- **A reassignment needs a stand-down.** The substitute drops its unmerged
  partial work cleanly, and the original resumes from its own branch.
- **A worker started by a message can't start sessions,** so it works in its
  own context, which grows with every job.
- **Keeping a remote worker's context small,** cheapest first: message it only
  when it must act; let idle compaction, or a `/compact` the human types while
  it's still warm, keep it small; or try a *thin dispatcher*, where the worker runs
  each job as a background subagent in its own worktree and only the job's
  summary lands in its context. The thin dispatcher is untested on long gated
  jobs (see Untested, below). Remote Control sessions can't be cleared by
  tool, so a worker past a few hundred thousand tokens is cleared by the human
  on their next visit to that box.

## The machine: a worked pattern

No scripts ship with this skill. These four pieces worked together on one
project. Each is a few dozen lines in whatever the project scripts in. Two
rules sit around them:

- Know which tools start heavy work by themselves, and route them through
  the gate too.
- With a second machine, put the most independent, longest jobs there.

- **The hold-first gate.** Every heavy job calls it first. It writes a hold (a
  file naming the job, its owner, its start time and its expected length)
  *before* waiting. Then it waits for the box to drain (free memory, no other
  heavy process), runs the job, and removes the hold. A pending hold from
  main's round outranks a worker's. Every gate on the box polls at the same
  short interval, seconds rather than a minute. A stale hold (its owner gone,
  or well past its expected length) is broken and logged, never silently
  ignored.
- **The round script.** It takes the hold once and keeps it from the build
  through the gate tests, the regenerated-artifact check and the full suite. It
  writes the full log to disk and filters only for display. It demands the test
  runner's own end marker: a short or unmarked run is a fail. When it is
  derived from the last round's script by edit, diff and byte-check it before
  it runs.
- **The full-bake job.** A long, machine-bound rebuild of derived data, run
  detached under the gate. It hashes every generated collection before and
  after, so the return brief has a proven answer about what changed. Its length
  is known, which makes it the natural tail for a night whose token queue ends
  early.
- **The package job.** It builds what the human will copy or install. It often
  needs elevation or credentials, so probe it in the pre-flight. If it needs
  the human, move it to their return.

## What a wake costs: the measurements

Price ratios at list price, 2026-10: input 1×, cache read 0.05×, 1-hour cache
write 2×, output 5× (thinking counts as output). Priced this way, one project's
transcripts reproduced the client's own cost totals within a few percent. The
plan's quota accounting isn't public, so treat dollars as a weight and
calibrate against the usage meter.

| A wake of a 400K context | Relative cost |
|---|---|
| Warm (last request under an hour ago) | 1 |
| Cold (over an hour) | about 40 |
| Cold, after a warm compaction to about 50K | about 5 |
| A fresh session | the harness prefix (tools, skills, system prompt: tens of thousands of tokens) plus the brief, but it must re-learn the job |

From one project's transcripts, 2026-10-24 to 10-27: one coordinator, about
half a dozen workers, two machines.

- About nine in ten coordinator wakes were injected (worker turn notes,
  messages from other machines, task completions), not the human. Re-reading was nearly all of the
  coordinator's raw tokens and well over half its cost.
- Nearly half the coordinator's wakes were one-request acknowledgements, each
  re-reading the whole context.
- Cold worker wakes were the largest avoidable cost, about a sixth of all
  spend. Over half came in bursts, where one dispatch woke several cold workers
  within minutes. A handful were pure FYIs.
- Workers' own `Monitor` events were most worker wakes, mostly warm
  one-request turns: several percent of spend.
- Compacting while warm made the next rewarm about 8× smaller. Most manual
  compactions of the coordinator were typed after an hour idle, so each paid
  the cold read first.
- The coordinator itself rarely went cold. Its overhead was the injected wakes.
- Machine-bound work burned the weekly meter about six times slower per hour
  than token-bound work.

## Host facts (dated; re-verify before relying on one)

### Checked against the Claude Code docs, 2026-10-25

- **The compaction trigger** is a token count: by default the model's context
  limit (about 967K on the Claude 5 family; 200K on some 4.x models without
  extended context). `CLAUDE_AUTOCOMPACT_PCT_OVERRIDE` (1-100) can only lower
  it, and applies to subagents too.
- **The window:** `autoCompactWindow` (100,000-1,000,000), `/autocompact
  <value>`, `--autocompact`, or `CLAUDE_CODE_AUTO_COMPACT_WINDOW`. A lower
  window caps the worst case but compacts long investigations mid-task. Leave
  the default unless workers keep hitting the full window.
- **Off:** `"autoCompactEnabled": false`, or `DISABLE_AUTO_COMPACT` for one
  session. Don't turn it off for an unattended shift: a session that fills its
  context with nobody there stalls.
- **Steering the summary:** `/compact <focus>`, or a `# Compact instructions`
  section in CLAUDE.md, read at every compaction. Steering it from a
  `PreCompact` hook is not documented.
- **Getting context back:** a `SessionStart` hook with the `compact` matcher
  re-injects context after a compaction. A hook that prints the shift order and
  the log's tail is the most useful single mechanism here.
- **What survives compaction:** root CLAUDE.md, auto memory, background
  commands and background subagents.
- **Idle compaction:** `"idleCompaction": false` turns it off (v2.1.290+). The
  docs describe a session idle for about 54 minutes with 200K+ of context
  being compacted when it next wakes.
- **Cache lifetime:** 1 hour for the main conversation on a claude.ai
  subscription within plan usage. 5 minutes for API keys, cloud and usage
  credits, and for subagents by default. Controls: `promptCacheTtl`,
  `subagentPromptCacheTtl` (`"5m"` or `"1h"`), `ENABLE_PROMPT_CACHING_1H=1`,
  `FORCE_PROMPT_CACHING_5M=1`.
- **Subagents** count toward the same limits, and only their summary returns.
  At most 20 run at once by default (`CLAUDE_CODE_MAX_CONCURRENT_SUBAGENTS`).
  By the docs' own figure, agent teams (experimental) cost about 7× a standard
  session.
- **Usage windows:** Pro and Max have a rolling 5-hour window and a 7-day
  window. `/usage` (also `/cost`, `/stats`) shows them. The statusline JSON
  carries `rate_limits.five_hour` and `rate_limits.seven_day` (each with
  `used_percentage` and `resets_at`), `context_window.used_percentage` and
  `cost.total_cost_usd`. Outside the desktop app, `rate_limits` reaches only
  the statusline script. An untested idea: a statusline script that also
  writes its JSON to a file the coordinator reads.
- **`autoContinueAtUsageLimit`** (on by default in interactive claude.ai
  sessions) waits in the open session and resumes after the reset, so a worker
  that hits the 5-hour limit pauses rather than dies.
- **Waiting without polling:**
  - `/loop` with no interval paces itself with `ScheduleWakeup`.
  - `/loop <interval>` uses `CronCreate`/`CronDelete`. These are
    session-scoped, fire only between turns, don't catch up, expire after 7
    days, and are capped at 50 per session. Neither form is restored on
    `--resume`.
  - Routines (cloud scheduled tasks) need neither the machine nor an open
    session; the minimum interval is 1 hour.
  - `Monitor` streams a background script's lines into the session, with a
    deadline of 5 minutes by default and 30 at most.
  - Background Bash writes to a file. Waking the model when a background task
    finishes is not documented, but it happened in practice.
- **Hooks worth offering for a shift:**
  - `SessionStart` (`compact`), above;
  - `Notification` (`idle_prompt`, `permission_prompt`,
    `quota_auto_resume_*`), to log stalls for the return brief;
  - `Stop`, where a prompt-type hook can check that the queue really is done
    before the coordinator stops;
  - `PreCompact` and `PostCompact`, to log when compactions happened.

### The desktop app's session tools (Code tab), 2026-10-27

- **`get_usage`** is the coordinator's meter, read at every wake. It returns
  the 5-hour window, the weekly window for all models and per model (each with
  percent used and reset time), and this session's context size and
  auto-compact point.
- **`start_session`** is refused on a turn that another session or an automated
  event began. The one exception is a side-session event right after the
  human's own turn.
- **`SendMessage`** to a `local_…` id: "delivered" means the turn started, and
  "queued" means it runs after the current one. A Remote Control worker gives no
  receipts beyond that. **`ListAgents`** shows workers on other machines as
  running, idle or offline. That is the liveness check before a send.
- **A worker's turn note** reaches the coordinator with only its first 400
  characters quoted. The full text needs `list_events`.
- **`clear_session`** clears a session this one started. It is refused for a
  session serving Remote Control, a pinned one, or one open on screen. `"self"`
  clears the coordinator itself once its turn ends.
- **`set_session_model` and `set_session_effort`:** moving a started session to
  a cheaper model needs no prompt.
- **`archive_session` and `detach_session`:** detaching keeps a worker alive
  when the coordinator retires.
- **`PushNotification`** reaches the phone when the session has Remote Control
  on, and is skipped while the human is active at the terminal. At the desk it
  answered "Not sent — this terminal is active". Ten minutes after the human's
  last message it answered "Mobile push requested". Whether it reached the
  phone is unconfirmed.
- **`Agent`** subagents run in the background, can use worktree isolation, and
  can start on any turn. Only a summary returns.

### Idle compaction as observed, 2026-10-27

Client 2.1.308, with no `idleCompaction` key in settings.

- The summary was written about 55 minutes into the idle stretch, before the
  one-hour cache expired, and applied when the next message arrived. The
  transcript marks the boundary `trigger: auto, precomputed: true`. The session
  shows "Compacted using a summary written while you were away".
- Sizes: a coordinator went from about 460K, and later from about 310K, to
  under 60K each time. A worker went from about 470K to 25K.
- It did not fire for eight idle wakes earlier the same day, so it was probably
  switched on from the server that morning. It also didn't fire for a later
  94-minute idle at about 170K, which rewarmed in full. It may act only above
  some size, which is where it matters anyway.

### 2026-10-28

- An app update switched Remote Control off for every local session.
  Messaging between sessions on the same machine kept working. Workers on
  another machine stayed reachable, because their Remote Control is set on
  their own box. `notify_when_idle` was not offered for those sessions in that release.

### Untested

- Whether a `/compact` sent by `SendMessage` runs as a command.
- Whether a subagent can wait out a long gated job. Foreground waits are capped
  at 10 minutes each, and a subagent's cache is 5 minutes unless
  `subagentPromptCacheTtl` is `"1h"`.

## Evidence

Why each rule exists, with its date and provenance, is in
[evidence.md](evidence.md). Improvement PRs add their rows there.
