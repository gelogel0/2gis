# Palette's Journal

## 2025-05-15 - Python-to-JS Interpolation Fix
**Learning:** When generating HTML/JS via Python f-strings or `.replace()`, JavaScript's double curly braces (e.g. in arrow functions or objects) can conflict with Python's own escaping or just remain as invalid JS syntax if not handled.
**Action:** Always include `.replace("{{", "{").replace("}}", "}")` at the end of the substitution chain in `scripts/4_build_send_page.py` to ensure the final output is valid JavaScript.

## 2025-05-15 - Dark Theme Focus Indicators
**Learning:** In a dark-themed UI (background `#0e1116`), standard focus outlines can be hard to see. The project's highlight green `#4ade80` provides excellent contrast.
**Action:** Use `*:focus-visible { outline: 2px solid #4ade80; outline-offset: 2px; }` to provide a clear, accessible focus state for keyboard users without affecting mouse users.
