# Botany Properties letterhead and company stamp

Reusable brand assets for Botany Properties L.L.C letters, plus the script that builds a letter on the letterhead.

## Assets (`assets/`)

| File | What it is |
|---|---|
| `botany-stamp.png` | Company stamp, 1000 x 1000 px, transparent background, full opacity. Digital rebuild of the physical round stamp: double outer ring, Arabic name on the top arc, two stars, "BOTANY PROPERTIES L.L.C" on the bottom arc, inner ring with the lotus and "DUBAI – U.A.E". |
| `botany-stamp-for-documents.png` | Same stamp at 88% opacity, the version placed on letters. |
| `botany-stamp-source.html` | Editable SVG source of the stamp (render with headless Chromium, `omitBackground: true`). |
| `botany-logo.png` | Lotus mark and BOTANY Properties wordmark on the brand green (#283718), cropped clean from the brand image. |
| `letterhead-header-band.png` | Full-bleed header band, 2550 x 560 px (8.5 in wide at 300 dpi). |
| `letterhead-footer-bar.png` | Thin green bar for the bottom page edge. |

## Building a letter

`build-letter.js` uses the `docx` npm package (`npm install docx`). Edit the `body` array with the letter text, then:

```bash
node build-letter.js
```

Layout rules the script encodes:

- US Letter, 1 in side margins, top margin clears the header band, footer with green rule, company name and "Dubai, United Arab Emirates".
- Header and footer repeat on every page.
- The stamp is a floating image anchored to the "Yours sincerely," paragraph, 150 x 150 px, tilted 8 degrees, placed 4.55 in from the left margin so it sits in the clear space to the right of the name, signature and date lines and never overlaps text.

`examples/` holds the goAML authorisation letter to the UAE Financial Intelligence Unit built with this script.
