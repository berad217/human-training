# Handover — human-training

**Session date:** 2026-06-20
**State:** All work committed AND pushed. `main` at `fe655bc`, tree clean, in sync with
origin. Plugin **1.13.0** is released (tag `human-training--v1.13.0`, GitHub release
"Cut to the Chapter"). New skill **`pdf-toc-splitter`** shipped. CLI plugin updated
1.12.0 -> 1.13.0 at user scope — **a full Claude Code relaunch is pending** to load it.
Nothing in flight.

---

## This session (short version)

Shipped a new session-authored skill, `pdf-toc-splitter`. `/start` surfaced it as an
untracked draft; from there: adversarial review -> hardening -> a **reframe** -> graduation
-> release. Workflows exercised: #2 (develop in `skills-drafts/`) -> #1 (wire from
`skills-source/`) -> #5 (version bump + cross-device release). All complete.

What it does now: splits a large PDF along an **editable slice plan** generated from the
TOC, inferred headings (font + regex), fixed-page intervals, or a manual page list —
preserving/rebasing bookmarks, reporting (and optionally capturing) uncovered pages, and
handing scanned PDFs off to OCR.

## The delta (decisions made in-conversation)

- **Editable-plan architecture (Brad's reframe — the load-bearing idea).** The break list
  IS the primitive; every mode just generates it; editing it is how you refine and recurse
  (delete a break -> merge, add one -> subdivide a giant chunk). Don't regress this back to
  TOC-only. Plans round-trip via `--dump-plan` / `--plan`.
- **Scope boundary, held deliberately.** Did NOT broaden into general PDF manipulation —
  `anthropic-skills:pdf` already owns merge/rotate/watermark/forms/OCR. This skill stays the
  structure-aware *splitter*; scanned PDFs hand OFF to that skill.
- `--cover-gaps` defaults **off** (gaps always reported loudly; written only on opt-in).
- Heading inference is **best-effort by design** — it seeds an editable plan, the human
  corrects; never trusted blindly.
- **Single source of truth:** shipped script lives in `skills-source/pdf-toc-splitter/`; the
  regression test stays at `skills-drafts/pdf-toc-splitter/test_pdf_splitter.py` (doesn't
  ship; `sys.path` points at the skills-source copy). Needs PyMuPDF (`pip install pymupdf`,
  installed locally this session). 33/33 tests green.

## Invariant checks (all passed)

`build-skills.ps1` + `diff -r skills /tmp/skills-rebuild` (sh) empty; `verify-plugin-manifests.py`
valid & aligned at 1.13.0. Added a repo `.gitignore` (`__pycache__/`, `*.py[cod]`) — the
plugin ships Python now, and stray bytecode was breaking build parity. New gotchas saved to
auto-memory (`project_skills-source-graduation-gotchas`).

## Carried forward (durable, unchanged)

- **Matt-skills roadmap — NEXT = `diagnose`** (disciplined live-bug loop; dynamic counterpart
  to `robustness-audit`). Behind it: `improve-codebase-architecture`, `tdd`.
- **Leroy live test** still never exercised (now on 1.13.0). Parked until inference-to-burn +
  a real goal.
- Branch protection on `main` still deferred (solo direct-to-main).
- **pdf-toc-splitter v2 ideas, if it ever needs more** (parked, not promised): JSON output
  manifest, token/size-aware thresholds, overlap windows, page-label fidelity, cross-chunk
  link-break reporting.

---

*Ephemeral bridge — prune once absorbed. The durable record is the commits, README, and
auto-memory.*
