## 2026-07-14 - [Copy to Clipboard with Visual Feedback]
**Learning:** For asynchronous 'Copy to Clipboard' actions, providing immediate visual feedback (changing icon and ARIA label) and then reverting after a timeout significantly improves user confidence and accessibility.
**Action:** Always implement a success/failure state with a timer for clipboard actions to ensure the UI returns to a predictable state.

## 2026-07-14 - [Browser Clipboard API in Headless Tests]
**Learning:** The `navigator.clipboard` API requires a Secure Context (HTTPS or localhost) and explicit browser permissions to work in Playwright.
**Action:** When testing clipboard features, use a local HTTP server and `browser.new_context(permissions=['clipboard-read', 'clipboard-write'])`.
