## 2025-05-15 - [Copy Offer Feature & Keyboard Accessibility]
**Learning:** When building a static HTML page with embedded JavaScript template strings in Python, using `.replace()` on a template with `{{ }}` for JS blocks requires a final pass to convert double braces back to single braces for valid browser execution.
**Action:** Always add `.replace("{{", "{").replace("}}", "}")` to the end of the substitution chain when using this pattern in `scripts/4_build_send_page.py`.

**Learning:** Interactive icon-only buttons (like 📋) provide better UX when accompanied by immediate visual feedback (e.g., icon change to ✅) and accessible updates (ARIA label change) to confirm background actions like "Copy to Clipboard".
**Action:** Implement a "Success state" with a 2000ms timeout for all one-click utility actions.
