## 2026-07-02 - [Copy to Clipboard and Status Persistence]
**Learning:** For 'Copy to Clipboard' actions, providing immediate visual feedback by temporarily changing the icon and color improves perceived responsiveness. For status changes like 'Mark Sent', using the native `disabled` attribute is critical for accessibility, while `pointer-events: none` is a useful fallback for non-button elements like anchor tags.
**Action:** Always use native `disabled` for buttons and provide visual feedback for async/clipboard operations.

## 2026-07-02 - [HTML Generation Hygiene]
**Learning:** In projects using string substitution for HTML/JS generation, development artifacts and temporary verification scripts should be rigorously cleaned up before submission to keep the patch focused and under line limits.
**Action:** Ensure all `verify_*.py`, `test_*.html`, and `screenshot_*.png` files are deleted before final submission.
