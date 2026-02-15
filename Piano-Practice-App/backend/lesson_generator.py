"""Random lesson generation from catalog using LessonNoteGenerator."""

from __future__ import annotations

import logging
import random
from typing import Any

from backend.config import KEYS
from backend.lesson_loader import load_lesson_definitions
from backend.lesson_notes import LessonDefinition, LessonNoteGenerator, semitones_to_scale_degrees

logger = logging.getLogger(__name__)


# Reference octaves for lesson display and root indicator (playable range)
LESSON_OCTAVES = (2, 3, 4, 5, 6)


def pick_random_lesson(
    catalog: dict[str, list[LessonDefinition]],
    note_generator: LessonNoteGenerator,
    keys: list[str] | None = None,
    octave: int | None = None,
) -> dict[str, Any] | None:
    """
    Pick a random lesson type, definition, key, and octave; compute note names and MIDI notes.
    midiNotes includes all octaves (every pitch class in the lesson, 0-127).
    Returns a dict for the frontend: type, key, name, octave, noteNames, midiNotes, rootMidi, etc.
    """
    keys = keys or KEYS
    types_with_defs = [
        (t, defs) for t, defs in [("chord", catalog["chords"]), ("scale", catalog["scales"]), ("arpeggio", catalog["arpeggios"])]
        if defs
    ]
    if not types_with_defs:
        return None
    lesson_type, defs = random.choice(types_with_defs)
    lesson = random.choice(defs)
    key = random.choice(keys)
    octave = octave if octave is not None else random.choice(LESSON_OCTAVES)
    logger.info("pick_random_lesson: type=%s name=%s key=%s octave=%s", lesson_type, lesson.name, key, octave)
    note_names, _ = note_generator.notes_and_midi(lesson, key, octave, include_octave_in_names=False)
    root_midi = note_generator.root_midi(key, octave)
    root_pc = root_midi % 12
    # Pitch classes in this lesson (e.g. C major scale → 0, 2, 4, 5, 7, 9, 11)
    pitch_classes = {(root_pc + interval) % 12 for interval in lesson.intervals}
    # Include all octaves: every MIDI note whose pitch class is in the lesson
    midi_notes = sorted(n for n in range(128) if n % 12 in pitch_classes)
    return {
        "type": lesson_type,
        "key": key,
        "octave": octave,
        "name": lesson.name,
        "intervals": lesson.intervals,
        "intervalLabels": semitones_to_scale_degrees(lesson.intervals, lesson.id),
        "noteNames": note_names,
        "midiNotes": midi_notes,
        "rootMidi": root_midi,
        "historicalBlurb": lesson.historical_blurb or "",
    }
