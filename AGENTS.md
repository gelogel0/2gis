# AGENTS.md

This file applies to the whole repository unless a deeper `AGENTS.md` overrides it.

## Core Standard

- Work in the user’s language unless the task clearly requires another language.
- Start from repository evidence, not assumptions.
- Prefer correctness, clarity, and trust over speed theater.
- Be autonomous for safe, obvious work.
- Ask only when ambiguity blocks a safe decision, when a product choice is genuinely open, or when the action is destructive, irreversible, security-sensitive, privacy-sensitive, or likely to affect unrelated users.
- Do not hallucinate. Verify uncertain claims through code, docs, tests, schemas, scripts, logs, or runtime output.
- Preserve unrelated user work. Do not revert or overwrite changes you did not make unless explicitly asked.
- Keep the system clearer, more correct, and easier to trust after your work.

## Repository First

- Read the repository before proposing architecture.
- For non-trivial tasks, inspect `README.md`, `docs/`, configs, scripts, tests, and the relevant entry points early.
- Trust current code and runnable behavior over stale docs.
- If docs drift from code, call it out and align when practical.
- Do not assume repository structure. Discover it from the repository itself.
- Use the repository’s existing package manager, formatter, linter, test runner, build tools, generators, and conventions.
- Do not add new production dependencies without explicit approval.

## Task Modes

Classify the task before acting.

### Direct
Use for simple local edits, copy changes, comments, formatting, or obvious low-risk fixes.

Rules:
- Inspect the affected file and nearby usage.
- Make the smallest coherent change.
- Run narrow validation if cheap and relevant.

### Investigation
Use for debugging, diagnosis, unstable behavior, unclear failures, or root-cause discovery.

Rules:
- Reproduce or trace the failure path when possible.
- Follow the runtime path vertically.
- Inspect neighboring systems horizontally.
- Do not patch symptoms before identifying the owning layer.
- If two attempts fail to improve the primary signal, stop and reframe.

### Implementation
Use for behavior changes, contracts, auth, validation, persistence, routing, state changes, concurrency, async flows, or other non-trivial user-visible logic.

Rules:
- Understand first.
- State a short plan before broad edits.
- Prefer test-first when supported and proportionate.
- Keep the change minimal in surface area, but complete in ownership.

## Acceptance Contract

For non-trivial tasks, briefly define:
- what “done” means;
- 3–5 observable pass/fail criteria;
- the primary signal;
- useful secondary signals such as tests, typecheck, lint, build, logs, or focused scripts.

Do not create unnecessary ceremony for trivial tasks.

## Root Cause Discipline

- Fix the owning layer, not the nearest visible symptom.
- Do not preserve broken upstream decisions with local guards, duplicated logic, or cosmetic fallbacks.
- One-file fixes for cross-layer problems are suspicious until proven otherwise.
- If the correct fix is larger than the smallest diff, choose the correct fix with the smallest system-wide footprint.
- Minimal does not mean tiny diff at any cost. Minimal means minimal complexity and minimal future confusion.

## Research Pattern

For non-trivial work, do both vertical and horizontal research.

### Vertical research
Trace the execution path end to end.

Examples:
- UI -> route -> container -> service -> API -> persistence
- Request boundary -> validation -> auth -> domain logic -> query -> response
- Trigger -> queue/job -> retry/idempotency -> side effect -> visibility

### Horizontal research
Inspect directly coupled neighboring surfaces.

Examples:
- sibling routes, similar handlers, shared services, serializers, schemas, tests, docs
- loading, empty, error, success, retry, disabled, stale states
- producer and consumer sides of contracts
- read paths and write paths for persistence changes

Do enough research to find the owner layer. Do not turn research into wandering.

## Change-Surface Rules

When touching a boundary, inspect directly coupled code.

- Contracts or schemas: validate producer and consumer sides.
- Routing, auth, guards, redirects, or layouts: inspect adjacent flows and user-visible states.
- Persistence or schema changes: inspect serializers, migrations, generated clients, and read/write paths.
- Async flows: inspect retries, idempotency, ordering, cancellation, and failure visibility.
- User-facing legal, billing, privacy, security, or support copy: preserve product meaning and flag ambiguity.

## Minimal Sufficient Change

- Make the smallest coherent change that fully solves the real problem.
- Prefer simple local clarity over clever abstractions.
- Prefer decoupling over forced DRY.
- Add abstractions only when they remove real current complexity.
- Delete obsolete code paths when a clearer ownership model replaces them.
- Do not build framework-like architecture for small features.

## Testing And Validation

- Run the smallest meaningful validation for the changed surface.
- Prefer cheap signals first: focused tests, typecheck, lint, build, scripts, then wider validation when needed.
- Use the repository’s existing validation infrastructure.
- Validate after implementation and before declaring success.
- If contracts changed, validate both producer and consumer sides.
- Treat non-zero exits, runtime errors, failed assertions, type errors, lint failures, build failures, and timeouts as failed validation.
- Do not claim success on secondary signals alone if the primary user-visible signal is still broken.
- If validation cannot be run, say why and identify the best substitute signal.

## Documentation Discipline

- Code is the primary source of truth for implementation details.
- Docs should capture durable context: architecture, workflows, runbooks, caveats, contracts, and non-obvious decisions.
- Do not create doc churn for trivial refactors or obvious changes.
- Update docs when architecture, setup, operations, contracts, or important engineering decisions change.
- If doc drift remains out of scope, call it out explicitly.

## Safety And Hygiene

- Do not expose secrets, tokens, credentials, cookies, private keys, or raw `.env` values.
- Do not add real secrets to code, tests, docs, fixtures, screenshots, or logs.
- Do not weaken auth, permissions, validation, encryption, rate limiting, or auditability to make progress easier.
- Do not manually edit generated files unless the repository explicitly requires it.
- Keep temporary artifacts out of the repository root.
- Do not commit, push, reset, rebase, stash, or delete files unless explicitly asked.

## Decision Rules

- If the safe solution is obvious and low-risk, execute it.
- If meaningful tradeoffs exist, present up to two viable options and recommend one.
- If a safe assumption unblocks work, proceed and state the assumption in the final report.
- If the action is destructive, irreversible, security-sensitive, privacy-sensitive, or cross-cutting, ask first.
- If the target behavior is still not achieved, report what remains wrong and the best next experiment.

## Completion Protocol

At the end of each investigation or implementation, report:

- what changed and why;
- root cause, when identified;
- affected layers;
- validation performed;
- `Primary signal status`: met / not met / partially validated;
- `Secondary signal status`: exact checks run and results;
- documentation status: updated / not needed / still needs alignment;
- remaining risks, missing coverage, and follow-up work;
- migration or rollout implications when relevant;
- a concise suggested commit message when the work is ready.