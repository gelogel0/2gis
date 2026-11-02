## 2026-11-02 - Table Search Filter Live Result Count & Keyboard Focus

**Learning:** When users filter long queue lists in dark-themed interfaces, pairing `:focus-visible` outline feedback with an accessible live announcement badge (`aria-live="polite"`) prevents ambiguity over whether zero or multiple items matched the filter query, while avoiding disruptive screen reader interruptions.
**Action:** Always include an `aria-live="polite"` result count adjacent to search inputs on data tables and ensure high-contrast `:focus-visible` styling is explicitly declared.
