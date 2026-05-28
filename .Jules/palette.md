## 2025-05-22 - Grayscale feedback for processed items
**Learning:** In a dark-themed, data-heavy table, using both `opacity: 0.4` and `filter: grayscale(1)` with a smooth CSS transition provides a much clearer "completed" state than opacity alone, especially when rows have colored backgrounds (like the A/B/C templates).
**Action:** Apply `filter: grayscale(1)` alongside opacity changes for terminal state transitions in list views.

## 2025-05-22 - Clipboard API and Browser Permissions in Headless Verification
**Learning:** When verifying "Copy to Clipboard" features using Playwright in a headless environment, the script will fail unless "clipboard-read" and "clipboard-write" permissions are explicitly granted in the browser context.
**Action:** Always include `permissions=["clipboard-read", "clipboard-write"]` in `browser.new_context()` when testing clipboard interactions.
