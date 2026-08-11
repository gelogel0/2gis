# Palette's Journal

This journal documents critical UX and accessibility learnings from working on the LeadHunter codebase.

## 2025-08-11 - Custom Clipboard Copy Verification & Secure Context constraints
**Learning:** When implementing clipboard copying features using `navigator.clipboard.writeText` within static web setups, headless browser environments (like Playwright) often disable the API for `file://` URLs because they are not considered a Secure Context. Additionally, browser contexts must explicitly grant permission for clipboard reading and writing in headless mode.
**Action:** Always verify Clipboard interactions by hosting the static pages via a local HTTP server (e.g., Python `http.server`) and calling `browser_context.grant_permissions(["clipboard-read", "clipboard-write"])` before starting Playwright user journey assertions.

## 2025-08-11 - Micro-UX and Native Accessible State-Locking in Table Rows
**Learning:** Marking an entire table row container as disabled using `pointer-events: none` or heavy grayscale filters breaks basic user workflows like selecting text or copying text fragments, and screen readers will fail to correctly navigate them. For proper accessibility, the row text must remain selectable, while action elements should be targeted individually (with native `disabled` attributes for `<button>` elements, and styled `pointer-events: none` only for elements that lack a native disabled state like `<a>`).
**Action:** When a table row changes state (e.g., to "sent"), apply visual indicators like 0.4 opacity, disable interactive buttons natively, block pointer events on specific links, but keep descriptive fields and helper tools (like copy to clipboard) fully interactive.
