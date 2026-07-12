## 2025-07-12 - [Clipboard API Verification in Headless Playwright]
**Learning:** The Clipboard API (`navigator.clipboard.writeText`) often fails or is disabled in headless browser environments when served via `file://` URLs because it requires a Secure Context (HTTPS or localhost).
**Action:** Always use a local HTTP server (like `http.server`) to serve HTML fragments during Playwright verification and explicitly grant `clipboard-read`/`clipboard-write` permissions in the browser context.
