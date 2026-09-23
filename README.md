> **Status: V1 un-frozen.** See `ROADMAP.md` for current enhancements. Optional extras (CI, SVG pack, speech scripts) are not required.

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

### Quick Start for AI (Agents & LLMs)

If you are instructing an AI agent (like a GitHub Agent, Copilot, or Cursor) to build an accessible UI, provide them with the master context file:

1. Point your agent to read [`agent-instructions.md`](./agent-instructions.md).
2. Or, copy the contents of `agent-instructions.md` into your agent's system prompt / `.cursorrules` file.

- **Direct Link for Remote Agents**: Provide the raw GitHub URL so web-browsing agents (ChatGPT, Claude, Gemini) can ingest the master rules in one turn:
  `https://raw.githubusercontent.com/gabrieldcpaiva/not-optional/main/agent-instructions.md`
- **1-Line CLI Drop-In**: Add `curl` snippets for terminal and IDE agents (Cursor, Windsurf, Claude Code, Aider):
  ```bash
  # Download directly as Cursor rules
  curl -fsSL https://raw.githubusercontent.com/gabrieldcpaiva/not-optional/main/agent-instructions.md -o .cursorrules

  # Or append to existing agent context
  curl -fsSL https://raw.githubusercontent.com/gabrieldcpaiva/not-optional/main/agent-instructions.md >> .agent-rules.md
  ```

## Agent Skills Registry Command
For systems adhering to the agentskills.io specification:

```bash
npx skills add gabrieldcpaiva/not-optional
```

*To rebuild this file after modifying rules, run `./build-agent-context.sh`.*

### Quick Start for Humans

To understand what these rules look like in practice, see the concrete baseline examples:

- **Web:** [`examples/web-baseline.html`](./examples/web-baseline.html) (Demonstrates tokens, focus rings, micro-chunking, and semantic HTML).
- **Print:** [`examples/print-baseline.html`](./examples/print-baseline.html) (Demonstrates physical geometry, safe margins, and vector text).

### Dual-medium boundary

- **Web:** semantic HTML, `:focus-visible`, WCAG 2.1 AA, ARIA only when a native element cannot express the state.
- **Print:** vector text, ≥12pt body, ≥12.7mm safe margins, high-contrast ink-saving layers. No ARIA, no focus logic, no live regions in PDFs.

### What this is

- Nine agent skills (`skills/*/SKILL.md`)
- Principles plus machine-readable token files
- Copy one file or the whole suite
- No installer required

### How to use it manually

1. Open the skill you need.
2. Copy `SKILL.md`.
3. Paste it into your agent or skills folder.

**Agent load order**

1. `principles/tokens.screen.json` (web) or `principles/tokens.print-monochrome.json` (print)
2. Matching files under `principles/`
3. The `SKILL.md` files you need
4. Fail closed on critical violations

Optional local HTML scan:

```bash
npx pa11y-ci --config .pa11yci.json
```

Exit `0` = pass. Exit `1` = fail. Optional tool, not a hidden dependency.

### License

Software: MIT.  
Documentation and design principles: CC BY 4.0.
