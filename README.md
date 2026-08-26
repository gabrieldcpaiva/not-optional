# not-optional

Accessibility is not a request.

It is not something you add because you are afraid of a fine or an invoice.
It is not a premium feature.
It is baseline competence that should already be inside the workflow.

This repository is a working system for making digital products and printables usable by neurodivergent people, low-vision users, motor-impaired users, and everyone else — without turning accessibility into a fear product or a consultancy performance.

It was built from lived experience, not from a compliance checklist.

### Core Philosophy

Accessibility is not a feature, an upsell, a marketing lever, or an afterthought. This repository operationalizes lived experience into tools that reduce cognitive load, eliminate visual strain, and keep assistive-technology parity across digital interfaces and physical printables.

### Dual-Medium Boundary

- **Web:** semantic HTML, `:focus-visible`, WCAG 2.1 AA contrast, ARIA only when native elements cannot express the state.
- **Print:** vector text, ≥12pt body, 12.7mm safe margins, high-contrast ink-saving layers. Never leak ARIA or focus logic into PDFs.

### What this is

A practical, forkable toolkit that includes:

- Nine focused accessibility skills (agent-ready)
- Design principles plus machine-readable color tokens
- Clear separation between screen and print requirements
- No upsells, no audit theater, no invoices

### How to use it

**Simplest path (recommended):**
1. Open the skill you need
2. Copy the `SKILL.md`
3. Paste it into your agent or skills folder

You can take one skill or the entire suite.
Nothing here requires a special installer.

**Agent entry (when a storefront or printable is in context):**
1. Load every file under `skills/*/SKILL.md` you need, or the full suite.
2. Load matching files under `principles/`.
3. Ingest `principles/tokens.screen.json` for web work and `principles/tokens.print-monochrome.json` for print work.
4. Apply the skill enforcement rules. Fail closed on critical violations.

Optional local scan if you already have a built HTML page:

```bash
npx pa11y-ci --config .pa11yci.json
```

Exit `0` = pass. Exit `1` = violations. This repo does not ship an npm app; the command is optional tooling, not a hidden dependency.

### Repository structure

```
not-optional/
├── README.md
├── LICENSE
├── .pa11yci.json
├── skills/
│   ├── a11y-ci-gatekeeper/
│   ├── alt-audio-synthesizer/
│   ├── aria-dom-architect/
│   ├── cognitive-load-linter/
│   ├── dual-format-a11y/
│   ├── focus-flow-tester/
│   ├── multimodal-cue-agent/
│   ├── print-scale-inspector/
│   └── tone-accessibility-auditor/
└── principles/
    ├── color-tokens.md
    ├── tokens.screen.json
    ├── tokens.print-monochrome.json
    ├── typography.md
    ├── soft-geometry.md
    ├── contrast.md
    └── micro-chunking.md
```

### License

Software: MIT.
Documentation and design principles: CC BY 4.0.
Fork it. Use it. Improve it.
Do not turn it into a $7k fear product.
