"""Note membership validation only (no order rules). Green if note in lesson, red if not."""

from __future__ import annotations


def is_note_in_lesson(midi_note: int, lesson_midi_notes: list[int]) -> bool:
    """Return True if the played MIDI note is in the current lesson's expected notes."""
    return midi_note in lesson_midi_notes
