## 2025-05-15 - [Preserving JS Braces in Python Templates]
**Learning:** In Python scripts that generate HTML via raw string templates (like `scripts/4_build_send_page.py`), JavaScript code blocks must use double curly braces (`{{ }}`) to prevent syntax errors or unintended interpolation if the template is ever processed with `.format()`, even if the current implementation uses `.replace()`.
**Action:** Always maintain the existing escaping convention (single vs double braces) when adding or modifying JavaScript within Python string templates.
