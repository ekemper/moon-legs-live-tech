# Architecture Reference - Piano Practice App

## Overview

Architecture is driven by `CLARIFICATION_QUESTIONS.md`. This document summarizes the decided patterns and where to reference the supercollider app for inspiration (adapted to FastAPI and piano-practice logic).

## Decided Architecture

```
React Frontend (TypeScript + Vite)
    ↕ WebSocket (port 8765) + optional HTTP
FastAPI Backend (Uvicorn)
    ↕ OSC (port 57120)
SuperCollider (scsynth; backend checks and starts if not running)
```

- **Platform:** Linux and macOS only. Local development only. No special Windows support.
- **Persistence:** Lesson definitions (`lesson_definitions.json`; intervals only) and device configurations (`device_configs.json`; device id → lowNote, highNote, keyCount). No practice history, statistics, or tracking for MVP.
- **Audio:** System default output. Volume control: frontend sends 0–1 over WebSocket; backend scales amplitude when sending notes to SuperCollider.
- **Errors:** No graceful degradation. Systemic errors (SuperCollider, MIDI, backend, WebSocket) are surfaced in the UI with clear messages.
- **Latency:** Target <10 ms for MIDI key press → audio output; visual feedback can be looser.

## Backend: FastAPI

- **Framework:** FastAPI + Uvicorn. Not raw asyncio + websockets.
- **Lifespan:** Use `@asynccontextmanager` passed to `FastAPI(lifespan=...)`:
  - **Startup:** Check if SuperCollider (scsynth) is running on 57120; if not, start it (e.g. via `sclang` bootstrap script that boots server and loads Rhodes synthdef). Load lesson definitions from JSON. Optionally enumerate MIDI ports for device list.
  - **Shutdown:** Close MIDI port; optional SuperCollider teardown.
- **Shared state:** Store in `app.state`: OSC client, MIDI port (or None), lesson catalog, active WebSocket (if single client). WebSocket handler uses `websocket.app.state`.
- **HTTP (optional):** e.g. `GET /health`, `GET /api/midi/devices`, `GET /api/lessons` if useful; otherwise all over WebSocket.
- **WebSocket:** Single endpoint (e.g. `/ws`). Accept connection, then loop: receive JSON (e.g. device select, next lesson, volume), send JSON (MIDI events, lesson, errors). Catch `WebSocketDisconnect` and remove connection.
- **MIDI + asyncio:** mido is callback/thread-based. Use a callback that pushes messages to an `asyncio.Queue` via `loop.call_soon_threadsafe()`; a background task consumes the queue and forwards to OSC and WebSocket. Run mido input in a thread or use mido’s callback API.

**Dependencies:** `fastapi`, `uvicorn[standard]`, `websockets`, `pythonosc`, `mido`.

## SuperCollider

- **Communication:** OSC to scsynth on port 57120 (standard).
- **Lifecycle:** Backend sends OSC `/status` to port 57120; if no reply within a timeout, assume scsynth is not running. Start by running `sclang bootstrap.scd`; the script boots the default server (port 57120) and loads the Rhodes SynthDef (e.g. from `rhodes_piano.scd`). Document script path and assumptions (SuperCollider installed, `sclang` on PATH).
- **Rhodes sound:** FM Rhodes SynthDef from sccode.org 1-522 / GitHub Gist (snappizz). SynthDef name `\rhodes` with args: `note` (MIDI), `gate`, `vel` (velocity 0–1). Velocity-sensitive only; no other user-configurable parameters.
- **References:** [sccode.org 1-522](https://sccode.org/1-522), [Gist](https://gist.github.com/mbutz/dc11a619b8e2f471bb11a3b89b899896).

## MIDI

- **Connection:** User selects one device from a list. Only one MIDI device per session. No auto-connect to first device.
- **Initialization workflow:** When a device is plugged in, the app checks for a stored configuration (by device name/ID). If none: show workflow; user plays **lowest note**, then **highest note** (in succession). Derive MIDI range (low, high) and key count (high − low + 1). Save as device config in `device_configs.json` and reuse for that device next time.
- **If no device / disconnect:** Surface error in UI. No graceful degradation. No auto-reconnect for MVP (user must refresh or reconnect / re-select device).
- **Channels / range:** Listen on all MIDI channels and full note range (from device config or init).

## Lesson System

- **Types:** Chords, scales, arpeggios (all three for MVP).
- **Content:** Deep research; include as many chord/scale/arpeggio types as practical. Each lesson includes a short historical blurb.
- **Validation:** No order or timing rules. Feedback is by note membership only: green if the note is in the lesson, red if not.
- **Generation:** Random for now. Next-lesson button; it also acts as skip. Auto-advance when lesson is completed.
- **UI:** No “New Lesson” button. Lesson display: key, name, notes in chord/scale/arp, interval numbers. Do not highlight expected notes on the keyboard.

## Frontend (React)

- **Stack:** React 18, TypeScript, Vite. WebSocket client (native API). State: React Context. Styling: CSS Modules (or as chosen).
- **Virtual keyboard:** Matches MIDI keyboard key count (from backend). Playable with mouse/touch. Note label on hover only.
- **Visual feedback:** Notes turn green/red immediately when pressed (correct vs incorrect). Don’t worry about order/timing for incorrect indication for MVP.
- **Volume:** In-app volume control; frontend sends 0–1 over WebSocket; backend scales amp when sending notes to SuperCollider.

## Data

- **Lesson definitions:** One JSON file (`lesson_definitions.json`) with top-level keys `chords`, `scales`, `arpeggios`. Each entry stores **intervals only** (id, name, intervals, historicalBlurb). Key/root is chosen at random; note names and MIDI are computed on the fly by **`LessonNoteGenerator`** in `backend/lesson_notes.py` from intervals + key + octave. See `IMPLEMENTATION.md` for schema and class contract.
- **Device configs:** One JSON file (`device_configs.json`): device identifier → lowNote, highNote, keyCount. Loaded/saved at runtime for init workflow.
- **Session:** No persistence of practice sessions, attempts, or statistics for MVP.

## Ports

- **Backend HTTP/WS:** 8765 (configurable).
- **OSC to SuperCollider:** 57120.
- **Frontend dev:** 5173 (Vite default).

## Project Structure (Target)

```
piano-practice-app/
├── backend/
│   ├── main.py              # FastAPI app, lifespan, WebSocket route
│   ├── midi_handler.py       # mido + asyncio queue bridge
│   ├── sc_manager.py         # SuperCollider check/start, OSC client
│   ├── lesson_loader.py      # Load lesson_definitions.json
│   ├── lesson_notes.py       # LessonNoteGenerator: intervals + key → notes + MIDI
│   ├── lesson_generator.py   # Random lesson; uses LessonNoteGenerator
│   ├── validator.py          # Note membership only (green/red)
│   ├── config.py            # Ports, paths
│   └── requirements.txt
├── frontend/                 # React + TypeScript + Vite
│   └── src/
│       ├── App.tsx
│       ├── contexts/        # WebSocket, app state
│       └── components/       # VirtualKeyboard, LessonDisplay, etc.
├── sc_programs/             # SuperCollider
│   ├── bootstrap.scd        # Boot server, load synthdefs
│   └── rhodes_piano.scd     # FM Rhodes SynthDef (from sccode 1-522)
└── data/
    ├── lesson_definitions.json   # chords, scales, arpeggios (intervals only)
    └── device_configs.json       # device id → lowNote, highNote, keyCount
```

## References

- **Clarifications:** `CLARIFICATION_QUESTIONS.md` (source of truth)
- **Decisions (all resolved):** `REMAINING_QUESTIONS.md`; implementation detail: `IMPLEMENTATION.md`
- **SuperCollider app (patterns only):** `/Users/edward.kemper/dev/supercollider` — WebSocket message patterns, OSC usage; backend is FastAPI here, not raw websockets
- **FastAPI:** [WebSockets](https://fastapi.tiangolo.com/advanced/websockets), [Lifespan](https://fastapi.tiangolo.com/advanced/events)
- **SuperCollider:** [Server Command Reference](https://doc.sccode.org/Reference/Server-Command-Reference.html), [sccode 1-522](https://sccode.org/1-522)
