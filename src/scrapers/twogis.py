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
from urllib.parse import quote

from playwright.sync_api import Page, sync_playwright

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
    headless: bool = False,  # default видимый, чтобы лучше обходить anti-bot
) -> list[TwoGisLead]:
    """Главный entry point — ищет до `limit` лидов в указанном городе по query.

    Замечание про headless:
    - В headless=True 2GIS чаще включает anti-bot (0 результатов).
    - В headless=False (default) — твой реальный десктопный fingerprint, работает почти всегда.
    - Если запускаешь на сервере без display — прокинь headless=True и приготовь terпение."""
    slug = _city_to_2gis_slug(city)
    # 2GIS ожидает Cyrillic URL без percent-encoding; Playwright сам кодирует.
    url = f"https://2gis.kz/{slug}/search/{query.replace(' ', '%20')}"

    leads: list[TwoGisLead] = []
    with sync_playwright() as p:
        browser = p.chromium.launch(
            headless=headless,
            args=[
                "--disable-blink-features=AutomationControlled",
                "--no-sandbox",
                "--disable-setuid-sandbox",
                "--disable-dev-shm-usage",
            ],
        )
        context = browser.new_context(
            user_agent=(
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                "(KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
            ),
            locale="ru-RU",
            viewport={"width": 1920, "height": 1080},
            timezone_id="Asia/Almaty",
        )
        # Stealth: убираем navigator.webdriver
        context.add_init_script(
            "Object.defineProperty(navigator, 'webdriver', {get: () => undefined});"
            "Object.defineProperty(navigator, 'languages', "
            "{get: () => ['ru-RU', 'ru', 'en']});"
        )
        page = context.new_page()
        log.info("Opening %s (headless=%s)", url, headless)
        page.goto(url, wait_until="domcontentloaded", timeout=60_000)

        # 2GIS — SPA, ему нужно время на гидрацию.
        # wait_for_selector ненадёжен (компоненты пересобираются),
        # надёжнее простой sleep и scroll loop с повторными попытками.
        time.sleep(8)

        # Прокручиваем для подгрузки. 2GIS lazy-loads.
        scroll_iters = max(limit // 12 + 1, 3)
        for _ in range(scroll_iters):
            page.mouse.wheel(0, 2000)
            time.sleep(1.8)

        # Если карточек нет — даём 2GIS ещё 10 сек на load
        cards_pre = page.query_selector_all('a[href*="/firm/"]')
        if len(cards_pre) == 0:
            log.warning("Карточек 0 после первого прохода — жду ещё 10s")
            time.sleep(10)
            for _ in range(2):
                page.mouse.wheel(0, 2000)
                time.sleep(1.5)

        # Собираем ссылки на карточки
        cards = page.query_selector_all('a[href*="/firm/"]')
        log.info("DOM содержит %d <a> с /firm/", len(cards))
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
                # Берём чистый URL без stat= (он мешает иногда)
                clean_path = f"/almaty/firm/{match.group(1)}".replace(
                    "/almaty/", f"/{slug}/"
                )
                firm_links.append(f"https://2gis.kz{clean_path}")
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
    # h1 появляется не сразу
    try:
        page.wait_for_selector("h1", timeout=15_000)
    except Exception:
        pass
    time.sleep(1.5)

    # Раскрытие "Показать телефон" если есть кнопки
    try:
        show_phone_btns = page.locator(
            'button:has-text("Показать"), button:has-text("телефон"), '
            'div[role="button"]:has-text("Показать")'
        )
        count = show_phone_btns.count()
        for i in range(min(count, 5)):
            try:
                show_phone_btns.nth(i).click(timeout=2_000)
                time.sleep(0.3)
            except Exception:
                pass
    except Exception:
        pass
    time.sleep(0.6)

    html = page.content()
    name_el = page.query_selector("h1")
    name = name_el.inner_text().strip() if name_el else ""

    # ID из URL
    id_match = re.search(r"/firm/(\d+)", url)
    firm_id = id_match.group(1) if id_match else f"unknown-{hash(url)}"

    phones = _extract_phones_from_text(html)
    instagram = _extract_instagram(html)
    main_phone = _pick_best_phone(phones)

    # Рейтинг и отзывы — несколько fallback селекторов
    rating: float | None = None
    reviews_count: int | None = None

    # Rating: ищем число вида X.X в специфических блоках
    for sel in ['div[class*="rating"]', 'div[class*="Rating"]',
                'span[class*="rating"]', '[itemprop="ratingValue"]']:
        el = page.query_selector(sel)
        if el:
            try:
                text = el.inner_text()
                m = re.search(r"(\d[.,]\d)", text)
                if m:
                    rating = float(m.group(1).replace(",", "."))
                    break
            except Exception:
                continue

    # Reviews count: "123 отзыва", "Отзывы (45)"
    reviews_match = re.search(r"(\d+)\s*(отзыв)", html)
    if reviews_match:
        reviews_count = int(reviews_match.group(1))

    # Адрес: ищем по паттерну "ул./пр./..." или ссылку с гео
    address = ""
    addr_el = page.query_selector('a[href*="geo"], div[class*="address"]')
    if addr_el:
        address = addr_el.inner_text().strip().split("\n")[0]

    # Категория из первой ссылки на rubric
    category = ""
    cat_el = page.query_selector('a[href*="rubric"]')
    if cat_el:
        category = cat_el.inner_text().strip()

    # Website: ищем внешние ссылки кроме социалок
    website = None
    website_el = page.query_selector(
        'a[href^="http"]:not([href*="2gis"]):not([href*="instagram"])'
        ':not([href*="facebook"]):not([href*="vk.com"])'
        ':not([href*="t.me"]):not([href*="wa.me"])'
        ':not([href*="whatsapp"]):not([href*="youtube"])'
    )
    if website_el:
        href = website_el.get_attribute("href") or ""
        if href.startswith("http"):
            website = href

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
        website=website,
        rating=rating,
        reviews_count=reviews_count,
        raw={"url": url},
    )
