---
name: dual-format-a11y
description: Split web rules from print rules. No ARIA or focus logic in PDFs. Optional artifact names *_Screen_Comfort.pdf and *_Print_Monochrome_HighContrast.pdf.
---

# dual-format-a11y

## Load with

`principles/tokens.screen.json` for web. `principles/tokens.print-monochrome.json` for print. `principles/color-tokens.md`.

## Law (once)

Web ≠ print.

- Web may use ARIA, `:focus-visible`, live regions.
- Print may not. Print is geometry, type size, ink, and margins (safe margin = 12.7mm / 0.5in).
- Print body contrast target ≥ 7:1. Do not use `#000000` on `#FFFFFF` for body text.

If a printable is emitted, prefer two files:

- `*_Screen_Comfort.pdf`
- `*_Print_Monochrome_HighContrast.pdf`
