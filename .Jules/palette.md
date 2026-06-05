## 2025-05-14 - [Copy to Clipboard Micro-UX]
**Learning:** For 'Copy to Clipboard' actions, providing immediate visual feedback by temporarily changing the icon and updating the `aria-label` makes the interaction feel much more responsive and accessible. Using flexbox with `align-items: flex-start` ensures the copy button stays aligned at the top of multi-line text blocks.
**Action:** Always include a success state (icon/text change) and update ARIA labels when implementing clipboard features. Use robust flexbox containers for action buttons next to text.
