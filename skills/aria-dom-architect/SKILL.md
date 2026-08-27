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
