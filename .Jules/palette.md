## 2026-05-24 - [Micro-UX: Copy to Clipboard]
**Learning:** In static HTML generation scripts where simple string replacement (`.replace()`) is used instead of sophisticated templating engines (like Jinja2) or Python's `.format()`, using double curly braces `{{ }}` in JavaScript/CSS blocks will persist in the output, causing syntax errors in the browser.
**Action:** Always verify how templates are being processed. If `.replace()` is used, keep JavaScript braces single. If `.format()` or f-strings are used, double them to escape.

## 2026-05-24 - [Clipboard API Verification]
**Learning:** Playwright requires explicit permission granting in the browser context to interact with the Clipboard API in a headless environment.
**Action:** Use `context.grant_permissions(["clipboard-read", "clipboard-write"])` in verification scripts for features involving copy-to-clipboard.
