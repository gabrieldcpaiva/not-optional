## 2026-10-08 - Accessible Disabled & Loading States
**Learning:** Adding a loading state to a submit button using `aria-disabled="true"` prevents double submissions while keeping the button discoverable and providing immediate visual feedback. Using the native `disabled` attribute would remove the element from the tab order.
**Action:** For async interactions, prevent default submission, apply `aria-disabled="true"`, update the visual cue (e.g., loading spinner and text), and use JavaScript to block subsequent activations until the async task is complete.
