# Palette's UX & Accessibility Journal

## 2025-02-15 - Micro-UX and Clipboard Accessibility
**Learning:** For 'Copy to Clipboard' actions, providing immediate feedback visually (e.g. green checkmark and text) and auditorily (via `aria-label` updates) prevents confusion, while keeping the container selectable and other action buttons interactive. Using a state flag like `btn.dataset.isCopying` prevents race conditions with rapid clicking.
**Action:** Use global event delegation, check for `dataset.isCopying`, update class and text, restore after a 2000ms timeout with proper ARIA labels.
