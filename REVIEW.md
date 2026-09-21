# Review: not-optional

First of all, congratulations on your first open source project! The repository has a very strong and opinionated stance, which is exactly what a good standard needs. You have done an excellent job of making accessibility actionable rather than just a theoretical checklist.

Here is a comprehensive review of what works, what doesn't, and suggestions for improving accessibility for both humans and AI agents.

## What Works Exceptionally Well

1. **Deterministic Constraints:** Your rules are incredibly clear and testable. Phrases like "Max visual lines per body block: 4", "Safe margin: 12.7mm", and "Ring: 3px solid, 2px offset" leave no room for ambiguity. This is perfect for both developers and AI agents.
2. **Dual-Medium Focus:** Treating web and physical print as two different mediums with distinct rules (e.g., no ARIA in PDFs) is a rare and highly valuable perspective.
3. **Modularity without Bloat:** The separation of `principles` (core laws) and `skills` (specific agent instructions) is very clean. The lack of heavy dependencies or build steps makes it lightweight and trustworthy.
4. **Tone Accessibility:** The `tone-accessibility-auditor` is a fantastic addition. Cognitive load and anxiety-inducing copy are often overlooked in standard a11y checklists.
5. **Clear Licensing and Status:** Having a `STATUS.md` freezing V1 and a clear dual-license (MIT/CC-BY) is very professional.

## What Could Be Improved

1. **Fragmentation for Agents:** While modularity is great, asking an LLM or an agent to piece together instructions from 14 different files (`principles/*` + `skills/*/SKILL.md`) can lead to context loss. Most modern AI workflows benefit from a single, cohesive context file.
2. **Human Onboarding:** For a human developer stumbling onto the repo, reading through rules is good, but seeing them in action is better. There are currently no complete examples of what a "compliant" HTML file or print PDF looks like.
3. **"Load with" Syntax:** The `SKILL.md` files use a `## Load with` directive. While a human understands this means "read this other file too," an AI agent might not automatically resolve and read those relative file paths unless specifically programmed to do so.

## Suggestions for Wider Accessibility

To make this toolkit easily adopted by anyone (human or agent), consider the following additions:

### 1. Create a Unified "System Prompt"
Create a single file (e.g., `not-optional-prompt.md` or `.cursorrules`) that concatenates the most critical rules into one dense document.
* **Why:** If a user wants their AI assistant (like ChatGPT, Cursor, or Claude) to follow your standard, they can just paste one file into their system prompt or project instructions instead of copying 10 separate files.

### 2. Add Practical Examples
Add an `examples/` directory containing:
* `web-example.html`: A minimal HTML file demonstrating the focus rings, native elements, and micro-chunking.
* `print-example.html` / `print-example.pdf`: A minimal example demonstrating the 12pt font, safe margins, and monochrome tokens.
* **Why:** Humans learn by example. Providing a "known good" baseline helps developers instantly grasp the end goal.

### 3. Make it "Drop-in" for Modern Tools
You mentioned you don't want "arena agents things", which is fair. But many developers use tools like Cursor or GitHub Copilot.
* Consider providing a script (e.g., `cat-all.sh`) that users can run to generate a `.cursorrules` file for their local repository.
* This bridges the gap between "copy one file" and "enforce this standard across my entire project."

### 4. Standardize the JSON structure
In `tokens.screen.json`, you provide example hexes. It might be useful to define a standard JSON schema (`$schema`) for these tokens so that if a developer changes them, their IDE can validate that they haven't accidentally removed a required key like `focus.width`.

## Conclusion
This is a brilliant and highly focused repository. By adding a single unified entry point for AI context windows and a couple of tangible code examples, you can drastically reduce the friction for adoption without adding unnecessary bloat.
