## 2026-10-08 - Accessible Disabled & Loading States
**Learning:** Adding a loading state to a submit button using `aria-disabled="true"` prevents double submissions while keeping the button discoverable and providing immediate visual feedback. Using the native `disabled` attribute would remove the element from the tab order.
**Action:** For async interactions, prevent default submission, apply `aria-disabled="true"`, update the visual cue (e.g., loading spinner and text), and use JavaScript to block subsequent activations until the async task is complete.
## 2026-10-09 - Accessible Keyboard Shortcuts
**Learning:** `title` attributes on buttons are often undiscoverable for touch users and keyboard-only users, and relying on them to expose power-user shortcuts is poor UX.
**Action:** When a keyboard shortcut exists, expose it visually near the trigger element using styled `<kbd>` tags and semantically using `aria-keyshortcuts` on the interactive element itself.
## 2026-10-10 - Custom Inline Validation vs Native Popups
**Learning:** Native browser validation popups contradict the app's `tone-auditor` requirements because their copy cannot be customized to the required low-demand tone.
**Action:** Override native `invalid` events (using `e.preventDefault()`) and render inline validation messages using existing `aria-describedby` elements to enforce the required tone and improve screen-reader accessibility.
