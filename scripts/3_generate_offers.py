"""Phase 3: GPT-4o-mini генерирует персонализированный оффер для каждого лида."""
from __future__ import annotations

import logging
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import typer

from src.ai.personalize import make_openai_client, make_wa_link, personalize_offer
from src.ai.prompts import ALL_TEMPLATES
from src.config import load_settings, setup_logging
from src.db import fetch_leads_by_status, get_client, update_lead

log = logging.getLogger(__name__)
app = typer.Typer(add_completion=False)


@app.command()
def main(
    limit: int = typer.Option(50, help="Сколько лидов обработать"),
    template_id: str | None = typer.Option(
        None, help="Принудительно выбрать шаблон A/B/C (default: авто-роутинг)"
    ),
) -> None:
    settings = load_settings()
    setup_logging(settings.log_level)
    client = get_client(settings)
    openai_client = make_openai_client(settings)

    leads = fetch_leads_by_status(client, status="enriched", limit=limit)
    log.info("Найдено %d лидов в статусе 'enriched'", len(leads))

    forced_template = None
    if template_id:
        forced_template = next(
            (t for t in ALL_TEMPLATES if t["id"] == template_id.upper()), None
        )
        if not forced_template:
            log.error("Неизвестный template_id: %s. Выбери из A/B/C.", template_id)
            raise typer.Exit(code=2)

    generated = 0
    for idx, lead in enumerate(leads, 1):
        try:
            tpl_id, message = personalize_offer(
                openai_client, settings, lead, template=forced_template
            )
        except Exception as exc:
            log.exception("OpenAI fail for %s: %s", lead["name"], exc)
            continue

        wa_link = ""
        if lead.get("main_phone"):
            wa_link = make_wa_link(lead["main_phone"], message)

        update_lead(client, lead["id"], {
            "template_id": tpl_id,
            "generated_offer": message,
            "wa_link": wa_link,
            "status": "generated",
        })
        generated += 1
        log.info("[%d/%d] %s → template=%s, %d chars",
                 idx, len(leads), lead["name"], tpl_id, len(message))

    log.info("Готово. Сгенерировано офферов: %d из %d", generated, len(leads))


if __name__ == "__main__":
    app()
