## 2024-05-22 - [Templating syntax collision]
**Learning:** In projects where HTML/JS is generated via Python's `.replace()` or `.format()` on a string, JavaScript curly braces `{}` often need to be doubled `{{}}` to avoid being interpreted as Python placeholders.
**Action:** Always check the templating logic in the build script before refactoring JS blocks, and verify that the build script itself still runs without `KeyError`.
