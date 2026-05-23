## 2025-05-23 - [Copy-to-Clipboard Micro-UX]
**Learning:** For static HTML generation, interactive features like copy-to-clipboard require careful integration between Python row generation (for unique IDs) and JS event delegation in the template. Providing immediate visual feedback (changing icon/ARIA label) significantly enhances perceived responsiveness.
**Action:** Use a "copy-feedback-revert" pattern: change button content/label on success, then use `setTimeout` to revert to the original state after 2 seconds.
