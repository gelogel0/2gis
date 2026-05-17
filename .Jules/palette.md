## 2025-05-15 - Escaping HTML Attributes in Python Templates
**Learning:** When generating HTML via Python strings (manual templating), using `html.escape(value, quote=True)` is critical when values are placed inside HTML attributes (like `data-*` or `aria-label`). Failure to do so allows characters like `"` to break the attribute structure and potentially the entire UI.
**Action:** Always use `quote=True` in `html.escape()` for attribute values in `src/ui/send_page.py`.
