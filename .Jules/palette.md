# Palette's UX & Accessibility Journal

## 2025-02-14 - Click-to-Send and Clipboard Experience
**Learning:** For a lead outreach web app, copy-to-clipboard functionality next to the offer template significantly reduces manual workflow friction. To make this accessible and reliable, we must handle transient states (success and error) cleanly, provide visual and ARIA feedback using temporary timeouts, prevent double-click race conditions via state flags (`dataset.isCopying`), and ensure that marking items as processed natively disables actions for screen readers without breaking general usability features like text selection.
**Action:** Implement a state-guarded clipboard action, use clear aria-labels on copy buttons, and design resilient interactive states that gracefully restore original text or indicators if things fail.
