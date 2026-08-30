# not-optional

Accessibility is not a request.

It is not something you add because of a fine or an invoice.
It is not a premium feature.
It is baseline competence inside the workflow.

This repository is a technical toolkit for web interfaces and physical printables. It combines WAI / WCAG 2.1 AA practice with four additional constraints that checklists often skip:

1. Physiological contrast (avoid pure black-on-white visual vibration)
2. Executive-function chunking (short measures, hard paragraph caps, empty space)
3. Dual medium (web code ≠ print geometry)
4. Multi-channel state (never hue alone)

It is for any surface a human has to read, tap, or print. Not for one brand, one shop, or one product line.

### Dual-medium boundary

- **Web:** semantic HTML, `:focus-visible`, WCAG 2.1 AA, ARIA only when a native element cannot express the state.
- **Print:** vector text, ≥12pt body, ≥12.7mm safe margins, high-contrast ink-saving layers. No ARIA, no focus logic, no live regions in PDFs.

### What this is

- Nine agent skills (`skills/*/SKILL.md`)
- Principles plus machine-readable token files
- Copy one file or the whole suite
- No installer required

### How to use it

1. Open the skill you need.
2. Copy `SKILL.md`.
3. Paste it into your agent or skills folder.

**Agent load order**

1. `principles/tokens.screen.json` (web) or `principles/tokens.print-monochrome.json` (print)
2. Matching files under `principles/`
3. The `SKILL.md` files you need
4. Fail closed on critical violations

Optional local HTML scan. Prerequisites: Node.js 18 or newer, Chrome or Chromium, npm access.

1. Add your URLs to `.pa11yci.json` under `"urls"` (example: `"http://localhost:8080/"`).
2. Serve your site, then run:

```bash
npx pa11y-ci --config .pa11yci.json
```

Exit `0` = pass. Any non-zero exit = fail. pa11y uses exit `2` for accessibility errors and `1` for a technical fault, so test for non-zero, not for `1`. Optional tool, not a hidden dependency.

### License

Software: MIT.  
Documentation and design principles: CC BY 4.0.
