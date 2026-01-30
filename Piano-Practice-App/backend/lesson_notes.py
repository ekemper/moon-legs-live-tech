"""
Generate musical note names and MIDI note numbers from lesson definitions (intervals) and key.

Lesson definitions store only intervals (semitones from root). This module computes
note names (A, B, C, D, sharps/flats) and MIDI numbers on the fly for any key and octave,
using standard interval notation (semitones from root).

Scale-degree display: intervals (semitones) are converted to scale-degree labels
(1, 2, ♭3, 4, 5, 6, ♭7, 8) using flats for lowered degrees per standard theory:
- Major chord = 1, 3, 5; minor = 1, ♭3, 5.
- Natural minor scale = 1, 2, ♭3, 4, 5, 6, ♭7, 8.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import List, Tuple

# Scale-degree labels for display (semitones from root → scale degree with flats).
# Major scale semitones: 0→1, 2→2, 4→3, 5→4, 7→5, 9→6, 11→7; 12→8.
# Lowered degrees use flat: 1→♭2, 3→♭3, 6→♭5, 10→♭7. 8 semitones = ♯5 (chord) or 6 (minor scale).
SEMITONE_TO_SCALE_DEGREE: Tuple[str, ...] = (
    "1", "♭2", "2", "♭3", "3", "4", "♭5", "5", "♯5", "6", "♭7", "7", "8",
)
# Minor scales: 8 semitones = 6th degree (not ♯5).
MINOR_SCALE_IDS: frozenset[str] = frozenset(("natural_minor", "harmonic_minor"))

# Pitch class 0-11 -> note name (sharp spelling: C, C#, D, ..., B)
PITCH_CLASS_NAMES_SHARP: Tuple[str, ...] = (
    "C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"
)

# Key name (with optional # or b) -> semitone offset from C (0-11)
KEY_TO_SEMITONE: dict[str, int] = {
    "C": 0, "C#": 1, "Db": 1, "D": 2, "D#": 3, "Eb": 3, "E": 4, "Fb": 4,
    "E#": 5, "F": 5, "F#": 6, "Gb": 6, "G": 7, "G#": 8, "Ab": 8, "A": 9,
    "A#": 10, "Bb": 10, "B": 11, "Cb": 11, "B#": 0,
}


def _parse_key(key: str) -> int:
    """Return semitone 0-11 for the given key name (e.g. 'C', 'F#', 'Bb')."""
    k = key.strip()
    if not k:
        raise ValueError("Key cannot be empty")
    if k in KEY_TO_SEMITONE:
        return KEY_TO_SEMITONE[k]
    # Try first char + rest (e.g. "C#", "Bb")
    if len(k) >= 2:
        candidate = k[0].upper() + k[1:].lower()
        if candidate in KEY_TO_SEMITONE:
            return KEY_TO_SEMITONE[candidate]
    raise ValueError(f"Unknown key: {key!r}")


def midi_to_note_name(midi: int, include_octave: bool = False) -> str:
    """
    Map a MIDI note number to a note name (pitch class, optionally with octave).
    Uses sharp spelling (C#, not Db). MIDI 60 = C4.
    """
    pitch_class = midi % 12
    name = PITCH_CLASS_NAMES_SHARP[pitch_class]
    if include_octave:
        octave = (midi // 12) - 1  # MIDI 12 = C0, 24 = C1, ..., 60 = C4
        name = f"{name}{octave}"
    return name


@dataclass
class LessonDefinition:
    """Minimal lesson definition: type and intervals (semitones from root)."""
    lesson_type: str  # "chord" | "scale" | "arpeggio"
    id: str
    name: str
    intervals: List[int]  # semitone offsets from root, e.g. [0, 4, 7] for major chord
    historical_blurb: str = ""


class LessonNoteGenerator:
    """
    Generates musical note names and MIDI note numbers from a lesson definition
    (intervals) and a key, for any key in any octave.

    Uses the rules of musical interval notation: intervals are semitone offsets
    from the root. The root is determined by the key (e.g. C, F#, Bb) and
    the reference octave (default 4; MIDI 60 = C4).
    """

    DEFAULT_OCTAVE = 4  # MIDI 60 = C4

    def __init__(self, reference_midi_c4: int = 60):
        """
        reference_midi_c4: MIDI number for C4 (default 60 per standard).
        """
        self.reference_midi_c4 = reference_midi_c4

    def root_midi(self, key: str, octave: int | None = None) -> int:
        """
        Return the MIDI note number for the root (key) in the given octave.
        octave defaults to DEFAULT_OCTAVE (4).
        """
        if octave is None:
            octave = self.DEFAULT_OCTAVE
        semitone = _parse_key(key)
        # C4 = 60 => octave 4 base = 60, so base = 60 + (octave - 4) * 12
        base = self.reference_midi_c4 + (octave - self.DEFAULT_OCTAVE) * 12
        return base + semitone

    def notes_and_midi(
        self,
        lesson: LessonDefinition,
        key: str,
        octave: int | None = None,
        *,
        clamp_midi: bool = True,
        include_octave_in_names: bool = False,
    ) -> Tuple[List[str], List[int]]:
        """
        From a lesson definition (intervals) and key, compute the list of
        musical note names and the list of MIDI note numbers.

        - lesson: definition with .intervals (semitones from root)
        - key: root key name (e.g. "C", "F#", "Bb")
        - octave: reference octave for the root (default 4)
        - clamp_midi: if True, clamp MIDI values to 0-127
        - include_octave_in_names: if True, note names include octave (e.g. "C4")

        Returns (note_names, midi_notes). Both lists have the same length and
        correspond 1:1 (note_names[i] is the name for midi_notes[i]).
        """
        root = self.root_midi(key, octave)
        midi_notes = [root + interval for interval in lesson.intervals]
        if clamp_midi:
            midi_notes = [max(0, min(127, n)) for n in midi_notes]
        note_names = [
            midi_to_note_name(m, include_octave=include_octave_in_names)
            for m in midi_notes
        ]
        return note_names, midi_notes

    def midi_only(
        self,
        intervals: List[int],
        key: str,
        octave: int | None = None,
        clamp_midi: bool = True,
    ) -> List[int]:
        """
        Return only MIDI note numbers for the given intervals, key, and octave.
        Convenience when note names are not needed.
        """
        root = self.root_midi(key, octave)
        midi_notes = [root + i for i in intervals]
        if clamp_midi:
            midi_notes = [max(0, min(127, n)) for n in midi_notes]
        return midi_notes


def semitones_to_scale_degrees(semitones: List[int], lesson_id: str = "") -> List[str]:
    """
    Convert semitone offsets from root to scale-degree labels (1, 2, ♭3, 4, 5, 6, ♭7, 8).
    Uses flats for lowered degrees. Octave (12 semitones) → "8"; above octave uses same
    pattern (e.g. 13 → "1" for 9th).
    For natural_minor / harmonic_minor, 8 semitones is shown as "6" (6th degree).
    """
    use_minor_6 = lesson_id in MINOR_SCALE_IDS
    result: List[str] = []
    for s in semitones:
        if s <= 12:
            label = SEMITONE_TO_SCALE_DEGREE[s]
            if use_minor_6 and s == 8:
                label = "6"
            result.append(label)
        else:
            idx = 12 if s % 12 == 0 else s % 12
            label = SEMITONE_TO_SCALE_DEGREE[idx]
            if use_minor_6 and idx == 8:
                label = "6"
            result.append(label)
    return result


def lesson_from_json_entry(entry: dict, lesson_type: str) -> LessonDefinition:
    """
    Build a LessonDefinition from a JSON object (e.g. from lesson_definitions.json).
    entry should have keys: id, name, intervals, historicalBlurb (optional).
    """
    return LessonDefinition(
        lesson_type=lesson_type,
        id=entry.get("id", ""),
        name=entry.get("name", ""),
        intervals=list(entry["intervals"]),
        historical_blurb=entry.get("historicalBlurb", ""),
    )
