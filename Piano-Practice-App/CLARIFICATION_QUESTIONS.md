# Piano Practice App - Clarification Questions

Please answer these questions to help finalize the implementation plan. Your answers will guide architectural decisions and implementation details.

## SuperCollider Integration

### Q1: SuperCollider Setup & Communication
- **A)** Do you already have SuperCollider installed and configured?
  - **Answer:** Yes, SuperCollider is already installed.
- **B)** Based on the supercollider app architecture, we'll use **OSC via scsynth (port 57120)** - this is the standard approach. Do you want to:
  - Option 1: Backend starts SuperCollider automatically (`sclang script.scd`)
  - Option 2: User manually starts SuperCollider before running the app
  - Option 3: Backend checks if SuperCollider is running, starts if not
  - **Answer:** Option 3 — backend checks if SuperCollider is running; if not, start it.
- **C)** Do you have a Rhodes piano synthdef already, or should we create one? (The supercollider app has examples we can reference)
  - **Answer:** No existing Rhodes synthdef. Use a standard Rhodes sound (see Rhodes sound source below).

### Q2: Rhodes Piano Sound
- **A)** Do you have a specific SuperCollider patch/synthdef for Rhodes piano, or should we create one?
  - **Answer:** Use the FM Rhodes from Q1 (sccode.org 1-522 / gist).
- **B)** What characteristics are most important?
  - Realism (sampled vs synthesized)
  - Low latency
  - CPU efficiency
  - **Answer:** Real-sounding Rhodes and low latency (practicing). CPU efficiency not a priority for now.
- **C)** Should the sound be configurable (brightness, velocity sensitivity, etc.) or fixed?
  - **Answer:** Velocity-sensitive only. No other parameters configurable.

## MIDI Device Handling

### Q3: MIDI Device Connection
- **A)** Should the app automatically connect to the first available MIDI device on startup?
- **B)** Or should users manually select from a list of available devices?
  - **Answer:** User selects from a list of available devices.
- **C)** What should happen if:
  - No MIDI device is connected?
  - MIDI device disconnects during use?
  - Multiple MIDI devices are connected?
  - **Answer:** No device connected → throw an error and surface it so the user knows. Only one MIDI device per session; if the device disconnects during use, throw an error so the user has visibility.

### Q4: MIDI Keyboard Detection
- **A)** How should we determine the number of keys on the connected keyboard?
  - Auto-detect from MIDI device name/manufacturer?
  - User configuration?
  - Assume standard sizes (25, 49, 61, 88 keys)?
  - **Answer:** Auto-detect.
- **B)** What's the minimum number of keys you expect? (affects lesson difficulty)
  - **Answer:** 32.

### Q5: MIDI Channel & Range
- **A)** Should we listen to all MIDI channels or a specific channel?
  - **Answer:** Listen on all MIDI channels supported by the device.
- **B)** What MIDI note range should we support? (e.g., C1-C8, or full 0-127 range?)
  - **Answer:** Entire note range supported by the device.

## Lesson System

### Q6: Lesson Types & Difficulty
- **A)** For MVP, which lesson types are essential?
  - [ ] Chords only
  - [ ] Scales only  
  - [ ] Arpeggios only
  - [ ] All three types
  - **Answer:** All three (chords, scales, arpeggios).
- **B)** What chord/scale/arpeggio types should be included?
  - Major/minor only?
  - Include diminished, augmented, suspended?
  - Include modes (Dorian, Mixolydian, etc.)?
  - Include jazz chords (7ths, 9ths, etc.)?
  - **Answer:** Do deep research and include as many as possible; for each lesson include a historical blurb about that chord/scale/arp. 

### Q7: Lesson Generation
- **A)** Should lessons be:
  - Completely random?
  - Weighted by difficulty?
  - Sequential (master one before moving to next)?
  - **Answer:** For now, choose lessons at random.
- **B)** Should there be a "next lesson" button, or auto-advance when completed?
  - **Answer:** Yes — need a next-lesson button.
- **C)** Should users be able to skip lessons?
  - **Answer:** Yes — the next button allows the user to skip.

### Q8: Lesson Validation Logic
- **A)** For **chords**: How strict should validation be?
  - Option 1: Exact match - must play exactly the correct notes, no extras
  - Option 2: Inclusive - correct notes must be present, extras allowed
  - Option 3: Order matters - must play notes in specific order
  - **Answer:** Exact match — must play exactly the correct notes (no extras).
- **B)** For **scales**: 
  - Must play all notes in order?
  - Can start from any note in the scale?
  - Timing requirements (must be sequential, or can overlap)?
  - **Answer:** Must play all notes in order.
- **C)** For **arpeggios**:
  - Must play notes in ascending/descending order?
  - Timing requirements (how fast between notes)?
  - Can notes overlap or must be separate?
  - **Answer:** Must play the correct notes in any order.

### Q9: Visual Feedback Timing
- **A)** Should notes turn green/red:
  - Immediately when pressed?
  - Only after all notes are played?
  - Based on validation against current lesson?
  - **Answer:** Immediately when pressed.
- **B)** Should incorrect notes show red:
  - Only if they're not in the lesson?
  - Or if they're in the lesson but wrong timing/order?
  - **Answer:** Don't worry about the order of the notes right now.  

## User Interface

### Q10: Virtual Keyboard Display
- **A)** Should the virtual keyboard:
  - Match the MIDI keyboard exactly (same number of keys)?
  - Show full 88-key piano range?
  - Show a fixed range (e.g., C2-C6)?
  - **Answer:** Match the MIDI keyboard exactly.
- **B)** Should the virtual keyboard be:
  - Playable with mouse/touch (for testing without MIDI)?
  - Visual-only (MIDI input only)?
  - **Answer:** Playable with mouse/touch.
- **C)** How should keys be labeled?
  - Note names (C, D, E, etc.)?
  - MIDI note numbers?
  - No labels?
  - **Answer:** Show the note label on hover.


### Q11: Lesson Display
- **A)** How should the current lesson be displayed?
  - Text only ("C Major Chord")?
  - Visual notation (staff notation)?
  - Both?
  - **Answer:** Describe the lesson by key, name, the notes in the chord/scale/arp, and the interval numbers.
- **B)** Should the lesson show:
  - Expected notes visually highlighted on keyboard?
  - Note names list?
  - Both?
  - **Answer:** Do not highlight keys on the keyboard. Show the notes, the key, and the numbers only.

### Q12: Practice Session UI
- **A)** Should there be:
  - A "New Lesson" button?
  - Auto-advance to next lesson?
  - Practice history/session view?
  - **Answer:** No "New Lesson" button. Yes, auto-advance to next lesson. No practice history/session view for MVP — future work.
- **B)** Should users see:
  - Success/failure feedback per attempt?
  - Overall statistics (accuracy, time spent)?
  - Progress tracking?
  - **Answer:** None of these for MVP. Defer practice history, training statistics, and tracking to future work.

## Data & Persistence

### Q13: Data Storage
- **A)** For MVP, is persistence required, or can we skip it initially?
  - **Answer:** No persistence for practice sessions yet — leave for future work.
- **B)** If yes, what data should be stored?
  - [ ] Practice sessions (date, duration)
  - [ ] Individual lesson attempts
  - [ ] Success/failure rates
  - [ ] User progress/statistics
  - **Answer:** None of the above for MVP. The only persistent data is lesson definitions (chord/scale/arp catalog).
- **C)** Storage preference:
  - JSON files (simple, easy to inspect)
  - SQLite database (more structured)
  - No storage (session-only)
  - **Answer:** Lesson definitions stored in JSON.

### Q14: Lesson History
- **A)** Should users be able to:
  - View past practice sessions?
  - See which lessons they've completed?
  - Retry specific lessons?
  - **Answer:** No — none of these for MVP.
- **B)** Should there be analytics/statistics?
  - Most practiced chords/scales?
  - Accuracy over time?
  - Practice streaks?
  - **Answer:** No — none for MVP.

## Technical Preferences

### Q15: Backend Language
- **A)** Based on the supercollider app architecture, we'll use **Python** with:
  - ✅ Python backend
  - ✅ pythonosc for SuperCollider (port 57120)
  - ✅ mido for MIDI
- **B)** Use **FastAPI** as the backend framework (not raw asyncio). See "FastAPI usage" below.

### Q16: Development Environment
- **A)** Target platform:
  - macOS only?
  - Cross-platform (Windows, Linux)?
  - **Answer:** Linux and macOS only (no special configuration for Windows).
- **B)** Deployment:
  - Local development only?
  - Eventually desktop app (Electron)?
  - Web app (browser-based)?
  - **Answer:** Local development only.

### Q17: Audio Output
- **A)** Should audio route to:
  - System default output (simplest)?
  - User-selectable audio device?
  - **Answer:** System default output.
- **B)** Should there be volume control in the app?
  - **Answer:** Yes.

## Error Handling & Edge Cases

### Q18: Error Scenarios
- **A)** What should happen when:
  - SuperCollider fails to start?
  - MIDI device disconnects mid-session?
  - Backend crashes/restarts?
  - WebSocket connection drops?
  - **Answer:** No graceful degradation. Any systemic error that prevents the app from running must be surfaced to the user in the UI.
- **B)** Should the app:
  - Auto-reconnect?
  - Show clear error messages?
  - Gracefully degrade (e.g., visual only if audio fails)?
  - **Answer:** Show clear error messages in the UI. No graceful degradation.

### Q19: Performance Requirements
- **A)** What's acceptable latency between:
  - MIDI key press → audio output?
  - MIDI key press → visual feedback?
  - **Answer:** Target &lt;10ms for MIDI → audio (tight). Visual feedback can be less strict; audio latency is the priority.
- **B)** Target: <10ms, <20ms, or <50ms?
  - **Answer:** &lt;10ms for audio output.

## MVP Scope

### Q20: MVP Priorities
- **A)** What's absolutely essential for MVP?
  - [x] MIDI keyboard connection
  - [x] SuperCollider audio
  - [x] Virtual keyboard visualization
  - [x] Green/red note feedback
  - [x] Random lesson generation
  - [ ] Data persistence (only lesson definitions in JSON; no session/history persistence)
  - [x] Error handling
  - **Answer:** All of the above except full data persistence. Only lesson definitions persist (JSON); everything else is session-only until v2.
- **B)** What can wait for v2?
  - **Answer:** Practice history, statistics, tracking, and any other persistence beyond lesson definitions.
- **C)** What's the target timeline for MVP?
  - **Answer:** No fixed timeline; proceed as needed.

## Additional Features (Future Consideration)

### Q21: Future Enhancements
- **A)** Are there features you'd like eventually but not for MVP?
  - Metronome?
  - Recording/playback?
  - Multiple instrument sounds?
  - Custom lesson creation?
  - Progress tracking/analytics?
  - Multi-user support?
  - **Answer:** Decide later after playing with the app.

---

## How to Answer

Please edit this file and add your answers below each question, or create a separate `ANSWERS.md` file with your responses. You can also answer in conversation format if preferred.

---

## Rhodes Sound Source (from Q1 research)

Use an **FM Rhodes SynthDef** (no WAV samples). Recommended source:

- **sccode.org 1-522** — “FM Rhodes” by snappizz, native port of STK’s Rhodey (DX7-style). Uses only basic UGens (`SinOsc`, `EnvGen`, `Mix`, `Pan2`, `Out`), low CPU, no sc3-plugins.  
  - https://sccode.org/1-522  
- **Same implementation** (with MIDI `note` arg): GitHub Gist “Rudimentary Fender Rhodes Synth Definition for Sonic Pi” — `\rhodes` SynthDef with `note = 60` (midicps), `gate`, `vel`, `modIndex`, `mix`, `lfoSpeed`, `lfoDepth`.  
  - https://gist.github.com/mbutz/dc11a619b8e2f471bb11a3b89b899896  

**Alternative (sample-based):** jRhodes3d (SFZ, 67 samples, 1977 Mark I, CC-BY-NC) could be used with SuperCollider `PlayBuf`/buffers, but adds sample packaging and licensing; FM synth is sufficient for a standard Rhodes and keeps the stack simple.

---

## FastAPI usage (from Q15 research)

Use **FastAPI** for the backend; keep it minimal — no over-engineering.

**Stack:** FastAPI + Uvicorn (+ `websockets` for WS). Same process handles HTTP and WebSocket on one ASGI app.

**Structure:**
- **HTTP:** Optional routes only where useful (e.g. `GET /health`, `GET /api/midi/devices`, `GET /api/lessons`). No HTTP if everything can go over WebSocket.
- **WebSocket:** Single endpoint (e.g. `GET /ws`). `await websocket.accept()`, then a loop: `receive_text()` / `receive_json()` and `send_text()` / `send_json()`. Catch `WebSocketDisconnect` and remove the connection (we only have one client per session; no broadcast list required unless we add it later).
- **Lifespan:** Use `@asynccontextmanager` and pass it to `FastAPI(lifespan=...)`. On startup: check/start SuperCollider, load lesson definitions from JSON, optionally enumerate MIDI ports. On shutdown: close MIDI port, optional SuperCollider teardown. Keep startup fast and failure modes clear.
- **Shared state:** Store OSC client, MIDI port, lesson catalog, and (if needed) single active WebSocket in `app.state`. WebSocket handler gets `websocket.app.state` for access. No Redis or DB for MVP.
- **Concurrency:** Use `asyncio.create_task()` only if we need a true background loop (e.g. MIDI input → OSC + forward to WebSocket). Otherwise a single async WebSocket loop that receives and sends is enough. Prefer async functions so the event loop isn’t blocked.
- **Run:** `uvicorn main:app --reload` or `fastapi dev main.py`. Port 8765 (or chosen port) for both HTTP and WS.

**References:** [FastAPI WebSockets](https://fastapi.tiangolo.com/advanced/websockets), [Lifespan events](https://fastapi.tiangolo.com/advanced/events).
