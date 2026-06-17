## 2025-05-15 - [Copy Button & Pointer Events]
**Learning:** To prevent redundant interactions in a processed table row, apply `pointer-events: none` to action buttons within a state-specific container (e.g., `.row-sent`). This ensures that once a lead is processed, it remains in a read-only state, preventing double-sends.
**Action:** Use CSS like `.row-sent .btn { pointer-events: none; }` alongside visual opacity changes for finalized states.

## 2025-05-15 - [Python Template String Escaping]
**Learning:** In this project's Phase 4 builder, the `HTML_TEMPLATE` uses `.replace()` for substitution rather than `.format()`. This means that literal JavaScript braces must NOT be doubled (no `{{ }}`), as `.replace()` will not unescape them, leading to syntax errors in the generated browser code.
**Action:** Always check the substitution method (`.replace` vs `.format`) before editing template strings containing CSS or JS blocks.
