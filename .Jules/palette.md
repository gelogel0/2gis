## 2025-05-15 - Processed State Interaction Control
**Learning:** When marking an item as processed (e.g., `.row-sent`), disabling primary action buttons while keeping utility buttons (like Copy) interactive improves efficiency and prevents redundant state changes without sacrificing usefulness.
**Action:** Use `pointer-events: none` and `opacity` on state-changing buttons within the processed row's CSS, but ensure utility buttons remain interactive.

## 2025-05-15 - Template Braces in Python-Embedded JS
**Learning:** In repositories where JS is embedded in Python strings processed by `.format()` or similar, JavaScript curly braces MUST be escaped as `{{` and `}}`. Failure to do so breaks the Python build process.
**Action:** Always verify that JS blocks in Python templates preserve double curly braces during edits.
