"""Phase 1: парсим 2GIS и складываем в Supabase."""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import logging

import typer

from src.config import load_settings, setup_logging
from src.db import get_client, upsert_leads
from src.scrapers.twogis import search_leads

log = logging.getLogger(__name__)
app = typer.Typer(add_completion=False)


@app.command()
def main(
    city: str = typer.Option("Алматы", help="Город (Алматы / Астана / Шымкент)"),
    category: str = typer.Option(
        "салон красоты",
        help='Поисковый запрос ("салон красоты", "стоматология", "фитнес")',
    ),
    limit: int = typer.Option(50, help="Сколько лидов парсить"),
    headless: bool = typer.Option(
        False, help="True = headless (для серверов). False (default) = видимый браузер."
    ),
) -> None:
    """python scripts/1_scrape_2gis.py --city Алматы --category 'салон красоты' --limit 50"""
    settings = load_settings()
    setup_logging(settings.log_level)

    log.info("Парсим 2GIS: %s / %s / limit=%d", city, category, limit)
    leads = search_leads(city=city, query=category, limit=limit, headless=headless)
    log.info("Получено %d лидов из 2GIS", len(leads))

    if not leads:
        log.warning("Ничего не найдено. Проверь селекторы или включи headless=False для отладки.")
        raise typer.Exit(code=1)

    rows = [lead.to_db_row() for lead in leads]
    # category override на уровне CLI — если пользователь указал, ставим
    for row in rows:
        if not row.get("category"):
            row["category"] = category

    client = get_client(settings)
    upsert_leads(client, rows)
    log.info("Готово. Открой Supabase Dashboard → table editor → leads.")


if __name__ == "__main__":
    app()
