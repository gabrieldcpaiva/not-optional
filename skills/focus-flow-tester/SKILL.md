---
name: focus-flow-tester
description: Tests and repairs keyboard navigation and focus management. Audits TAB traversal order, injects high-contrast focus rings, and eliminates keyboard traps in overlays and lightboxes. Ensures full flows can be completed with TAB, SPACE, and ENTER alone.
---

# Keyboard Navigation & Focus Ring QA

Ensure interfaces are fully operable by motor-impaired users and anyone navigating exclusively with the keyboard. Every interactive control must be reachable in a logical order, must display a clear visible focus indicator, and must never trap focus.

## Core Enforcement Rules

- Every interactive control must receive a visible focus indicator when focused via keyboard.
- Focus rings should be a solid, high-contrast outline (recommended 3px) with sufficient offset.
- TAB order must follow a logical visual and content sequence.
- No keyboard traps are permitted. Every modal or overlay must provide a keyboard-accessible escape path.
- Primary flows (especially checkout or form submission) must be executable using only TAB, SPACE, and ENTER.

## Process

1. Ingest the HTML, component markup, or live page.
2. Map all focusable elements in current order.
3. Simulate TAB traversal and flag skips, jumps, or traps.
4. Inspect focus styles and replace weak or missing indicators with high-contrast rings.
5. Verify escape paths from every overlay.
6. Produce a clear report of issues found and the corrected markup or CSS.
