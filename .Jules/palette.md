## 2025-02-12 - Secure Context requirement for Clipboard APIs and Random Ports

**Learning:** Headless browser environments (like Playwright) restrict access to `navigator.clipboard.writeText` when a static page is accessed via the `file://` protocol. Running a local HTTP server ensures a Secure Context, permitting proper clipboard access. Furthermore, utilizing random port allocation minimizes port-in-use collisions in multi-user/CI shared environments.

**Action:** Always host static HTML payloads on a local python `http.server` during Playwright testing, explicitly request browser context permissions (`clipboard-read`, `clipboard-write`), and bind to random ports to prevent environment conflicts.
