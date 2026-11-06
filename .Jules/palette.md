# Palette's UX Journal

## 2026-11-06 - Accessible Clipboard Actions with State Guards
**Learning:** Icon-only copy buttons require explicit accessible names matching the application's target language, dynamic feedback via `aria-label` updates, and state flags (`dataset.isCopying`) to avoid race conditions during feedback timeouts.
**Action:** When implementing quick copy actions in data tables, wrap the target text and button in a flex container, provide immediate visual/a11y feedback (`✅` / `aria-label="Скопировано!"`), and restore defaults after 2000ms.
