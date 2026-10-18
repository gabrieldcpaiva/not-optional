# Contributing to not-optional

Thank you for your interest in contributing. This project is a technical toolkit for building accessible web interfaces and physical printables. You can learn more about it in the [README.md](README.md).

## How to report a problem

If you find a bug or an issue, please report it using the [bug report template](.github/ISSUE_TEMPLATE/bug_report.yml). Provide as much detail as you can so we can understand and fix the problem.

## How to propose a rule

A new rule must always come with evidence. When proposing a rule, please include:
- The problem it solves and who it helps.
- A measurable number or threshold (like a ratio, a size in px/pt/mm, a word or line count, or a timing).
- A clear source for that number (like a WCAG success criterion, a research paper, a standard, or documented user testing).
- The medium it applies to (web, print, or both).
- A short example showing a good and a bad implementation.

Rules proposed without numbers or sources are welcome, but they will be kept as discussions until evidence is provided.

## How to change a skill or principle

If you want to edit a skill or principle:
1. Make your edits to the files under `skills/*/SKILL.md` or `principles/`.
2. Run the build script: `./build-agent-context.sh`.
3. Commit the updated `agent-instructions.md` file along with your changes.
4. Run the test script to verify: `./test-build-agent-context.sh`.

## How to run the local scan

You can run an optional local accessibility scan using pa11y-ci. To do this, run:
```bash
npx pa11y-ci --config .pa11yci.json
```

## Licenses

- Code contributions are accepted under the [MIT License](LICENSE).
- Documentation and principle contributions are accepted under the [CC BY 4.0 License](LICENSE-CC-BY-4.0).

## Code of Conduct and Security

Please review our [Code of Conduct](CODE_OF_CONDUCT.md) to understand the standards for participating in our community. If you discover a security vulnerability, please refer to our [Security Policy](SECURITY.md) for reporting instructions.
