---
name: pdf-toc-splitter
description: Split a large PDF into smaller PDFs along an editable, structure-aware plan, preserving and rebasing bookmarks in each chunk. Use when a PDF is too large to process and must be broken into chapters/sections (for reading, LLM ingestion, or RAG), when splitting a book/manual/standard by its table of contents, or when a bookmark-less PDF needs its structure inferred or simple page-based splitting. Scales to 6000+ page documents; when there is no TOC it falls back to heading inference, fixed-page splitting, or a hand-edited page list.
allowed-tools: [Read, Write, Edit, Bash, Glob, Grep]
---

# PDF Splitter — structure-aware, editable plan

Break a large PDF into smaller files. The split PDFs are the deliverable; what the user does with them afterward (markdown conversion, LLM ingestion, reading) is their call — don't assume a next step.

## The one idea: an editable slice plan

Every split is defined by a **plan** — a sorted list of break points (the start page of each chunk) with titles. Chunk *i* runs from its break to the page before the next break.

```
breaks:  [1,        50,         210,        ...]
chunks:  [1-49]     [50-209]    [210-...]
```

Four sources can **generate** a plan; you **review and edit** it; then slicing **consumes** it:

- **TOC / bookmarks** (default) — split along the document's own structure.
- **Heading inference** (`--infer-headings`) — when there's text but no bookmarks.
- **Fixed-page** (`--fixed-pages N`) — mechanical fallback for any paged PDF.
- **Manual** (`--breaks 1,340,720`) — an explicit, hand-picked page list.

The plan is the leverage point. Because a chunk is just "this break to the next," **editing the plan is how you refine and recurse**: add a break to sub-divide a chunk, delete one to merge two, change a start page to move a boundary. Nothing is written to disk until you slice, so iterating is free.

This is what makes huge documents tractable: eyeball the first ten chapter starts of a 6,000-page PDF, slice into ten files plus one giant tail, then go back and add more breaks inside the tail — same loop, any depth.

---

## Setup

The splitter is `assets/pdf_splitter.py`, bundled next to this file. It needs Python 3.10+ and PyMuPDF.

```bash
python -c "import fitz" 2>&1 || pip install pymupdf
```

Set `SCRIPT` to the bundled script. It lives at `assets/pdf_splitter.py` alongside this SKILL.md; if that path isn't directly runnable from the user's project, read it and write a copy into the working directory, then point `SCRIPT` at the copy. All commands below use `"$SCRIPT"`.

---

## Workflow

### 1. Analyze — decide which plan source fits

Always start here:

```bash
python "$SCRIPT" "<pdf>" --analyze
```

It reports page count and tells you the lay of the land:

- **Has a TOC** → it lists the hierarchy levels and the level-2 sections. Use the default (TOC) source.
- **No bookmarks, has text** → use `--infer-headings`, `--fixed-pages N`, or `--breaks`.
- **No bookmarks, no text** → it's a scanned/image PDF. OCR it first (the `anthropic-skills:pdf` skill, or `ocrmypdf`), then re-run — or split mechanically with `--fixed-pages N`.

### 2. Generate a plan (always dry-run first)

Pick the source from step 1 and preview with `--dry-run` — this writes nothing, just prints the plan and a coverage report:

```bash
# From the TOC:
python "$SCRIPT" "<pdf>" --dry-run --max-pages 500

# Infer structure from headings (best-effort — review it):
python "$SCRIPT" "<pdf>" --infer-headings --dry-run

# Mechanical, every N pages:
python "$SCRIPT" "<pdf>" --fixed-pages 300 --dry-run

# An explicit page list:
python "$SCRIPT" "<pdf>" --breaks 1,340,720,1100 --dry-run
```

`--max-pages` controls granularity for the TOC and inference sources: any section bigger than the threshold is automatically split one level deeper, recursively. Pick by intended use:

| max-pages | Good for |
|-----------|----------|
| 300–500 | Markdown conversion, fitting chunks into LLM context windows |
| 800–1200 | Fewer larger chunks, reference documentation |
| 2000+ | Minimal splitting, only breaks truly massive sections |

Show the user the planned chunk list and ask if the granularity looks right. Too many tiny chunks (100+) means the threshold is too low; too few oversized chunks means it's too high.

> **Heading inference is best-effort.** It reads font sizes and common heading patterns, which works well on cleanly-typeset documents and poorly on multi-column layouts, decorative fonts, or running headers. Treat its output as a *starting* plan to be reviewed and edited (step 3), never as ground truth.

### 3. Review and edit the plan (the human-in-the-loop core)

Dump the proposed plan to an editable file:

```bash
python "$SCRIPT" "<pdf>" --infer-headings --dump-plan plan.json
```

`plan.json` is a simple list of `{start_page, title}`. Edit it — on the user's behalf via conversation, or let them hand-edit:

- **Delete a line** → that chunk merges into the one before it.
- **Add a line** → split a chunk at that page (this is how you recurse into a big region).
- **Change `start_page`** → move a boundary. **Change `title`** → rename the output file and its bookmark.

Then slice the edited plan:

```bash
python "$SCRIPT" "<pdf>" --plan plan.json --output-dir ./splits
```

**Recursion / drilling in.** Suppose a 6,000-page manual has no usable TOC. Get the user to name the chapter start pages they can see, slice with `--breaks`, and you'll have a few files plus a large tail. To subdivide the tail, scope inference to it and append to the plan:

```bash
python "$SCRIPT" "<pdf>" --infer-headings --range 3500-6000 --dump-plan tail.json
# merge tail.json's breaks into plan.json (or just add the start pages), then re-slice
```

### 4. Don't lose pages — coverage and gaps

Splitting along structure does **not** guarantee the chunks tile the whole document: pages before the first section (front matter), or a parent's own pages before its first subsection, belong to no chunk. The tool **always reports** these as gaps in the plan summary (`N/total pages covered`, plus a per-gap `WARNING`). To capture them as their own files so nothing is dropped, add `--cover-gaps`:

```bash
python "$SCRIPT" "<pdf>" --plan plan.json --output-dir ./splits --cover-gaps
```

If the document has front matter the user cares about, surface this and include gaps rather than silently dropping them.

### 5. Execute and report

Default output directory is `./splits`. Files are named `NNN_Title.pdf` in page order, each with its bookmark hierarchy rebuilt and rebased to start at page 1. Report: how many chunks, total size, any notably large chunks, and whether any pages were left uncovered.

### 6. What's next? (ask the user)

The split PDFs are the primary output. Ask what they want to do rather than assuming.

If they want **markdown conversion**, check for a `markitdown-file` MCP server by attempting `mcp__markitdown-file__batch_convert_to_markdown` — it writes to disk and does not pipe content through the context window. If that MCP isn't available, **do not fall back to methods that stream file content through the conversation** (large chunks will blow up context). Instead, point them to tools that convert outside the conversation:

- `pip install markitdown` — local CLI converter
- any PDF-to-text tool of their choice
- they can always come back with the smaller chunk PDFs for targeted reading via the Read tool's built-in PDF support

---

## Reference

For debugging or explaining the mechanism, read `assets/internals.md`.

### CLI quick reference

```
python pdf_splitter.py <pdf> --analyze                         # Inspect structure, get a recommendation
python pdf_splitter.py <pdf> --dry-run                         # Preview the TOC-based plan
python pdf_splitter.py <pdf> --infer-headings --dry-run        # Preview an inferred plan (no bookmarks)
python pdf_splitter.py <pdf> --fixed-pages 300 --dry-run       # Preview a fixed-page plan
python pdf_splitter.py <pdf> --breaks 1,340,720 --dry-run      # Preview a manual plan
python pdf_splitter.py <pdf> --dump-plan plan.json             # Write a plan to edit
python pdf_splitter.py <pdf> --plan plan.json --output-dir out # Slice an edited plan
python pdf_splitter.py <pdf> --output-dir out --cover-gaps     # Slice, also emit uncovered pages
```

| Option | Default | Purpose |
|--------|---------|---------|
| `--split-level N` | 2 (TOC), 1 (inferred) | Structure level to break at |
| `--max-pages N` | 500 | Auto-deepen sections larger than this (TOC/inference) |
| `--output-dir DIR` | ./splits | Output directory for chunk PDFs |
| `--cover-gaps` | off | Also write pages not covered by the plan (front matter, gaps) |
| `--infer-headings` | off | Build the plan by inferring headings from page content |
| `--fixed-pages N` | off | Build the plan by breaking every N pages |
| `--breaks LIST` | off | Build the plan from a comma-separated list of start pages |
| `--range A-B` | whole doc | Limit `--infer-headings` to a page range (for recursion) |
| `--dump-plan FILE` | off | Write the proposed plan to JSON instead of slicing |
| `--plan FILE` | off | Slice using a plan loaded from JSON |
| `--analyze` | off | Print structure summary and a recommendation only |
| `--dry-run` | off | Show the plan + coverage without writing files |
