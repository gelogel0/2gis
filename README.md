# LeadHunter MVP

Парсер B2B-лидов для Казахстана: 2GIS → Instagram enrichment → GPT-4o-mini персонализация → wa.me click-to-send links.

## Цель проекта

Собрать список целевых SMB-бизнесов в KZ (салоны красоты, стоматологии, фитнес), обогатить их профили данными из Instagram, сгенерировать персонализированный outreach для каждого, и дать удобный интерфейс для ручной отправки через WhatsApp Web (1 клик = 1 сообщение).

Без over-engineering. Python + Supabase + минимальный HTML.

## Архитектура

```
[2GIS Playwright scraper] ──→ [Supabase: leads]
                                    │
                                    ↓
[Instagram enrich (Instaloader)] ──→ обогащение профиля
                                    │
                                    ↓
[GPT-4o-mini offer generator] ──→ персонализированное сообщение по 1 из 3 шаблонов
                                    │
                                    ↓
[HTML send-page] ──→ wa.me click-to-send → ты жмёшь Enter в WhatsApp Web
                                    │
                                    ↓
[Supabase: помечается status=sent]
```

## Стек

- **Python 3.11+**
- **Playwright** — обход 2GIS API лимита, парсинг телефонов с web-страниц
- **Instaloader** — парсинг Instagram bio + последних постов
- **OpenAI GPT-4o-mini** — персонализация офферов
- **Supabase** — хранение лидов и tracking
- **HTML/JS** (vanilla) — простая страница для click-to-send

## Структура проекта

```
lead-hunter-mvp/
├── README.md
├── .env.example
├── requirements.txt
├── pyproject.toml
├── src/
│   ├── __init__.py
│   ├── config.py              # env loading
│   ├── db.py                   # Supabase client
│   ├── scrapers/
│   │   ├── __init__.py
│   │   ├── twogis.py           # Playwright 2GIS scraper
│   │   └── instagram.py        # Instagram bio + posts enrich
│   ├── ai/
│   │   ├── __init__.py
│   │   ├── personalize.py      # GPT-4o-mini offer generation
│   │   └── prompts.py          # 3 базовых шаблона A/B/C
│   └── ui/
│       └── send_page.py        # генерация HTML для отправки
├── scripts/
│   ├── 1_scrape_2gis.py        # Phase 1
│   ├── 2_enrich_instagram.py   # Phase 2
│   ├── 3_generate_offers.py    # Phase 3
│   └── 4_build_send_page.py    # Phase 4
├── templates/
│   └── send_page.html          # HTML template для отправки
├── data/                       # gitignored
└── sql/
    └── 001_init_schema.sql     # Supabase init
```

## Quickstart

```bash
# 1. clone & install
git clone https://github.com/gelogel0/lead-hunter-mvp.git
cd lead-hunter-mvp
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
playwright install chromium

# 2. env
cp .env.example .env
# Заполни OPENAI_API_KEY, SUPABASE_URL, SUPABASE_SERVICE_ROLE_KEY, SUPABASE_ANON_KEY

# 3. инит Supabase схемы (один раз)
psql -h <supabase-host> -d postgres -f sql/001_init_schema.sql
# или вставить в Supabase Dashboard → SQL Editor

# 4. парсим 2GIS
python scripts/1_scrape_2gis.py --city "Алматы" --category "салон красоты" --limit 100

# 5. обогащаем инстой
python scripts/2_enrich_instagram.py --limit 100

# 6. генерим офферы (выбирает A/B/C шаблон + персонализирует)
python scripts/3_generate_offers.py --limit 100

# 7. собираем HTML страницу для отправки
python scripts/4_build_send_page.py --output data/send_page.html
# открыть в браузере и кликать [Send via WhatsApp Web]

# или одним запуском пройти весь pipeline
python scripts/0_run_pipeline.py --city "Алматы" --category "салон красоты"
# dry-run (показать команды без запуска)
python scripts/0_run_pipeline.py --dry-run
# с таймаутом шага и продолжением при ошибках
python scripts/0_run_pipeline.py --timeout-sec 1800 --continue-on-error
```

## Автозапуск по расписанию (systemd)

В репозитории есть шаблоны:
- `deploy/lead-hunter.service`
- `deploy/lead-hunter.timer`

Быстрый setup на Linux/VPS:

```bash
# авто-генерация unit-файлов под текущий путь проекта + запуск timer
./deploy/install_systemd.sh
```

Проверь и поправь в `lead-hunter.service`:
- `WorkingDirectory`
- путь к Python в `.venv`
- параметры `--city`, `--category`

Можно переопределить перед установкой:

```bash
CITY="Астана" CATEGORY="стоматология" ./deploy/install_systemd.sh /opt/lead-hunter lead-hunter "$USER"
```

## Деплой на Vercel + Supabase

Рекомендуемая схема для MVP:
- backend-пайплайн (scrape/enrich/generate) крутится на VPS/локально;
- в Vercel публикуется только готовая send-page (`public/index.html`);
- отправка `status=sent` идёт напрямую в Supabase через `SUPABASE_ANON_KEY`.

Шаги:

```bash
# 1) собрать страницу отправки
python scripts/4_build_send_page.py --output data/send_page.html

# 2) подготовить статический артефакт для Vercel
python scripts/6_prepare_vercel.py --source data/send_page.html --target public/index.html

# 3) залить в git и деплоить в Vercel
```

Что важно в Supabase перед публикацией:
- включить RLS для таблицы `leads`;
- добавить policy, разрешающую `UPDATE status,sent_at` только для нужных строк/ролей;
- использовать только `SUPABASE_ANON_KEY` на фронте (service role нельзя).

## Шаблоны outreach (A/B/C)

3 базовых шаблона, протестированных на CIS-B2B аудитории. GPT-4o-mini только персонализирует, не пишет с нуля.

См. `src/ai/prompts.py`.

## Что НЕ делает (на MVP)

- Не отправляет сообщения автоматически (по соображениям WhatsApp ToS — wa.me click-to-send это compliant способ)
- Нет React-dashboard'а (HTML-страница достаточна для первых 500 отправок)
- Нет follow-up automation (Phase 5)
- Нет AI-image-generation в офферах (Phase 5)

## A/B tracking

В таблице `leads` хранится `template_id` (A/B/C) и `status` (new/generated/sent/replied/closed). После 50+ отправок видно конверсию по каждому шаблону через простой SQL:

```sql
SELECT template_id, COUNT(*) as sent, 
       COUNT(*) FILTER (WHERE status='replied') as replied,
       ROUND(100.0 * COUNT(*) FILTER (WHERE status='replied') / COUNT(*), 1) as reply_rate_pct
FROM leads WHERE status IN ('sent','replied','closed')
GROUP BY template_id;
```

## Лицензия

Private project. Всё внутри.
