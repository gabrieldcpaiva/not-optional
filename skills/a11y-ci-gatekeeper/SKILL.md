---
name: a11y-ci-gatekeeper
description: Runs automated accessibility regression checks before publishing. Uses axe-core and pa11y-style rules to block contrast, alt-text, focus, and keyboard regressions. Exit 0 pass, exit 1 fail.
---

# Automated Accessibility Regression Tester

Zero accessibility regressions on production-bound builds.

## Core Enforcement Rules

- Contrast below WCAG 2.1 AA blocks release (4.5:1 normal text, 3:1 large text and UI).
- Interactive images missing meaningful alt text block release.
- Interactive controls without a visible focus indicator block release.
- Keyboard traps or incomplete keyboard operability on primary flows block release.
- Missing ARIA on expandables, broken heading order, and hue-only state indicators block unless waived in writing.

## Inputs and outputs

- Input: built static directory or local URL.
- Output: `./reports/a11y-report.json` when the runner supports it.
- Exit `0` = pass. Exit `1` = violation.

## Execution

```bash
npx pa11y-ci --config .pa11yci.json
```

Use root `.pa11yci.json`. Standard: WCAG2AA. Runners: axe + htmlcs.
This repo does not require npm install to use the skill. The command is optional local tooling.

## Acceptance

- [ ] Scan completes against listed URLs.
- [ ] WCAG 2.1 AA violations = 0.
- [ ] Missing alt, broken ARIA, and contrast failures fail the gate.
