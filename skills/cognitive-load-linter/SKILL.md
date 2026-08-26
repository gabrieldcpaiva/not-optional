---
name: cognitive-load-linter
description: Caps paragraphs at 4 lines / 45 words / 65 characters per line and enforces ≥40 percent empty space on printable canvases.
---

# Cognitive Load & Micro-Chunking Linter

## Core Enforcement Rules

- Zero continuous body-text blocks longer than 4 visual lines.
- Quantified cap: ≤65 characters per line and ≤45 words per paragraph before list decomposition.
- Convert longer descriptions into short bullets.
- Every printable canvas keeps ≥40 percent unencumbered space.

## Process

1. Ingest copy or layout text.
2. Measure line length in characters and word count per paragraph.
3. Flag blocks over 4 lines, 65 characters/line, or 45 words.
4. Rewrite into short sentences or bullets.
5. Verify printable negative-space quota.
