## 2025-05-18 - Robust DOM query fallbacks for event-delegated action buttons
**Learning:** When using global event delegation where row templates or class names may vary between server-side HTML and client dynamic state, using query selector fallbacks (e.g., `row.querySelector(".js-mark-btn") || row.querySelector(".mark-btn")`) prevents silent feedback loop failures when triggering status updates.
**Action:** Always provide fallbacks for class-based DOM queries in event delegation handlers when element classes might differ across template versions.
