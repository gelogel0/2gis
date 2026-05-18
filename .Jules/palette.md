## 2025-05-18 - [Python Template Escaping]
**Learning:** In `scripts/4_build_send_page.py`, the `HTML_TEMPLATE` should use single curly braces `{ }` for JavaScript/CSS blocks as the templating logic uses `.replace()`. Avoid double curly braces to prevent syntax errors in the generated HTML.
**Action:** Always check the templating method used in Python scripts before applying braces.

## 2025-05-18 - [Accessible Feedback for Copy Action]
**Learning:** For 'Copy to Clipboard' actions, providing visual feedback via icon change should be accompanied by updating the `aria-label` (e.g., to "Copied!") to ensure the state change is announced to screen reader users.
**Action:** When implementing temporary state changes in the UI, ensure accessibility attributes are updated alongside visual elements.
