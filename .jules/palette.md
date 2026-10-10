## 2025-02-14 - Accessible Disabled State on Submit Buttons
**Learning:** Using the native `disabled` attribute on buttons removes them from the tab order, which hides the element and its state from screen readers that navigate by keyboard focus.
**Action:** Use `aria-disabled="true"` combined with JavaScript to prevent double submissions and CSS for visual styling (e.g., `cursor: not-allowed; opacity: 0.6;`). This preserves keyboard discoverability while clearly communicating the disabled/loading state.
