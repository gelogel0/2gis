## 2025-05-20 - High-Contrast Focus Indicators for Dark Mode UI
**Learning:** In dark mode interfaces (`#0e1116`), default browser outlines on inputs and buttons can be low-contrast or invisible during keyboard navigation. Using `:focus-visible` with a high-contrast accent ring (`outline: 2px solid #4ade80`, `outline-offset: 2px`) guarantees visible focus for keyboard users without affecting mouse clicks.
**Action:** Always apply high-contrast `:focus-visible` outline styles matching the theme's primary accent color on interactive inputs and buttons.
