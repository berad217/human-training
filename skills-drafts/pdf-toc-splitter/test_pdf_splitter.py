"""Regression tests for pdf_splitter (plan-centric).

Dev artifact -- lives at the draft top level so it stays in skills-drafts/ and
does NOT travel into the shipped assets/ on graduation.

Pure logic (planning, coverage, bookmark rebuild, level-jump guard, plan I/O)
runs on synthetic TOC lists. Generated PDFs exercise the end-to-end slice,
heading inference (varied fonts), and scanned-PDF detection.

Run:  python test_pdf_splitter.py
"""

import io
import json
import sys
import tempfile
from contextlib import redirect_stdout
from pathlib import Path

sys.dont_write_bytecode = True  # don't drop __pycache__ into skills-source/ (it would ship)

import fitz  # noqa: E402 - confirms PyMuPDF is present before importing the module

# The shipped script now lives in skills-source/; this test validates that copy.
_ASSETS = Path(__file__).resolve().parents[2] / "skills-source" / "pdf-toc-splitter" / "assets"
sys.path.insert(0, str(_ASSETS))
import pdf_splitter as ps  # noqa: E402


# Synthetic source TOC: front matter (first L2 at page 4), a virtual bookmark
# (Chapter 3, page -1), deepening (Chapter 2 -> L3 -> L4), and a level jump
# (Chapter 4 L2 -> L4, no L3 between).
TOC = [
    [1, "Book", 1],
    [2, "Chapter 1", 4],
    [3, "1.1 Intro", 4],
    [3, "1.2 Details", 7],
    [2, "Chapter 2 (big)", 10],
    [3, "2.1", 10],
    [3, "2.2", 20],
    [4, "2.2.1", 20],
    [4, "2.2.2", 30],
    [3, "2.3", 40],
    [2, "Chapter 3 (virtual)", -1],
    [3, "3.1", 50],
    [3, "3.2", 55],
    [2, "Chapter 4 (jump)", 60],
    [4, "4.0.1 deep", 62],
]
TOTAL = 70

_failures = []


def check(name, cond, detail=""):
    status = "PASS" if cond else "FAIL"
    print(f"  [{status}] {name}" + (f" -- {detail}" if detail and not cond else ""))
    if not cond:
        _failures.append(name)


def _starts(plan):
    return [c["start_page"] for c in plan]


def _ranges(plan):
    return [(c["start_page"], c["end_page"]) for c in plan]


def test_toc_planning():
    print("plan_from_toc (level 2, max_pages 15)")
    plan = ps.plan_from_toc(TOC, TOTAL, split_level=2, max_pages=15)
    got = [(c["title"], c["start_page"], c["end_page"]) for c in plan]
    expected = [
        ("Chapter 1", 4, 9),
        ("2.1", 10, 19),
        ("2.2.1", 20, 29),
        ("2.2.2", 30, 39),
        ("2.3", 40, 49),
        ("Chapter 3 (virtual)", 50, 59),
        ("Chapter 4 (jump)", 60, 70),
    ]
    check("deepens oversized sections + resolves virtual bookmark", got == expected,
          f"\n    got={got}\n    exp={expected}")
    return plan


def test_coverage(plan):
    print("compute_gaps / make_gap_chunks")
    gaps = ps.compute_gaps(plan, TOTAL)
    check("only gap is the front matter (pages 1-3)", gaps == [(1, 3)], gaps)
    gap_chunks = ps.make_gap_chunks(gaps)
    check("front-matter gap chunk shaped correctly",
          len(gap_chunks) == 1 and gap_chunks[0]["title"] == "Front matter"
          and gap_chunks[0]["page_count"] == 3 and gap_chunks[0]["is_gap"] is True,
          gap_chunks)
    check("contiguous coverage yields no gaps",
          ps.compute_gaps([ps._chunk("x", 1, TOTAL)], TOTAL) == [])
    interior = ps.compute_gaps([ps._chunk("a", 1, 5), ps._chunk("b", 9, 10)], 10)
    check("interior gap detected", interior == [(6, 8)], interior)


def test_break_and_fixed_plans():
    print("plan_from_breaks / parse_breaks / plan_fixed_pages")
    p = ps.parse_breaks("1,20,50", TOTAL)
    check("manual breaks -> correct ranges",
          _ranges(p) == [(1, 19), (20, 49), (50, 70)], _ranges(p))
    messy = ps.parse_breaks("50, 20, 1, 200, 20, junk", TOTAL)
    check("breaks deduped, sorted, clamped, junk ignored",
          _starts(messy) == [1, 20, 50], _starts(messy))
    fp = ps.plan_fixed_pages(TOTAL, 25)
    check("fixed-pages tiles the whole document",
          _ranges(fp) == [(1, 25), (26, 50), (51, 70)], _ranges(fp))
    check("fixed-pages leaves no gaps", ps.compute_gaps(fp, TOTAL) == [])


def test_plan_roundtrip():
    print("dump_plan / load_plan (the editable, recursive primitive)")
    plan = ps.parse_breaks("1,20,50", TOTAL)
    with tempfile.TemporaryDirectory() as tmp:
        path = str(Path(tmp) / "plan.json")
        with redirect_stdout(io.StringIO()):
            ps.dump_plan(plan, path)
        data = json.loads(Path(path).read_text(encoding="utf-8"))
        check("dumped plan is a start_page/title list",
              all("start_page" in d and "title" in d for d in data) and len(data) == 3)
        reloaded = ps.load_plan(path, TOTAL)
        check("round-trip preserves break ranges", _ranges(reloaded) == _ranges(plan))

        # Editing: delete the middle break -> two chunks merge into one.
        edited = [data[0], data[2]]
        Path(path).write_text(json.dumps(edited), encoding="utf-8")
        merged = ps.load_plan(path, TOTAL)
        check("deleting a break merges its range (1-49, 50-70)",
              _ranges(merged) == [(1, 49), (50, 70)], _ranges(merged))

        # Adding a break inside a chunk -> recursion (split the big tail).
        edited2 = data + [{"start_page": 60, "title": "deeper"}]
        Path(path).write_text(json.dumps(edited2), encoding="utf-8")
        deeper = ps.load_plan(path, TOTAL)
        check("adding a break sub-divides a chunk (50-59, 60-70)",
              (50, 59) in _ranges(deeper) and (60, 70) in _ranges(deeper), _ranges(deeper))


def test_level_jump_guard():
    print("level-jump guard (build_chunk_toc / _make_levels_contiguous)")
    rebuilt = ps.build_chunk_toc(TOC, 60, 70)  # Chapter 4: L2 root + L4 child, no L3
    check("chunk TOC starts at level 1", rebuilt and rebuilt[0][0] == 1, rebuilt)
    check("level jump flattened to contiguous (1,2)",
          [r[0] for r in rebuilt] == [1, 2], rebuilt)
    check("pages rebased into chunk (root -> 1)", rebuilt[0][2] == 1, rebuilt)
    flat = ps._make_levels_contiguous([[1, "a", 1], [3, "b", 2], [5, "c", 3]])
    check("multi-level jump flattened", [f[0] for f in flat] == [1, 2, 3], flat)

    doc = fitz.open()
    for _ in range(5):
        doc.new_page()
    raised = False
    try:
        doc.set_toc([[1, "root", 1], [3, "deep", 3]])
    except Exception:
        raised = True
    check("PyMuPDF rejects an un-guarded level jump", raised)
    accepted = True
    try:
        doc.set_toc([[1, "root", 1], [2, "deep", 3]])
    except Exception:
        accepted = False
    check("PyMuPDF accepts the guarded hierarchy", accepted)
    doc.close()


def _build_sample_pdf(path):
    """Valid source PDF (contiguous TOC, pages >= 1) for end-to-end slicing."""
    src_toc = [
        [1, "Book", 1],
        [2, "Chapter 1", 4],
        [3, "1.1 Intro", 4],
        [3, "1.2 Details", 7],
        [2, "Chapter 2 (big)", 10],
        [3, "2.1", 10],
        [3, "2.2", 20],
        [4, "2.2.1", 20],
        [4, "2.2.2", 30],
        [3, "2.3", 40],
        [2, "Chapter 3", 50],
        [3, "3.1", 50],
        [3, "3.2", 55],
        [2, "Chapter 4", 60],
        [3, "4.1", 62],
    ]
    doc = fitz.open()
    for n in range(TOTAL):
        doc.new_page().insert_text((72, 72), f"page {n + 1} body text")
    doc.set_toc(src_toc)
    doc.save(str(path))
    doc.close()


def test_end_to_end():
    print("end-to-end slice on a generated PDF")
    with tempfile.TemporaryDirectory() as tmp:
        tmp = Path(tmp)
        src = tmp / "sample.pdf"
        _build_sample_pdf(src)
        doc = ps.open_pdf(str(src))
        toc = doc.get_toc()

        plan = ps.plan_from_toc(toc, doc.page_count, split_level=2, max_pages=15)
        out1 = tmp / "out_sections"
        with redirect_stdout(io.StringIO()):
            results = ps.slice_by_plan(doc, toc, plan, str(out1))
        files = sorted(out1.glob("*.pdf"))
        check("one file per section chunk", len(files) == 7 and len(results) == 7,
              f"{len(files)} files / {len(results)} results")
        total_out, toc_ok = 0, True
        for f in files:
            d = fitz.open(str(f))
            total_out += d.page_count
            t = d.get_toc()
            if t and (t[0][0] != 1 or any(not (1 <= r[2] <= d.page_count) for r in t)):
                toc_ok = False
            d.close()
        check("section files cover exactly the 67 covered pages", total_out == 67, total_out)
        check("every rebuilt TOC is valid (set_toc accepted it)", toc_ok)

        out2 = tmp / "out_gaps"
        with redirect_stdout(io.StringIO()):
            ps.slice_by_plan(doc, toc, plan, str(out2), cover_gaps=True)
        files2 = sorted(out2.glob("*.pdf"))
        front = files2[0]
        d = fitz.open(str(front))
        fm_pages = d.page_count
        d.close()
        check("cover-gaps adds the front-matter file (8 total, 3 pp)",
              len(files2) == 8 and front.name == "001_Front_matter.pdf" and fm_pages == 3,
              f"{len(files2)} files, {front.name}, {fm_pages}pp")
        total2 = sum(fitz.open(str(f)).page_count for f in files2)
        check("cover-gaps accounts for ALL 70 pages", total2 == TOTAL, total2)

        # Manual breaks on a TOC'd doc still preserve the real bookmarks in range.
        out3 = tmp / "out_manual"
        manual = ps.parse_breaks("1,35", doc.page_count)
        with redirect_stdout(io.StringIO()):
            mres = ps.slice_by_plan(doc, toc, manual, str(out3))
        check("manual-break chunk keeps the real bookmarks it spans",
              mres and mres[0]["bookmark_count"] > 1, mres[0]["bookmark_count"] if mres else None)
        doc.close()


def _build_inferred_pdf(path):
    """No-TOC PDF with large-font headings on known pages (1, 6, 10)."""
    headings = {0: "Chapter 1 Alpha", 5: "Chapter 2 Beta", 9: "Chapter 3 Gamma"}
    doc = fitz.open()
    for n in range(12):
        page = doc.new_page()
        if n in headings:
            page.insert_text((72, 72), headings[n], fontsize=24)
            page.insert_text((72, 130), "body " * 30, fontsize=11)
        else:
            page.insert_text((72, 72), "body " * 60, fontsize=11)
    doc.save(str(path))  # no set_toc -> no bookmarks
    doc.close()


def test_inference_and_scanned():
    print("heading inference + scanned detection (the no-TOC completeness path)")
    with tempfile.TemporaryDirectory() as tmp:
        tmp = Path(tmp)
        inf = tmp / "inferred.pdf"
        _build_inferred_pdf(inf)
        doc = ps.open_pdf(str(inf))
        check("no bookmarks present", doc.get_toc() == [])
        check("text layer detected", ps.has_text_layer(doc) is True)

        plan, synth = ps.infer_headings(doc, doc.page_count, split_level=1)
        check("inference finds the 3 heading pages", _starts(plan) == [1, 6, 10], _starts(plan))
        check("synthetic TOC carries the heading titles",
              len(synth) == 3 and synth[0][1].startswith("Chapter 1"))
        check("inferred plan covers the whole doc",
              ps.compute_gaps(plan, doc.page_count) == [])

        # Recursion: scope inference to a sub-range (e.g. drill into the tail).
        sub_plan, _ = ps.infer_headings(doc, doc.page_count, split_level=1, start=6, end=12)
        check("range-scoped inference only finds in-range headings",
              _starts(sub_plan) == [6, 10], _starts(sub_plan))

        # End-to-end slice from inferred plan, with the synthetic TOC as bookmarks.
        out = tmp / "inf_out"
        with redirect_stdout(io.StringIO()):
            res = ps.slice_by_plan(doc, synth, plan, str(out))
        check("inferred slice writes a file per heading with a bookmark",
              len(res) == 3 and all(r["bookmark_count"] >= 1 for r in res), len(res))
        doc.close()

        blank = tmp / "blank.pdf"
        bdoc = fitz.open()
        for _ in range(4):
            bdoc.new_page()
        bdoc.save(str(blank))
        bdoc.close()
        sdoc = ps.open_pdf(str(blank))
        check("scanned/blank PDF reports no text layer", ps.has_text_layer(sdoc) is False)
        empty_plan, _ = ps.infer_headings(sdoc, sdoc.page_count)
        check("inference yields nothing on a no-text PDF", empty_plan == [])
        sdoc.close()


def test_io_guards():
    print("I/O guards")
    with redirect_stdout(io.StringIO()):
        none_doc = ps.open_pdf("does_not_exist_12345.pdf")
    check("open_pdf returns None for a missing file", none_doc is None)


def main():
    print("=" * 64)
    print("pdf_splitter regression tests")
    print("=" * 64)
    plan = test_toc_planning()
    test_coverage(plan)
    test_break_and_fixed_plans()
    test_plan_roundtrip()
    test_level_jump_guard()
    test_end_to_end()
    test_inference_and_scanned()
    test_io_guards()
    print("-" * 64)
    if _failures:
        print(f"FAILED ({len(_failures)}): {', '.join(_failures)}")
        sys.exit(1)
    print("ALL TESTS PASSED")


if __name__ == "__main__":
    main()
