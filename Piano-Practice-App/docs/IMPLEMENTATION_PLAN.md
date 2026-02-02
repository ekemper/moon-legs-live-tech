# Piano Practice App - Implementation Plan

## Overview

A React-based piano practice application with SuperCollider integration for realistic Rhodes piano sounds. The app provides flashcard-style practice for chords, scales, and arpeggios with real-time visual feedback on a virtual keyboard.

## Architecture Overview

All architectural decisions are recorded in `CLARIFICATION_QUESTIONS.md`. Summary:

### Decided Stack

1. **Backend: FastAPI (not raw asyncio + websockets)**
   - FastAPI + Uvicorn; WebSocket endpoint (e.g. `/ws`) and optional HTTP routes
   - Lifespan: check/start SuperCollider, load lesson definitions from JSON, enumerate MIDI ports
   - Shared state in `app.state`: OSC client, MIDI port, lesson catalog, active WebSocket
   - Port 8765 for HTTP/WebSocket

2. **OSC to SuperCollider**
   - pythonosc to scsynth on port 57120
   - Backend checks if scsynth is running (e.g. OSC `/status`); if not, starts it (e.g. `sclang bootstrap.scd`)
   - Rhodes: FM Rhodes SynthDef (sccode 1-522 / Gist), velocity-sensitive only

3. **React Frontend**
   - TypeScript + Vite, WebSocket client, React Context
   - Virtual keyboard matches MIDI keyboard key count; playable with mouse/touch; note label on hover
   - Lesson display: key, name, notes, interval numbers (no key highlighting)
   - Green/red feedback immediately on key press; errors surfaced in UI

4. **MIDI**
   - User selects one device from list; one device per session
   - **Initialization workflow:** If device has no stored config, show workflow: user plays lowest note, then highest note (in succession). Derive range (low, high) and key count (high − low + 1). Save as device config (by device name/ID) in `device_configs.json`. Known devices reuse stored config.
   - No device / disconnect → surface error in UI; no auto-reconnect for MVP
   - All channels, full note range (from device config or init)

5. **Data**
   - **Persist:** Lesson definitions (`lesson_definitions.json`; intervals only). Device configurations (`device_configs.json`; device id → lowNote, highNote, keyCount). No practice history, statistics, or tracking for MVP.

6. **Platform & deployment**
   - Linux and macOS only. Local development only. System default audio; volume control in app. Target <10 ms MIDI → audio latency.

### Architecture Comparison: supercollider app vs Piano Practice App

| Component | supercollider app | Piano Practice App |
|-----------|------------------|-------------------|
| **Backend** | asyncio + websockets | **FastAPI** + Uvicorn |
| **WebSocket** | Port 8765 | Port 8765 |
| **OSC to SC** | pythonosc → 57120 | pythonosc → 57120; backend checks/starts scsynth |
| **Frontend** | React + TypeScript + Vite | Same |
| **Config** | config.py | config.py + **lesson definitions JSON** |
| **MIDI** | None | mido; **user selects device**; one per session |
| **Persistence** | N/A | **Lesson definitions** + **device configs** (JSON); no session/history |
| **Errors** | — | **Surface in UI; no graceful degradation** |

### Proposed Architecture

```
┌─────────────────┐
│   React App     │  ← Vite + TypeScript; WebSocket client (8765)
│   (Frontend)    │     Virtual keyboard (match MIDI keys; mouse/touch; label on hover)
└────────┬────────┘     Lesson display (key, name, notes, intervals); green/red feedback; errors in UI
         │ WebSocket (+ optional HTTP)
         │
┌────────▼────────┐
│ FastAPI Backend │  ← Uvicorn; lifespan (check/start SC, load lessons JSON)
│   (main.py)     │     WebSocket /ws; app.state: OSC, MIDI port, lessons, WS
└────────┬────────┘     MIDI → asyncio queue → OSC + WebSocket; validation; random lesson; next/auto-advance
         │
    ┌────┴────┐
    │         │
┌───▼───┐ ┌──▼──────────┐
│ MIDI  │ │ SuperCollider│  ← scsynth 57120; backend checks/starts if not running
│(user  │ │ FM Rhodes    │     Velocity-sensitive only; system default out; app volume control
│select)│ │ OSC:57120   │
└───────┘ └─────────────┘
```

**Key Components:**
1. **FastAPI Backend** (`backend/main.py` + modules):
   - **Lifespan:** Check scsynth (OSC `/status` to 57120); if no reply, start `sclang bootstrap.scd` (boots server, loads Rhodes). Load `lesson_definitions.json` and `device_configs.json`. Enumerate MIDI ports.
   - WebSocket on 8765; optional HTTP (health, devices, lessons). Volume: frontend sends 0–1; backend scales amp per note to SuperCollider.
   - **MIDI:** User selects device. If device has no config, run init workflow (lowest/highest note) and save to `device_configs.json`. mido → asyncio queue → OSC (note/vel) + WebSocket (note + correct/incorrect). No auto-reconnect on disconnect.
   - Lesson: random selection via `LessonNoteGenerator` (intervals + key → notes + MIDI); validation (note membership only); next button + auto-advance on complete.
   - Persist: lesson definitions + device configs only; no session/history.

2. **React Frontend** (`frontend/`):
   - WebSocket client; device list and selection; virtual keyboard (key count from backend); lesson display; error display; volume control

3. **SuperCollider** (separate process, started by backend if needed):
   - Backend checks OSC `/status` on 57120; if not running, starts `sclang bootstrap.scd` (script boots server, loads `rhodes_piano.scd`). scsynth on 57120; FM Rhodes SynthDef; receive note + velocity (and scaled amp) via OSC.

## Component Breakdown

### 1. Frontend (React App)

#### Components:
- **MainPage**: Container; device selector (list from backend); init workflow modal when new device has no config (prompt lowest then highest note)
- **VirtualKeyboard**: Matches MIDI keyboard key count (from device config); playable with mouse/touch; note label on hover; green/red on key press (immediate)
- **LessonDisplay**: Key, name, notes in chord/scale/arp, interval numbers (no key highlighting)
- **MIDIStatus**: Selected device, key count and range (from backend / device config)
- **ErrorDisplay**: All systemic errors (no device, disconnect, SC fail, backend/WS errors); no auto-reconnect — user must refresh or reconnect
- **NextLessonButton**: Skip / get next lesson; auto-advance when lesson completed
- **VolumeControl**: In-app volume; frontend sends 0–1 over WebSocket; backend scales amp when sending notes to SuperCollider

#### State:
- Current lesson; MIDI device (selected, key count); active notes; errors. No session/history state for MVP.

### 2. Backend (FastAPI)

#### Structure:
```
backend/
├── main.py              # FastAPI app, lifespan, WebSocket /ws, optional HTTP
├── config.py            # Ports, paths, defaults
├── sc_manager.py        # SuperCollider check (OSC /status), start (sclang bootstrap.scd), OSC client
├── midi_handler.py      # mido callback → asyncio.Queue; device list; open/close port
├── lesson_loader.py     # Load lesson_definitions.json at startup
├── lesson_notes.py      # LessonNoteGenerator: intervals + key → note names + MIDI
├── lesson_generator.py  # Random lesson from catalog; uses LessonNoteGenerator
├── validator.py         # Note membership only (no order rules); green/red per note
└── requirements.txt    # fastapi, uvicorn[standard], websockets, pythonosc, mido
```

#### Responsibilities:
- Lifespan: check/start SuperCollider; load lesson JSON; enumerate MIDI ports
- WebSocket: device select, next lesson, volume; send MIDI events (note, velocity, correct/incorrect), lesson, errors
- MIDI: one selected device; mido → queue → OSC (note/vel) + validation → WebSocket
- No practice session or history persistence

#### WebSocket Message Types

**React → Backend:**
- `midi_device_select` — `{ "type": "midi_device_select", "deviceId": "..." }` (or device name/index)
- `next_lesson` — `{ "type": "next_lesson" }` (skip / get next)
- `set_volume` — `{ "type": "set_volume", "value": 0.8 }` (0–1, if volume over WS)

**Backend → React:**
- `lesson` — current lesson (key, name, notes, intervals, type, historical blurb)
- `midi_note` — `{ "type": "midi_note", "note": 60, "velocity": 127, "on": true, "isCorrect": true }` (immediate green/red)
- `midi_devices` — list of available devices (on connect or request)
- `midi_device` — selected device, key count (after select or on connect)
- `error` — `{ "type": "error", "message": "..." }` (all systemic errors)

On connect: backend sends current lesson, device list, and (if device selected) device/key count. Optional: separate HTTP routes for `GET /api/midi/devices`, `GET /api/lessons` for initial load.

### 3. SuperCollider Integration (Decided)

- **Communication:** OSC to scsynth on port 57120.
- **Lifecycle:** Backend checks if scsynth is running (e.g. send OSC `/status`, wait for reply). If not, start it (e.g. `sclang bootstrap.scd` that boots server and loads Rhodes synthdef).
- **Sound:** FM Rhodes SynthDef from sccode.org 1-522 / Gist. Args: `note` (MIDI), `gate`, `vel` (0–1). Velocity-sensitive only.
- **Audio:** System default output. Volume control in app (see REMAINING_QUESTIONS.md for how to drive from UI).

### 4. MIDI Input Handler

- **Connection:** User selects one device from list (from backend enumeration). Only one device per session.
- **Flow:** mido uses callbacks/threads; push messages to `asyncio.Queue` via `loop.call_soon_threadsafe()`. Background task consumes queue: send note/velocity to OSC (SuperCollider), run validation against current lesson, send `midi_note` (with `isCorrect`) to WebSocket.
- **Disconnect / no device:** Surface error to UI; do not graceful-degrade.
- **Channels / range:** All MIDI channels and full note range supported by device. Key count: auto-detect (min 32); see REMAINING_QUESTIONS.md for heuristic.

### 5. Data Models and lesson_definitions schema

**Stored in JSON (intervals only):** One file `lesson_definitions.json` with top-level keys `chords`, `scales`, `arpeggios`. Each entry: `id`, `name`, `intervals` (semitones from root), `historicalBlurb`. Key/root is not stored; it is chosen at random when generating a lesson. See **`IMPLEMENTATION.md`** for the full schema and examples.

**Computed at lesson generation:** From a lesson definition (intervals) + key + octave, the backend computes note names (A, B, C, D, sharps/flats) and MIDI notes using **`LessonNoteGenerator`** in `backend/lesson_notes.py`. That class implements interval rules so every note in the chord/scale/arpeggio can be determined for any key in any octave.

**Current lesson in memory (not persisted):** type, key, lesson name, intervals, note names, MIDI notes, historical blurb. Validation: note membership only (green if in lesson, red if not).

No session/history persistence for MVP. Lesson definitions + device configs only in JSON.

### 6. Data Persistence (Decided)

- **Persist:** (1) Lesson definitions (`data/lesson_definitions.json`: chords, scales, arpeggios; intervals only + historicalBlurb). (2) Device configurations (`data/device_configs.json` or similar: device id → lowNote, highNote, keyCount). Loaded at backend startup.
- **Do not persist for MVP:** Practice sessions, attempts, success/failure rates, progress, statistics. Defer to v2.

## Technical Stack

### Frontend
- React 18, TypeScript, Vite. WebSocket (native). React Context. CSS Modules (or chosen).
- Virtual keyboard: match MIDI key count; mouse/touch; note label on hover. Green/red on key press.

### Backend
- **FastAPI** + Uvicorn. Python 3.9+.
- WebSocket (port 8765); optional HTTP. Lifespan for SuperCollider and lesson load.
- **mido** (MIDI; callback → asyncio queue). **pythonosc** (OSC to scsynth 57120).
- Linux and macOS only. Local development only.

### Audio
- SuperCollider (scsynth 57120). Backend checks OSC `/status`; if not running, starts `sclang bootstrap.scd`. System default output. In-app volume: frontend sends 0–1; backend scales amp to SC.
- Latency target: <10 ms MIDI → audio.

## Implementation Phases

### Phase 1: MVP Core
1. FastAPI app with lifespan (SuperCollider check/start, load lesson JSON)
2. WebSocket endpoint; MIDI device list and selection; mido → queue → OSC + WebSocket
3. FM Rhodes SynthDef (sccode 1-522); OSC note/velocity
4. React app: device selector, virtual keyboard (match key count; mouse/touch; label on hover), lesson display (key, name, notes, intervals), error display
5. Lesson definitions JSON (chords, scales, arpeggios; historical blurbs); random lesson; next button; auto-advance on complete

### Phase 2: Validation & Feedback
1. Validation: note membership only (green/red per note; no order rules)
2. Green/red feedback immediately on key press
3. Volume control in app (implementation per REMAINING_QUESTIONS.md)
4. All systemic errors surfaced in UI; no graceful degradation

### Phase 3: Content & Polish
1. Deep research: chord/scale/arpeggio types; historical blurbs per lesson
2. MIDI key count auto-detect heuristic (see REMAINING_QUESTIONS.md)
3. Latency tuning (target <10 ms MIDI → audio)
4. No practice history/stats/tracking (v2)

## Decided vs Open

All decisions from `CLARIFICATION_QUESTIONS.md` and `REMAINING_QUESTIONS.md` are reflected in this plan. See those files and `IMPLEMENTATION.md` for schema and class contracts. (volume control, MIDI key-count heuristic, scale “in order” start note, lesson JSON schema, etc.).

## MVP Scope (from Q20)

**In scope for MVP:**
- MIDI keyboard connection (user selects from list; one per session)
- SuperCollider audio (check/start; FM Rhodes; velocity-sensitive)
- Virtual keyboard (match MIDI keys; mouse/touch; label on hover)
- Green/red note feedback (immediately on key press)
- Random lesson generation (chords, scales, arpeggios)
- Error handling (surface all systemic errors in UI; no graceful degradation)
- Lesson definitions + device configs in JSON (no session/history persistence)
- Volume control in app (frontend sends 0–1; backend scales amp to SC)
- Next-lesson button + auto-advance on complete
- No auto-reconnect for WebSocket or MIDI; show error only

**Deferred to v2:** Practice history, statistics, tracking. No fixed timeline; proceed as needed.

## Reusable Patterns

- **supercollider app** (`/Users/edward.kemper/dev/supercollider`): React WebSocket client pattern, OSC message patterns, config structure — adapt for FastAPI (we use FastAPI + WebSocket, not raw `websockets.serve()`).
- **FastAPI:** [WebSockets](https://fastapi.tiangolo.com/advanced/websockets), [Lifespan](https://fastapi.tiangolo.com/advanced/events). Use lifespan for SuperCollider and lesson load; `app.state` for shared state.
- **mido + asyncio:** Callback pushes to `asyncio.Queue` via `loop.call_soon_threadsafe()`; consume in background task.

## Next Steps

1. All remaining questions are decided; see `REMAINING_QUESTIONS.md`.
2. Set up project structure (backend: FastAPI, main.py, lifespan; frontend: React + Vite).
3. Implement Phase 1 (MVP Core): SuperCollider check/start, lesson JSON, WebSocket, MIDI → queue → OSC + WS, virtual keyboard, lesson display, device selection, errors in UI.
4. Implement Phase 2 (validation, green/red, volume, error surfacing).
5. Implement Phase 3 (lesson content, device init workflow + device_configs, latency tuning).
6. Test end-to-end: MIDI → audio (<10 ms target) and visual feedback.
