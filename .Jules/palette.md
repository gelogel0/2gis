## 2025-05-22 - Python Template Substitution Gotcha
**Learning:** In this project, `scripts/4_build_send_page.py` uses `.replace()` for HTML template substitution. This means literal curly braces in JavaScript/CSS blocks must NOT be doubled (escaped), unlike when using `.format()` or f-strings. Doubling them results in invalid JS/CSS in the generated output.
**Action:** Always verify the substitution method used in the build script before applying Python escaping rules to curly braces in templates.

## 2025-05-22 - Accessible Copy Feedback
**Learning:** Providing immediate visual and accessible feedback for "Copy to Clipboard" actions (e.g., changing icon to ✅ and updating `aria-label` to "Скопировано!") significantly improves the perceived responsiveness and accessibility of the interface.
**Action:** Always implement temporary visual (icon) and audible (ARIA label) feedback for background interactions like clipboard copies.
