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
