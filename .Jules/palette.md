## 2025-05-22 - [Feedback & Contrast]
**Learning:** Providing immediate visual feedback for background actions (like copying) significantly improves perceived responsiveness. However, when combined with 'completed' states (like marking a row sent), care must be taken not to stack filters (like opacity and grayscale) that could push text contrast below accessible limits.
**Action:** Use single, clear visual indicators for state changes (e.g., just opacity for 'sent' rows) and ensure interactive feedback (e.g., 'Copied!') is also communicated via ARIA labels for screen reader users.
