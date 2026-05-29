# Palette Journal 🎨

Mission: To add small touches of delight and accessibility to the LeadHunter interface, making it more intuitive and pleasant for users.

## 2025-05-14 - Initial Setup
**Learning:** The lead sender interface is a generated static HTML page, which requires careful handling of templates and vanilla JS for interactivity.
**Action:** Use vanilla JS and CSS in the Python script to enhance the user experience without adding heavy dependencies.

## 2025-05-14 - Python HTML Template Braces
**Learning:** In `scripts/4_build_send_page.py`, the `HTML_TEMPLATE` must use single curly braces `{ }` for JavaScript/CSS blocks because the script uses `.replace()` for substitution, not `.format()`. Doubled braces `{{ }}` in the Python source will persist as literal `{{ }}` in the generated HTML, causing JavaScript syntax errors.
**Action:** Always use single braces in this specific template and verify the output HTML for syntax errors.
