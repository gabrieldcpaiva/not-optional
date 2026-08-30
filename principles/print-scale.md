# Print scale and margins

## Law (not optional)

- Safe area: no text, art, QR, or fold-critical element inside 12.7mm (0.5in) of any trimmed edge on A4 and US Letter. The 12.7mm strip itself is the safe margin and it stays empty.
- Body type ≥ 12pt. Large print ≥ 18pt.
- Body line-height ≥ 1.5.
- Body text is vector and selectable, never a raster of type.
- Strokes ≥ 1.5pt (2px at 96dpi). Strokes under 1pt are forbidden on printables.
- Body ink is dark off-black (example `#2C2A28`), target ≥ 7:1 on cheap inkjet output. Never `#000000` body text on `#FFFFFF`.
- No ARIA, no focus logic, no live regions in PDFs. Print state is carried by geometry and text, per `principles/soft-geometry.md`.

This file is the single source of truth for print numbers. Skills may repeat a number so they can run standalone; if any file disagrees with this one, this file wins.
