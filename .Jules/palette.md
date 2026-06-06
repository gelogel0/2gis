## 2025-05-22 - Python Template substitution and JS curly braces
**Learning:** When using Python's `.replace()` for HTML/JS template substitution in a raw string, double curly braces `{{ }}` in the source are preserved as `{{ }}` in the output, which causes JavaScript syntax errors. Single braces `{ }` should be used for literal JS/CSS blocks in this specific setup, even though it feels counter-intuitive to Python developers used to `.format()` or f-strings.
**Action:** Always verify generated HTML for literal double braces if the build script uses `.replace()`. Use a reproduction script that simulates the substitution to catch these before deployment.

## 2025-05-22 - Visual feedback for row processing
**Learning:** Applying `filter: grayscale(1)` and `opacity: 0.4` with a smooth transition provides an intuitive way to mark items as "processed" in a list without removing them, maintaining context while showing progress.
**Action:** Use this pattern for 'Mark as Sent' or similar status transitions in data-heavy tables.
