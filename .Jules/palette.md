# Palette's Journal - Critical Learnings Only

## 2025-01-16 - Prevent Copying Race Conditions in Global Event Delegation
**Learning:** When using global click event delegation for copy-to-clipboard interactions on tables (especially on rapid click inputs), multiple simultaneous clicks can lead to overlapping timers, visual feedback glints, and unexpected clipboard content state. Guiding execution with a dataset state flag (e.g. `element.dataset.isCopying`) protects the feedback loop.
**Action:** Use a state flag on the button to guard asynchronous execution, preventing race conditions during active feedback timeouts.
