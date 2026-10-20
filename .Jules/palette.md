## 2025-05-20 - High-contrast focus indicators in dark themes & localized input ARIA labels

**Learning:** In dark-themed web interfaces (`#0e1116`), default browser focus rings are often nearly invisible or low-contrast. Furthermore, inputs relying solely on placeholders lack proper accessible names for screen readers, and localized web apps require localized ARIA labels matching the primary language (Russian/Kazakh) to avoid context switching.
**Action:** Always provide explicit `:focus-visible` styling with a high-contrast theme color (e.g., `#4ade80`) and ensure localized `aria-label` attributes on search/filter inputs.
