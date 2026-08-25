---
name: a11y-ci-gatekeeper
description: Runs automated accessibility regression checks on storefront and product page releases before publishing. Uses axe-core and pa11y-style rules to block deployments that regress contrast, alt-text, focus indicators, or keyboard operability. Generates a compliance report for every release build.
---

# Automated Accessibility Regression Tester

Prevent storefronts and product pages from quietly losing accessibility quality over successive releases. Every candidate build must pass a fixed set of automated and rule-based checks before it is allowed to reach production.

## Core Enforcement Rules

- Zero accessibility regressions are permitted in any production-bound build.
- Critical failures that always block release:
  - Contrast ratio below WCAG 2.1 AA (4.5:1 for normal text, 3:1 for large text and UI components).
  - Interactive images or product thumbnails missing meaningful alt text.
  - Any interactive control lacking a visible focus indicator.
  - Keyboard traps or incomplete keyboard operability on primary flows (especially checkout).
- High-severity issues (missing ARIA on expandables, broken heading order, pure-color state indicators) also block unless explicitly waived with documented justification.
- The gatekeeper produces a machine-readable and human-readable compliance report for every run.

## Process

1. Ingest the candidate release (live preview URL, staging HTML, component library snapshot, or design-to-code export).
2. Run the automated rule suite focusing on contrast, alt-text, focus indicators, and keyboard operability.
3. Generate a clear pass/fail report with specific failures and suggested fixes.
4. Block the release if any critical or high-severity issues remain unaddressed.
