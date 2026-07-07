## 2025-05-15 - Clipboard Feedback and Keyboard Accessibility

**Learning:** When implementing "Copy to Clipboard" buttons, providing immediate visual feedback (e.g., changing the icon to a checkmark) and a clear focus indicator for keyboard users significantly improves perceived responsiveness and usability. Using global event delegation makes the UI more robust to dynamic row updates.

**Action:** Always provide tactile/visual feedback for background actions like copying. Use high-contrast `:focus-visible` outlines in dark-themed UIs to ensure keyboard navigation is intuitive without cluttering the mouse-driven experience.
