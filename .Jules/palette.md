# Palette's UX Journal

This journal documents critical UX and accessibility learnings from working on LeadHunter.

## 2025-02-15 - [Copy to Clipboard Micro-UX Interaction]
**Learning:** For 'Copy to Clipboard' buttons, relying purely on visual feedback like changing the emoji to ✅ leaves screen reader users unaware of the change. Supplementing visual changes with an updated `aria-label` (e.g., from 'Copy offer to clipboard' to 'Copied!') ensures seamless accessibility. Moreover, protecting the transition state using an asynchronous flag (`dataset.isCopying`) avoids race conditions from rapid double-clicks during the restore timeout.
**Action:** When adding simple copy buttons, always bundle visual transitions (hover scale, color changes) with explicit ARIA label updates, keyboard focus visibility (`:focus-visible`), and a robust state lock flag to ensure accessible and solid interaction design.
