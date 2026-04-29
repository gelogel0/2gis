"""Supabase client (service-role для бэкенд-операций)."""
from __future__ import annotations

import logging
from typing import Any

from supabase import Client, create_client

from .config import Settings

log = logging.getLogger(__name__)


def get_client(settings: Settings) -> Client:
    """Bекend-клиент с service_role (обходит RLS)."""
    return create_client(settings.supabase_url, settings.supabase_service_role_key)


def upsert_leads(client: Client, leads: list[dict[str, Any]]) -> int:
    """Идемпотентный upsert по `id` (2GIS org ID).
    Возвращает количество вставленных/обновлённых записей."""
    if not leads:
        return 0

    response = client.table("leads").upsert(leads, on_conflict="id").execute()
    count = len(response.data) if response.data else 0
    log.info("Upserted %d leads", count)
    return count


def fetch_leads_by_status(
    client: Client,
    status: str,
    limit: int = 100,
    category: str | None = None,
    city: str | None = None,
) -> list[dict[str, Any]]:
    query = client.table("leads").select("*").eq("status", status)
    if category:
        query = query.eq("category", category)
    if city:
        query = query.eq("city", city)
    response = query.limit(limit).execute()
    return response.data or []


def update_lead(client: Client, lead_id: str, fields: dict[str, Any]) -> None:
    client.table("leads").update(fields).eq("id", lead_id).execute()


def log_outreach(
    client: Client,
    lead_id: str,
    template_id: str,
    message: str,
    channel: str = "whatsapp",
) -> None:
    client.table("outreach_log").insert(
        {
            "lead_id": lead_id,
            "template_id": template_id,
            "message": message,
            "channel": channel,
        }
    ).execute()
