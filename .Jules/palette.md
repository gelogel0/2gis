## 2025-05-14 - Robust Async Interaction Feedback
**Learning:** For asynchronous micro-interactions like 'Copy to Clipboard', providing visual success feedback (✅) is common, but neglecting the error state (❌) or failing to restore the original UI state (icon and ARIA label) in the catch block creates a 'stuck' interface that degrades accessibility and trust.
**Action:** Always capture original UI state (textContent, aria-label) before starting an async operation and use a `finally` block or symmetrical `then/catch` blocks with `setTimeout` to ensure the interface returns to a functional baseline regardless of the outcome.

## 2025-05-14 - Clipboard API Verification in Headless Environments
**Learning:** Testing the Clipboard API (`navigator.clipboard`) with Playwright requires two non-obvious steps: the page must be served over HTTPS (or localhost) to establish a Secure Context, and 'clipboard-read/write' permissions must be explicitly granted to the browser context.
**Action:** When verifying clipboard features, use a temporary local HTTP server and `browser.new_context(permissions=['clipboard-read', 'clipboard-write'])` in the Playwright script.
