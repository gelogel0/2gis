## 2026-07-09 - Handling JavaScript Braces in Python Templating
**Learning:** When using Python's `.replace()` to inject data into a JavaScript template string, pre-existing double curly braces `{{ }}` (often used for escaping in f-strings or just as part of JS logic) can be problematic if the final output needs to be valid JavaScript. Explicitly replacing `{{` and `}}` with single braces at the end of the chain ensures the resulting HTML/JS is correct.
**Action:** Always append `.replace("{{", "{").replace("}}", "}")` when performing string-based replacements on templates containing JavaScript logic.

## 2026-07-09 - Secure Context for Clipboard API in Playwright
**Learning:** The `navigator.clipboard` API is often unavailable in headless browsers when loading files via `file://` URLs. Using a simple HTTP server (like `python -m http.server`) to serve the test file ensures a Secure Context, allowing the API to function correctly during frontend verification.
**Action:** Use a local HTTP server when verifying features that rely on Secure Context APIs like Clipboard or Geolocation in Playwright.
