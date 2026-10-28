# Writing rules for every document (read fully before writing)

1. Read `/home/user/aura-reset-center/aura-documents/BRIEF.md` first. Use only its facts; unknowns become [Placeholders].
2. **Never print a price.** Every price is `AED [___]`. Percentages of member discounts (10% / 15%) from the brief are fine.
3. Each document is ONE Markdown file written to the folder you are given, named `NN-kebab-name.md` (NN = 01, 02…).
4. The first line of every file is `# <Document title>`. The second non-empty line is a metadata line exactly in this form:
   `> Document No. AUR-<GROUP>-<NN> · Version 0.1 (Draft) · Owner: <role> · Effective: [Date]`
   Do NOT add a company header, logo, address block or footer — the build script adds letterhead, page numbers and confidentiality footer.
5. Supported Markdown ONLY (the converter handles nothing else):
   - `#`, `##`, `###` headings (no deeper)
   - paragraphs, `**bold**`, `*italic*`
   - bullet lists with `- ` and numbered lists with `1. ` (one level of nesting allowed with two-space indent `  - `)
   - pipe tables with a header row and `|---|` separator (keep to ≤ 6 columns; use them for forms, matrices, logs)
   - `> ` blockquote for notes / callouts (one paragraph each)
   - `---` horizontal rule
   - form blanks as `__________` (underscores) and tick boxes as `☐`
   - a line `<<<PAGEBREAK>>>` on its own to force a new page
   - signature blocks: a table with columns like `| Name | Signature | Date |` and an empty row of blanks
   No HTML, no images, no code blocks, no footnotes, no emoji.
6. Write for Dubai, UAE (UAE Federal Decree-Law No. 33 of 2021 on labour relations; Federal Decree-Law No. 45 of 2021 on personal
   data protection (PDPL); Dubai Health Authority (DHA) for clinical services; Dubai Municipality for health & safety/hygiene;
   Dubai Civil Defence for fire). Cite laws generally — do not quote article numbers unless certain. Add the line
   `> Draft for internal use. To be reviewed by a UAE-qualified legal adviser once the trade license is issued.` near the top of any
   policy, contract, consent, waiver or T&C document.
7. Make documents genuinely usable and specific to The Aura (its 11 modalities, Elevé equipment, Hosts, memberships, founding members,
   Jumeirah 1 studio, Nov 2026 opening). Avoid generic filler. Be complete but tight: typically 600–2,500 words per document; forms shorter.
8. Use British/UAE spelling (colour, centre in prose — but keep the brand name "The Aura Reset Center" exactly). Calm, clear, professional tone.
9. Refer to the founders/GM by title (Founder & CEO, CEO, General Manager); never use he/she for them.
10. When finished, reply with ONLY a list of the files you wrote (path + one-line description). Do not paste document contents back.
