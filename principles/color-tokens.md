# Dual-Layer Color Tokens

Accessibility requires two different color systems depending on the medium.

Machine-readable sources:

- `principles/tokens.screen.json`
- `principles/tokens.print-monochrome.json`

These values are a **reference palette** (warm paper, muted sage, dark ink). Forks may substitute equivalent low-saturation screen colors and high-contrast print colors. The rules are the law: two maps, no pure black-on-white vibration, no hue-only state.

## Screen (Comfort Mode)

- Paper `#F7F3EE`
- Sand `#E8D9C8`
- Sage `#7A8F7A`
- Deep Moss `#4A5D4E`
- Warm Edge `#DFCDBA`
- Ink `#2C2A28`

## Print (High-Contrast / Low-Ink Mode)

Target ≥7:1 for body text on cheap inkjets. Body text stays Ink `#2C2A28` (not pure `#000000` on `#FFFFFF`) to avoid visual vibration. Strokes may use a 100% dark channel. Paper stock may be white.

## Implementation

Never force the screen comfort palette onto print. Never force print-high-contrast values onto a calm screen interface.
