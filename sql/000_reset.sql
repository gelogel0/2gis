-- 000_reset.sql
-- Запустить ОДИН РАЗ если у тебя уже есть старая таблица leads (без колонки city и т.п.)
-- Удалит таблицы и view; данные внутри потеряются.
-- После этого запусти 001_init_schema.sql.

drop view  if exists public.template_stats cascade;
drop table if exists public.outreach_log    cascade;
drop table if exists public.leads           cascade;
