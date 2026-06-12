## 2025-05-14 - Fix for broken JavaScript in generated HTML

**Learning:** When using Python's `.replace()` for HTML/JS template substitution, literal braces in JavaScript must NOT be doubled (unlike with `.format()`). Doubled braces `{{ }}` cause syntax errors in the resulting browser code.

**Action:** Always use single braces `{ }` for literal code blocks in templates processed with `.replace()`, and verify the output HTML for syntax correctness.
