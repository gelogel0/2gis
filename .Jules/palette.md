## 2025-05-14 - [Visual Consistency for Sent Rows]
**Learning:** Applying UX states (like `.row-sent`) only in client-side JavaScript leads to visual "jank" or inconsistency when the page is refreshed if the initial HTML generation doesn't account for the same state.
**Action:** Always ensure that server-side (or build-time) HTML generation logic reflects the same state-based styling as the client-side interactive logic.

## 2025-05-14 - [Copy to Clipboard Feedback]
**Learning:** Users need immediate and clear visual feedback for "Copy to Clipboard" actions, especially when there's no native OS notification.
**Action:** Use a combination of icon change (📋 -> ✅), color change, and accessible labels (ARIA) to confirm success, with a timed reset to the original state.
