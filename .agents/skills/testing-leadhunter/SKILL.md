---
name: testing-leadhunter
description: Test the LeadHunter MVP project. Covers unit tests, ruff lint, and file integrity verification. Use when verifying PRs or code changes in the 2gis repo.
---

# Testing LeadHunter MVP

## Prerequisites

- Python 3.11+ installed
- Project dependencies: `pip install -r requirements.txt`
- No `.env` file needed for unit tests (tests mock external services)

## Unit Tests

```bash
cd /path/to/repo
python -m unittest discover -s tests
```

Expected: 6 tests pass (pipeline orchestrator + send page HTML tests).

Test files:
- `tests/test_run_pipeline.py` — tests `build_steps` and `run_plan` from `src/pipeline/orchestrator.py`
- `tests/test_send_page_html.py` — tests XSS escaping in `src/ui/send_page.py` (`row_html`, `safe_wa_link`)

## Lint

```bash
ruff check .
```

Config is in `pyproject.toml` (line-length=100, target py311, select E/F/W/I/N/UP/B/SIM, ignore E501).

Note: As of the initial codebase, there are 9 pre-existing lint warnings (unused imports, typer.Option in defaults, etc.). These are not blockers.

## CI

- **Vercel** check is optional and may fail because `public/index.html` is generated at runtime by `scripts/4_build_send_page.py`, not committed to the repo.
- No other CI checks are configured.

## End-to-End Pipeline

The full pipeline requires external services (Supabase, OpenAI, 2GIS, Instagram) and corresponding secrets. For E2E testing:

### Devin Secrets Needed
- `SUPABASE_URL` — Supabase project URL
- `SUPABASE_ANON_KEY` — Supabase anonymous key
- `SUPABASE_SERVICE_ROLE_KEY` — Supabase service role key
- `OPENAI_API_KEY` — OpenAI API key

### Dry-Run Test (no secrets needed)

```bash
python scripts/0_run_pipeline.py --dry-run
```

This prints the pipeline commands without executing them.

## File Structure Notes

- `src/` — main source code (config, db, scrapers, ai, ui, pipeline)
- `scripts/` — CLI entrypoints (numbered 0-6)
- `tests/` — unit tests
- `sql/` — Supabase schema
- `deploy/` — systemd service/timer templates
- `.claude/skills/` — Claude Code skills (LLM Council)
- No pre-commit hooks configured
