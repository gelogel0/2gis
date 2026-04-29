-- LeadHunter MVP — Supabase schema
-- Запустить один раз через Supabase Dashboard → SQL Editor

create extension if not exists "uuid-ossp";

-- Leads table
create table if not exists public.leads (
    id              text primary key,                    -- 2GIS org ID (или synthetic)
    name            text not null,
    category        text,
    address         text,
    city            text,
    main_phone      text,                                 -- лучший номер (mobile/whatsapp)
    all_phones      text[],                               -- все найденные номера
    instagram       text,                                 -- @handle (без @)
    website         text,
    rating          numeric(3,2),
    reviews_count   integer,
    raw_2gis        jsonb,                                -- сырой JSON ответа 2gis
    ig_bio          text,
    ig_followers    integer,
    ig_recent_posts jsonb,                                -- [{caption, url, likes}]
    ai_analysis     jsonb,                                -- {pains, opportunities, hooks}
    template_id     text,                                 -- 'A' / 'B' / 'C'
    generated_offer text,                                 -- финальное сообщение
    wa_link         text,                                 -- wa.me/...?text=...
    status          text default 'new'                    -- new / enriched / generated / sent / replied / closed / dead
        check (status in ('new','enriched','generated','sent','replied','closed','dead')),
    sent_at         timestamptz,
    replied_at      timestamptz,
    notes           text,
    created_at      timestamptz default now(),
    updated_at      timestamptz default now()
);

create index if not exists idx_leads_status on public.leads(status);
create index if not exists idx_leads_category on public.leads(category);
create index if not exists idx_leads_city on public.leads(city);
create index if not exists idx_leads_template on public.leads(template_id);

-- Auto-update updated_at
create or replace function public.set_updated_at()
returns trigger as $$
begin
    new.updated_at = now();
    return new;
end;
$$ language plpgsql;

drop trigger if exists trg_leads_updated_at on public.leads;
create trigger trg_leads_updated_at
    before update on public.leads
    for each row execute function public.set_updated_at();

-- Outreach log (история отправок для A/B аналитики)
create table if not exists public.outreach_log (
    id              uuid default uuid_generate_v4() primary key,
    lead_id         text references public.leads(id) on delete cascade,
    template_id     text not null,
    message         text not null,
    sent_at         timestamptz default now(),
    channel         text default 'whatsapp'              -- whatsapp / instagram / email
);

create index if not exists idx_outreach_lead on public.outreach_log(lead_id);
create index if not exists idx_outreach_template on public.outreach_log(template_id);

-- View: A/B conversion stats
create or replace view public.template_stats as
select
    template_id,
    count(*) as total_sent,
    count(*) filter (where status = 'replied') as replies,
    count(*) filter (where status = 'closed') as closes,
    round(100.0 * count(*) filter (where status = 'replied') / nullif(count(*), 0), 2) as reply_rate_pct,
    round(100.0 * count(*) filter (where status = 'closed') / nullif(count(*), 0), 2) as close_rate_pct
from public.leads
where status in ('sent','replied','closed')
group by template_id
order by reply_rate_pct desc nulls last;

-- RLS: для MVP — отключено, но в проде включить и сделать service-role-only
alter table public.leads disable row level security;
alter table public.outreach_log disable row level security;

-- Comments
comment on table public.leads is 'B2B leads parsed from 2GIS, enriched with Instagram, with AI-generated offers';
comment on column public.leads.template_id is 'Which outreach template was selected: A, B, or C';
comment on column public.leads.status is 'Lead lifecycle: new -> enriched -> generated -> sent -> replied/dead -> closed';
