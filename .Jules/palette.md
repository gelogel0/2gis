# Palette UX Journal

## 2026-07-11 - Clipboard Copy Feedback Loop
**Learning:** Asynchronous actions that modify state (like 'Copy to Clipboard') benefit from immediate visual and ARIA feedback. Using emojis (✅) and color changes (`.copy-success`) provides a delightful touch, while updating `aria-label` ensures accessibility for screen readers. Restoring the original state after a timeout (e.g., 2000ms) maintains UI predictability.
**Action:** Always provide visual and ARIA confirmation for 'silent' actions like clipboard copies.

## 2026-07-11 - Accessible Table Interactions
**Learning:** When adding multiple action buttons to a table row, ensure they don't break the layout. Using a flexbox wrapper (`.offer-wrapper`) with `align-items: flex-start` keeps the 'Copy' button aligned with the top of multi-line text. Also, using `:focus-visible` for high-contrast focus indicators improves keyboard navigation without cluttering the experience for mouse users.
**Action:** Use flexbox for button-text alignment and `:focus-visible` for accessible focus states.
