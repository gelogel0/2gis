## 2025-05-22 - [Template Literal Escaping and Variable Consistency]
**Learning:** When using Python's `.replace()` for manual HTML templating, literal curly braces `{{ }}` in the template source will persist in the output, causing JavaScript syntax errors. Additionally, ensuring all variables are correctly scoped and defined before insertion into templates is crucial for avoiding runtime errors.
**Action:** Always verify the generated HTML for literal double-braces and use tools like Playwright to catch JavaScript errors early. Check that all template placeholders correspond to correctly defined variables in the Python script.

## 2025-05-22 - [Double Escaping in HTML Attributes]
**Learning:** Escaping text for HTML display and then escaping it again for an HTML attribute (like `data-text`) leads to double-escaping in the attribute value, which breaks functionality when retrieved via JavaScript (e.g., `&quot;` becoming `&amp;quot;`).
**Action:** Maintain a "raw" version of the content and apply `escape(value, quote=True)` only once when injecting into HTML attributes. Use Playwright to verify that the value retrieved by JavaScript matches the original raw text.
