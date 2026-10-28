# coordinator — evidence

Why each rule in [SKILL.md](SKILL.md) and [reference.md](reference.md) exists:
one rule per row, with the date and a short phrase for where it came from.

**This is the file improvement PRs add rows to** (SKILL.md §9). A new row
appends with the next number, in the group it supports, and cites its run's
date and PR. A delta that changes a rule cites the row that motivates it. The
consolidation pass merges rows into rules and retires stale ones.

**Never exercised.** Every row below comes from one project on one pair of
machines, 2026-10-24 to 10-28: three nights, a burn before a reset, an away day,
and the transcripts of those days. No run has had a red round, a crash, a
budget-ceiling breach or colliding lanes. The rules for those cases (red rounds
held and re-run, stop conditions, lanes escalating shared files, the cap) are
reasoning, not evidence.

## The machine

| # | Rule | Provenance |
|---|---|---|
| 1 | Main goes first. Lanes give the hold back between steps and leave a gap | 2026-10-25 night: one lane's back-to-back holds kept the round waiting at its build gate |
| 2 | A gate takes the hold first, then waits for the box to drain | 2026-10-25 night: two gates that waited for an empty box never got a turn behind a stream of short jobs |
| 3 | The round holds the machine once, from its build through its suite, and every gate polls at the same short interval. Integration outranks a lane's measurement | 2026-10-27: a round passed its build, then waited behind lane holds for its tests. 2026-10-27/28 night: lanes slipped in twice, through a slower poll and through the gap between gate tests and suite |
| 4 | Know which tools start heavy work by themselves, and gate them | 2026-10-25 night: a helper silently started a heavy process outside the gate |
| 5 | A thrift night is still a full night for the machine: rank its jobs by machine-hours per token. When the token queue ends early, a machine-bound job of known length is the tail | 2026-10-26/27 night: no token budget left, and one detached full rebuild gave the morning a proven answer. 2026-10-27/28 night: queues ran dry in the small hours, and a full rebuild carried the box to morning |

## Before the human leaves

| # | Rule | Provenance |
|---|---|---|
| 6 | Probe the human-only steps in the pre-flight. A step that needs elevation moves to the human's return | 2026-10-25 night, and a later night: a package build met an elevation prompt nobody could answer |
| 7 | Peers on other machines are native sessions the human opens in the pre-flight. Probe a remote host's port before relying on it | 2026-10-25 night: a session launched over SSH had no network credentials, sessions couldn't be started on the remote host, and a stopped SSH server looked like a timeout |
| 8 | Open every lane the shift could need while the human is present, a spare included | 2026-10-27: session starts are refused on a turn another session began. The human hit it too, and ruled to keep lanes rather than count on respawning |

## Reports and wakes

| # | Rule | Provenance |
|---|---|---|
| 9 | Lanes report results, failures, decisions needed and handoffs, never status. The verdict goes in the first sentence | 2026-10-25 night: dozens of status-only notes woke the coordinator. 2026-10-27: notes were cut to 400 characters, and several opened with process |
| 10 | Lanes watch quietly: a `Monitor` filtered to the lines that need action, or a background task's single completion | 2026-10-24..27 transcripts: most lane wakes were the lanes' own `Monitor` events |
| 11 | Hold FYIs for the lane's next real job | 2026-10-24..27 transcripts: pure-FYI messages ("merged", "thanks") woke lanes idle past the hour, for nothing |

## Lifecycle

| # | Rule | Provenance |
|---|---|---|
| 12 | Compact before the hour, never after | 2026-10-24..27 transcripts: most manual compactions of the coordinator came after an hour idle and paid the cold read first. Lanes compacted while warm rewarmed about 8× smaller |
| 13 | Keep lanes by default, since idle compaction compacts them before the hour. Retire only finished areas, after a lane note | 2026-10-27 morning: four lanes kept idle overnight "for one pending item" each rewarmed in full. That afternoon, idle compaction took a lane from about 470K to 25K |
| 14 | Keep the coordinator lean. A job whose rule demands heavy reading goes to a fork, which freezes a copy, diffs it by hash against the live version, and uploads only what changed | 2026-10-28: publishing a large page under "read every file before publishing it" would have filled the coordinator's context |
| 15 | Mechanical lanes start on a cheaper model at medium effort; code, design and taste stay on the top model | 2026-10-27, the human's ruling. Not yet exercised |

## The integration round

| # | Rule | Provenance |
|---|---|---|
| 16 | Never merge into a running round | 2026-10-25 night: avoided only by a standing rule |
| 17 | The gate tells "passed" from "stopped talking": demand the runner's own end marker | 2026-10-26/27 night: a test run that died mid-batch was counted green until the runner demanded its end marker |
| 18 | The independent review of the round's diff is part of the round | 2026-10-27: a review of the merged range found two real bugs the suite passed. 2026-10-27/28 night: it was dropped when the queues ran dry, and never ran |
| 19 | Check a red that only a lane's worktree shows against main's checkout. After merging main, sync the ignored derived files | 2026-10-28: a lane's first full suite failed on derived files its worktree lacked |

## On disk

| # | Rule | Provenance |
|---|---|---|
| 20 | The shift order, log, decision list and roster live on disk, in the repo. Re-read them after compaction | 2026-10-25 night: the coordinator compacted mid-shift, and only what was on disk survived intact |
| 21 | Keep full logs; filter only for display | 2026-10-25 night: a package step exited at once on a quoting bug, and a filtered log showed nothing |
| 22 | Scripts and docs written through a shell are byte-checked, and derived scripts are diffed, before use | 2026-10-27: a scripted edit turned backslashes into a backspace and a tab. 2026-10-28: a here-document on Windows did the same to a doc. A control-character check caught both |

## Authority

| # | Rule | Provenance |
|---|---|---|
| 23 | Discarding uncommitted work is a delete, so what a lane flags as the human's call is parked. A relayed instruction more cautious than yours wins until the human confirms | 2026-10-25 night: a revert ran on a file a lane had flagged as the human's call, before a relayed "leave it" arrived. The lost bytes happened to be regenerable |
| 24 | Grants are per repo. The harness is a gate a grant doesn't open: report, never route around it | 2026-10-27: a push to a second repo was refused by the harness's auto-mode check, though the push grant covered the first. 2026-10-25 night: a remote worker hit two access refusals and stopped, correctly |
| 25 | Outward-facing actions go through the session holding the human's request. Lanes stage; the coordinator ships | 2026-10-28: a lane's publish of a shared page was refused by its own permission check. It reported and didn't retry, and the coordinator, which held the request, published |

## Peers

| # | Rule | Provenance |
|---|---|---|
| 26 | Check a peer's liveness, ask for a "started" line with a deadline, and give a reassignment a clean stand-down | 2026-10-25 night: Remote Control peers sent no turn notes or receipts. 2026-10-27: a peer went dark when its Remote Control was switched off; its job moved to a local lane, then back |
| 27 | A lane or peer given work by the human directly tells the coordinator in one line | 2026-10-27: the human gave a job to a peer directly |
| 28 | The coordinator's links to local lanes don't depend on Remote Control. After an app update, list the agents | 2026-10-28: an update switched Remote Control off for every local lane, and same-machine messaging kept working |

## The human's attention

| # | Rule | Provenance |
|---|---|---|
| 29 | The decision list has three tiers. Whether silence settles the middle one is unconfirmed | 2026-10-26 evening: the first list to use the middle tier |
| 30 | There is one list of open asks, and each brief carries it forward | 2026-10-28: the night's brief held the open asks, and the day added more |
| 31 | Away is said, not inferred | 2026-10-27, the human's ruling: "Away explicitly." |
| 32 | Send at most one push between check-ins, and only for a ten-second answer that unblocks real work | 2026-10-27: a push reaches the phone only when the human isn't active at the terminal. Its arrival is unconfirmed |

## Budget and the supply of work

| # | Rule | Provenance |
|---|---|---|
| 33 | With headroom, the queue must outlast the shift: a machine queue plus a burn backlog. The usual failure is running out of work, not budget | 2026-10-25 night: every session stopped in the small hours, and the box and the quota sat idle until morning with most of the allowance unspent. 2026-10-28: an away day's lanes ran dry by midday, because everything left was the human's call |
| 34 | A burn needs a ready token-bound backlog. Measure the burn rate before promising a spend | 2026-10-27, before a reset: serial coordinator work barely moved the meter, and the fleet burned about a sixth of the assumed rate. Four fresh token-bound sessions spent the quota, and their ideas became the week's lanes |
| 35 | Budget has pools. Machine-bound work stays local; reading and docs can go to another pool and return as PRs | 2026-10-28: credits outside the subscription were available, but on a project that builds and tests only locally, a code PR from the cloud would come back blind |
