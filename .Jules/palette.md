## 2024-07-30 - Template Double Curly Braces Syntax Error
**Learning:** Raw HTML templates processed via Python's `.replace()` must preserve double braces `{{` and `}}` for formatting compatibility but must have them replaced with single braces `{` and `}` before writing to final output files, otherwise browser engines trigger a JS parser syntax error on encounter.
**Action:** Always append `.replace("{{", "{").replace("}}", "}")` to any raw template replacement pipeline that outputs client-side executed Javascript.
