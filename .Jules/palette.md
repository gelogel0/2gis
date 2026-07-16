## 2026-07-16 - Prevent race conditions in UI feedback timeouts
**Learning:** When providing temporary visual feedback (e.g., changing a button icon to ✅ after copying) using `setTimeout`, rapid repeated clicks can capture the intermediate "success" state as the "original" state, causing the UI to get stuck.
**Action:** Use a state flag (e.g., `element.dataset.isCopying`) to guard the function and prevent concurrent feedback loops.
