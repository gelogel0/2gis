## 2025-08-08 - Accessible Copy Offer Micro-Interactions with Clipboards in Headless Testing
**Learning:** When implementing clipboard-related actions, testing in headless environments requires granting browser context permissions ('clipboard-read', 'clipboard-write') and serving the app via localhost to satisfy the secure context requirement for `navigator.clipboard`.
**Action:** Always start a local HTTP server and use `context.grant_permissions` in Playwright tests targeting clipboard operations.
