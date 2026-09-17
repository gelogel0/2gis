# Palette Journal

## 2026-03-31 - Keyboard Focus Contrast in Dark Themes
**Learning:** Default browser focus rings have poor visual contrast on custom dark backgrounds (`#0e1116`), making keyboard navigation difficult for users relying on Tab key traversal.
**Action:** Use `:focus-visible` with high-contrast accent colors (e.g., `#4ade80`) and `outline-offset: 2px` to make interactive elements clearly visible when focused via keyboard without affecting mouse clicks.
