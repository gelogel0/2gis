-- 002_disable_rls.sql
-- Отключаем RLS на таблицах для MVP (репо приватный, ты единственный пользователь).
-- Это нужно чтобы:
--  - HTML send-page (использует anon key) могла обновлять status='sent'
--  - service-role-скрипты работали без необходимости описывать policies
--
-- ⚠️ ЕСЛИ В БУДУЩЕМ ОТКРОЕШЬ DASHBOARD ПУБЛИЧНО — вернуть RLS + написать policies.
--
-- Запустить через: Supabase Dashboard → SQL Editor → New query → вставить → Run

alter table public.leads disable row level security;
alter table public.outreach_log disable row level security;

-- Для быстрой проверки — должно быть rowsecurity = false
select schemaname, tablename, rowsecurity
from pg_tables
where schemaname = 'public' and tablename in ('leads', 'outreach_log');
