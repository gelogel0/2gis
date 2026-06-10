## 2024-06-10 - [Clipboard Feedback & Template Escaping]
**Learning:** In projects using Python's `.replace()` for HTML/JS generation, literal curly braces in JS should not be escaped (unlike `.format()`). Providing immediate visual feedback for "Copy" actions (icon change + ARIA label update) significantly improves the perceived responsiveness of the UI.
**Action:** Always check the string substitution method used in build scripts before deciding on brace escaping. Combine visual and screen-reader feedback for background actions like clipboard copying.
