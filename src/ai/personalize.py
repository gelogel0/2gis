"""GPT-4o-mini персонализация офферов на основе шаблонов."""
from __future__ import annotations

import json
import logging
from typing import Any
from urllib.parse import quote

from openai import OpenAI

from ..config import Settings
from .prompts import (
    ALL_TEMPLATES,
    PERSONALIZATION_SYSTEM_PROMPT,
    select_template_by_category,
)

log = logging.getLogger(__name__)


def make_openai_client(settings: Settings) -> OpenAI:
    return OpenAI(api_key=settings.openai_api_key)


def _build_lead_context(lead: dict[str, Any]) -> str:
    """Компактный контекст бизнеса для GPT (минимум токенов)."""
    parts = [
        f"name: {lead.get('name', '')}",
        f"category: {lead.get('category', '')}",
        f"city: {lead.get('city', '')}",
    ]
    if lead.get("rating"):
        parts.append(f"rating: {lead['rating']}")
    if lead.get("reviews_count"):
        parts.append(f"reviews_count: {lead['reviews_count']}")
    if lead.get("ig_bio"):
        parts.append(f"instagram_bio: {lead['ig_bio'][:500]}")
    if lead.get("ig_followers"):
        parts.append(f"ig_followers: {lead['ig_followers']}")
    posts = lead.get("ig_recent_posts") or []
    if posts:
        captions = [p.get("caption", "")[:200] for p in posts[:3] if p.get("caption")]
        if captions:
            parts.append("recent_posts: " + " | ".join(captions))
    return "\n".join(parts)


def personalize_offer(
    openai_client: OpenAI,
    settings: Settings,
    lead: dict[str, Any],
    template: dict | None = None,
) -> tuple[str, str]:
    """Возвращает (template_id, personalized_message)."""
    if template is None:
        template = select_template_by_category(lead.get("category", ""))

    context = _build_lead_context(lead)
    user_prompt = (
        f"DATA ABOUT BUSINESS:\n{context}\n\n"
        f"TEMPLATE TO PERSONALIZE (template_id={template['id']}, "
        f"target_pain={template['target_pain']}):\n\n"
        f"{template['template']}\n\n"
        f"Заполни placeholder'ы и верни готовый текст сообщения."
    )

    response = openai_client.chat.completions.create(
        model=settings.openai_model,
        messages=[
            {"role": "system", "content": PERSONALIZATION_SYSTEM_PROMPT},
            {"role": "user", "content": user_prompt},
        ],
        temperature=0.7,
        max_tokens=400,
    )
    message = response.choices[0].message.content or ""
    message = message.strip()
    log.debug("Generated offer for %s (template=%s, %d chars)",
              lead.get("name"), template["id"], len(message))
    return template["id"], message


def make_wa_link(phone: str, message: str) -> str:
    """Создаёт wa.me click-to-send link.
    phone должен быть в формате международного номера БЕЗ + и без пробелов."""
    clean = "".join(c for c in phone if c.isdigit())
    # Казахстанские номера: 8-XXX → 7-XXX, 7XXX уже OK
    if clean.startswith("8") and len(clean) == 11:
        clean = "7" + clean[1:]
    encoded = quote(message, safe="")
    return f"https://wa.me/{clean}?text={encoded}"
