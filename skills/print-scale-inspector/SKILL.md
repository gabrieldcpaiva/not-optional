---
name: print-scale-inspector
description: Enforces ≥12pt body (18pt Large Print), left alignment, ≥1.4 line-height, 12.7mm safe margins, and vector text on print PDFs.
---

# Physical Print Scale & Legibility Inspector

## Core Enforcement Rules

- Body ≥12pt. Large Print ≥18pt.
- Body left-aligned only. Justified text forbidden.
- Line-height ≥1.4× body size (prefer 1.5).
- Safe margin ≥12.7mm on all four sides.
- Body text must be real/vector text, not rasterized type.

## Pre-flight

1. Ingest PDF or print master.
2. Check point size, line-height, alignment, and bounding-box distance to each edge.
3. Flag content inside the 12.7mm zone.
4. Report exact numeric fixes.
