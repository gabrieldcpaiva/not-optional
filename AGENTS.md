# AI Agent Instructions for not-optional

If you are an AI agent working in this repository or contributing to it, you must follow the accessibility rules defined in `agent-instructions.md`.

## Agent Load Order

When parsing rules for a task, follow this precedence:
1. `principles/tokens.screen.json` (web) or `principles/tokens.print-monochrome.json` (print)
2. Matching files under `principles/`
3. The `SKILL.md` files you need from `skills/`
4. **Fail closed** on critical violations.

## Contributor Rules

- **Do not edit `agent-instructions.md` by hand.** It is auto-generated.
- If you edit any files in `principles/`, `skills/`, or the token schemas, you **must** run `./build-agent-context.sh` afterwards to rebuild the master file.
- Before committing, run `./test-build-agent-context.sh` to ensure the generated file matches the current rules.