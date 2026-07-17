# Palette's UX & Accessibility Journal

## 2025-02-17 - Add accessible offer copying & improved keyboard navigation
**Learning:** Adding interactive copy capabilities directly next to generated offers requires a clean layout (flex wrap/align) that doesn't break table column layouts. Using a focus indicator that doesn't trigger on clicks but appears clearly on tab navigation (`:focus-visible`) prevents styling noise for mouse users while providing standard-compliant visual focus for keyboard users.
**Action:** Use `:focus-visible` with `#4ade80` (green focus ring) for high contrast and style copy triggers inside dynamic tables within a flex `.offer-wrapper` to keep UI aligned and visually delight.
