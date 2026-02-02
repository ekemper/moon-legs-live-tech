# Implementation Details — Piano Practice App

Concrete schema and class contracts for the backend. See `IMPLEMENTATION_PLAN.md` for phases and `ARCHITECTURE_REFERENCE.md` for architecture.

---

## 1. Lesson definitions JSON schema

**File:** One JSON file (e.g. `data/lesson_definitions.json`) holds all chord, scale, and arpeggio definitions.

**Rule:** Store **intervals only**. Do not store root, note names, or MIDI numbers in the file. The key (root) is chosen at random when generating a lesson; notes and MIDI are computed on the fly from intervals + key.

**Structure:**

```json
{
  "chords": [
    {
      "id": "major",
      "name": "Major",
      "intervals": [0, 4, 7],
      "historicalBlurb": "..."
    }
  ],
  "scales": [
    {
      "id": "major",
      "name": "Major",
      "intervals": [0, 2, 4, 5, 7, 9, 11],
      "historicalBlurb": "..."
    }
  ],
  "arpeggios": [
    {
      "id": "major",
      "name": "Major",
      "intervals": [0, 4, 7, 12],
      "historicalBlurb": "..."
    }
  ]
}
```

**Fields per entry:**

| Field            | Required | Description |
|------------------|----------|-------------|
| `id`             | Yes      | Unique identifier within the section (chords/scales/arpeggios). |
| `name`           | Yes      | Display name (e.g. "Major", "Natural Minor"). |
| `intervals`      | Yes      | Array of integers: semitone offsets from the root. Order defines the chord/scale/arpeggio. |
| `historicalBlurb`| No       | Short historical/cultural blurb for the lesson. |

**Interval rules:** Intervals are semitones from the root (0 = root). Adjacent intervals define the steps (e.g. major scale: 0, 2, 4, 5, 7, 9, 11). Arpeggios can span octaves (e.g. 12 = root one octave up).

---

## 2. Note and MIDI generation from intervals + key

Notes (letter names A, B, C, D, sharps/flats) and MIDI note numbers are **not** stored; they are computed from the lesson definition (intervals) and the chosen key (and octave) when creating a random lesson.

**Python class:** `LessonNoteGenerator` in `backend/lesson_notes.py`.

**Responsibilities:**

- Given a **lesson definition** (type + intervals) and a **key** (e.g. `"C"`, `"F#"`, `"Bb"`) and optional **octave** (default 4):
  - Compute the **root MIDI** note for that key in that octave (e.g. C4 = 60).
  - For each interval, compute **MIDI note = root_midi + interval** (clamped to 0–127 if desired).
  - Map each MIDI note to a **musical note name** (pitch class: C, C#, D, …, B) using standard interval/semitone rules; optionally include octave (e.g. C4).

**Public API:**

- `LessonNoteGenerator(reference_midi_c4=60)` — C4 MIDI number (default 60).
- `root_midi(key, octave=None)` — MIDI number of the root for the given key and octave.
- `notes_and_midi(lesson, key, octave=None, *, clamp_midi=True, include_octave_in_names=False)` — returns `(note_names: list[str], midi_notes: list[int])`.
- `midi_only(intervals, key, octave=None, clamp_midi=True)` — returns `list[int]` when note names are not needed.

**Helper:**

- `lesson_from_json_entry(entry, lesson_type)` — build a `LessonDefinition` from a JSON object (id, name, intervals, historicalBlurb).

**Key parsing:** Keys are parsed from strings like `"C"`, `"F#"`, `"Bb"` to a semitone 0–11 (C=0, C#/Db=1, …, B=11). Root MIDI for octave 4 is then `60 + semitone`; other octaves use the same formula from a C4 reference.

**Note names:** Pitch classes are spelled with sharps (C, C#, D, …, B) by default. Key-appropriate flats can be added later if desired.

---

## 3. Random lesson creation flow

1. Load `lesson_definitions.json` (chords, scales, arpeggios).
2. Pick at random: lesson type (chord / scale / arpeggio), then one definition from that section, then a key (e.g. from a list of 12 keys), and optionally an octave (e.g. 4).
3. Use `LessonNoteGenerator.notes_and_midi(lesson, key, octave)` to get note names and MIDI notes for the lesson.
4. Send to the frontend: key, lesson name, intervals, note names, MIDI notes, historical blurb. Use MIDI notes for comparison with MIDI input (green/red by membership).

---

## 4. Data types (backend)

- **LessonDefinition:** `lesson_type`, `id`, `name`, `intervals` (list of int), `historical_blurb`. See `backend/lesson_notes.py` (`LessonDefinition` dataclass and `lesson_from_json_entry`).
