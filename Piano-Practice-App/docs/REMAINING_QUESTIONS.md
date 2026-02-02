# Remaining Questions — Piano Practice App

These are open implementation choices and small ambiguities left after `CLARIFICATION_QUESTIONS.md`. Resolve before or during implementation as needed.

---

## 1. Volume control implementation ✅ Decided

**Decision:** Option A — Backend scales amplitude.

- Frontend sends volume (0–1) over WebSocket. Backend holds the value and, when sending each note to SuperCollider, multiplies amplitude accordingly (`amp = base_amp * volume`). Rhodes SynthDef receives the scaled `amp` per note. Get something working first; can update to OSC gain in SC later.

---

## 2. MIDI keyboard key-count and range ✅ Decided

**Decision:** Initialization workflow when a new device is plugged in.

- **Known device:** When a device is plugged in, the app checks if it has a stored configuration for that device (correlated by device name/ID). If yes, use that config (key count, range); no workflow.
- **Unknown device:** Automatically show an initialization workflow. Prompt the user to play the **lowest note** on the keyboard, then the **highest note** (in succession). From that we get: full MIDI range (low, high) and key count (high − low + 1). Save as a new device configuration correlated to the device (e.g. device name) and use it for future connections.
- **Persistence:** Device configurations (device identifier → lowNote, highNote, keyCount) must be stored so they can be reused. Store in JSON (e.g. `device_configs.json`); location TBD in implementation.

---

## 3. Order/timing rules for chord, scale, arpeggio ✅ Decided

**Decision:** No order or timing rules. For chords, scales, and arpeggios: it only matters that the user hits the right notes. Visual feedback: green for notes in the lesson, red for notes not in the lesson. No rules about sequence or order of play.

---

## 4. Lesson definitions JSON schema ✅ Decided

**Decision:** One JSON file for all chords, scales, and arpeggios. Store **intervals only**; do not store root, note names, or MIDI numbers in the definitions.

- **Structure:** Single file with top-level keys `chords`, `scales`, `arpeggios`. Each entry has a lesson type (implicit by section), `id`, `name`, `intervals`, `historicalBlurb`.
- **On the fly:** When generating a random lesson, pick a key (and optionally octave). From the lesson definition (intervals) + key, compute: (1) musical note names (A, B, C, D, sharps/flats), (2) MIDI note numbers for comparison and playback. Use standard interval notation (semitones from root); intervals between adjacent notes define the chord/scale/arpeggio.
- **Python:** A dedicated class in the backend generates musical notes and MIDI notes from a lesson definition (intervals) and key for any key in any octave. See `IMPLEMENTATION.md` and `backend/lesson_notes.py`.

---

## 5. SuperCollider bootstrap script contents ✅ Decided

**Decision:** Check via OSC; start via `sclang bootstrap.scd`.

- **Check:** Backend sends OSC `/status` to port 57120; if no reply within a timeout, assume scsynth is not running.
- **Start:** Run `sclang bootstrap.scd`. The script boots the default server (port 57120) and loads the Rhodes SynthDef (e.g. from `rhodes_piano.scd` or inlined). Document script path and assumptions (SuperCollider installed, `sclang` on PATH).

---

## 6. Auto-reconnect (WebSocket / MIDI) ✅ Decided

**Decision:** No auto-reconnect for MVP. Show error in UI; user must refresh or reconnect manually (WebSocket) or re-select device (MIDI).

---

## Summary

| # | Topic                     | Action |
|---|----------------------------|--------|
| 1 | Volume control             | ✅ Option A (backend scale amp). |
| 2 | MIDI key count / range     | ✅ Init workflow: lowest/highest note; persist device configs. |
| 3 | Order/timing rules         | ✅ No order rules; green/red by note membership only. |
| 4 | Lesson JSON schema         | ✅ One file; intervals only; notes/MIDI computed on the fly; Python generator class. |
| 5 | SC bootstrap               | ✅ Check OSC /status; start `sclang bootstrap.scd`. |
| 6 | Auto-reconnect             | ✅ No auto-reconnect for MVP; show error only. |

All items above are decided. See `ARCHITECTURE_REFERENCE.md` and `IMPLEMENTATION_PLAN.md` for full detail.
