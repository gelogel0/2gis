## 2025-05-21 - Localization & Template Consistency
**Learning:** Micro-UX enhancements like ARIA labels and visual feedback must respect the application's primary language to avoid cognitive friction. Additionally, when using raw string templates in Python, the choice of placeholder syntax (e.g., `.replace()` vs `.format()`) dictates how curly braces should be handled in CSS/JS blocks.
**Action:** Always check the existing placeholder replacement logic before deciding whether to escape curly braces in templates, and ensure all user-visible strings match the app's locale.
