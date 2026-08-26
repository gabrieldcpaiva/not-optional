---
name: dual-format-a11y
description: Splits web a11y from print a11y. Names dual artifacts and keeps ARIA out of PDFs.
---

# Dual-Format Accessibility Workflows

## Core Principle

Web a11y and print a11y solve different problems. Never leak ARIA, live regions, or focus management into print PDFs.

## Artifact names

- `*_Screen_Comfort.pdf` for screen-comfort review copies
- `*_Print_Monochrome_HighContrast.pdf` for home-print masters

Print body contrast target ≥7:1. Use `principles/tokens.print-monochrome.json` for print builds and `principles/tokens.screen.json` for web.

## Process

1. Split the spec into web-only and print-only requirements.
2. Emit both artifact names when a printable is produced.
3. Verify no web-only markup remains in the print file.
