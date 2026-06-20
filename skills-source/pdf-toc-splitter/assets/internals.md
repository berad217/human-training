# PDF Splitter — Internals Reference

Read this only to debug issues or explain the mechanism to the user.

## Architecture: the slice plan

Everything centers on a **slice plan** — a list of chunk descriptors, each with a
1-indexed inclusive `start_page`, `end_page`, `title`, and `page_count`. The plan
is the single contract between *deciding where to cut* and *doing the cut*:

```
generators  ->  plan (list of chunks)  ->  slice_by_plan()  ->  PDF files
```

- **Generators** produce a plan: `plan_from_toc` (bookmarks), `infer_headings`
  (font/regex), `plan_fixed_pages` (every N), `plan_from_breaks` / `parse_breaks`
  (explicit page list), and `load_plan` (an edited JSON plan).
- **`slice_by_plan`** extracts each chunk's pages, rebuilds its bookmarks, runs
  coverage accounting, and writes the files.

Because a chunk is "this break to the next," editing the plan *is* the
refine/recurse mechanism — no intermediate files, no fidelity loss from
re-deriving. `dump_plan` / `load_plan` make that round-trip explicit (the JSON
contract is just `start_page` + `title`; the end of each chunk is derived from the
next break).

## How a split runs

1. **Open** the PDF (`open_pdf`), rejecting missing files and encrypted PDFs up front.
2. **Generate a plan** from the chosen source.
3. **Account for coverage** (`compute_gaps`) — find pages no chunk covers.
4. **Extract pages** per chunk via `insert_pdf()` into a fresh document.
5. **Rebuild bookmarks** (`build_chunk_toc`) — `insert_pdf()` does NOT carry
   bookmarks, so each chunk's tree is rebuilt with `set_toc()`: pages rebased to
   start at 1, levels normalized to start at L1 and flattened to be contiguous.

## Bookmark rebuilding (`build_chunk_toc`)

Selects every source-TOC entry whose **resolved page** falls in the chunk's
`[start_page, end_page]`, regardless of how the boundary was chosen. Consequence:
a manually-broken chunk still keeps any real bookmarks it happens to span, and an
inferred-heading chunk keeps its inferred sub-headings (the synthetic TOC is
passed in as the bookmark source). Virtual bookmarks (`page <= 0`) resolve to
their first real descendant.

## Heading inference (`infer_headings`)

Best-effort, deliberately bounded. Used when there's a text layer but no TOC:

1. Estimate the **body font size** = the most common rounded span size (by total
   character count) across a sample of pages.
2. Scan lines; a line is a heading candidate if its max span size is clearly
   larger than body (`>= body + 2`) **or** it matches a heading regex
   (`Chapter|Section|Part|Appendix...`, or numbered `1.2.3 Title`) or is a short
   ALL-CAPS line.
3. Tier the distinct large font sizes into levels 1–3; regex-only hits default to
   level 1. Keep one heading per page (largest font wins).
4. Feed the resulting **synthetic TOC** through `plan_from_toc`, so `--max-pages`
   deepening and all downstream logic apply unchanged.

`--range A-B` limits the scan to a page window, which is how you drill into one
large region without re-processing the whole document.

## Key design decisions

- **Plan-centric.** Sources only decide *where* to cut; one slicer does the cut.
  This is what unifies TOC, inference, fixed-page, and manual modes, and what
  makes plans editable and recursive.
- **Coverage is never silent.** Splitting along a structure level does not
  necessarily tile the document (front matter, a parent's pages before its first
  child). Gaps are always reported; `--cover-gaps` captures them as their own
  files. Pages are never lost without a warning.
- **Bookmark preservation by rebuilding**, not copying — `insert_pdf` strips them.
- **Levels are clamped contiguous** before `set_toc`, which rejects level jumps
  (e.g. L1 -> L3). Such a jump can arise when an intermediate level is absent from
  a chunk's included entries; without the clamp `set_toc` raises and aborts.
- **Bookmarks selected by page range**, so all four plan sources get correct
  bookmarks (real ones in range, or the chunk title as a single placeholder).
- **ASCII-only console output** to avoid Windows cp1252 encoding errors.

## Edge cases

- **No TOC, has text**: not an error — fall back to `--infer-headings`,
  `--fixed-pages N`, or `--breaks`.
- **No TOC, no text (scanned)**: detected via `has_text_layer`; the tool stops and
  recommends OCR (e.g. `anthropic-skills:pdf`, `ocrmypdf`) rather than producing
  garbage. `--fixed-pages N` still works for a purely mechanical split.
- **Password-protected PDFs**: detected via `doc.needs_pass` and rejected with a
  clear error rather than misreported as having no TOC. Decrypt first.
- **Pages outside the plan**: reported as gaps; `--cover-gaps` writes them.
- **Unsplittable large sections**: a section bigger than `--max-pages` with no
  sub-bookmarks (or inferred sub-headings) below it can't be deepened
  automatically — add manual breaks (`--dump-plan`, edit, `--plan`) to subdivide.
- **Inference accuracy**: variable on multi-column layouts, decorative fonts, or
  running headers. Always review/edit the inferred plan before slicing.
- **Windows paths**: pass Windows-style paths (`D:\path\file.pdf`), not Git Bash
  Unix-style (`/d/path/file.pdf`).
- **Unicode titles**: handled by PyMuPDF; filename sanitization strips unsafe
  characters and caps length at 80.
