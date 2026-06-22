## 2025-05-15 - [Persistent Utility in Processed Rows]
**Learning:** To prevent redundant interactions in a processed table row (e.g., 'Sent' state), applying `pointer-events: none` to the entire row or state-changing buttons is effective, but utility actions like 'Copy' should remain interactive as users may still need the data for reference.
**Action:** Use specific selectors like `.row-sent .js-send-btn, .row-sent .js-mark-btn` for disabling interactions rather than the whole container, ensuring utility buttons remain reachable.
