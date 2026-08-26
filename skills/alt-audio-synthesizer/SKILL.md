---
name: alt-audio-synthesizer
description: Builds ~30-second audio descriptions plus QR and a full-text transcript fallback for printables.
---

# Screen-Reader Audio Preview Synthesizer

## Core Enforcement Rules

- Every printable includes a QR linking to audio plus a full-text transcript page for users without a camera or mobile device.
- QR: error correction Level M or Q, minimum 15×15mm, high contrast, inside the 12.7mm safe margin, not clipped.
- Narration ~30 seconds (70–90 words): layout, zones, sequence, plain language.
- Complex diagrams get spoken alt-text.
- Tone stays low-demand. No exclamation points or medical jargon.

## Process

1. Ingest the sheet layout.
2. Draft narration and transcript.
3. Specify QR size, ECC level, placement, and fallback URL.
