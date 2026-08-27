---
name: focus-flow-tester
description: Tab order matches reading order. Visible focus 3px solid + 2px offset. Escape closes overlay and restores focus. No keyboard traps.
---

# focus-flow-tester

## Load with

`principles/tokens.screen.json` (`focus.*` keys). Color hex is an example; contrast of the ring is the law.

## Law (once)

- Every interactive control has `:focus-visible`.
- Ring: 3px solid, 2px offset, contrast ≥ 3:1 against adjacent background.
- Tab order = reading order.
- Escape closes the top overlay and returns focus to the opener.
- Skip link exists and its target can take focus.
- No keyboard trap.
- Primary flow completable with Tab, Shift+Tab, Space, Enter, Escape only.
- Do not use `outline: none` unless a replacement ring meeting the rule above is present.

## Output

Failing control and the missing key or trap.
