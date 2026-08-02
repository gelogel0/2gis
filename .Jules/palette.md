# Palette's UX Journal

This journal documents key UX and accessibility learnings from the LeadHunter MVP project.

## 2026-08-02 - Copy-to-Clipboard Micro-UX Integration
**Learning:** Adding immediate visual and screen-reader accessible feedback (e.g., transition from 📋 to ✅ with corresponding `aria-label` updates) dramatically improves interaction confidence during quick bulk outreach. Furthermore, browser security requires Secure Context (HTTPS or localhost) for clipboard write permissions, requiring careful Playwright environment configuration during testing.
**Action:** When adding any clipboard interaction next time, ensure immediate feedback and proper clean up of state variables to prevent overlapping timers, and configure Playwright tests using localhost HTTP servers with granted clipboard permissions.
