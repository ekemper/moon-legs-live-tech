# Piano Practice App

React + FastAPI app for practicing chords, scales, and arpeggios with a MIDI keyboard and Rhodes piano sound (SuperCollider). See `CLARIFICATION_QUESTIONS.md` and `IMPLEMENTATION_PLAN.md` for scope and architecture.

## Requirements

- **Python 3.9+** (backend)
- **Node 18+** (frontend)
- **SuperCollider** (sclang + scsynth) for Rhodes sound
- **MIDI keyboard** (optional for init; use virtual keyboard without)

## Quick start

### 1. Backend

```bash
cd Piano-Practice-App
python -m venv .venv
source .venv/bin/activate   # or .venv\Scripts\activate on Windows
pip install -r backend/requirements.txt
# Run from repo root so backend can import as backend.*
cd ..
python -m uvicorn Piano-Practice-App.backend.main:app --reload --host 0.0.0.0 --port 8765
```

Or from `Piano-Practice-App`:

```bash
cd Piano-Practice-App
pip install -r backend/requirements.txt
PYTHONPATH=. python -m uvicorn backend.main:app --reload --host 0.0.0.0 --port 8765
```

### 2. SuperCollider (optional; for audio)

If you want Rhodes sound, start SuperCollider first:

```bash
cd Piano-Practice-App/sc_programs
sclang bootstrap.scd
```

Leave it running. The backend will try to start it automatically if not running (when the bootstrap script path exists).

### 3. Frontend

```bash
cd Piano-Practice-App/frontend
npm install
npm run dev
```

Open http://localhost:5173. Select a MIDI device (or use the virtual keyboard). Use "Next lesson" to get a new chord/scale/arpeggio.

**Rebuild on change:** The frontend is **not** served by the Python app. Locally, Vite (`npm run dev`) serves the app and has **HMR** (hot module replacement), so edits to the frontend rebuild and refresh automatically. In Docker, the frontend is served by **nginx** (a separate container) from a one-time build; there is no live reload unless you use the [Docker dev setup](#docker-dev-with-live-frontend) below.

## Docker

SuperCollider still runs on the host. Start scsynth first, then run the stack:

```bash
cd Piano-Practice-App
# On host: start SuperCollider (optional, for Rhodes sound)
# cd sc_programs && sclang bootstrap.scd

docker compose up --build
```

- **Frontend:** http://localhost (port 80)
- **Backend:** http://localhost:8765 (API/health; frontend proxies `/api` and `/ws` through nginx)

The backend uses `SC_HOST=host.docker.internal` so it can reach scsynth on the host. On Linux, `extra_hosts: host.docker.internal:host-gateway` is set in `docker-compose.yml` so that name resolves. MIDI hardware is not visible inside the backend container; use the in-app virtual keyboard when running with Docker.

Data is persisted via the `./data` bind mount so `device_configs.json` and `lesson_definitions.json` are kept on the host.

### Docker dev with live frontend

To run the full stack in Docker and have the frontend **rebuild on change** (HMR), use the dev override:

```bash
cd Piano-Practice-App
docker compose -f docker-compose.yml -f docker-compose.dev.yml up --build
```

- **Frontend:** http://localhost:5173 (Vite dev server; edits to `frontend/` trigger rebuild and HMR).
- **Backend:** unchanged; frontend container proxies `/api` and `/ws` to the backend service.
- Start SuperCollider on the host first.
- **HMR:** Open the app at **http://localhost:5173** (not 127.0.0.1 or the container IP) so the HMR WebSocket connects correctly. If HMR still doesn’t update, ensure you’re using the dev override (`docker-compose.dev.yml`) and that port 5173 is mapped.

## Project layout

- `backend/` — FastAPI app, MIDI, OSC, lessons
- `frontend/` — React + Vite + TypeScript
- `sc_programs/` — SuperCollider bootstrap and Rhodes SynthDef
- `data/` — `lesson_definitions.json`, `device_configs.json`
- `IMPLEMENTATION_PLAN.md`, `ARCHITECTURE_REFERENCE.md`, `IMPLEMENTATION.md` — design and implementation details

## Device setup

On first use with a new MIDI keyboard, the app will prompt you to play the **lowest** then **highest** note so it can store the key count and range. After that, the device is recognized automatically.
