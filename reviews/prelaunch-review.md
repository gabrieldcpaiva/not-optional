# Pre-launch review — `not-optional`

Reviewed branch: `arena/01a0505a-not-optional` @ `61907e9` ("fix(skills): tone dictionary, multimodal names, audio QR numbers")
Review date: 2026-08-30 · Reviewer scope: **every file in the repository** (19 files).

**Coverage confirmation.** Files read in full, no exceptions:

| Path | Status |
| --- | --- |
| `README.md` | read |
| `LICENSE` | read |
| `.pa11yci.json` | read (not in the provided structure list — reviewed anyway) |
| `principles/color-tokens.md`, `contrast.md`, `micro-chunking.md`, `soft-geometry.md`, `typography.md` | read |
| `principles/tokens.screen.json`, `principles/tokens.print-monochrome.json` | read (not in the provided structure list — reviewed anyway) |
| `skills/{a11y-ci-gatekeeper, alt-audio-synthesizer, aria-dom-architect, cognitive-load-linter, dual-format-a11y, focus-flow-tester, multimodal-cue-agent, print-scale-inspector, tone-accessibility-auditor}/SKILL.md` | read (all 9) |

Every numeric claim in the repo was recomputed (WCAG contrast math), and the pa11y exit-code claims were checked against pa11y's documentation. Nothing below is guessed.

---

## 0. Definitions applied in this review

These two terms are the rubric axes for every file below.

**Forkable** — a first-time contributor can run, adapt, and extend the toolkit without hidden setup. To qualify, the repo must expose: (a) prerequisites, (b) installation/entry steps, (c) inputs/outputs, (d) configuration points, (e) expected artifacts, (f) troubleshooting. A repo fails forkability if any runnable instruction errors as written, or if a referenced file does not exist.

**Agent-ready** — instructions are unambiguous, copy/paste friendly, and carry exact acceptance criteria: *what to check, how to verify it, and what "done" means*. A skill fails agent-readiness if a rule has no measurable threshold, if two loaded files state different thresholds for the same check, or if an agent cannot decide pass/fail from the text alone.

---

## 1. Executive summary

- **The stance is intact and rare.** The repo treats accessibility as baseline competence inside the workflow ("Accessibility is not a request", `README.md`), bans hue-only state, caps cognitive load with deterministic numbers, and explicitly refuses brand capture ("Do not treat the suggested faces as a brand kit", `principles/typography.md`). Nothing here needs softening. The fixes below are about making the machinery as good as the philosophy.
- **P0 — the repo cites a file that does not exist.** `skills/alt-audio-synthesizer/SKILL.md:10` says `Load with: principles/print-scale` — there is no `principles/print-scale.md`. This breaks the documented agent load order on first use.
- **P0 — a print instruction places content in the clipping zone.** "fully inside the 12.7mm safe margin" (`skills/alt-audio-synthesizer/SKILL.md:16`) literally instructs putting the QR code *inside* the 12.7mm keep-out strip, contradicting `skills/print-scale-inspector/SKILL.md:17` ("no content inside 12.7mm of any edge"). Margin-strip QRs get clipped by consumer printers.
- **P0 — the documented CI exit-code contract is factually wrong.** `README.md:49` and `skills/a11y-ci-gatekeeper/SKILL.md:27` say "Exit `0` = pass. Exit `1` = fail." pa11y exits **2** for accessibility errors and **1** for a technical fault. A gate scripted as `[ "$?" -eq 1 ]` treats real accessibility failures as a pass — the exact audit-theater failure mode this repo exists to prevent.
- **P0 — the shipped example token set fails the repo's own law.** `color.accent` `#7A8F7A` is **2.52:1** on `color.surface` `#E8D9C8` (fails the ≥3:1 UI rule) and **3.15:1** on canvas (fails 4.5:1 if used as text). Agents copy worked examples; the example must pass its own gate.
- **P0 — the only runnable command in the README fails as written.** `npx pa11y-ci --config .pa11yci.json` runs against `.pa11yci.json`, whose `"urls": []` is empty; pa11y-ci errors with no URLs configured, and the README never tells the contributor to add them or what prerequisites exist (Node 18+, Chrome/Chromium).
- **P1 — the README violates the repo's own heading law.** `# not-optional` (`README.md:1`) jumps straight to `###` headings (lines 18, 23, 30, 51) — a skipped level, which `skills/aria-dom-architect/SKILL.md` forbids ("Headings sequential. No skipped levels."). For a repo whose product *is* the rules, self-consistency is the product.
- **P1 — two loaded files state different line-height laws.** `principles/typography.md:8` says "Body line-height ≥ 1.5"; `skills/print-scale-inspector/SKILL.md:16` says "≥ 1.4× (prefer 1.5)" — and that skill loads typography.md. Deterministic agents need one number (1.5 — see fix).
- **P1 — motor-impairment coverage stops at the keyboard.** Focus/keyboard flow is excellent, but pointer/touch target size appears nowhere, despite the README's claim to cover "any surface a human has to read, **tap**, or print."
- **Print/web boundary is otherwise the strongest part of the design** — clearly stated twice, no real contradiction except the QR wording, and the dual-PDF artifact convention (`*_Screen_Comfort.pdf` / `*_Print_Monochrome_HighContrast.pdf`) is a genuinely good forkable convention.

---

## 2. Detailed file-by-file review

Format per file: **Findings → Evidence → Impact → Fix** (Fix cross-references section 3 where a paste exists).

---

### 2.1 `README.md`

**Findings.**
Good: the voice is the product — "Accessibility is not a request… not something you add because of a fine or an invoice" frames accessibility as baseline competence, not a service tier. The four constraints are numbered and each one is operationalized somewhere real in the repo (verified in §5). "How to use it" is a 3-step copy path with no installer, which is genuinely forkable. The dual-medium boundary is stated up front.

Breaks baseline competence:
1. Heading hierarchy skips a level (`#` → `###`), violating the repo's own sequential-headings law.
2. The exit-code contract is wrong (pa11y exits 2 on accessibility errors, 1 on technical fault — verified against pa11y's README).
3. The only executable instruction fails as written: `.pa11yci.json` has `"urls": []`, no URL-adding step, no prerequisites.
4. Not forkable per the definition in §0: no prerequisites, no inputs/outputs per skill, no troubleshooting, no glossary. "Fail closed on critical violations" (step 4 of load order) does not say where the critical list lives.
5. Terminology drift: the README says "safe margins" (things to keep clear) while `alt-audio-synthesizer` says "inside the safe margin" — same word, opposite meaning (see §4.3, stall point 1).

**Evidence.**
- `README.md:1` `# not-optional` → `README.md:18` `### Dual-medium boundary` (no `##` anywhere; confirmed by heading scan of all files).
- `README.md:49`: "Exit `0` = pass. Exit `1` = fail. Optional tool, not a hidden dependency."
- `README.md:44–48`: the `npx pa11y-ci` block, with no URL or prerequisite step; `.pa11yci.json` `"urls": []`.
- `README.md:41`: "Fail closed on critical violations" — no pointer to the list.

**Impact.**
For users: a screen-reader user navigating the README by headings loses the hierarchy the repo demands of everyone else; a first-time contributor hits an error on the repo's only runnable command and has no troubleshooting section to catch them (stall → abandonment, the classic forkability death). For maintainers: the wrong exit-code contract is a liability — anyone who wires the documented "exit 1" check into CI silently passes failures, which is audit theater with extra steps.

**Fix.** Full replacement README provided as **P1-1** (it also resolves P0-3 and P0-5 for this file). Surgical pastes for the exit code and scan prerequisites are in **P0-3/P0-5**.

---

### 2.2 `skills/a11y-ci-gatekeeper/SKILL.md`

**Findings.**
Good: the frontmatter `description` is a complete, agent-discoverable contract (what it blocks + the command + exit semantics). "Fail closed if any of these are true" is a proper deterministic gate list — contrast thresholds, alt, focus, keyboard trap, all measurable. "No npm app ships in this repo" is the right anti-dependency stance. The `Load with` line correctly names an existing file (`principles/contrast.md`).

Breaks baseline: the exit-code line is wrong (same as README). Agent-ready gap: "List each violation with the selector or URL" has no output format, so two runs produce non-comparable artifacts.

**Evidence.**
- `SKILL.md:27`: "Exit `0` = pass. Exit `1` = fail. No npm app ships in this repo."
- `SKILL.md:12–16`: the fail-closed list (good — this is the "critical violations" list the README should point at).

**Impact.**
The gate is the repo's enforcement teeth; a wrong exit contract means the gate can pass a failing build. Low-vision/keyboard users are the ones the gate silently stops protecting. Non-deterministic output format means maintainers can't diff runs.

**Fix.** P0-3 (exit codes), P2-7 (output format).

---

### 2.3 `skills/alt-audio-synthesizer/SKILL.md`

**Findings.**
Good: this is the most original skill in the suite and the most lived-experience-driven — a ~30s layout narration *plus* a full-text transcript "(no phone required)" explicitly refuses the extractive pattern where the accessible route demands a device/app. Word-count bound (70–90 words ≈ 30s) is measurable; "No `!`. No medical terms." ties into the tone skill's deterministic style; "fallback URL" as a required output means the QR is never a single point of failure.

Breaks baseline competence:
1. `Load with` points at `principles/print-scale` — **file does not exist** (verified against the file tree).
2. The QR instruction places the code in the keep-out strip ("fully inside the 12.7mm safe margin"), contradicting print-scale-inspector.
3. "high contrast" for the QR is unmeasured — the one spec in the suite with no number.

**Evidence.**
- `SKILL.md:10`: "`principles/print-scale` numbers: safe margin = 12.7mm (0.5in) on A4 and US Letter."
- `SKILL.md:16`: "- QR: error correction Level M or Q, ≥15×15mm, high contrast, fully inside the 12.7mm safe margin."
- `SKILL.md:3` (frontmatter description) repeats the same "inside the 12.7mm safe margin" error.
- File tree check: `principles/` contains only `color-tokens.md`, `contrast.md`, `micro-chunking.md`, `soft-geometry.md`, `typography.md`, `tokens.screen.json`, `tokens.print-monochrome.json`.

**Impact.**
An agent following this skill literally renders a QR whose edges sit in the margin strip; consumer printers clip ~5mm at edges, so the code — the *access route* — is the thing destroyed. For a low-vision user, a clipped QR is not "slightly degraded," it's absent. The broken `Load with` reference makes any load-order-following agent stall or silently skip (fail-open), the opposite of the repo's own "fail closed" rule.

**Fix.** **P0-1** (create `principles/print-scale.md`), **P0-2** (QR wording, both in the frontmatter description and the Law bullet, plus quiet-zone spec).

---

### 2.4 `skills/aria-dom-architect/SKILL.md`

**Findings.**
Good: "Native first" with a concrete element list (`<button>`, `<a href>`, `<label for>`, `<details>`/`<summary>`, `<dialog>`) is exactly the right order of operations; the forbidden list is copy-checkable ("clickable `<div>` or `<span>`; `div` + `onclick` + `role=\"button\"` when a native control exists"); decorative vs. meaningful image handling ("descriptive `alt`" / `alt=\"\"` or `aria-hidden=\"true\"`") is correct and brief.

Agent-ready gaps: forms stop at `label for`. Nothing covers error identification/linking (a screen-reader user hears "Error!" with no field attached), status messaging (`role="status"`/`aria-live`), or pointer target size — this is the natural home for all three. No `Load with` line (acceptable if intentional — it's self-contained — but see consistency note P2-4).

**Evidence.**
- `SKILL.md:13`: "- Native first: `<button>`, `<a href>`, `<label for>`, `<details>`/`<summary>`, `<dialog>`."
- Absence check: no `aria-describedby`, no `role="status"`, no target size anywhere in the repo (grep across all files).

**Impact.**
A blind user submitting an invalid form gets the repo's *tone* fix ("That field needs an email address") but not its *semantics* — the message is not programmatically tied to the field, so their screen reader may never announce it. Motor-impaired users get keyboard excellence but no pointer-target floor; the README promises surfaces "a human has to… tap," so this is in-scope by the repo's own claim.

**Fix.** **P1-4** (paste three bullets: field errors, status regions, target size).

---

### 2.5 `skills/cognitive-load-linter/SKILL.md`

**Findings.**
Good: the table is a pure decision function — check, threshold, fail condition — and mirrors `principles/micro-chunking.md` exactly (verified: 4 lines / 45 words / 65 chars hard-75 / 40% empty). "On fail: split into a shorter paragraph or a list. Do not publish the long block." is a real acceptance criterion. This is the executive-function support the README promises, and it's the strongest "lived experience, not checklist" item in the suite because the thresholds encode real reading behavior.

Agent-ready gaps: (1) "Visual lines in one body block" cannot be evaluated from source without rendering — `principles/micro-chunking.md:16` even acknowledges the problem ("without guessing viewport width") but only solves it for characters. (2) "Empty space on a printable page < 40%" has no measurement method. (3) No `## Output` section, unlike sibling skills — output is a sentence inside the Law table's shadow.

**Evidence.**
- `SKILL.md:14`: "| Visual lines in one body block | > 4 |" — no definition of the rendering context.
- `SKILL.md:17`: "| Empty space on a printable page | < 40% |" — no method.
- `principles/micro-chunking.md:16`: "Deterministic so an agent can fail a block without guessing viewport width."

**Impact.**
An agent auditing unrendered markdown/HTML stalls on "visual lines" or invents its own rule (non-deterministic → results differ run to run). A maintainer can't reproduce a 40%-empty verdict between two reviewers. This is the exact "vibes" failure the tone skill explicitly rejects ("Test = this list… Not a mood judgment").

**Fix.** **P1-2** (define the two measurement methods), **P2-3** (add `## Output`).

---

### 2.6 `skills/dual-format-a11y/SKILL.md`

**Findings.**
Good: "Web ≠ print." as a section opener is the cleanest boundary statement in the repo; the may/may-not pair ("Web may use ARIA, `:focus-visible`, live regions. / Print may not.") is copy-paste friendly and correct; the two-artifact convention with exact filenames is a genuinely forkable expected-artifact spec; the `Load with` lines all point at existing files.

Agent-ready gap: it governs PDFs ("No ARIA… in PDFs") but never requires the thing PDFs actually need — **tagging** (reading order, document language, alt text carried into the PDF). An untagged PDF with perfect 12pt type and 12.7mm margins is still unreadable in the wrong order for a screen-reader user. Also, "prefer two files" — prefer is not a law; the skill that elsewhere says "not optional" should say when one file is acceptable.

**Evidence.**
- `SKILL.md:14–15`: "Web may use ARIA… / Print may not. Print is geometry, type size, ink, and margins."
- `SKILL.md:20–23`: "- If a printable is emitted, prefer two files:" (conditional "prefer").
- Absence check: no occurrence of "tagged", "reading order", or "language" in any print-related file.

**Impact.**
For a blind user, an untagged PDF is a wall — the skill's own numeric laws all pass while the document is unusable. For maintainers, "prefer" produces fork drift: some forks emit one file, some two, with no rule to appeal to.

**Fix.** **P1-5** (tagged-PDF bullet + tighten "prefer").

---

### 2.7 `skills/focus-flow-tester/SKILL.md`

**Findings.**
Good: this is the most complete agent-ready skill in the suite. Every rule is measurable (3px solid, 2px offset, ≥3:1 against adjacent background); the keyboard alphabet is enumerated ("Tab, Shift+Tab, Space, Enter, Escape only" — so "done" is testable); skip-link target focusability and the `outline: none` replacement rule are exactly the two things maintainers get wrong. "Color hex is an example; contrast of the ring is the law" correctly separates example from law — and the example actually passes (verified: `#4A5D4E` ring is 6.41:1 on canvas, 5.12:1 on surface, both ≥3:1).

Minor gaps: "Tab order = reading order" doesn't name the reference order (DOM order), so an agent comparing against visual layout will false-positive on correct CSS reordering — or worse, "fix" correct DOM order. "Output: Failing control and the missing key or trap" has no pass-output statement (an agent that finds nothing reports nothing — indistinguishable from not having run).

**Evidence.**
- `SKILL.md:15`: "- Tab order = reading order." — no reference definition.
- `SKILL.md:23`: "## Output" → "Failing control and the missing key or trap." — no pass case.
- Contrast verification (computed): `#4A5D4E` vs `#F7F3EE` = 6.41:1; vs `#E8D9C8` = 5.12:1. Pass.

**Impact.**
DOM-order ambiguity creates non-reproducible verdicts between agents — a maintainer gets contradictory reviews and loses trust in the suite. Missing pass-output means silence reads as success ("did it run?" is unknowable) — a small audit-theater door left open.

**Fix.** **P2-1** (define reading order as DOM order; add a pass line to Output).

---

### 2.8 `skills/multimodal-cue-agent/SKILL.md`

**Findings.**
Good: the core law is the repo's most distinctive constraint and it's fully operational — "Color change is never the only state cue" plus the three acceptable second cues (shape, pattern, visible text). Banning the instruction pattern ("click the green button") rather than just the design pattern is smart: it catches docs and support copy too, which colorblind users hit constantly. The HTML example is correct and minimal (`aria-hidden="true"`, `focusable="false"`, adjacent `<span>Saved</span>` — text cue present, so the example satisfies its own law).

Gaps: no `## Output` section (the only cue skill without one, an agent has no "done" contract); grayscale/CVD verification method is in `principles/soft-geometry.md` ("readable with color removed") but the skill never says *how* to check (e.g., desaturate and re-read).

**Evidence.**
- `SKILL.md:12–17`: Law bullets (all measurable).
- `SKILL.md:19–24`: the HTML example.
- Heading scan: file ends at the code fence — no Output section.

**Impact.**
Without an output contract, two agents produce different artifacts for the same input (one returns corrected markup, one returns a prose list). Without a check method, "verify with color removed" becomes a judgment call — the "mood judgment" the tone skill bans.

**Fix.** **P2-2** (add Output + a one-line desaturation check).

---

### 2.9 `skills/print-scale-inspector/SKILL.md`

**Findings.**
Good: every rule is a number with a unit (≥12pt, ≥18pt large print, 12.7mm, ≥1.4× line-height, vector/selectable text); "Name the failing edge, point size, or alignment. Give the numeric fix." is an exemplary output contract — it demands the fix be numeric, closing the vibes door. `Load with` points at existing files.

Breaks consistency: line-height 1.4 (prefer 1.5) contradicts `principles/typography.md`'s ≥1.5 law, and typography.md is loaded by this very skill. Also "Body `text-align: left` only" — correct for body, but a maintainer may read it as banning centered display headings; typography.md scopes alignment to body ("Body left-aligned"), so the skill should carry the same scope.

**Evidence.**
- `SKILL.md:16`: "- Line-height ≥ 1.4× (prefer 1.5)." vs `principles/typography.md:8`: "- Body line-height ≥ 1.5."
- `SKILL.md:15`: "- Body `text-align: left` only."

**Impact.**
Two thresholds for one check = non-deterministic gate. An agent loading both files (as instructed) must pick arbitrarily; audits differ run to run and the maintainer can't tell which rule fired. The alignment overreach can produce false failures on legitimate centered titles.

**Fix.** **P1-3** (align on 1.5 in file + frontmatter; scope the alignment rule to body).

---

### 2.10 `skills/tone-accessibility-auditor/SKILL.md`

**Findings.**
Good: "Test = this list and the `!` ban. Not a mood judgment." is the single most agent-ready sentence in the repo — it converts tone policing into a deterministic string check. The forbidden list targets real harm patterns: false urgency ("last chance, act fast") which is an anxiety/ADHD exploit, and medicalized labeling of the user ("symptom, disorder… as labels for the user"), which respects that the reader is a person, not a diagnosis. The replacement table keeps replacements low-demand ("Available when you are ready").

Gaps: one table row is context-locked — "Error! Invalid input → That field needs an email address" assumes an email field; an agent matching generically will emit wrong copy for a name field. The `!` ban scope is unstated for code (`!==`, `!important`) — a literal agent could flag source code.

**Evidence.**
- `SKILL.md:10`: "Test = this list and the `!` ban. Not a mood judgment."
- `SKILL.md:21`: "| Error! Invalid input | That field needs an email address |"
- `SKILL.md:8`: "Forbidden in instructions, product text, forms, errors, and CTAs:" (scope covers UI copy — but code adjacency is untested wording).

**Impact.**
Context-locked replacement produces confidently wrong copy (an agent telling a name field it "needs an email address" is worse than generic). Unscoped `!` ban wastes a review cycle on code, or teaches maintainers to ignore the skill's flags (alarm fatigue → the deterministic gate erodes).

**Fix.** **P2-5** (generic pattern row + code-scope line).

---

### 2.11 `principles/color-tokens.md`

**Findings.**
Good: "Agents: read the JSON first. This file only states the rules." is a clean separation of law from data; "Law (not optional)" framing is consistent with the suite; "Replace them with any equivalents that still pass the law above. Do not treat example names or example hexes as a required brand." is the anti-brand-capture stance done exactly right.

Breaks baseline: the stable-key table documents `color.accent` and `color.divider` without usage constraints, and the shipped example values fail or skirt the law (accent 2.52:1 on surface — §2.13); `principles/tokens.print-monochrome.json` ships a key (`color.line`) the table doesn't document, and omits `accent`/`emphasis`/`divider` with no screen-only/print-only marking. The table says "stable" but the two JSONs have different key sets — an agent validating against the table will fail valid print files.

**Evidence.**
- `principles/color-tokens.md:20–28`: the token-key table (includes `focus.*` marked "(screen only)" but nothing for print-only keys).
- `principles/tokens.print-monochrome.json`: `"line": { "value": "#2C2A28" }` — key absent from the table.
- Computed: accent `#7A8F7A` on surface `#E8D9C8` = **2.52:1**; on canvas `#F7F3EE` = **3.15:1**; divider `#DFCDBA` on canvas = **1.40:1**.

**Impact.**
Agents copy examples — a 2.52:1 accent button on a card is shipped believing it passed. The key-set mismatch makes "stable keys" unverifiable, so forks diverge on what a token file must contain.

**Fix.** **P0-4** (accent value + usage constraints), **P1-6** (key table: mark screen-only/print-only, document `color.line`, divider role), **P1-7** (divider statement or compliant hex `#8A775A` — computed 3.91:1 canvas / 3.12:1 surface).

---

### 2.12 `principles/contrast.md`

**Findings.**
Good: the physiological rule is the repo's signature and it's stated with its reason ("high ratio and still harmful: it produces visual vibration and text freezing for many dyslexic and fatigued readers") — lived experience encoded as law, exactly the stance to preserve. "CSS luminance is not ink" is a rare and correct print insight. Screen thresholds match WCAG 2.1 AA (4.5:1 / 3:1 — verified).

One factual slip: the example ratio "≈13.5:1" for `#2C2A28` on `#F7F3EE` is wrong — the computed value is **12.94:1**. Still far above 4.5:1, so the law holds; the number doesn't.

**Evidence.**
- `principles/contrast.md:7`: "Example only: `#2C2A28` on `#F7F3EE` (≈13.5:1)." — computed: 12.94:1.
- `principles/contrast.md:12–13`: "Normal text ≥ 4.5:1 / Large text and UI components ≥ 3:1" — matches WCAG 2.1 AA.

**Impact.**
Small, but this repo's entire value proposition is deterministic numbers; a wrong ratio in the flagship principle invites "check the others, then" — and an agent asked to verify 13.5:1 will report a failure of a passing pair.

**Fix.** **P2-6** (correct to 12.9:1).

---

### 2.13 `principles/tokens.screen.json` and `principles/tokens.print-monochrome.json`

**Findings.**
Good: the `note` field in both files explicitly marks values as examples and points back to the law files — configuration point documented at the point of configuration. Print set correctly uses ink-dark `#2C2A28` text (computed 14.30:1 on `#FFFFFF`, clearing its own ≥7:1 print target) with no pure black.

Breaks baseline (screen set): `accent #7A8F7A` fails the repo's own UI rule on `surface #E8D9C8` (2.52:1) and fails 4.5:1 as text on canvas (3.15:1). The print set's key structure diverges from the documented "stable" table (§2.11). The screen `note` also doesn't warn that accent is UI-only.

**Evidence (computed, WCAG relative-luminance math).**

| Pair | Ratio | Law | Verdict |
| --- | --- | --- | --- |
| text `#2C2A28` / canvas `#F7F3EE` | 12.94:1 | ≥4.5:1 | pass |
| text `#2C2A28` / surface `#E8D9C8` | 10.34:1 | ≥4.5:1 | pass |
| emphasis `#4A5D4E` / canvas | 6.41:1 | ≥4.5:1 (headings) | pass |
| **accent `#7A8F7A` / canvas** | **3.15:1** | ≥3:1 UI, 4.5:1 text | UI pass, text **fail** |
| **accent `#7A8F7A` / surface `#E8D9C8`** | **2.52:1** | ≥3:1 UI | **fail** |
| focus `#4A5D4E` / canvas | 6.41:1 | ≥3:1 | pass |
| focus `#4A5D4E` / surface | 5.12:1 | ≥3:1 | pass |
| divider `#DFCDBA` / canvas | 1.40:1 | 3:1 if meaningful | see P1-7 |
| print text `#2C2A28` / `#FFFFFF` | 14.30:1 | ≥7:1 | pass |
| print line `#2C2A28` / `#F0F0F0` | 12.54:1 | ≥3:1 | pass |

Proposed replacement accent `#5F7360` (same low-saturation green family): **4.63:1** on canvas, **3.70:1** on surface — passes both UI floors everywhere and even clears 4.5:1 on canvas if a fork uses it as text.

**Impact.**
The token files are step 1 of the README's agent load order — they are the most-copied files in the repo. A worked example that violates its own law isn't a neutral typo; it teaches agents that the law is aspirational. Low-vision users get the 2.52:1 button on the card.

**Fix.** **P0-4** (accent value + note).

---

### 2.14 `principles/typography.md`

**Findings.**
Good: the serif carve-out is scoped and defended ("There is no contradiction: serif is a display-only exception, never a body face") — anticipating the misreading is kind to neurodivergent maintainers who need rules, not exceptions-to-infer. Hard caps (45–65 chars, max 75; ≤4 lines; ≤45 words) match micro-chunking exactly (verified). "Screen layouts remain usable at 200% zoom" covers low-vision reflow at the AA level. The suggested-faces section stays anti-brand twice.

Gaps: 200% is the floor; WCAG reflow is satisfiable at 400%/320px, and the repo's low-vision stance would be better served by saying both. Text-spacing tolerance (user-applied spacing overrides) is unmentioned. And the print line-height law (≥1.5) is undercut by print-scale-inspector's 1.4 (§2.9).

**Evidence.**
- `principles/typography.md:10`: "Measure 45–65 characters per line. Hard max 75." = `principles/micro-chunking.md` row 3 (consistent).
- `principles/typography.md:13`: "- Screen layouts remain usable at 200% zoom with no horizontal scroll."

**Impact.**
Minor: a fork following only this file passes 2.1 AA but misses the repo's own "any surface a human has to read" promise at extreme zoom (users with low vision commonly sit at 300–400%).

**Fix.** **P2-8** (reflow wording + spacing tolerance).

---

### 2.15 `principles/soft-geometry.md`

**Findings.**
Good: "State, category, and progress must remain readable with color removed (grayscale, print, CVD)" — the parenthetical names the actual human situations, which is the lived-experience register the whole repo aims for. Stroke floors are numeric (≥1.5pt, sub-1pt forbidden). "Do not require a private icon set, named product diagrams, or a brand motif library" keeps the constraint forkable for someone with no design budget.

Gap: no verification instruction (how to check "readable with color removed") — the method lives nowhere; multimodal-cue-agent inherits the same gap (§2.8).

**Evidence.** `principles/soft-geometry.md:5`: "readable with color removed (grayscale, print, CVD)" — no check step anywhere in the repo.

**Impact.** Agents improvise: some simulate grayscale, some skip. Non-reproducible verdicts.

**Fix.** **P2-2** (one-line method, shared by principle + skill).

---

### 2.16 `principles/micro-chunking.md`

**Findings.**
Good: the whole file is one table and one action rule ("If any threshold is exceeded, split… before publish") — the most agent-ready principle in the set; "Executive-function support. Deterministic so an agent can fail a block without guessing viewport width" states intent, which is rare and valuable.

Gap: the determinism claim only holds for words/characters. "Max visual lines per body block | 4" and "Min empty space… 40%" still require rendering or a method (see §2.5 — the same gap propagates from principle to skill, so fixing the principle fixes both).

**Evidence.** `principles/micro-chunking.md:6–11` (table); line 16 (determinism claim).

**Impact.** Same as §2.5: stalls or improvised rules.

**Fix.** **P1-2** (measurement definitions, stated once here and referenced by the skill).

---

### 2.17 `.pa11yci.json`

**Findings.**
Good: `standard: WCAG2AA` matches the repo's claimed level; dual runners (`axe`, `htmlcs`) is the right belt-and-braces; `--no-sandbox` args are the correct container/CI setup; `timeout: 30000` is sane; keeping it in-repo with no npm dependency honors "no hidden dependency."

Gaps: `"urls": []` makes the documented command error out (see P0-5); JSON cannot carry comments, so the config's one non-obvious field (where URLs go) has no inline explanation — the README must carry it; `standard` is honored by the htmlcs runner only (axe brings its own rule set) — worth one README line so a maintainer doesn't expect identical counts between runners.

**Evidence.** `.pa11yci.json:8`: `"urls": []`.

**Impact.** First-run failure with a config error is the moment most casual forkers quit.

**Fix.** Covered by **P0-5** (README steps) — no change to this file itself beyond the URLs a fork adds.

---

### 2.18 `LICENSE`

**Findings.**
Good: a clean dual license — full MIT text for software plus a documentation/design-assets grant under CC BY 4.0. This aligns with forkable, non-extractive intent: attribution-only, no further-restrictions trap, commercial reuse allowed both ways. Copyright line (`2026 Gabriel Paiva`) is present and matches the repo owner.

Gaps: (1) the CC BY 4.0 grant is named but not linked — the deed/URL should appear so a forker can find the terms without a search; (2) the split is only exemplified in the README as "Software: MIT. Documentation and design principles: CC BY 4.0." — the JSON token files, `.pa11yci.json`, and `SKILL.md` files sit in an unstated bucket. A forker remixing tokens into a product needs to know which grant applies.

**Evidence.**
- `LICENSE:1–20`: full MIT text (verified standard wording).
- `LICENSE:23–25`: "All documentation, guidelines, geometry specifications, and design principles in this repository are licensed under the Creative Commons Attribution 4.0 International License (CC BY 4.0)." — grep confirms **no creativecommons.org URL anywhere in the file**.

**Impact.**
Ambiguity at fork time is a tax on the exact reuse the repo invites; the missing deed link is a small but real friction for a first-time contributor complying in good faith.

**Fix.** **P1-8** (URL + scope table; scope split needs maintainer confirmation — see §7, Q3).

---

## 3. Neurodivergence / low-vision / motor-impairment review

### 3.1 Cognitive load

- **Reading order:** the README's numbered "Agent load order" (tokens → principles → skills → fail closed) is the right shape; each skill's `Load with` respects it — except `alt-audio-synthesizer`, which loads a nonexistent file (P0-1), breaking the chain at step 2.
- **Heading hierarchy:** `README.md` skips `##` (P1-1). Every other file is sequential (verified by heading scan of all 19 files — principles use `#`→`##` correctly, skills use `#`→`##` correctly).
- **Chunk size:** the docs practice their own micro-chunking law — files are short, rules are tables, no paragraph approaches 45 words (spot-checked the longest paragraphs; all pass). This self-consistency is worth saying out loud because it's rare.
- **Terminology consistency:** three drift pairs: "safe margin" vs "safe area" (opposite directions — §4.3.1); "Law (not optional)" (principles) vs "Law (once)" (skills, undefined); "Exit 1 = fail" vs pa11y's actual 2-for-errors.

### 3.2 Operational clarity

The suite is strongest where rules are numeric (focus ring, type sizes, margins, chunk caps — all pass the "do this → then this with a measurable acceptance criterion" test). The stall points below are every place an agent or a human cannot finish the instruction as written.

### 3.3 Failure modes — stall points and exact replacements

1. **"fully inside the 12.7mm safe margin"** (`skills/alt-audio-synthesizer/SKILL.md:3,16`) — self-contradictory (P0-2 replacement text).
2. **"`principles/print-scale` numbers"** (`skills/alt-audio-synthesizer/SKILL.md:10`) — target missing (P0-1 creates it).
3. **"Exit `1` = fail"** (`README.md:49`, `skills/a11y-ci-gatekeeper/SKILL.md:27`) — wrong contract (P0-3).
4. **"high contrast"** (QR, `skills/alt-audio-synthesizer/SKILL.md:16`) — unmeasured. Replace with: "dark modules on a light background (never inverted), quiet zone of at least 4 modules clear on every side."
5. **"Visual lines in one body block > 4"** (`skills/cognitive-load-linter/SKILL.md:14`) — unrenderable from source. Replace with the P1-2 proxy rule.
6. **"Empty space on a printable page < 40%"** (`skills/cognitive-load-linter/SKILL.md:17`) — no method. Replace with the P1-2 grid rule.
7. **"Line-height ≥ 1.4× (prefer 1.5)"** vs "**≥ 1.5**" (`print-scale-inspector` vs `typography.md`) — two laws, one check (P1-3).
8. **"Tab order = reading order"** (`skills/focus-flow-tester/SKILL.md:15`) — undefined reference. Replace with: "Tab order follows DOM order, and DOM order matches the visual reading order of the page."
9. **"prefer two files"** (`skills/dual-format-a11y/SKILL.md:20`) — optional verb in a law suite. Replace with: "Emit two files. A single file is acceptable only when the printable will never be read on paper."
10. **"Fail closed on critical violations"** (`README.md:41`) — critical list not linked. Replace with a pointer to `skills/a11y-ci-gatekeeper/SKILL.md`.
11. **"Law (once)"** (all skills) — undefined idiom. Either define it in the README glossary (P1-1 includes this) or rename to "## Law".

---

## 4. Accessibility baseline check

### 4.1 Claimed topic → operationalization

| Claimed topic | Where operationalized | Verdict |
| --- | --- | --- |
| Color / contrast | `contrast.md` + `color-tokens.md` + both token JSONs | **Operational, but example accent fails its own law** (P0-4); one wrong ratio constant (P2-6) |
| Physiological contrast (no #000/#FFF) | `contrast.md`, `dual-format-a11y`, both JSONs | Operational and consistently applied (print text 14.30:1, no pure black) |
| Typography | `typography.md` + `print-scale-inspector` | Operational; one numeric drift (P1-3) |
| Focus | `focus-flow-tester` + `focus.*` tokens | Fully operational; example ring passes (6.41:1 / 5.12:1) |
| Keyboard / traps | `focus-flow-tester` + `a11y-ci-gatekeeper` | Fully operational, enumerated key alphabet |
| Forms | `aria-dom-architect` (`label for`) + tone replacements | **Partial — error linking, status regions, target size missing** (P1-4) |
| Alt text (web) | `aria-dom-architect` (decorative vs meaningful) | Operational |
| Audio descriptions / alt-audio | `alt-audio-synthesizer` | Operational and original; QR placement bug (P0-2), missing quiet zone (P1/P2) |
| Micro-chunking | `micro-chunking.md` + `cognitive-load-linter` | Operational; two unmeasurable checks need methods (P1-2) |
| Multi-channel state | `soft-geometry.md` + `multimodal-cue-agent` | Operational; no verification method (P2-2) |
| Tone / low-demand copy | `tone-accessibility-auditor` | Operational, deterministic; one context-locked row (P2-5) |
| Tagged PDF / reading order in PDFs | nowhere | **Gap** (P1-5) |
| Pointer/touch target size | nowhere | **Gap** vs the repo's own "read, tap, or print" claim (P1-4) |

### 4.2 Screen vs print boundary

- **Boundary statement:** present and good — `README.md` "Dual-medium boundary" (web: ARIA/focus/WCAG; print: geometry/type/ink/margins, "No ARIA, no focus logic, no live regions in PDFs") and restated as law in `dual-format-a11y`. No genuine contradiction in the boundary itself.
- **Duplication:** the 12.7mm constant appears in 4 files (`README.md:21`, `alt-audio-synthesizer:10,16`, `dual-format-a11y:17`, `print-scale-inspector:17`) with no declared single source of truth — drift risk, and one of the four already states it backwards (P0-2). The 12pt/18pt pair appears in 3 files. P0-1's new `principles/print-scale.md` declares itself the authority, which resolves the duplication policy without deleting the inlined numbers agents need.
- **Missing boundary statement:** PDF tagging — the web/print split says what print may not use (ARIA/focus/live regions) but never says what print must use instead (tagged reading order, document language). P1-5.

---

## 5. License review (see also §2.18)

- **Existence:** confirmed; full MIT text present, plus an explicit documentation grant.
- **Intent alignment:** strong. MIT + CC BY 4.0 is the permissive, attribution-only combination: anyone may fork, adapt, commercialize, and re-license derivatives of the software side; documentation reuse requires attribution only, with no anti-competitive or further-restrictions terms. This matches the repo's non-extractive stance — the same terms for a solo disabled maker and a corporate design system, no invoice implied or required.
- **Two frictions:** no CC BY 4.0 deed URL; the software/docs split doesn't say where JSON tokens, `.pa11yci.json`, or `SKILL.md` files fall (P1-8; needs one maintainer decision — §7 Q3).

---

## 6. Prioritized fixes

### P0 — blocks usability, causes baseline failures, or breaks forkability

All P0 items include exact paste text, split by file.

---

#### **P0-1. Create the missing `principles/print-scale.md` (single source of truth for print numbers)**
Fixes: broken reference at `skills/alt-audio-synthesizer/SKILL.md:10`; 4-way duplication of print constants; also settles the line-height law (see P1-3).

**Target file (new): `principles/print-scale.md`** — paste in full:

```markdown
# Print scale and margins

## Law (not optional)

- Safe area: no text, art, QR, or fold-critical element inside 12.7mm (0.5in) of any trimmed edge on A4 and US Letter. The 12.7mm strip itself is the safe margin and it stays empty.
- Body type ≥ 12pt. Large print ≥ 18pt.
- Body line-height ≥ 1.5.
- Body text is vector and selectable, never a raster of type.
- Strokes ≥ 1.5pt (2px at 96dpi). Strokes under 1pt are forbidden on printables.
- Body ink is dark off-black (example `#2C2A28`), target ≥ 7:1 on cheap inkjet output. Never `#000000` body text on `#FFFFFF`.
- No ARIA, no focus logic, no live regions in PDFs. Print state is carried by geometry and text, per `principles/soft-geometry.md`.

This file is the single source of truth for print numbers. Skills may repeat a number so they can run standalone; if any file disagrees with this one, this file wins.
```

**Target file: `skills/alt-audio-synthesizer/SKILL.md`** — replace line 10:

```markdown
`principles/print-scale.md`: safe area = keep the 12.7mm (0.5in) margin strip at every edge empty on A4 and US Letter.
```

---

#### **P0-2. Fix the QR placement instruction (it currently places the QR in the clipping zone) + add quiet zone**

**Target file: `skills/alt-audio-synthesizer/SKILL.md`** — replace the frontmatter `description` (line 3):

```yaml
description: For each printable, write a ~30s layout narration (70–90 words), a full-text transcript, and QR specs: ECC M or Q, ≥15×15mm, quiet zone ≥4 modules, every edge of the code at least 12.7mm (0.5in) from the trimmed page edge.
```

**Same file** — replace the QR law bullet (line 16):

```markdown
- QR: error correction Level M or Q, ≥15×15mm, dark modules on a light background (never inverted), quiet zone of at least 4 modules clear on every side, fully inside the safe area (every edge of the code at least 12.7mm / 0.5in from the trimmed page edge), and not crossing a fold.
```

---

#### **P0-3. Correct the exit-code contract (documented "exit 1 = fail" lets real failures pass)**

Verified against pa11y's documentation: `0` = no errors, `1` = technical fault, `2` = accessibility errors found; pa11y-ci exits non-zero on any failure.

**Target file: `README.md`** — replace line 49:

```markdown
Exit `0` = pass. Any non-zero exit = fail. pa11y uses exit `2` for accessibility errors and `1` for a technical fault, so test for non-zero, not for `1`.
```

**Target file: `skills/a11y-ci-gatekeeper/SKILL.md`** — replace line 27:

```markdown
Exit `0` = pass. Any non-zero exit = fail. pa11y uses exit `2` for accessibility errors and `1` for a technical fault, so test for non-zero, not for `1`. No npm app ships in this repo.
```

**Same file** — replace the `description` in the frontmatter (line 3):

```yaml
description: Block a release if WCAG 2.1 AA contrast, alt-text, focus, or keyboard checks fail. Optional command: npx pa11y-ci --config .pa11yci.json. Exit 0 pass, any non-zero fail (2 = accessibility errors, 1 = technical fault).
```

---

#### **P0-4. Fix the example accent that fails the repo's own law**

Computed: `#7A8F7A` = 2.52:1 on surface `#E8D9C8` (fails ≥3:1 UI), 3.15:1 on canvas (fails 4.5:1 as text). Replacement `#5F7360` = 4.63:1 canvas / 3.70:1 surface.

**Target file: `principles/tokens.screen.json`** — replace the accent line and the note:

```json
  "note": "Example hexes. Swap any values that still meet principles/color-tokens.md and principles/contrast.md. accent is for UI and graphics only, never normal text; it must pass 3:1 on canvas and surface.",
```

```json
      "accent": { "value": "#5F7360" },
```

**Target file: `principles/color-tokens.md`** — append to "## Law (not optional)":

```markdown
- `color.accent` is for UI components and graphics only. It must pass ≥3:1 against `color.canvas` and `color.surface`. Never use it for normal text; use `color.text` or `color.emphasis`.
```

---

#### **P0-5. Make the README's only runnable command work as written**

**Target file: `README.md`** — replace the "Optional local HTML scan" block (lines 43–49):

```markdown
Optional local HTML scan. Prerequisites: Node.js 18 or newer, a local Chrome or Chromium, network access to npm.

1. Add your URLs to `.pa11yci.json`:

   ```json
   "urls": ["http://localhost:8080/", "http://localhost:8080/pricing/"]
   ```

2. Serve your site, then run:

   ```bash
   npx pa11y-ci --config .pa11yci.json
   ```

Exit `0` = pass. Any non-zero exit = fail (pa11y uses `2` for accessibility errors and `1` for a technical fault). Optional tool, not a hidden dependency.
```

---

### P1 — materially improves clarity/coverage, moderate effort

| # | Fix | File(s) |
| --- | --- | --- |
| P1-1 | Full README replacement: sequential `##` headings, prerequisites, inputs/outputs table per skill, glossary ("Law (once)", "fail closed", "safe area"), troubleshooting, corrected exit codes and scan steps. Text below. | `README.md` |
| P1-2 | Define the two unmeasurable checks. Paste into `principles/micro-chunking.md` (the skill inherits it): "**Visual lines:** if you cannot render, treat a block as 4 lines when it is ≤45 words and ≤65 characters per line; anything longer fails. **Empty space:** overlay a 5×5 grid (25 cells) on the page; at least 10 cells (40%) must contain no text, rule, or graphic." | `principles/micro-chunking.md`, `skills/cognitive-load-linter/SKILL.md` |
| P1-3 | One line-height law. Change `print-scale-inspector` line 16 to "- Line-height ≥ 1.5." and the frontmatter description's "line-height ≥1.4" to "line-height ≥1.5"; scope alignment: "- Body `text-align: left` only (display headings may be centered)." | `skills/print-scale-inspector/SKILL.md` |
| P1-4 | Close the forms/motor gaps. Paste into `aria-dom-architect` Law: "- Every field has a persistent visible `<label for>`. Placeholder is never the label.\n- On error: name the field in text, say how to fix it, link the message with `aria-describedby=\"<id>-error\"`, and move focus to the first invalid field.\n- Save/result changes use `role=\"status\"` or `aria-live=\"polite\"`; blocking errors use `role=\"alert\"`.\n- Pointer targets ≥24×24 CSS px (44×44 preferred) with ≥8px between adjacent targets." | `skills/aria-dom-architect/SKILL.md` |
| P1-5 | Require tagged PDFs. Paste into `dual-format-a11y` Law: "- PDF exports must be tagged: reading order set, document language set, image alt text carried into the PDF. An untagged export fails even when type and margins pass." Change "If a printable is emitted, prefer two files:" → "When a printable is emitted, produce two files:". | `skills/dual-format-a11y/SKILL.md` |
| P1-6 | Make the "stable keys" table match reality: mark `focus.*` screen-only, add `color.line` (print-only: rules/strokes), note print omits `accent`/`emphasis`/`divider`. | `principles/color-tokens.md` |
| P1-7 | Divider role statement: "- `color.divider` is decorative; separators are exempt from 3:1. If a line is a meaningful boundary of a control or group, use `color.emphasis` or a divider ≥3:1 (example `#8A775A`: 3.91:1 canvas, 3.12:1 surface)." | `principles/color-tokens.md` |
| P1-8 | LICENSE: add the CC BY 4.0 deed URL and a scope table (needs maintainer decision — Q3). | `LICENSE`, `README.md` |

**P1-1 full README replacement text** (preserves the original voice; fixes headings, forkability, exit codes, glossary, troubleshooting):

```markdown
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

## What is in the box

- Nine agent skills: `skills/<name>/SKILL.md`
- Five principle files: `principles/*.md`
- Two machine-readable token sets: `principles/tokens.screen.json` (web), `principles/tokens.print-monochrome.json` (print)
- One optional scan config: `.pa11yci.json`

Copy one file or the whole suite. No installer required.

## Dual-medium boundary

- **Web:** semantic HTML, `:focus-visible`, WCAG 2.1 AA, ARIA only when a native element cannot express the state.
- **Print:** vector text, ≥12pt body, 12.7mm (0.5in) safe margin kept empty at every edge, high-contrast ink-saving layers. No ARIA, no focus logic, no live regions in PDFs.

Print numbers live in one place: `principles/print-scale.md`. If any other file disagrees, that file wins.

## How to use it (copy path, no tools required)

1. Open the skill you need.
2. Copy `SKILL.md`.
3. Paste it into your agent or skills folder.

### Agent load order

1. `principles/tokens.screen.json` (web) or `principles/tokens.print-monochrome.json` (print)
2. Matching files under `principles/`
3. The `SKILL.md` files you need
4. Fail closed on critical violations — the list lives in `skills/a11y-ci-gatekeeper/SKILL.md`

### Inputs and outputs per skill

| Skill | Input | Output |
| --- | --- | --- |
| a11y-ci-gatekeeper | URL or HTML build | Pass/fail plus a violation list |
| alt-audio-synthesizer | Printable layout | ~30s script, transcript, QR spec |
| aria-dom-architect | HTML or DOM | Corrected markup plus a change list |
| cognitive-load-linter | Copy or a printable | Failing blocks plus their splits |
| dual-format-a11y | One design, two media | Screen file plus print file |
| focus-flow-tester | One keyboard pass | Failing control plus the missing key |
| multimodal-cue-agent | States and icons | A second cue for every state |
| print-scale-inspector | A printable | Failing edge, size, or alignment |
| tone-accessibility-auditor | User-facing copy | Corrected copy plus removed strings |

## Optional local HTML scan

Prerequisites: Node.js 18 or newer, a local Chrome or Chromium, network access to npm.

1. Add your URLs to `.pa11yci.json`:

   ```json
   "urls": ["http://localhost:8080/", "http://localhost:8080/pricing/"]
   ```

2. Serve your site, then run:

   ```bash
   npx pa11y-ci --config .pa11yci.json
   ```

Exit `0` = pass. Any non-zero exit = fail (pa11y uses `2` for accessibility errors and `1` for a technical fault). Test for non-zero, not for `1`. Optional tool, not a hidden dependency.

## Glossary

- **Law (once):** the non-negotiable rules of a skill. Read once, apply to every item in the run.
- **Fail closed:** if a check cannot run or a value is missing, the result is fail, never pass.
- **Safe area / safe margin:** the 12.7mm (0.5in) strip at every trimmed edge that must stay empty. Content sits inside the safe area, never in the margin.
- **Worked example:** token hexes and font names that pass the law but are not a brand. Replace them with any values that still pass.

## Troubleshooting

- `npx pa11y-ci` reports no URLs: add them to `.pa11yci.json` under `"urls"`.
- Chrome fails to launch inside a container: keep the `--no-sandbox` args already present in `.pa11yci.json`.
- You copied a skill without `principles/`: each skill restates the numbers it needs, so it still runs; drop the `Load with` line.

## License

Software: MIT. Documentation and design principles: CC BY 4.0. See `LICENSE` for the split.
```

---

### P2 — polish, consistency, optional enhancements

| # | Fix | File(s) |
| --- | --- | --- |
| P2-1 | Define reading order and add a pass output: "- Tab order follows DOM order, and DOM order matches the visual reading order." Output: "On pass: list the controls checked and confirm each rule. On fail: the failing control and the missing key or trap." | `skills/focus-flow-tester/SKILL.md` |
| P2-2 | Add a verification method + Output section: "Check: desaturate the artifact (or print grayscale) and re-read every state; each must still be identifiable." Output: "Each state, its hue, and its second cue." | `skills/multimodal-cue-agent/SKILL.md`, `principles/soft-geometry.md` |
| P2-3 | Add `## Output`: "Failing block, the threshold it broke, and the split that replaces it." | `skills/cognitive-load-linter/SKILL.md` |
| P2-4 | Add a `Load with: none; self-contained` line to the two skills without one, for shape consistency | `skills/aria-dom-architect/SKILL.md`, `skills/tone-accessibility-auditor/SKILL.md` |
| P2-5 | Tone table: replace the context-locked row with "\| Error! Invalid input \| That field needs a valid email address (or: name, date…) \|" and add "The `!` ban applies to rendered UI copy, not source code (`!==`, `!important` are fine)." | `skills/tone-accessibility-auditor/SKILL.md` |
| P2-6 | Correct the ratio constant: `(≈13.5:1)` → `(12.9:1)` | `principles/contrast.md:7` |
| P2-7 | Gatekeeper output format: "One line per violation: `[rule] selector or URL — fix.` Then a final line: `PASS` or `FAIL (n)`." | `skills/a11y-ci-gatekeeper/SKILL.md` |
| P2-8 | Zoom wording: "usable at 200% zoom (and reflowed at 320px width) with no horizontal scroll" + text-spacing tolerance: "Layout survives user-applied spacing: line-height 1.5×, paragraph spacing 2×, letter 0.12×, word 0.16×." | `principles/typography.md` |
| P2-9 | alt-audio cross-load: add `skills/tone-accessibility-auditor/SKILL.md` to `Load with` (script must obey the tone bans) | `skills/alt-audio-synthesizer/SKILL.md` |
| P2-10 | One README line: "`standard` applies to the htmlcs runner; axe brings its own rules, so counts can differ between runners." | `README.md` |

---

## 7. Minimum viable polish checklist

Ship-blocking (do these five, in order):

1. ☐ Create `principles/print-scale.md` (P0-1 paste).
2. ☐ Fix QR wording + quiet zone in `alt-audio-synthesizer`, description and Law (P0-2 paste).
3. ☐ Fix exit-code text in `README.md` and `a11y-ci-gatekeeper` (P0-3 paste).
4. ☐ Change accent to `#5F7360` + add the accent usage law (P0-4 paste).
5. ☐ Add scan prerequisites + URL step to the README (P0-5 paste).

Same-afternoon (highest value per minute):

6. ☐ Swap in the P1-1 README (fixes the heading skip, glossary, troubleshooting in one paste).
7. ☐ Align line-height to 1.5 in `print-scale-inspector` (P1-3).
8. ☐ Paste the four forms/motor bullets into `aria-dom-architect` (P1-4).
9. ☐ Paste the tagged-PDF bullet into `dual-format-a11y` (P1-5).
10. ☐ Paste the two measurement definitions into `micro-chunking.md` (P1-2).

When convenient: the P2 table, license scope table (P1-8), and the corrected 13.5:1 → 12.9:1.

---

## 8. Missing content needed

One item — and it blocks the second half of your request:

- **The Gemini Spark audit attachment did not arrive.** No file was attached to your message and nothing beyond this repository exists in my workspace. I have not fabricated an opinion of a document I haven't seen. **Please attach the audit file (any format: md, txt, pdf, docx)** and I will analyze it in full — agreements, disagreements, anything it caught that I missed, anything it got wrong, and how its recommendations would interact with the P0/P1 fixes above.

No repository content is missing: all 19 files were read in full.

## 9. Clarifying questions (only where a fix depends on your intent)

1. **The Gemini Spark audit** — please attach it (see §8).
2. **"Law (once)"** — I inferred "read once, apply to every item" and wrote that into the glossary. If you meant something else (e.g., "evaluate once per run, not per element"), say the word and I'll adjust the glossary line.
3. **License scope** — where do `principles/*.json` and `.pa11yci.json` fall: MIT (software/config) or CC BY 4.0 (docs)? My proposed default: JSON = MIT, all prose = CC BY 4.0.
4. **Divider semantics** — is `color.divider` decorative-only (my assumption, P1-7 wording) or does it ever bound a meaningful control? If meaningful, ship `#8A775A` instead of keeping `#DFCDBA`.
