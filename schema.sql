create table if not exists public.entries (
  id bigint generated always as identity primary key,
  update_id bigint unique,
  trader_id bigint not null,
  kind text not null check (kind in ('sale','purchase','expense')),
  item text,
  qty numeric,
  amount numeric not null check (amount > 0),
  note text,
  raw_text text,
  receipt_path text,
  created_at timestamptz not null default now()
);
create index if not exists entries_trader_created_idx on public.entries (trader_id, created_at desc);
alter table public.entries enable row level security;
