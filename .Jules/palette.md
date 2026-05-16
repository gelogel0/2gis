## 2025-05-15 - [Templating in Static Generation]
**Learning:** In projects using manual `.replace()` for HTML templating (rather than f-strings or Jinja), double curly braces `{{ }}` in CSS/JS are preserved as `{{ }}` and cause syntax errors in the browser.
**Action:** Use single curly braces `{ }` in the template string and avoid doubling them if the processing logic doesn't use `.format()`.
