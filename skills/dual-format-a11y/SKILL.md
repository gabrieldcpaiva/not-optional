---
name: dual-format-a11y
description: Analyze design specifications and webpage content to separate accessibility into web components (ARIA, keyboard focus, live regions) and static print assets (vector text, minimum point size, correct physical dimensions). Strip web-only markup from print configurations and verify print readiness.
---

# Dual-Format Accessibility Workflows

Separate dynamic web accessibility requirements from static print/PDF standards for products that ship both a storefront experience and downloadable assets.

## Core Principle

Web a11y and print a11y solve different problems. Never let ARIA, live regions, or focus management leak into print PDFs. Never let print-only constraints dictate the interactive storefront.

## Process

1. Ingest design specs, HTML/CSS, or webpage content for dual-delivery products.
2. Identify all web-only accessibility features (ARIA attributes, focus states, live regions).
3. Identify all print-specific requirements (minimum 12pt body text, vector text, physical margins, page size).
4. Produce two clean outputs:
   - Web version that retains full interactive accessibility
   - Print/PDF version with web-only markup removed and print constraints enforced
5. Verify that neither version contaminates the other.
