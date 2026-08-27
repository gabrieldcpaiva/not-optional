---
name: multimodal-cue-agent
description: State cannot be hue-only. Pair color with shape, pattern, or visible text. Decorative SVG aria-hidden; meaningful icons need a name.
---

# multimodal-cue-agent

## Load with

`principles/soft-geometry.md`

## Law (once)

- Color change is never the only state cue.
- Add at least one of: distinct shape, pattern fill, visible text label.
- Forbidden instruction: “click the green button” (or any hue-only direction).
- Decorative icon/SVG: `aria-hidden="true"` plus adjacent text or `.sr-only` text.
- Meaningful icon: accessible name required.

```html
<button type="button">
  <svg aria-hidden="true" focusable="false"></svg>
  <span>Saved</span>
</button>
```
