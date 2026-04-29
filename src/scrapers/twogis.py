"""2GIS scraper через Playwright (web), обходит лимит API на телефоны.

Стратегия:
- Открываем 2gis.kz/{city}/search/{query} в headless Chromium.
- 2GIS отдаёт результаты в DOM как карточки.
- Для каждой карточки забираем: name, rating, reviews_count, address, category, ссылку на детальную.
- Открываем детальную и парсим: phone(s), website, instagram (часто в социалках).

Замечание: 2GIS активно меняет HTML; селекторы могут потребовать обновления.
Если что-то ломается — сначала запусти scraper c headless=False и посмотри визуально.
"""
from __future__ import annotations

import logging
import re
import time
from dataclasses import dataclass, field
from typing import Any

from playwright.sync_api import Browser, Page, sync_playwright

log = logging.getLogger(__name__)

PHONE_RE = re.compile(r"\+?\d[\d\s()\-]{8,}\d")
INSTAGRAM_RE = re.compile(r"instagram\.com/([A-Za-z0-9_.]+)/?")


@dataclass
class TwoGisLead:
    id: str
    name: str
    category: str
    address: str
    city: str
    main_phone: str | None
    all_phones: list[str] = field(default_factory=list)
    instagram: str | None = None
    website: str | None = None
    rating: float | None = None
    reviews_count: int | None = None
    raw: dict[str, Any] = field(default_factory=dict)

    def to_db_row(self) -> dict[str, Any]:
        return {
            "id": self.id,
            "name": self.name,
            "category": self.category,
            "address": self.address,
            "city": self.city,
            "main_phone": self.main_phone,
            "all_phones": self.all_phones,
            "instagram": self.instagram,
            "website": self.website,
            "rating": self.rating,
            "reviews_count": self.reviews_count,
            "raw_2gis": self.raw,
            "status": "new",
        }


def _normalize_phone(raw: str) -> str:
    """Нормализация в формат +7XXXXXXXXXX."""
    digits = re.sub(r"\D", "", raw)
    if not digits:
        return raw
    if digits.startswith("8") and len(digits) == 11:
        digits = "7" + digits[1:]
    if len(digits) == 10:
        digits = "7" + digits
    return f"+{digits}"


def _score_phone(phone: str) -> int:
    """Чем выше score — тем вероятнее это мобильный/WhatsApp.
    Городские номера, колл-центры, '8 800' — низкий score."""
    digits = re.sub(r"\D", "", phone)
    score = 0
    # Казахстанские мобильные: 7 (7XX) — Beeline/Activ/Tele2 → 700-708, 747, 771-778
    if digits.startswith("77") or (digits.startswith("7") and len(digits) >= 4
                                    and digits[1] == "7"):
        score += 10
    if digits.startswith("8800") or digits.startswith("78002"):
        score -= 5  # городской/колл-центр
    if len(digits) < 10:
        score -= 10
    return score


def _pick_best_phone(phones: list[str]) -> str | None:
    if not phones:
        return None
    scored = sorted(
        ({"phone": p, "score": _score_phone(p)} for p in phones),
        key=lambda x: x["score"],
        reverse=True,
    )
    return scored[0]["phone"]


def _extract_phones_from_text(text: str) -> list[str]:
    raw_matches = PHONE_RE.findall(text)
    normalized: list[str] = []
    seen: set[str] = set()
    for raw in raw_matches:
        norm = _normalize_phone(raw)
        if norm not in seen and len(re.sub(r"\D", "", norm)) >= 10:
            seen.add(norm)
            normalized.append(norm)
    return normalized


def _extract_instagram(text: str) -> str | None:
    match = INSTAGRAM_RE.search(text)
    if match:
        return match.group(1)
    return None


def _city_to_2gis_slug(city: str) -> str:
    mapping = {
        "Алматы": "almaty",
        "Астана": "astana",
        "Шымкент": "shymkent",
        "Караганда": "karaganda",
    }
    return mapping.get(city, city.lower())


def search_leads(
    city: str,
    query: str,
    limit: int = 50,
    headless: bool = True,
) -> list[TwoGisLead]:
    """Главный entry point — ищет до `limit` лидов в указанном городе по query."""
    slug = _city_to_2gis_slug(city)
    url = f"https://2gis.kz/{slug}/search/{query}"

    leads: list[TwoGisLead] = []
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=headless)
        context = browser.new_context(
            user_agent=(
                "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "
                "(KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
            ),
            locale="ru-RU",
        )
        page = context.new_page()
        log.info("Opening %s", url)
        page.goto(url, wait_until="domcontentloaded", timeout=60_000)
        # 2GIS использует динамический рендер — подождём
        try:
            page.wait_for_selector('div[class*="_1kf6gff"], a[href*="/firm/"]',
                                    timeout=20_000)
        except Exception:
            log.warning("Timeout ожидания результатов поиска — продолжаю")

        # Прокручиваем для подгрузки
        for _ in range(min(limit // 12 + 1, 5)):
            page.mouse.wheel(0, 2000)
            time.sleep(1.5)

        # Собираем ссылки на карточки
        cards = page.query_selector_all('a[href*="/firm/"]')
        seen_ids: set[str] = set()
        firm_links: list[str] = []
        for card in cards:
            href = card.get_attribute("href")
            if not href:
                continue
            # /firm/123456789 → 123456789
            match = re.search(r"/firm/(\d+)", href)
            if match and match.group(1) not in seen_ids:
                seen_ids.add(match.group(1))
                firm_links.append(href if href.startswith("http")
                                   else f"https://2gis.kz{href}")
            if len(firm_links) >= limit:
                break

        log.info("Найдено %d уникальных карточек, обхожу детальные", len(firm_links))

        for idx, link in enumerate(firm_links[:limit], 1):
            try:
                lead = _scrape_firm_page(page, link, city)
                if lead:
                    leads.append(lead)
                    log.info("[%d/%d] %s — %s", idx, len(firm_links),
                             lead.name, lead.main_phone or "no phone")
            except Exception as exc:
                log.exception("Ошибка парсинга %s: %s", link, exc)
            time.sleep(1.0)

        browser.close()

    return leads


def _scrape_firm_page(page: Page, url: str, city: str) -> TwoGisLead | None:
    page.goto(url, wait_until="domcontentloaded", timeout=30_000)
    time.sleep(2)
    # Раскрытие "Показать телефон" если есть
    try:
        show_phone_btns = page.query_selector_all('button:has-text("Показать телефон"), '
                                                    'button:has-text("телефон")')
        for btn in show_phone_btns:
            try:
                btn.click(timeout=2_000)
                time.sleep(0.4)
            except Exception:
                pass
    except Exception:
        pass

    html = page.content()
    name = (page.query_selector("h1") and
            page.query_selector("h1").inner_text().strip()) or ""

    # ID из URL
    id_match = re.search(r"/firm/(\d+)", url)
    firm_id = id_match.group(1) if id_match else f"unknown-{hash(url)}"

    phones = _extract_phones_from_text(html)
    instagram = _extract_instagram(html)
    main_phone = _pick_best_phone(phones)

    # Простые селекторы для рейтинга и отзывов (могут потребовать обновления):
    rating: float | None = None
    reviews_count: int | None = None
    rating_el = page.query_selector('div[class*="rating"]')
    if rating_el:
        text = rating_el.inner_text()
        m = re.search(r"(\d[.,]\d)", text)
        if m:
            try:
                rating = float(m.group(1).replace(",", "."))
            except ValueError:
                pass
    reviews_el = page.query_selector('a[href*="reviews"]')
    if reviews_el:
        text = reviews_el.inner_text()
        m = re.search(r"(\d+)", text)
        if m:
            reviews_count = int(m.group(1))

    address_el = page.query_selector('a[href*="geo"]')
    address = address_el.inner_text().strip() if address_el else ""

    category_el = page.query_selector('a[class*="rubric"]')
    category = category_el.inner_text().strip() if category_el else ""

    if not name:
        log.warning("Не удалось получить имя для %s", url)
        return None

    return TwoGisLead(
        id=firm_id,
        name=name,
        category=category,
        address=address,
        city=city,
        main_phone=main_phone,
        all_phones=phones,
        instagram=instagram,
        rating=rating,
        reviews_count=reviews_count,
        raw={"url": url},
    )
