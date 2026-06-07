## 2025-05-15 - [Brace Escaping in Python HTML Templates]
**Learning:** In Python scripts that generate HTML via `.replace()`, JavaScript braces should NOT be doubled (unlike `.format()`). Doubling them results in invalid JS in the final output.
**Action:** Always check the substitution method (`.replace` vs `.format` vs f-string) before assuming brace escaping rules. Added `tests/test_build_page.py` to prevent regressions.

## 2025-05-15 - [Clipboard API in Headless Playwright]
**Learning:** Testing "Copy to Clipboard" in headless Playwright requires granting `clipboard-read` and `clipboard-write` permissions to the browser context.
**Action:** Use `browser.new_context(permissions=['clipboard-read', 'clipboard-write'])` when verifying copy features.
