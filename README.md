# Roamwise · Personalized Travel Itinerary Planner

React + Vite frontend, FastAPI backend, Supabase Auth/Postgres, and Groq itinerary generation.

## Run locally

Requirements: Node 20.19+ and Python 3.11+. Hosted AI inference does not require TensorFlow, CUDA, local model files, or loading three models into RAM.

```sh
npm install
npm run dev
```

Without frontend environment variables, the app runs in **demo mode**. It generates generic planning outlines, stores trips in this browser, and supports editing, regeneration, favorites, search, deletion, and JSON export. Demo outlines are not live AI recommendations or verified travel routes. Destination photos use Unsplash image URLs; a separate Unsplash API integration is not required for these editorial images.

For cloud mode, copy `.env.example` to `.env` and set the API URL, Supabase project URL, and Supabase public anon key. These frontend values are public by design. Never put a Groq key or Supabase service-role key in a `VITE_` variable. Restart Vite after configuration changes.

```sh
python3 -m venv .venv
.venv/bin/python -m pip install -r backend/requirements.txt
cd backend
cp .env.example .env
../.venv/bin/uvicorn app.main:app --reload
```

Populate `backend/.env` with Supabase URL/public anon key, Groq key, model ID, and allowed frontend origins. Run `supabase/schema.sql` in the Supabase SQL editor. Enable email sign-in and add your frontend origin to Auth redirect URLs. Use the profile button to sign in with an email link. Cloud API requests require a valid Supabase session. Local guest trips are separate from account trips; sign-in does not automatically upload them.

## Architecture

```text
React / Vite → FastAPI → Groq Chat Completions
     ↓            ↓
Supabase Auth → Supabase Postgres + per-owner RLS
```

The backend verifies bearer tokens through Supabase Auth and forwards the user token to PostgREST. RLS enforces ownership on reads and writes. No service-role credentials are used. AI JSON output is validated with Pydantic, including dates, sequential days, cost types, activity order and overlapping time slots. Provider errors are surfaced to the user; cloud mode never silently substitutes demo output. Suggestions geographically group activities through prompting, but there is no live routing engine, price feed, booking system, or guarantee of route optimality. Costs are for the entire group, excluding flights; the UI flags budget overruns.

## API

- `GET /health` — configuration readiness
- `POST /generate` — preferences to itinerary
- `POST /regenerate` — preferences, day number and current day to replacement day
- `GET /trips` and `GET /trips/{id}` — owner-scoped trips
- `PUT /trips/{id}` — validate and save a complete itinerary
- `DELETE /trips/{id}` — delete an owned itinerary

Interactive API documentation: `http://localhost:8000/docs`.

## Verification

```sh
npm run build
cd backend
../.venv/bin/python -m pytest -q
```

Live provider/database checks require your configured accounts. The database migration should also be tested with two users: user B must not be able to select, update or delete user A's trip. Frontend guest storage is local to one browser and is not suitable for sensitive travel details on shared devices.

## Deployment

- **Frontend:** Vercel can import this directory using `vercel.json`. Configure `VITE_API_URL`, `VITE_SUPABASE_URL`, and `VITE_SUPABASE_ANON_KEY` before building.
- **Backend:** deploy `render.yaml` as a Render Blueprint, set the environment values, and set `ALLOWED_ORIGINS` to the exact deployed frontend origins (comma-separated).
- **Supabase:** apply the migration and configure production email redirect URLs.
- **Sites:** the static React build can be published as a private demo. Sites runs Workers and does not host this Python backend. Configure a separately deployed FastAPI endpoint and rebuild to enable cloud mode.

Real-time shared editing, membership/invites and conflict resolution are not implemented; a group organizer can plan for up to 20 travelers and export the plan. Editing preferences currently creates a new trip through the builder. Before opening to a broad public audience, add account quotas/rate limiting and monitoring for paid AI requests.

Provider references: [Groq JSON output](https://console.groq.com/docs/structured-outputs), [Supabase RLS](https://supabase.com/docs/guides/database/postgres/row-level-security).
