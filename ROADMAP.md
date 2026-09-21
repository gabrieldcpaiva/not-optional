# Roadmap: Enhancing `not-optional` Accessibility

This roadmap outlines a step-by-step plan to transform the `not-optional` toolkit from a collection of brilliant, modular rules into a highly accessible, "drop-in" standard that is instantly usable by human developers and AI agents alike.

## Phase 1: AI Agent Unification (The "Drop-In" Context)
Currently, an AI needs to stitch together multiple markdown files. We need to create a single source of truth for AI context windows.

### Tasks:
- [ ] **Create `agent-instructions.md`**: Combine the core laws from all `principles/` and `skills/` files into a single, dense Markdown file. This file will serve as the master prompt for any LLM (ChatGPT, Claude, etc.) instructed to build accessible UI.
- [ ] **Create `.cursorrules` (or similar IDE rules)**: Provide a pre-packaged ruleset that users can drop directly into their repository to enforce these accessibility constraints instantly in tools like Cursor or GitHub Copilot.
- [ ] **Develop an Aggregator Script (`build-agent-context.sh`)**: Instead of manually maintaining `agent-instructions.md`, write a simple bash script that concatenates the principles and skills into one file whenever updates are made.

## Phase 2: Human Onboarding & Tangible Examples
Rules are powerful, but humans learn best by seeing working code. We need a definitive "good" baseline.

### Tasks:
- [ ] **Create an `examples/` directory.**
- [ ] **Web Example (`examples/web-baseline.html`)**:
  - Implement a simple interface (e.g., a form or a card layout).
  - Demonstrate strict adherence: native HTML elements, `focus-visible` with the 3px/2px offset, semantic headings, and text contrast complying with WCAG 2.1 AA.
  - Implement the micro-chunking laws (max 4 visual lines, 45 words, 65-75 characters per line).
- [ ] **Print Example (`examples/print-baseline.html` & `print-baseline.pdf`)**:
  - Demonstrate the strict 12.7mm safe margins.
  - Apply the monochrome high-contrast print tokens.
  - Use vector text, 12pt minimum font size, and a line-height of ≥1.4.
  - Include an example of the QR code specification from `alt-audio-synthesizer`.

## Phase 3: Token Validation & Developer Experience (DX)
Right now, the JSON files (`tokens.screen.json` and `tokens.print-monochrome.json`) contain examples, but they lack schema validation.

### Tasks:
- [ ] **Create JSON Schemas**:
  - Define `schemas/tokens.schema.json`.
  - Enforce required keys (e.g., `color.canvas`, `color.text`, `focus.width`).
  - Link the schema in the token JSON files so modern IDEs (VSCode, WebStorm) provide autocomplete and instantly flag missing or invalid keys.
- [ ] **Update README.md**:
  - Add a "Quick Start for AI" section linking to the new unified prompt file.
  - Add a "Quick Start for Humans" section linking to the examples.

## Phase 4: CI/CD & Automation (Optional but Recommended)
Make the `a11y-ci-gatekeeper` fully actionable.

### Tasks:
- [ ] **Provide a GitHub Action Template**: Provide a `.github/workflows/a11y-check.yml` template using `pa11y-ci` so users can just copy-paste it into their repos to enforce the laws on every PR.

## Execution Plan & Status Unfreezing
> **Note:** According to `STATUS.md`, the repository is currently in a "V1 frozen" state.
> To begin executing this roadmap, the next commit must include the word `unfreeze` in the commit message to signal the resumption of the learning loop.

**Next Steps to Start:**
1. Commit `unfreeze` to open development.
2. We tackle Phase 1 first to make this instantly useful for your new GitHub Agent.
