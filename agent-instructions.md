# not-optional: Agent Accessibility Instructions

This document aggregates the accessibility laws and constraints from the `not-optional` toolkit.
When building or auditing web interfaces and print documents, you must strictly follow these rules.

## Core Principles

### color-tokens
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

### contrast
# Contrast

## Physiological rule

Do not set body text to `#000000` on `#FFFFFF`. That pair is high ratio and still harmful: it produces visual vibration and text freezing for many dyslexic and fatigued readers.

Use off-black text on off-white canvas on screens. Example only: `#2C2A28` on `#F7F3EE` (≈13.5:1).

## Screen (WCAG 2.1 AA)

- Normal text ≥ 4.5:1
- Large text and UI components ≥ 3:1

## Print (physical)

CSS luminance is not ink. Target ≥7:1 for printed body text on cheap inkjets. Keep body as dark ink (example `#2C2A28`), not pure black on pure white. Strokes may use a full dark channel.

### micro-chunking
# Micro-chunking

## Law (not optional)

| Check | Threshold |
| --- | --- |
| Max visual lines per body block | 4 |
| Max words per body block | 45 |
| Max characters per line | 65 (hard max 75) |
| Min empty space on a printable canvas | 40% |

If any threshold is exceeded, split into a shorter paragraph or a list before publish.

## Intent

Executive-function support. Deterministic so an agent can fail a block without guessing viewport width.

### soft-geometry
# Geometry over hue

## Law (not optional)

- State, category, and progress must remain readable with color removed (grayscale, print, CVD).
- Pair every hue change with at least one of: distinct shape, pattern fill, or visible text label.
- Print strokes ≥ 1.5pt (≈2px at 96dpi). Strokes under 1pt are forbidden on printables.

## Generic motifs (examples, not a product pack)

Use ordinary geometry:

- rounded rectangle / pill
- circle / disc
- triangle / chevron
- hatch, dots, or dashes as fills

Do not require a private icon set, named product diagrams, or a brand motif library to satisfy this rule.

### typography
# Typography

## Law (not optional)

- **Body, UI, forms, tables, instructions:** sans-serif only. Serif is forbidden at these sizes.
- **Display headings ≥24pt / 32px only:** a warm open-geometry serif is allowed. Below that size, use the body sans.
- Body left-aligned. Justified text is forbidden.
- Body line-height ≥ 1.5. Display headings 1.2–1.3.
- Measure 45–65 characters per line. Hard max 75.
- Paragraph cap: ≤4 visual lines and ≤45 words, then a list or break.
- Print body ≥ 12pt. Large print ≥ 18pt.
- Screen layouts remain usable at 200% zoom with no horizontal scroll.

There is no contradiction: serif is a display-only exception, never a body face.

## Suggested faces (not required)

- Display (≥24pt): Fraunces or Lora, or any high-aperture serif.
- Body: Plus Jakarta Sans or Inter, or any humanist sans with a tall x-height and distinct `1` / `l` / `I`.
- Fallback: `ui-sans-serif, system-ui, sans-serif`.

Do not treat Tahoma/Arial as the standard. Do not treat the suggested faces as a brand kit.

## Agent Skills

### Skill: a11y-ci-gatekeeper
---
name: a11y-ci-gatekeeper
description: Block a release if WCAG 2.1 AA contrast, alt-text, focus, or keyboard checks fail. Optional command: npx pa11y-ci --config .pa11yci.json. Exit 0 pass, 1 fail.
---

# a11y-ci-gatekeeper

## Load with

`principles/contrast.md` and `.pa11yci.json` when a web URL or HTML build is in context.

## Law (once)

Fail closed if any of these are true:

- Text contrast below WCAG 2.1 AA (4.5:1 normal, 3:1 large text / UI)
- Interactive image missing meaningful `alt`
- Interactive control with no visible `:focus-visible` indicator
- Keyboard trap or primary flow not completable with Tab / Shift+Tab / Enter / Space / Escape

## Execution (optional tooling)

```bash
npx pa11y-ci --config .pa11yci.json
```

Exit `0` = pass. Exit `1` = fail. No npm app ships in this repo.

## Output

List each violation with the selector or URL. Do not ship if any critical item remains.

### Skill: alt-audio-synthesizer
---
name: alt-audio-synthesizer
description: For each printable, write a ~30s layout narration (70–90 words), a full-text transcript, and QR specs: ECC M or Q, ≥15×15mm, inside the 12.7mm safe margin.
---

# alt-audio-synthesizer

## Load with

`principles/print-scale` numbers: safe margin = 12.7mm (0.5in) on A4 and US Letter.

## Law (once)

- Output three things: spoken script, full-text transcript (no phone required), QR placement.
- Script length: ~30 seconds, 70–90 words. Layout order, zones, how to use. No `!`. No medical terms.
- QR: error correction Level M or Q, ≥15×15mm, high contrast, fully inside the 12.7mm safe margin.

## Output

Script, transcript, QR size, ECC level, corner, fallback URL.

### Skill: aria-dom-architect
---
name: aria-dom-architect
description: Sequential headings. Native HTML first. No clickable div or span. ARIA only for state native elements cannot express.
---

# aria-dom-architect

## Law (once)

- Headings sequential. No skipped levels. One `h1`.
- Native first: `<button>`, `<a href>`, `<label for>`, `<details>`/`<summary>`, `<dialog>`.
- Forbidden: clickable `<div>` or `<span>`; `div` + `onclick` + `role="button"` when a native control exists.
- `<div>` / `<span>` = layout only. No click handlers. No keyboard roles.
- Expand/collapse must expose `aria-expanded` and an accessible name.
- Meaningful images: descriptive `alt`. Decorative: `alt=""` or `aria-hidden="true"`.

## Output

Corrected markup plus a short list of what changed.

### Skill: cognitive-load-linter
---
name: cognitive-load-linter
description: Fail body blocks over 4 lines or 45 words or 65 characters per line. Printable canvas must keep ≥40% empty space.
---

# cognitive-load-linter

## Load with

`principles/micro-chunking.md`

## Law (once)

| Check | Fail if |
| --- | --- |
| Visual lines in one body block | > 4 |
| Words in one body block | > 45 |
| Characters per line | > 65 (hard max 75) |
| Empty space on a printable page | < 40% |

On fail: split into a shorter paragraph or a list. Do not publish the long block.

### Skill: dual-format-a11y
---
name: dual-format-a11y
description: Split web rules from print rules. No ARIA or focus logic in PDFs. Optional artifact names *_Screen_Comfort.pdf and *_Print_Monochrome_HighContrast.pdf.
---

# dual-format-a11y

## Load with

`principles/tokens.screen.json` for web. `principles/tokens.print-monochrome.json` for print. `principles/color-tokens.md`.

## Law (once)

Web ≠ print.

- Web may use ARIA, `:focus-visible`, live regions.
- Print may not. Print is geometry, type size, ink, and margins (safe margin = 12.7mm / 0.5in).
- Print body contrast target ≥ 7:1. Do not use `#000000` on `#FFFFFF` for body text.

If a printable is emitted, prefer two files:

- `*_Screen_Comfort.pdf`
- `*_Print_Monochrome_HighContrast.pdf`

### Skill: focus-flow-tester
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

### Skill: multimodal-cue-agent
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

### Skill: print-scale-inspector
---
name: print-scale-inspector
description: Print body ≥12pt (≥18pt large print), left-align only, line-height ≥1.4, safe margin ≥12.7mm (0.5in) on A4 and US Letter, vector text only.
---

# print-scale-inspector

## Load with

`principles/typography.md` and `principles/contrast.md`

## Law (once)

- Body ≥ 12pt. Large print ≥ 18pt.
- Body `text-align: left` only. Justified body is forbidden.
- Line-height ≥ 1.4× (prefer 1.5).
- Safe margin: no content inside 12.7mm (0.5in) of any edge on A4 and US Letter.
- Body must be vector/selectable text, not a raster of type.

## Output

Name the failing edge, point size, or alignment. Give the numeric fix.

### Skill: tone-accessibility-auditor
---
name: tone-accessibility-auditor
description: Ban ! in UI and instructions. Ban listed urgency and medical strings. Replace from the table. Intent is low-demand copy, not vibes.
---

# tone-accessibility-auditor

## Law (once)

Forbidden in instructions, product text, forms, errors, and CTAs:

- the character `!`
- last chance, don't miss out, act fast, buy now, limited time
- you've got this, amazing progress, celebrate every win
- symptom, disorder, treatment, intervention, deficit (as labels for the user)

Test = this list and the `!` ban. Not a mood judgment.

## Replace

| Forbidden | Use |
| --- | --- |
| Buy now / last chance / don't miss out | Available when you are ready / still listed |
| You've got this! | You can start with one step |
| Error! Invalid input | That field needs an email address |
| Warning! | This page did not save. You can try again |

## Output

Corrected copy and the strings removed.

## Design Tokens
Agents: Refer to the raw JSON files for exact values, but use these as a structural guide:

### Screen Tokens (principles/tokens.screen.json)
```json
{
  "name": "not-optional screen tokens",
  "version": "1.0.0",
  "note": "Example hexes. Swap any values that still meet principles/color-tokens.md and principles/contrast.md.",
  "tokens": {
    "color": {
      "canvas": { "value": "#F7F3EE" },
      "surface": { "value": "#E8D9C8" },
      "accent": { "value": "#7A8F7A" },
      "emphasis": { "value": "#4A5D4E" },
      "divider": { "value": "#DFCDBA" },
      "text": { "value": "#2C2A28" }
    },
    "focus": {
      "width": { "value": "3px" },
      "style": { "value": "solid" },
      "color": { "value": "#4A5D4E" },
      "offset": { "value": "2px" }
    }
  }
}
```

### Print Tokens (principles/tokens.print-monochrome.json)
```json
{
  "name": "not-optional print monochrome tokens",
  "version": "1.0.0",
  "note": "Example hexes. Body text is ink-dark, not #000 on #FFF.",
  "tokens": {
    "color": {
      "canvas": { "value": "#FFFFFF" },
      "surface": { "value": "#F0F0F0" },
      "line": { "value": "#2C2A28" },
      "text": { "value": "#2C2A28" }
    }
  }
}
```
