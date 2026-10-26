-- Run in the Supabase SQL editor before using cloud trip storage.
create table if not exists public.trips (
 id uuid primary key,
 user_id uuid not null references auth.users(id) on delete cascade,
 data jsonb not null,
 created_at timestamptz not null default now()
);
create index if not exists trips_user_created_idx on public.trips(user_id, created_at desc);
alter table public.trips enable row level security;
revoke all on public.trips from anon;
grant select, insert, update, delete on public.trips to authenticated;
drop policy if exists "Owners read trips" on public.trips;
create policy "Owners read trips" on public.trips for select to authenticated using ((select auth.uid()) = user_id);
drop policy if exists "Owners create trips" on public.trips;
create policy "Owners create trips" on public.trips for insert to authenticated with check ((select auth.uid()) = user_id);
drop policy if exists "Owners update trips" on public.trips;
create policy "Owners update trips" on public.trips for update to authenticated using ((select auth.uid()) = user_id) with check ((select auth.uid()) = user_id);
drop policy if exists "Owners delete trips" on public.trips;
create policy "Owners delete trips" on public.trips for delete to authenticated using ((select auth.uid()) = user_id);
