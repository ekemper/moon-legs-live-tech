"""Random lesson generation from catalog using LessonNoteGenerator."""

from __future__ import annotations

import logging
import random
from typing import Any

from backend.config import KEYS
from backend.lesson_loader import load_lesson_definitions
from backend.lesson_notes import LessonDefinition, LessonNoteGenerator, semitones_to_scale_degrees

logger = logging.getLogger(__name__)


def pick_random_lesson(
    catalog: dict[str, list[LessonDefinition]],
    note_generator: LessonNoteGenerator,
    keys: list[str] | None = None,
    octave: int = 4,
) -> dict[str, Any] | None:
    """
    Pick a random lesson type, definition, and key; compute note names and MIDI notes.
    Returns a dict for the frontend: type, key, name, intervals, noteNames, midiNotes, historicalBlurb.
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
    logger.info("pick_random_lesson: type=%s name=%s key=%s octave=%s", lesson_type, lesson.name, key, octave)
    note_names, midi_notes = note_generator.notes_and_midi(lesson, key, octave, include_octave_in_names=False)
    return {
        "type": lesson_type,
        "key": key,
        "octave": octave,
        "name": lesson.name,
        "intervals": lesson.intervals,
        "intervalLabels": semitones_to_scale_degrees(lesson.intervals, lesson.id),
        "noteNames": note_names,
        "midiNotes": midi_notes,
        "historicalBlurb": lesson.historical_blurb or "",
    }
