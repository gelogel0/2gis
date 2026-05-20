## 2025-05-15 - Python String Templating Gotchas
**Learning:** When a Python script uses `.replace("{key}", value)` for simple templating instead of `.format()` or f-strings, JavaScript/CSS blocks in the template must use single curly braces `{ }`. Double braces `{{ }}` (common in `.format()`) will be rendered literally, breaking the frontend logic.
**Action:** Always check the templating method before assuming double-brace escaping is needed for JS/CSS in Python-generated HTML.
