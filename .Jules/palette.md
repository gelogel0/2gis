# Palette's Journal - LeadHunter MVP

## Core Principles
- Accessibility is not optional.
- Interaction should feel smooth and provide feedback.
- Good UX is invisible and just works.
- Keep changes minimal and impactful (< 50 lines).

## 2025-05-14 - Initial Setup
**Learning:** The project uses a dark theme and is optimized for quick manual outreach via WhatsApp.
**Action:** Focus on making the outreach process even smoother by adding a 'Copy Offer' button and improving keyboard accessibility.

## 2025-05-14 - Copy Offer Utility
**Learning:** For a tool centered on manual outreach, providing a secondary way to copy the personalized offer text (besides the primary WhatsApp link) significantly improves the tool's utility for other platforms.
**Action:** Added a 'Copy Offer' button with immediate visual feedback (📋 -> ✅) and ensured it works correctly within the existing event delegation pattern.

## 2025-05-14 - Keyboard Accessibility in Dark Theme
**Learning:** Standard focus outlines can be hard to see in dark themes. High-contrast focus indicators are essential.
**Action:** Implemented `:focus-visible` styles using the project's brand green (`#4ade80`) for better keyboard navigation visibility.
