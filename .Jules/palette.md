# Palette's UX Journal

This journal documents critical UX and accessibility learnings from implementing improvements in LeadHunter.

## 2025-05-15 - [Copy to Clipboard with Feedback]
**Learning:** For 'Copy to Clipboard' actions in a table context, providing immediate visual feedback (changing icon to ✅) and updating the `aria-label` for screen readers (to "Copied!") is essential for a smooth experience. Restoring the original state after a short timeout (2000ms) prevents the UI from feeling "stuck" in the success state.
**Action:** Use a flexbox wrapper (`.offer-wrapper`) for the text and button to keep the layout stable during multi-line content. Always restore `aria-label` and icon/text in both success and `catch` (error) blocks.
