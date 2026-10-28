#!/usr/bin/env python3
"""Regenerate README.md: the index of every document in content/."""
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent
GROUPS = {
    "01-governance": "Governance & brand",
    "02-people-policies": "People policies",
    "03-safety-and-privacy": "Safety, hygiene & privacy",
    "04-client-policies": "Client-facing policies & service menu",
    "05-client-forms": "Client forms & consents",
    "06-hr-templates": "HR templates",
    "07-operations-sops": "Operations SOPs",
    "08-treatment-sops": "Treatment SOPs",
    "09-marketing-and-finance": "Marketing, website & finance",
}

HEAD = """# The Aura Reset Center — document pack

Pre-licence documents for The Aura Reset Center, Dubai, built from the company website and the General
Manager's operating decisions (see `BRIEF.md`). All are drafts. Prices are deliberately left as `AED [___]`
until final pricing is set. Anything in [square brackets] (shown in bronze in the Word/PDF files) is a blank to
fill in — trade license number, TRN, phone, email, Elevé settings, etc.

## Where the files are

- `output/word/` — editable Word files with the Aura letterhead (logo header, address and legal footer, page numbers)
- `output/pdf/` — the same documents as PDF
- `output/stationery/` — letterhead template (Word + PDF), business cards for all three leaders (90 × 55 mm,
  print-ready), compliment slip, DL envelope and email signatures
- `content/` — the Markdown source of every document; edit here and rebuild
- `brand/` — logo PNGs (light and dark) and the brand fonts (Marcellus, Jost, Caveat — install these on any
  computer that edits the Word files)

## Rebuilding

```
python3 build_documents.py      # all documents → Word + PDF
python3 build_stationery.py     # stationery
python3 make_index.py           # this README
```

## Still to come

- Elevé operating instructions — machine settings in the treatment SOPs are marked "[per Elevé protocol — pending]".
- Legal documents (employment contracts, shareholder agreement, supplier contracts) — after the trade license is issued.

## Contents
"""


def main():
    out = [HEAD]
    for folder, label in GROUPS.items():
        out += [f"### {label}", "", "| No. | Document |", "|---|---|"]
        for f in sorted((ROOT / "content" / folder).glob("*.md")):
            text = f.read_text(encoding="utf-8")
            title = re.search(r"^# (.+)$", text, re.M).group(1).strip()
            no = re.search(r"(AUR-[A-Z]+-\d+)", text)
            out.append(f"| {no.group(1) if no else ''} | [{title}](output/pdf/{folder}/{f.stem}.pdf) |")
        out.append("")
    (ROOT / "README.md").write_text("\n".join(out), encoding="utf-8")


if __name__ == "__main__":
    main()
