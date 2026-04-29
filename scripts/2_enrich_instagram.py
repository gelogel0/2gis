"""Phase 2: обогащаем лидов Instagram-данными (bio + последние посты)."""
from __future__ import annotations

import logging
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import typer

from src.config import load_settings, setup_logging
from src.db import fetch_leads_by_status, get_client, update_lead
from src.scrapers.instagram import fetch_profile

log = logging.getLogger(__name__)
app = typer.Typer(add_completion=False)


@app.command()
def main(
    limit: int = typer.Option(50, help="Сколько лидов обработать"),
    delay: float = typer.Option(3.0, help="Сек. между запросами в IG (избегать бана)"),
) -> None:
    settings = load_settings()
    setup_logging(settings.log_level)
    client = get_client(settings)

    leads = fetch_leads_by_status(client, status="new", limit=limit)
    log.info("Найдено %d лидов в статусе 'new'", len(leads))

    enriched = 0
    for idx, lead in enumerate(leads, 1):
        ig_handle = lead.get("instagram")
        if not ig_handle:
            log.info("[%d/%d] %s — нет инсты, помечаю enriched без IG",
                     idx, len(leads), lead["name"])
            update_lead(client, lead["id"], {"status": "enriched"})
            continue

        profile = fetch_profile(ig_handle, max_posts=3)
        if profile is None:
            log.info("[%d/%d] %s — IG @%s не найден",
                     idx, len(leads), lead["name"], ig_handle)
            update_lead(client, lead["id"], {"status": "enriched"})
            time.sleep(delay)
            continue

        update_lead(client, lead["id"], {
            "ig_bio": profile.bio,
            "ig_followers": profile.followers,
            "ig_recent_posts": profile.posts,
            "status": "enriched",
        })
        enriched += 1
        log.info("[%d/%d] %s — bio %d chars, %d followers, %d posts",
                 idx, len(leads), lead["name"], len(profile.bio),
                 profile.followers, len(profile.posts))
        time.sleep(delay)

    log.info("Готово. Обогащено: %d из %d", enriched, len(leads))


if __name__ == "__main__":
    app()
