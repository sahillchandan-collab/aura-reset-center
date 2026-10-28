#!/usr/bin/env python3
"""Build branded Word (.docx) and PDF files for The Aura Reset Center.

Reads every Markdown draft under content/, applies the Aura letterhead
(logo header, legal footer, brand fonts and colours) and writes:
  output/word/<group>/<doc>.docx
  output/pdf/<group>/<doc>.pdf      (via LibreOffice, unless --no-pdf)

Usage: python3 build_documents.py [--no-pdf] [path/to/one.md ...]
"""
import re
import subprocess
import sys
from pathlib import Path

from docx import Document
from docx.enum.section import WD_SECTION
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.enum.text import WD_ALIGN_PARAGRAPH, WD_BREAK
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.shared import Cm, Pt, RGBColor

ROOT = Path(__file__).resolve().parent
CONTENT = ROOT / "content"
OUT_WORD = ROOT / "output" / "word"
OUT_PDF = ROOT / "output" / "pdf"
LOGO = ROOT / "brand" / "logo-light.png"

# Brand palette (see content/01-governance/06-brand-guidelines.md)
ESPRESSO = RGBColor(0x22, 0x19, 0x13)
COCOA = RGBColor(0x4A, 0x3A, 0x2C)
TAUPE = RGBColor(0x7A, 0x67, 0x53)
BRONZE = RGBColor(0xA6, 0x75, 0x4C)
HEX = {"espresso": "221913", "bronze": "A6754C", "clay": "DCC6B0",
       "sand": "E8D7C5", "shell": "FBF5EE", "cream": "F2E7DB"}

DISPLAY = "Marcellus"
SANS = "Jost"

FOOTER_ADDRESS = ("The Aura Reset Center  ·  332 Jumeirah First, Jumeirah 1, Dubai, UAE  ·  "
                  "[Phone]  ·  [Email]  ·  [Website]")
FOOTER_LEGAL = "[Registered Company Name]  ·  Trade License No. [___]  ·  TRN [___]"

INLINE = re.compile(r"(\*\*[^*]+\*\*|\*[^*\s][^*]*\*|\[[^\]]+\])")


# ----------------------------------------------------------------- helpers
def set_font(run, name=SANS, size=None, color=None, bold=None, italic=None):
    run.font.name = name
    rpr = run._element.get_or_add_rPr()
    rfonts = rpr.find(qn("w:rFonts"))
    if rfonts is None:
        rfonts = OxmlElement("w:rFonts")
        rpr.insert(0, rfonts)
    for attr in ("w:ascii", "w:hAnsi", "w:cs", "w:eastAsia"):
        rfonts.set(qn(attr), name)
    if size:
        run.font.size = Pt(size)
    if color is not None:
        run.font.color.rgb = color
    if bold is not None:
        run.bold = bold
    if italic is not None:
        run.italic = italic


def shade(cell_or_par_pr, fill):
    shd = OxmlElement("w:shd")
    shd.set(qn("w:val"), "clear")
    shd.set(qn("w:color"), "auto")
    shd.set(qn("w:fill"), fill)
    cell_or_par_pr.append(shd)


def par_border(paragraph, side, color, size=8, space=4):
    ppr = paragraph._p.get_or_add_pPr()
    bdr = ppr.find(qn("w:pBdr"))
    if bdr is None:
        bdr = OxmlElement("w:pBdr")
        ppr.append(bdr)
    el = OxmlElement(f"w:{side}")
    el.set(qn("w:val"), "single")
    el.set(qn("w:sz"), str(size))
    el.set(qn("w:space"), str(space))
    el.set(qn("w:color"), color)
    bdr.append(el)


def add_field(paragraph, instr, size, color):
    run = paragraph.add_run()
    set_font(run, size=size, color=color)
    for tag, text in (("begin", None), ("instr", instr), ("separate", None), ("text", "1"), ("end", None)):
        if tag == "instr":
            el = OxmlElement("w:instrText")
            el.set(qn("xml:space"), "preserve")
            el.text = f" {text} "
            run._r.append(el)
        elif tag == "text":
            el = OxmlElement("w:t")
            el.text = text
            run._r.append(el)
        else:
            el = OxmlElement("w:fldChar")
            el.set(qn("w:fldCharType"), tag)
            run._r.append(el)


def add_inline(paragraph, text, size=10, color=COCOA, bold=False, italic=False):
    """Write text with **bold**, *italic* and [placeholder] styling."""
    for part in INLINE.split(text):
        if not part:
            continue
        b, i, c = bold, italic, color
        if part.startswith("**") and part.endswith("**"):
            part, b = part[2:-2], True
        elif part.startswith("*") and part.endswith("*") and len(part) > 2:
            part, i = part[1:-1], True
        elif part.startswith("[") and part.endswith("]"):
            c = BRONZE  # placeholders stand out so they get filled in
        run = paragraph.add_run(part)
        set_font(run, size=size, color=c, bold=b, italic=i)


def spacing(paragraph, before=0, after=6, line=1.25):
    pf = paragraph.paragraph_format
    pf.space_before = Pt(before)
    pf.space_after = Pt(after)
    pf.line_spacing = line


# ------------------------------------------------------------ letterhead
def setup_document(doc_no):
    doc = Document()
    sec = doc.sections[0]
    sec.page_height, sec.page_width = Cm(29.7), Cm(21.0)
    sec.left_margin = sec.right_margin = Cm(2.2)
    sec.top_margin, sec.bottom_margin = Cm(3.6), Cm(2.6)
    sec.header_distance, sec.footer_distance = Cm(1.0), Cm(0.9)

    normal = doc.styles["Normal"]
    normal.font.name = SANS
    normal.font.size = Pt(10)
    normal.font.color.rgb = COCOA
    normal.element.rPr.rFonts.set(qn("w:eastAsia"), SANS)

    # Header: centred logo over a hairline bronze rule
    hp = sec.header.paragraphs[0]
    hp.alignment = WD_ALIGN_PARAGRAPH.CENTER
    hp.add_run().add_picture(str(LOGO), width=Cm(4.0))
    spacing(hp, after=0, line=1.0)
    par_border(hp, "bottom", HEX["clay"], size=4, space=6)

    # Footer: address, legal line, document number and page x of y
    f = sec.footer
    p1 = f.paragraphs[0]
    p1.alignment = WD_ALIGN_PARAGRAPH.CENTER
    par_border(p1, "top", HEX["clay"], size=4, space=6)
    add_inline(p1, FOOTER_ADDRESS, size=7, color=TAUPE)
    spacing(p1, after=0, line=1.1)
    p2 = f.add_paragraph()
    p2.alignment = WD_ALIGN_PARAGRAPH.CENTER
    add_inline(p2, FOOTER_LEGAL, size=7, color=TAUPE)
    spacing(p2, after=0, line=1.1)
    p3 = f.add_paragraph()
    p3.alignment = WD_ALIGN_PARAGRAPH.CENTER
    spacing(p3, before=2, after=0, line=1.1)
    lead = p3.add_run(f"{doc_no}  ·  Confidential — internal draft  ·  Page " if doc_no else "Page ")
    set_font(lead, size=7, color=BRONZE)
    add_field(p3, "PAGE", 7, BRONZE)
    r = p3.add_run(" of ")
    set_font(r, size=7, color=BRONZE)
    add_field(p3, "NUMPAGES", 7, BRONZE)
    return doc


# ------------------------------------------------------------ markdown
def add_table(doc, rows):
    if not rows:
        return
    ncols = max(len(r) for r in rows)
    table = doc.add_table(rows=len(rows), cols=ncols)
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    tbl_pr = table._tbl.tblPr
    borders = OxmlElement("w:tblBorders")
    for side in ("top", "left", "bottom", "right", "insideH", "insideV"):
        el = OxmlElement(f"w:{side}")
        el.set(qn("w:val"), "single")
        el.set(qn("w:sz"), "4")
        el.set(qn("w:color"), HEX["clay"])
        borders.append(el)
    tbl_pr.append(borders)
    for ri, row in enumerate(rows):
        for ci in range(ncols):
            text = row[ci] if ci < len(row) else ""
            cell = table.cell(ri, ci)
            p = cell.paragraphs[0]
            spacing(p, before=2, after=2, line=1.15)
            if ri == 0:
                shade(cell._tc.get_or_add_tcPr(), HEX["espresso"])
                add_inline(p, text.replace("**", ""), size=8.5, color=RGBColor(0xFB, 0xF5, 0xEE), bold=True)
            else:
                if ri % 2 == 0:
                    shade(cell._tc.get_or_add_tcPr(), HEX["shell"])
                add_inline(p, text, size=8.5)
    # repeat header row on each page
    trpr = table.rows[0]._tr.get_or_add_trPr()
    hdr = OxmlElement("w:tblHeader")
    hdr.set(qn("w:val"), "true")
    trpr.append(hdr)
    gap = doc.add_paragraph()
    spacing(gap, after=4, line=1.0)


def is_sep_row(line):
    s = line.strip().strip("|").replace("|", "").replace(":", "").replace("-", "").replace(" ", "")
    return s == "" and "-" in line


def build_docx(md_path, out_path):
    text = md_path.read_text(encoding="utf-8")
    lines = text.splitlines()

    title, doc_no, meta = md_path.stem, "", ""
    for ln in lines[:8]:
        if ln.startswith("# "):
            title = ln[2:].strip()
        m = re.match(r"^>\s*(Document No\..*)$", ln.strip())
        if m:
            meta = m.group(1)
            dm = re.search(r"(AUR-[A-Z]+-\d+)", meta)
            doc_no = dm.group(1) if dm else ""
            break

    doc = setup_document(doc_no)
    doc.core_properties.title = title
    doc.core_properties.author = "The Aura Reset Center"

    i, n = 0, len(lines)
    seen_title = seen_meta = False
    counters = [0, 0]  # running numbers for top-level and nested numbered lists
    while i < n:
        raw = lines[i]
        ln = raw.rstrip()
        s = ln.strip()

        if not s:
            i += 1
            continue
        if not re.match(r"^\s*(\d+[.)]|[-*]) ", ln):
            counters = [0, 0]

        if s == "<<<PAGEBREAK>>>":
            doc.add_paragraph().add_run().add_break(WD_BREAK.PAGE)
            i += 1
            continue

        if s.startswith("# ") and not seen_title:
            seen_title = True
            p = doc.add_paragraph()
            r = p.add_run(s[2:].strip())
            set_font(r, DISPLAY, 22, ESPRESSO)
            spacing(p, after=2, line=1.1)
            i += 1
            continue

        if s.startswith(">") and meta and not seen_meta and meta in s:
            seen_meta = True
            p = doc.add_paragraph()
            add_inline(p, meta, size=8, color=TAUPE)
            spacing(p, after=14, line=1.1)
            par_border(p, "bottom", HEX["bronze"], size=6, space=8)
            i += 1
            continue

        if s.startswith("# "):  # a later H1 (e.g. multi-form documents)
            p = doc.add_paragraph()
            set_font(p.add_run(s[2:].strip()), DISPLAY, 18, ESPRESSO)
            spacing(p, before=10, after=6, line=1.1)
            i += 1
            continue
        if s.startswith("## "):
            p = doc.add_paragraph()
            set_font(p.add_run(s[3:].strip().replace("**", "")), DISPLAY, 14, ESPRESSO)
            spacing(p, before=14, after=5, line=1.1)
            p.paragraph_format.keep_with_next = True
            i += 1
            continue
        if s.startswith("### "):
            p = doc.add_paragraph()
            set_font(p.add_run(s[4:].strip().replace("**", "").upper()), SANS, 8.5, BRONZE, bold=True)
            spacing(p, before=10, after=3, line=1.1)
            p.paragraph_format.keep_with_next = True
            i += 1
            continue

        if s in ("---", "***", "___"):
            p = doc.add_paragraph()
            spacing(p, before=4, after=8, line=1.0)
            par_border(p, "bottom", HEX["clay"], size=4, space=1)
            i += 1
            continue

        if s.startswith("|"):
            block = []
            while i < n and lines[i].strip().startswith("|"):
                if not is_sep_row(lines[i]):
                    block.append([c.strip() for c in lines[i].strip().strip("|").split("|")])
                i += 1
            add_table(doc, block)
            continue

        if s.startswith(">"):
            body = []
            while i < n and lines[i].strip().startswith(">"):
                body.append(lines[i].strip().lstrip(">").strip())
                i += 1
            p = doc.add_paragraph()
            shade(p._p.get_or_add_pPr(), HEX["shell"])
            par_border(p, "left", HEX["bronze"], size=18, space=8)
            p.paragraph_format.left_indent = Cm(0.3)
            add_inline(p, " ".join(b for b in body if b), size=9, color=COCOA, italic=False)
            spacing(p, before=4, after=8, line=1.25)
            continue

        m_b = re.match(r"^(\s*)[-*] (.*)$", ln)
        m_n = re.match(r"^(\s*)(\d+)[.)] (.*)$", ln)
        if m_b or m_n:
            indent = len((m_b or m_n).group(1))
            level = 1 if indent >= 2 else 0
            if m_b:
                style = "List Bullet 2" if level else "List Bullet"
                content = m_b.group(2)
                p = doc.add_paragraph(style=style)
            else:
                style = "List Number 2" if level else "List Number"
                content = m_n.group(3)
                # Use a literal number so separate lists don't continue counting
                p = doc.add_paragraph()
                p.paragraph_format.left_indent = Cm(0.63 + 0.63 * level)
                p.paragraph_format.first_line_indent = Cm(-0.5)
                counters[level] += 1
                if level == 0:
                    counters[1] = 0
                r = p.add_run(f"{counters[level]}.\t")
                set_font(r, size=10, color=BRONZE, bold=True)
                p.paragraph_format.tab_stops.add_tab_stop(Cm(0.63 + 0.63 * level))
            add_inline(p, content)
            spacing(p, after=3, line=1.25)
            i += 1
            continue

        # plain paragraph: join soft-wrapped lines
        buf = [s]
        i += 1
        while i < n:
            nxt = lines[i].strip()
            if (not nxt or nxt.startswith(("#", "|", ">", "- ", "* ", "<<<")) or re.match(r"^\d+[.)] ", nxt)
                    or nxt in ("---", "***", "___")):
                break
            buf.append(nxt)
            i += 1
        p = doc.add_paragraph()
        add_inline(p, " ".join(buf))
        spacing(p, after=6, line=1.3)

    # Bullet colour/font
    for name in ("List Bullet", "List Bullet 2"):
        st = doc.styles[name]
        st.font.name = SANS
        st.font.size = Pt(10)
        st.font.color.rgb = COCOA

    out_path.parent.mkdir(parents=True, exist_ok=True)
    doc.save(out_path)


def to_pdf(docx_path, pdf_dir):
    pdf_dir.mkdir(parents=True, exist_ok=True)
    subprocess.run(["soffice", "--headless", "--convert-to", "pdf", "--outdir", str(pdf_dir), str(docx_path)],
                   check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)


def main(argv):
    make_pdf = "--no-pdf" not in argv
    targets = [Path(a) for a in argv if not a.startswith("--")]
    files = [t.resolve() for t in targets] if targets else sorted(CONTENT.glob("*/*.md"))
    for md in files:
        group = md.parent.name
        out = OUT_WORD / group / (md.stem + ".docx")
        build_docx(md, out)
        if make_pdf:
            to_pdf(out, OUT_PDF / group)
        print(f"built {group}/{md.stem}")


if __name__ == "__main__":
    main(sys.argv[1:])
