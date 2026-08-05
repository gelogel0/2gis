# Palette's Journal — LeadHunter MVP

This journal tracks critical UX and accessibility learnings and patterns discovered during the implementation of frontend improvements in the LeadHunter MVP.

## 2025-01-15 - Clipboard API in Headless Environments
**Learning:** When using Playwright or other headless testing frameworks to verify "Copy to Clipboard" interactions, the `navigator.clipboard.writeText` API often fails or requires explicit browser context permissions (`clipboard-read` and `clipboard-write`). Testing this functionality also requires a Secure Context (e.g. running over an HTTP server rather than `file://` URLs).
**Action:** Use a local HTTP server (such as Python's `http.server`) to host the target HTML page on a random port, and configure the Playwright browser context to explicitly grant clipboard permissions.

## 2025-01-15 - Accessible Feedback Transitions
**Learning:** Changing the content or status of elements asynchronously (such as a copy confirmation or sent confirmation) requires robust user feedback. However, replacing text content without careful guard against race conditions can cause visual jitter. Additionally, screen readers need to receive immediate updates without losing focus, which is achieved by utilizing clear ARIA attributes and temporary feedback timeouts.
**Action:** Guard interactions using state flags (`element.dataset.isCopying`) to prevent rapid-click concurrency issues, use appropriate focus states, and cleanly revert the original label, class, and ARIA attributes after a short delay (e.g. 2000ms).
