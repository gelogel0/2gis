# Palette's UX & Accessibility Journal

## 2026-08-16 - 1-Click Clipboard Actions in Dark Theme Lead Queues
**Learning:** For fast-paced outreach workflows, multi-line preview text requires immediate 1-click clipboard actions next to the text container. Visual feedback (`📋` -> `✅`) must combine color highlights (`#4ade80`) with updated ARIA labels (`aria-label="Скопировано!"`) so screen reader users receive explicit feedback. State guarding (`dataset.isCopying`) is crucial to prevent rapid click race conditions during feedback timeouts.
**Action:** When adding inline utility actions to text previews, wrap the text and action button in a flex container (`align-items: flex-start`), provide temporary visual and ARIA feedback with timeout resets, and guard against re-entry.
