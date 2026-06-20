"""
PDF TOC-Aware Splitter
======================
Splits a large PDF into smaller files. The core primitive is an editable
*slice plan* -- a sorted list of break points (start pages) with titles. Every
mode just generates that plan; slicing consumes it. Plans can be dumped to JSON,
edited (by hand or by an agent), and re-loaded, which makes splitting iterative
and recursive: seed a coarse plan, add finer breaks inside a big chunk, re-slice.

Plan sources (pick one):
    (default)              Build the plan from the PDF's bookmark/TOC tree
    --infer-headings       Infer headings (font size + regex) when there is text
                           but no bookmarks, and build a plan from them
    --fixed-pages N        Break every N pages (works on any paged PDF)
    --breaks 1,340,720     Break at an explicit, hand-typed list of start pages
    --plan FILE            Load a previously dumped (and edited) plan

Usage:
    python pdf_splitter.py <input.pdf> [options]

Options:
    --split-level N        TOC level to split at (default: 2 for TOC, 1 inferred)
    --max-pages N          Max pages per chunk before auto-deepening (default: 500)
    --output-dir DIR       Output directory (default: ./splits)
    --cover-gaps           Also write pages not covered by the plan (front matter, gaps)
    --range A-B            Limit --infer-headings to a page range (for recursion)
    --dump-plan FILE       Write the proposed plan to FILE (JSON) instead of slicing
    --plan FILE            Slice using a plan loaded from FILE (JSON)
    --breaks LIST          Slice at an explicit comma-separated list of start pages
    --fixed-pages N        Slice every N pages
    --infer-headings       Build the plan by inferring headings from page content
    --analyze              Print TOC / structure summary, don't split
    --dry-run              Show the plan without writing files

Dependencies:
    pip install pymupdf
"""

import argparse
import json
import re
import sys
from collections import Counter
from pathlib import Path

try:
    import fitz  # PyMuPDF
except ImportError:
    print("PyMuPDF required: pip install pymupdf")
    sys.exit(1)


# ---------------------------------------------------------------------------
# Document access
# ---------------------------------------------------------------------------

def open_pdf(pdf_path: str) -> "fitz.Document | None":
    """Open a PDF for reading, surfacing missing-file and encryption errors.

    Args:
        pdf_path: Path to the input PDF.

    Returns:
        An open ``fitz.Document``, or ``None`` if the file is missing,
        unreadable, or password-protected.
    """
    path = Path(pdf_path)
    if not path.is_file():
        print(f"ERROR: File not found: {pdf_path}")
        return None
    try:
        doc = fitz.open(pdf_path)
    except Exception as exc:  # any PyMuPDF open failure -> clean message, no traceback
        print(f"ERROR: Could not open PDF: {exc}")
        return None
    if doc.needs_pass:
        print("ERROR: PDF is password-protected. Decrypt it first, then retry.")
        doc.close()
        return None
    return doc


def has_text_layer(doc: "fitz.Document", sample: int = 12) -> bool:
    """Return True if the document appears to contain extractable text.

    Samples pages spread across the document; an image-only (scanned) PDF
    yields no text and should be routed to OCR rather than split by content.

    Args:
        doc: An open document.
        sample: How many pages to probe.

    Returns:
        True if any sampled page has non-whitespace text.
    """
    n = doc.page_count
    if n == 0:
        return False
    count = min(sample, n)
    step = max(1, n // count)
    for i in range(0, n, step):
        try:
            if doc[i].get_text().strip():
                return True
        except Exception:
            continue
    return False


# ---------------------------------------------------------------------------
# TOC navigation (operates on get_toc() lists: [level, title, page])
# ---------------------------------------------------------------------------

def resolve_start_page(toc: list, idx: int) -> int | None:
    """For entries with page<=0 (virtual bookmarks), find first descendant with a real page."""
    entry = toc[idx]
    if entry[2] > 0:
        return entry[2]
    level = entry[0]
    for j in range(idx + 1, len(toc)):
        if toc[j][0] <= level:
            break
        if toc[j][2] > 0:
            return toc[j][2]
    return None


def find_section_end(toc: list, idx: int, total_pages: int) -> int:
    """Find the start page of the next sibling or parent's sibling (exclusive end)."""
    level = toc[idx][0]
    for j in range(idx + 1, len(toc)):
        if toc[j][0] <= level:
            rp = resolve_start_page(toc, j)
            if rp:
                return rp
    return total_pages + 1


def get_children_at_level(toc: list, idx: int, child_level: int) -> list[tuple[int, list]]:
    """Get direct children at a specific level under toc[idx]."""
    parent_level = toc[idx][0]
    children = []
    for j in range(idx + 1, len(toc)):
        if toc[j][0] <= parent_level:
            break
        if toc[j][0] == child_level:
            children.append((j, toc[j]))
    return children


# ---------------------------------------------------------------------------
# Filenames and bookmark rebuilding
# ---------------------------------------------------------------------------

def sanitize_filename(name: str) -> str:
    """Convert a TOC title to a safe filename."""
    name = re.sub(r'[<>:"/\\|?*]', '_', name)
    name = re.sub(r'\s+', '_', name.strip())
    name = re.sub(r'_+', '_', name)
    name = name.strip('_.')
    return name[:80] if name else 'unnamed'


def _make_levels_contiguous(entries: list[list]) -> list[list]:
    """Clamp TOC levels so each step increases by at most one.

    PyMuPDF's ``set_toc`` rejects a hierarchy that jumps more than one level
    (e.g. 1 -> 3). After level-normalization a chunk can still contain such a
    jump if an intermediate level is absent from the included entries; this
    flattens those jumps so ``set_toc`` always accepts the result.

    Args:
        entries: TOC rows ``[level, title, page]`` in document order.

    Returns:
        The same rows with levels adjusted to be contiguous.
    """
    result = []
    prev_level = 0
    for level, title, page in entries:
        if level > prev_level + 1:
            level = prev_level + 1
        result.append([level, title, page])
        prev_level = level
    return result


def build_chunk_toc(toc: list, start_page: int, end_page: int) -> list:
    """Build a rebased bookmark tree for a chunk spanning a page range.

    Selects every source TOC entry whose resolved page falls within
    ``[start_page, end_page]`` -- independent of how the chunk boundary was
    chosen -- so manually-broken chunks still keep any real bookmarks they
    contain. Pages are rebased to start at 1 and levels normalized + flattened.

    Args:
        toc: The source document TOC (may be the real TOC or a synthetic one
            built from inferred headings).
        start_page: 1-indexed inclusive first page of the chunk.
        end_page: 1-indexed inclusive last page of the chunk.

    Returns:
        A TOC list suitable for ``set_toc`` on the extracted chunk, or [].
    """
    page_offset = start_page - 1
    raw_entries = []
    for i in range(len(toc)):
        resolved = resolve_start_page(toc, i)
        if resolved is None:
            continue
        if start_page <= resolved <= end_page:
            raw_entries.append([toc[i][0], toc[i][1], max(1, resolved - page_offset)])

    if not raw_entries:
        return []

    min_level = min(e[0] for e in raw_entries)
    shift = min_level - 1
    shifted = [[e[0] - shift, e[1], e[2]] for e in raw_entries]
    return _make_levels_contiguous(shifted)


# ---------------------------------------------------------------------------
# The slice plan: a list of chunk descriptors. This is the central object.
#   {title, start_page, end_page, page_count, is_gap}
# ---------------------------------------------------------------------------

def _chunk(title: str, start_page: int, end_page: int, is_gap: bool = False) -> dict:
    """Build a single chunk descriptor (1-indexed inclusive page range)."""
    return {
        'title': title,
        'start_page': start_page,
        'end_page': end_page,
        'page_count': end_page - start_page + 1,
        'is_gap': is_gap,
    }


def plan_from_toc(toc: list, total_pages: int, split_level: int = 2,
                  max_pages: int = 500) -> list[dict]:
    """Build a slice plan from the document TOC, deepening oversized sections.

    Args:
        toc: Source TOC list.
        total_pages: Total pages in the document.
        split_level: TOC level to break at.
        max_pages: Sections larger than this are split one level deeper,
            recursively up to level 6.

    Returns:
        A slice plan (list of chunk descriptors).
    """
    chunks = []
    target_entries = [(i, e) for i, e in enumerate(toc) if e[0] == split_level]

    if not target_entries:
        if split_level < 6:
            return plan_from_toc(toc, total_pages, split_level + 1, max_pages)
        return []

    for toc_idx, entry in target_entries:
        start = resolve_start_page(toc, toc_idx)
        if start is None:
            continue
        end = find_section_end(toc, toc_idx, total_pages)
        page_count = end - start

        if page_count > max_pages:
            sub = _split_deeper(toc, toc_idx, total_pages, max_pages)
            if sub:
                chunks.extend(sub)
                continue

        chunks.append(_chunk(entry[1], start, end - 1))

    return chunks


def _split_deeper(toc: list, parent_idx: int, total_pages: int, max_pages: int) -> list[dict] | None:
    """Recursively split an oversized section by going one TOC level deeper."""
    parent_level = toc[parent_idx][0]
    child_level = parent_level + 1
    children = get_children_at_level(toc, parent_idx, child_level)
    if not children:
        return None

    chunks = []
    for child_idx, child_entry in children:
        start = resolve_start_page(toc, child_idx)
        if start is None:
            continue
        end = find_section_end(toc, child_idx, total_pages)
        page_count = end - start

        if page_count > max_pages and child_level < 6:
            sub = _split_deeper(toc, child_idx, total_pages, max_pages)
            if sub:
                chunks.extend(sub)
                continue

        chunks.append(_chunk(child_entry[1], start, end - 1))

    return chunks if chunks else None


def plan_from_breaks(starts: list[int], total_pages: int,
                     titles: list[str] | None = None) -> list[dict]:
    """Build a slice plan from an explicit list of start pages.

    Args:
        starts: Page numbers (1-indexed) where new chunks begin.
        total_pages: Total pages in the document.
        titles: Optional per-break titles, aligned to sorted unique starts.

    Returns:
        A slice plan covering from each break to the page before the next.
    """
    pages = sorted({p for p in starts if 1 <= p <= total_pages})
    if not pages:
        return []
    plan = []
    for i, start in enumerate(pages):
        end = pages[i + 1] - 1 if i + 1 < len(pages) else total_pages
        if titles and i < len(titles) and titles[i]:
            title = titles[i]
        else:
            title = f"Section {i + 1} (p{start}-{end})"
        plan.append(_chunk(title, start, end))
    return plan


def parse_breaks(spec: str, total_pages: int) -> list[dict]:
    """Parse a comma-separated start-page list into a slice plan."""
    nums = []
    for token in spec.split(','):
        token = token.strip()
        if not token:
            continue
        try:
            nums.append(int(token))
        except ValueError:
            print(f"WARNING: ignoring non-integer break '{token}'")
    return plan_from_breaks(nums, total_pages)


def plan_fixed_pages(total_pages: int, pages_per_chunk: int) -> list[dict]:
    """Build a slice plan that breaks every ``pages_per_chunk`` pages."""
    if pages_per_chunk < 1:
        return []
    plan = []
    start = 1
    while start <= total_pages:
        end = min(start + pages_per_chunk - 1, total_pages)
        plan.append(_chunk(f"Pages {start}-{end}", start, end))
        start = end + 1
    return plan


# ---------------------------------------------------------------------------
# Heading inference (no-TOC fallback): font-size cues + regex, bounded
# ---------------------------------------------------------------------------

_HEADING_RE = [
    re.compile(r'^(chapter|section|part|appendix|book|unit|module)\b', re.I),
    re.compile(r'^\d+(\.\d+){0,3}\.?\s+\S'),   # "1 Title", "1.2 Title", "1.2.3 Title"
]


def _looks_like_heading(text: str) -> bool:
    """Regex/shape heuristic for a heading line (used when font cues are weak)."""
    if not text or len(text) > 120:
        return False
    if any(p.match(text) for p in _HEADING_RE):
        return True
    words = text.split()
    return text.isupper() and 1 <= len(words) <= 12


def _sample_page_indices(start: int, end: int, cap: int) -> list[int]:
    """Evenly spaced 0-indexed page indices within [start, end] (1-indexed)."""
    rng = list(range(start - 1, end))
    if len(rng) <= cap:
        return rng
    step = len(rng) / cap
    return [rng[int(i * step)] for i in range(cap)]


def _body_font_size(doc: "fitz.Document", page_indices: list[int]) -> int:
    """Estimate the body text size (most common rounded span size by char count)."""
    counter: Counter = Counter()
    for i in page_indices:
        try:
            info = doc[i].get_text("dict")
        except Exception:
            continue
        for block in info.get("blocks", []):
            for line in block.get("lines", []):
                for span in line.get("spans", []):
                    text = span.get("text", "").strip()
                    if text:
                        counter[round(span.get("size", 0))] += len(text)
    return counter.most_common(1)[0][0] if counter else 0


def infer_headings(doc: "fitz.Document", total_pages: int, split_level: int = 1,
                   max_pages: int = 500, start: int = 1,
                   end: int | None = None) -> tuple[list[dict], list]:
    """Infer a slice plan from page content when the PDF has no bookmarks.

    Combines two best-effort cues: spans whose font is clearly larger than the
    body text, and lines matching common heading patterns. Distinct large font
    sizes map to levels 1..3; everything else is level 1. The result is a
    synthetic TOC that is fed through the normal TOC planner.

    Args:
        doc: Open document with a text layer.
        total_pages: Total pages in the document.
        split_level: Synthetic-TOC level to break at (default 1).
        max_pages: Deepen sections larger than this.
        start: 1-indexed first page to scan (for recursion into a region).
        end: 1-indexed last page to scan (default: end of document).

    Returns:
        ``(plan, synthetic_toc)``. ``synthetic_toc`` is passed to the slicer so
        each chunk keeps its inferred sub-headings as bookmarks. Both empty if
        nothing heading-like is found.
    """
    end = end or total_pages
    body = _body_font_size(doc, _sample_page_indices(start, end, 60))

    raw = []  # (page_1indexed, big_size_or_0, text)
    for p in range(start - 1, end):
        try:
            info = doc[p].get_text("dict")
        except Exception:
            continue
        for block in info.get("blocks", []):
            for line in block.get("lines", []):
                spans = [s for s in line.get("spans", []) if s.get("text", "").strip()]
                if not spans:
                    continue
                text = "".join(s.get("text", "") for s in spans).strip()
                if not text or len(text) > 120:
                    continue
                size = round(max(s.get("size", 0) for s in spans))
                big = bool(body) and size >= body + 2
                if big or _looks_like_heading(text):
                    raw.append((p + 1, size if big else 0, text))

    if not raw:
        return [], []

    # Tier by font size: the distinct large sizes become levels 1..3.
    big_sizes = sorted({s for _, s, _ in raw if s}, reverse=True)[:3]
    size_level = {s: i + 1 for i, s in enumerate(big_sizes)}

    # One heading per page (prefer the largest font on that page).
    raw.sort(key=lambda r: (r[0], -r[1]))
    synth = []
    seen = set()
    for page, size, text in raw:
        if page in seen:
            continue
        seen.add(page)
        level = size_level.get(size, 1) if size else 1
        synth.append([level, text, page])

    synth.sort(key=lambda e: e[2])
    plan = plan_from_toc(synth, total_pages, split_level=split_level, max_pages=max_pages)
    return plan, synth


# ---------------------------------------------------------------------------
# Coverage and plan I/O
# ---------------------------------------------------------------------------

def compute_gaps(plan: list[dict], total_pages: int) -> list[tuple[int, int]]:
    """Find page ranges that no chunk in the plan covers.

    Args:
        plan: Slice plan (chunks with 1-indexed inclusive page ranges).
        total_pages: Total number of pages in the source document.

    Returns:
        Ascending ``(start, end)`` inclusive page ranges left uncovered.
    """
    covered = sorted((c['start_page'], c['end_page']) for c in plan)
    gaps = []
    cursor = 1
    for start, end in covered:
        if start > cursor:
            gaps.append((cursor, start - 1))
        cursor = max(cursor, end + 1)
    if cursor <= total_pages:
        gaps.append((cursor, total_pages))
    return gaps


def make_gap_chunks(gaps: list[tuple[int, int]]) -> list[dict]:
    """Turn uncovered page ranges into chunk descriptors (flagged ``is_gap``)."""
    chunks = []
    for start, end in gaps:
        title = "Front matter" if start == 1 else f"Gap pages {start}-{end}"
        chunks.append(_chunk(title, start, end, is_gap=True))
    return chunks


def dump_plan(plan: list[dict], path: str) -> None:
    """Write the plan to JSON for review/editing (gap chunks excluded).

    The editable contract is just ``start_page`` + ``title``; ``pages`` is an
    informational hint. Loading derives each chunk's end from the next break,
    so editing is intuitive: delete a line to merge, add a line to split.
    """
    out = [
        {
            'start_page': c['start_page'],
            'title': c['title'],
            'pages': f"{c['start_page']}-{c['end_page']} ({c['page_count']} pp)",
        }
        for c in plan if not c.get('is_gap')
    ]
    with open(path, 'w', encoding='utf-8') as fh:
        json.dump(out, fh, indent=2)
    print(f"Wrote plan with {len(out)} break(s) to {path}")
    print("Edit start_page/title as needed, then slice with --plan " + path)


def load_plan(path: str, total_pages: int) -> list[dict]:
    """Load and validate a slice plan from JSON; derive end pages from starts."""
    try:
        with open(path, 'r', encoding='utf-8') as fh:
            data = json.load(fh)
    except (OSError, json.JSONDecodeError) as exc:
        print(f"ERROR: Could not read plan {path}: {exc}")
        return []
    starts, titles = [], []
    for item in data:
        try:
            starts.append(int(item['start_page']))
        except (KeyError, TypeError, ValueError):
            print(f"WARNING: skipping plan entry without a valid start_page: {item}")
            continue
        titles.append(item.get('title'))
    # Re-pair titles to sorted unique starts.
    pairs = sorted({s: t for s, t in zip(starts, titles)}.items())
    sorted_starts = [s for s, _ in pairs]
    sorted_titles = [t for _, t in pairs]
    return plan_from_breaks(sorted_starts, total_pages, sorted_titles)


# ---------------------------------------------------------------------------
# Slicing
# ---------------------------------------------------------------------------

def slice_by_plan(doc: "fitz.Document", toc: list, plan: list[dict],
                  output_dir: str = './splits', dry_run: bool = False,
                  cover_gaps: bool = False) -> list[dict]:
    """Slice the document into files according to a plan.

    Args:
        doc: Open source document.
        toc: TOC used to rebuild per-chunk bookmarks (real or synthetic; may be
            empty, in which case each chunk gets a single title bookmark).
        plan: Slice plan to execute.
        output_dir: Where chunk PDFs are written.
        dry_run: If True, print the plan and coverage but write nothing.
        cover_gaps: If True, also write pages no chunk covers as their own files.

    Returns:
        A list of per-file result dicts (empty on dry-run or failure).
    """
    total_pages = doc.page_count
    if not plan:
        print("ERROR: empty plan, nothing to slice.")
        return []

    gaps = compute_gaps(plan, total_pages)
    gap_chunks = make_gap_chunks(gaps)
    uncovered = sum(g['page_count'] for g in gap_chunks)
    covered = total_pages - uncovered

    chunks = plan
    if cover_gaps and gap_chunks:
        chunks = sorted(plan + gap_chunks, key=lambda c: c['start_page'])

    print(f"Plan: {len(plan)} chunk(s); {covered}/{total_pages} pages covered.")
    print()
    for i, chunk in enumerate(chunks):
        tag = " [gap]" if chunk.get('is_gap') else ""
        print(f"  {i + 1:>3}. [{chunk['page_count']:>5} pp]  {chunk['title']}{tag}")
    print()

    if gap_chunks:
        print(f"WARNING: {uncovered} page(s) lie outside the slice plan, in "
              f"{len(gap_chunks)} gap(s):")
        for g in gap_chunks:
            print(f"    pages {g['start_page']}-{g['end_page']}  ({g['title']})")
        if cover_gaps:
            print("  -> included above as [gap] chunks.")
        else:
            print("  -> re-run with --cover-gaps to write these to their own files.")
        print()

    if dry_run:
        print("(dry run, no files written)")
        return []

    out_path = Path(output_dir)
    try:
        out_path.mkdir(parents=True, exist_ok=True)
    except OSError as exc:
        print(f"ERROR: Could not create output directory {output_dir}: {exc}")
        return []

    results = []
    for i, chunk in enumerate(chunks):
        filename = f"{i + 1:03d}_{sanitize_filename(chunk['title'])}.pdf"
        filepath = out_path / filename
        from_page = chunk['start_page'] - 1
        to_page = chunk['end_page'] - 1

        try:
            new_doc = fitz.open()
            new_doc.insert_pdf(doc, from_page=from_page, to_page=to_page)

            # insert_pdf drops bookmarks; rebuild from the (real or synthetic) TOC.
            new_toc = []
            if toc and not chunk.get('is_gap'):
                new_toc = build_chunk_toc(toc, chunk['start_page'], chunk['end_page'])
            if not new_toc:
                new_toc = [[1, chunk['title'], 1]]
            new_doc.set_toc(new_toc)

            new_doc.save(str(filepath))
            new_doc.close()
        except Exception as exc:  # skip a chunk that fails; keep going
            print(f"  FAILED {filename}: {exc}")
            continue

        results.append({
            'title': chunk['title'],
            'output_path': str(filepath),
            'start_page': chunk['start_page'],
            'end_page': chunk['end_page'],
            'page_count': chunk['page_count'],
            'bookmark_count': len(new_toc),
        })
        print(f"  OK {filename}  ({chunk['page_count']} pages, {len(new_toc)} bookmarks)")

    print(f"\nDone. {len(results)} files written to {output_dir}/")
    return results


# ---------------------------------------------------------------------------
# Analysis
# ---------------------------------------------------------------------------

def analyze(pdf_path: str) -> None:
    """Print a structure summary and suggest a plan source.

    Args:
        pdf_path: Path to the input PDF.
    """
    doc = open_pdf(pdf_path)
    if doc is None:
        return

    try:
        toc = doc.get_toc()
        print(f"File: {pdf_path}")
        print(f"Pages: {doc.page_count}")
        print(f"TOC entries: {len(toc)}")
        print()

        if not toc:
            if has_text_layer(doc):
                print("No bookmarks, but the document has a text layer.")
                print("Plan sources:")
                print("  --infer-headings           infer structure from headings")
                print("  --fixed-pages N            break every N pages")
                print("  --breaks p1,p2,...         break at a hand-picked page list")
            else:
                print("No bookmarks and no text layer -- this looks like a scanned PDF.")
                print("OCR it first (e.g. the anthropic-skills:pdf skill, or ocrmypdf),")
                print("then re-run, or split mechanically with --fixed-pages N.")
            return

        levels = sorted({e[0] for e in toc})
        print(f"Hierarchy levels: {levels}")
        for lvl in levels:
            count = sum(1 for e in toc if e[0] == lvl)
            print(f"  Level {lvl}: {count} entries")
        print()

        split_level = 2 if 2 in levels else levels[0]
        print(f"=== Level {split_level} sections ===")
        print()
        entries = [(i, e) for i, e in enumerate(toc) if e[0] == split_level]
        for n, (i, entry) in enumerate(entries):
            start = resolve_start_page(toc, i)
            end = find_section_end(toc, i, doc.page_count)
            if start:
                print(f"  {n + 1:>2}. {entry[1]:<55s}  pages {start:>5}-{end - 1:<5}  "
                      f"({end - start:>5} pages)")
            else:
                print(f"  {n + 1:>2}. {entry[1]:<55s}  (no page destination)")
    finally:
        doc.close()


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def _parse_range(spec: str, total_pages: int) -> tuple[int, int]:
    """Parse an 'A-B' page range, clamped to the document."""
    parts = spec.split('-', 1)
    try:
        a = int(parts[0])
        b = int(parts[1]) if len(parts) > 1 and parts[1].strip() else total_pages
    except ValueError:
        print(f"WARNING: bad --range '{spec}', using whole document")
        return 1, total_pages
    return max(1, a), min(total_pages, b)


def build_plan(doc: "fitz.Document", toc: list, args) -> tuple[list[dict], list]:
    """Resolve CLI args into a (plan, bookmark_toc) pair.

    Returns the slice plan and the TOC to rebuild chunk bookmarks from (the
    real TOC, a synthetic inferred one, or [] for placeholder bookmarks).
    """
    total = doc.page_count
    max_pages = args.max_pages

    if args.plan:
        return load_plan(args.plan, total), toc
    if args.breaks:
        return parse_breaks(args.breaks, total), toc
    if args.fixed_pages:
        return plan_fixed_pages(total, args.fixed_pages), toc
    if args.infer_headings:
        if not has_text_layer(doc):
            print("ERROR: no text layer -- cannot infer headings. OCR first, or use "
                  "--fixed-pages N.")
            return [], []
        level = args.split_level if args.split_level is not None else 1
        start, end = (1, total)
        if args.range:
            start, end = _parse_range(args.range, total)
        plan, synth = infer_headings(doc, total, split_level=level,
                                     max_pages=max_pages, start=start, end=end)
        if not plan:
            print("No headings could be inferred. Try --fixed-pages N or --breaks.")
        return plan, synth

    # Default: build from the document TOC.
    if not toc:
        if has_text_layer(doc):
            print("ERROR: no bookmarks. Choose a plan source: --infer-headings, "
                  "--fixed-pages N, or --breaks p1,p2,...")
        else:
            print("ERROR: no bookmarks and no text layer (scanned PDF). OCR it first "
                  "(e.g. anthropic-skills:pdf), or use --fixed-pages N.")
        return [], []
    level = args.split_level if args.split_level is not None else 2
    return plan_from_toc(toc, total, split_level=level, max_pages=max_pages), toc


def main() -> None:
    parser = argparse.ArgumentParser(description="Split a PDF using an editable slice plan")
    parser.add_argument("pdf", help="Path to the input PDF")
    parser.add_argument("--split-level", type=int, default=None,
                        help="TOC level to split at (default: 2 for TOC, 1 for inferred)")
    parser.add_argument("--max-pages", type=int, default=500,
                        help="Max pages per chunk before auto-deepening (default: 500)")
    parser.add_argument("--output-dir", default="./splits",
                        help="Output directory (default: ./splits)")
    parser.add_argument("--cover-gaps", action="store_true",
                        help="Also write pages not covered by the plan (front matter, gaps)")
    parser.add_argument("--range", default=None,
                        help="Limit --infer-headings to a page range 'A-B'")
    parser.add_argument("--dump-plan", default=None,
                        help="Write the proposed plan to this JSON file instead of slicing")
    parser.add_argument("--plan", default=None,
                        help="Slice using a plan loaded from this JSON file")
    parser.add_argument("--breaks", default=None,
                        help="Slice at an explicit comma-separated list of start pages")
    parser.add_argument("--fixed-pages", type=int, default=None,
                        help="Slice every N pages")
    parser.add_argument("--infer-headings", action="store_true",
                        help="Build the plan by inferring headings from page content")
    parser.add_argument("--analyze", action="store_true",
                        help="Print TOC / structure summary, don't split")
    parser.add_argument("--dry-run", action="store_true",
                        help="Show the plan without writing files")

    args = parser.parse_args()

    if args.analyze:
        analyze(args.pdf)
        return

    doc = open_pdf(args.pdf)
    if doc is None:
        sys.exit(1)
    try:
        toc = doc.get_toc()
        plan, book_toc = build_plan(doc, toc, args)
        if not plan:
            sys.exit(1)
        if args.dump_plan:
            dump_plan(plan, args.dump_plan)
            return
        slice_by_plan(doc, book_toc, plan, output_dir=args.output_dir,
                      dry_run=args.dry_run, cover_gaps=args.cover_gaps)
    finally:
        doc.close()


if __name__ == "__main__":
    main()
