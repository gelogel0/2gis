
## 2026-06-03 - [JS Template Escaping in Python Builder]
**Learning:** In this repo, 'scripts/4_build_send_page.py' uses '.replace()' for HTML generation rather than '.format()' or f-strings. Doubled curly braces '{{ }}' in the Python source are NOT escaped but preserved literally in the output HTML, causing JavaScript syntax errors (especially in template literals like '${{...}}').
**Action:** Always use single curly braces '{ }' for both replacement tokens and literal JS/CSS blocks in 'HTML_TEMPLATE' when '.replace()' is the substitution method.
