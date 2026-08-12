# Palette's Journal - Critical Learnings Only

## 2024-08-12 - Double-Brace Elimination for Clean Browser-Side JavaScript
**Learning:** When template files or raw string templates use double curly braces `{{` and `}}` (often to prevent Python string formatter interpolation or to adhere to styling rules), keeping them in the browser-side JavaScript can cause subtle "Unexpected token '}'" syntax errors (e.g. inside nested object literals, arrow function arguments, or callbacks). While some nested blocks are technically valid JS, object properties like `headers: {{ ... }}` fail parsing in modern engines.
**Action:** Always strip or replace double braces `{{` and `}}` with single braces `{` and `}` when generating the final HTML output file to ensure standard, clean, and compliant JavaScript runs flawlessly in the browser.
