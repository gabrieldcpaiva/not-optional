# Color tokens

Agents: read the JSON first. This file only states the rules.

```
principles/tokens.screen.json
principles/tokens.print-monochrome.json
```

## Law (not optional)

- Two maps. Screen comfort ≠ print contrast.
- Never pair `#000000` body text with `#FFFFFF` canvas (visual vibration).
- Never encode state with hue alone.
- Screen body contrast ≥ WCAG 2.1 AA (4.5:1 normal text).
- Print body contrast ≥ 7:1 on cheap inkjet output.

## Token keys (stable)

| Key | Role |
| --- | --- |
| `color.canvas` | Page background |
| `color.surface` | Secondary surface |
| `color.accent` | Quiet accent |
| `color.emphasis` | Focus rings, headings, structure |
| `color.divider` | Rules / separators |
| `color.text` | Body text |
| `focus.width` `focus.style` `focus.color` `focus.offset` | Keyboard focus (screen only) |

Hex values in the JSON are a **worked example** of a low-saturation warm screen set and an ink-safe print set. Replace them with any equivalents that still pass the law above. Do not treat example names or example hexes as a required brand.
