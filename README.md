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

## Quickstart (запуск локально)

### 0. Один раз — настроить Supabase

В Supabase Dashboard → SQL Editor → создать new query → запустить по очереди:
1. `sql/001_init_schema.sql` (создаёт таблицы)
2. `sql/002_disable_rls.sql` (отключает RLS для MVP)

### 1. Клонировать и установить (Windows / macOS / Linux)

```bash
git clone https://github.com/gelogel0/2gis.git lead-hunter-mvp
cd lead-hunter-mvp

# Создать виртуальное окружение
python3 -m venv .venv

# Активация:
#   macOS/Linux:
source .venv/bin/activate
#   Windows (PowerShell):
.venv\Scripts\Activate.ps1
#   Windows (CMD):
.venv\Scripts\activate.bat

pip install -r requirements.txt
playwright install chromium
```

### 2. Заполнить .env

```bash
cp .env.example .env
# (на Windows: copy .env.example .env)
# Открыть .env в редакторе и заполнить:
#   SUPABASE_URL=https://zwyzrbenpqzqjxqdcywu.supabase.co
#   SUPABASE_ANON_KEY=sb_publishable_...
#   SUPABASE_SERVICE_ROLE_KEY=eyJ...   ← service_role из Supabase Dashboard → API
#   OPENAI_API_KEY=sk-proj-...
```

### 3. Health check (проверяем что всё подключено)

```bash
python scripts/health.py
```

Должно вывести:
```
✓ Supabase OK — таблица leads доступна
✓ OpenAI OK — model=gpt-4o-mini, ответ='ping'
✓ Playwright OK — example.com title='Example Domain'
```

Если что-то ✗ — исправить указанное и снова запустить health.py.

### 4. Полный pipeline (~20-40 минут на 30-50 лидов)

```bash
# Phase 1: парсим 2GIS — откроется видимый Chrome (так надёжнее)
python scripts/1_scrape_2gis.py --city "Алматы" --category "салон красоты" --limit 30

# Phase 2: обогащаем Instagram (~3 сек на лид)
python scripts/2_enrich_instagram.py --limit 30

# Phase 3: GPT-4o-mini генерит персонализированные офферы (~$0.001 за лид)
python scripts/3_generate_offers.py --limit 30

# Phase 4: собираем HTML-страницу с кнопками отправки
python scripts/4_build_send_page.py
```

### 5. Отправлять сообщения

Открой `data/send_page.html` двойным кликом — откроется в браузере.

Каждая строка — лид. Кнопка **📨 Send WA** открывает WhatsApp Web с уже забитым персонализированным сообщением. Тебе остаётся:
1. Проверить, что сообщение норм
2. Нажать Enter (отправить)
3. Вернуться на вкладку с send_page → автоматически помечается `status=sent`

Через ~50 отправок открой Supabase SQL Editor:
```sql
select * from public.template_stats;
```
— увидишь conversion rate по каждому шаблону A/B/C.

### Параметры запуска

| Параметр | Что делает |
|---|---|
| `--city "Алматы"` | город (Алматы/Астана/Шымкент) |
| `--category "салон красоты"` | что искать в 2GIS |
| `--limit 30` | сколько лидов парсить за один прогон |
| `--headless True` | (только для серверов) запуск без UI; на твоей машине — НЕ используй |

### Запуск разных категорий
Просто запусти scrape несколько раз:

```bash
python scripts/1_scrape_2gis.py --city "Алматы" --category "ногтевая студия" --limit 30
python scripts/1_scrape_2gis.py --city "Алматы" --category "косметология" --limit 30
python scripts/1_scrape_2gis.py --city "Астана" --category "стоматология" --limit 30
```

`upsert` идемпотентен по `id` 2GIS — дубли не создадутся.

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
