# Palette's Journal

## 2025-05-22 - Fix JS Syntax Errors in HTML Template
**Learning:** In projects using manual string replacement for HTML generation, standard Python `{{ }}` escaping can lead to invalid JavaScript in the final output if not handled carefully.
**Action:** Always verify generated HTML for literal `{{` or `}}` when using `.replace()` instead of `.format()` or Jinja2.

## 2025-05-22 - Visual Feedback for Copy and Sent Actions
**Learning:** Providing immediate, non-intrusive visual feedback (like grayscale/opacity for sent items or icon changes for copy) significantly improves the perceived responsiveness of the UI.
**Action:** Use CSS transitions and temporary text/icon changes to confirm user actions.
