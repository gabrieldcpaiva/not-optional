---
name: focus-flow-tester
description: Tests keyboard navigation, 3px Deep Moss focus rings, Escape dismiss, skip links, and Tab / Shift+Tab loops. No keyboard traps.
---

# Keyboard Navigation & Focus Ring QA

## Core Enforcement Rules

- Every interactive control gets a visible `:focus-visible` indicator.
- Focus ring: `3px solid #4A5D4E` with `2px` offset. Forks may change the color if contrast holds.
- TAB order follows reading order.
- No keyboard traps.
- Escape closes the topmost modal and restores focus to the opener.
- Skip-link target exists and receives focus.
- Primary flows complete with TAB, SHIFT+TAB, SPACE, ENTER, and ESC only.

## Process

1. Inventory focusable controls.
2. Walk Tab and Shift+Tab; flag skips, jumps, and reverse-order failures.
3. Open each overlay; confirm Escape dismiss and focus restoration.
4. Confirm skip-link destination.
5. Report failures and the corrected CSS/markup.
