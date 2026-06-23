# Palette's Journal - LeadHunter MVP UX & Accessibility

This journal tracks critical UX and accessibility learnings for the LeadHunter MVP project.

## 2024-05-14 - Initial Setup
**Learning:** Initializing the Palette journal to track UX improvements.
**Action:** Always document significant UX/a11y patterns discovered during the mission.

## 2024-05-14 - Copy to Clipboard & Interaction Feedback
**Learning:** Providing immediate visual feedback for "Copy" actions (changing icon and ARIA label) significantly improves the perceived responsiveness of the UI. Disabling interactive elements in processed rows via `pointer-events: none` prevents redundant actions and clarifies the current state.
**Action:** Always include temporary success/feedback states for background operations.
