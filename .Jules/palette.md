# Palette UX & Accessibility Journal

## 2025-02-15 - [Unified Copy-to-Clipboard & Tactical Transitions]
**Learning:** Copying generated offers is a frequent action. Adding an accessible copy button with immediate visual/screen-reader feedback and smooth tactile interactions enhances productivity. High-contrast `:focus-visible` styling improves keyboard navigation.
**Action:** Use `.offer-wrapper` with `display: flex` and `align-items: flex-start` to layout the copy button. Implement secure Clipboard API, transitions on hover (`scale(1.1)`) / active (`scale(0.95)`), and explicit ARIA labels.
