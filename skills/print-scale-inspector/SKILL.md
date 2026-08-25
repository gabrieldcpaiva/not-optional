---
name: print-scale-inspector
description: Inspects printable PDF layers and design specs to enforce a 12pt minimum body font (18pt+ for Large Print), left-aligned text blocks, and 12.7mm (0.5 in) safe margins that prevent home printer edge clipping.
---

# Physical Print Scale & Legibility Inspector

Enforce physical-print constraints that screen-based design cannot assume. Pinch-to-zoom does not exist on paper; body text that reads fine at 9–10 pt on a retina display becomes illegible once printed.

## Core Enforcement Rules

- Body text must be ≥ 12 pt. Large Print variants must be ≥ 18 pt.
- All body text blocks must be left-aligned. Justified text is forbidden because it produces irregular white-space rivers that impair reading fluency.
- Every page must maintain a minimum 12.7 mm (0.5 in) safe margin on all four sides.

## Process

1. Ingest the PDF, design specification, or print master.
2. Extract or declare the text layer and measure effective point sizes.
3. Measure distance from content to each page edge and flag anything inside the safe margin.
4. Inspect paragraph alignment and flag justified or problematic body text.
5. Produce a clear compliance report with concrete fixes (exact point sizes, alignment changes, margin adjustments).
