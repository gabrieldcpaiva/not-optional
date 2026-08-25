---
name: cognitive-load-linter
description: Scans product copy and layout templates for paragraphs exceeding 4 lines, inserts clear bulleted lists for long descriptions, and enforces at least 40 percent empty space on printable canvases to reduce cognitive load for neurodivergent users.
---

# Cognitive Load & Micro-Chunking Linter

Enforce micro-chunking and generous negative space so neurodivergent and high-stress users can process product copy and printable layouts without executive overload or visual fatigue.

## Core Enforcement Rules

- Zero continuous body-text blocks longer than 4 lines.
- Convert any longer description into a short bulleted list.
- Every printable canvas must keep at least 40 percent unencumbered empty or negative space.

## Process

1. Ingest the supplied product copy, layout template, or text layer.
2. Identify every body-text block and measure line count under the intended rendering width.
3. Flag any block that exceeds 4 continuous lines of prose.
4. Rewrite flagged blocks into short sentences or bulleted lists.
5. Verify that printable pages maintain the 40% negative space rule.
