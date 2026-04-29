"""Health check: проверяет коннект к Supabase и OpenAI до полного прогона."""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from openai import OpenAI

from src.config import load_settings, setup_logging
from src.db import get_client


def check_supabase() -> bool:
    settings = load_settings()
    client = get_client(settings)
    try:
        # Простой select — проверяем что таблица доступна
        response = client.table("leads").select("id", count="exact").limit(1).execute()
        count = response.count if hasattr(response, "count") else None
        print(f"✓ Supabase OK — таблица leads доступна (count={count})")
        return True
    except Exception as exc:
        print(f"✗ Supabase FAIL: {exc}")
        print("  Проверь:")
        print("    1. SUPABASE_URL и SUPABASE_SERVICE_ROLE_KEY в .env")
        print("    2. Запустил ли sql/001_init_schema.sql и sql/002_disable_rls.sql")
        return False


def check_openai() -> bool:
    settings = load_settings()
    client = OpenAI(api_key=settings.openai_api_key)
    try:
        response = client.chat.completions.create(
            model=settings.openai_model,
            messages=[{"role": "user", "content": "ping"}],
            max_tokens=5,
        )
        content = response.choices[0].message.content
        print(f"✓ OpenAI OK — model={settings.openai_model}, ответ={content!r}")
        return True
    except Exception as exc:
        print(f"✗ OpenAI FAIL: {exc}")
        print("  Проверь OPENAI_API_KEY в .env (он должен начинаться с sk-...)")
        return False


def check_playwright() -> bool:
    try:
        from playwright.sync_api import sync_playwright

        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page()
            page.goto("https://example.com", timeout=10_000)
            title = page.title()
            browser.close()
        print(f"✓ Playwright OK — example.com title={title!r}")
        return True
    except Exception as exc:
        print(f"✗ Playwright FAIL: {exc}")
        print("  Запусти: playwright install chromium")
        return False


def main() -> None:
    setup_logging("WARNING")  # тише для health check
    print("Lead Hunter — Health Check")
    print("=" * 50)
    ok = all([
        check_supabase(),
        check_openai(),
        check_playwright(),
    ])
    print("=" * 50)
    if ok:
        print("Все системы готовы. Можешь запускать pipeline:")
        print("  python scripts/1_scrape_2gis.py --city Алматы --category 'салон красоты' --limit 30")
    else:
        print("Есть проблемы — исправь ↑ и запусти health.py снова.")
        sys.exit(1)


if __name__ == "__main__":
    main()
