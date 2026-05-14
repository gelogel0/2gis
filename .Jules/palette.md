# Palette's Journal - Critical UX/Accessibility Learnings

## 2025-05-14 - Python Raw String Template Gotcha
**Learning:** In `scripts/4_build_send_page.py`, the `HTML_TEMPLATE` is a raw string processed with `str.replace()`. JavaScript/CSS blocks using `{{ }}` must be manually unescaped if they are intended to be literal `{ }` in the output, especially after multiple `.replace()` calls that might have been expected to handle them if `.format()` was used. Maintaining consistency with existing unescaping patterns is crucial.
**Action:** Always check how templates are rendered. If using `str.replace()` on a string containing `{{ }}`, add a final `.replace("{{", "{").replace("}}", "}")` step if those braces are meant for the browser.
