## 2025-05-14 - [Templating in Python Scripts]
**Learning:** When HTML/JS templates are embedded in Python scripts and processed using `.replace()`, literal JavaScript braces should remain as single braces `{ }`. Using doubled braces `{{ }}` (standard for `.format()` or f-strings) will result in broken JavaScript syntax in the output HTML.
**Action:** Always check the substitution method used in the Python script before modifying embedded templates.

## 2025-05-14 - [Accessibility vs Screen Readers]
**Learning:** Screen readers automatically announce the text content of interactive elements like buttons. Adding a redundant `aria-label` that matches the text content (e.g., `aria-label="mark sent"` on a button with text "mark sent") provides no additional value and can be repetitive for users.
**Action:** Only use `aria-label` when the visual text is missing or insufficient (e.g., icon-only buttons).
