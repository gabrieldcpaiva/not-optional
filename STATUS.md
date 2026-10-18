# Status: v1 released, still improving

Date: 2026-09-24

v1.0.0 was released on 2026-09-24. Work continues and current enhancements are tracked in `ROADMAP.md`.

In the tree:

- Public repository
- Universal rules, not tied to a specific brand or shop
- Dual license (MIT for software, CC BY 4.0 for docs and principles)
- Principles and design token JSON (token names first, hex values only as examples), with JSON schema validation (`schemas/`)
- Nine agent skills, each with measurable numbers and one ban per file (e.g., no clickable divs)
- `agent-instructions.md` master context, rebuilt with `build-agent-context.sh`
- Web and print baselines (`examples/`)
- GitHub Action template for accessibility testing (`.github/workflows/a11y-check.yml`)

Not in scope yet:

- Focus CSS snippet file, SVG pack, speech scripts
- Testing the rules against a low-cost AI model
