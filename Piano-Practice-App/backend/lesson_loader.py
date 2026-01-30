"""Load lesson definitions and device configs from JSON."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from backend.config import DEVICE_CONFIGS_PATH, LESSON_DEFINITIONS_PATH
from backend.lesson_notes import LessonDefinition, lesson_from_json_entry


def load_lesson_definitions(path: Path | None = None) -> dict[str, list[LessonDefinition]]:
    """Load lesson_definitions.json; return { 'chords': [...], 'scales': [...], 'arpeggios': [...] }."""
    path = path or LESSON_DEFINITIONS_PATH
    empty = {"chords": [], "scales": [], "arpeggios": []}
    if not path.exists():
        return empty
    try:
        with open(path, encoding="utf-8") as f:
            data = json.load(f)
    except (OSError, PermissionError, json.JSONDecodeError):
        return empty
    result: dict[str, list[LessonDefinition]] = {
        "chords": [],
        "scales": [],
        "arpeggios": [],
    }
    for key in result:
        for entry in data.get(key, []):
            result[key].append(lesson_from_json_entry(entry, key[:-1]))  # "chords" -> "chord"
    return result


def load_device_configs(path: Path | None = None) -> dict[str, dict[str, Any]]:
    """Load device_configs.json; return { device_id: { lowNote, highNote, keyCount }, ... }."""
    path = path or DEVICE_CONFIGS_PATH
    if not path.exists():
        return {}
    try:
        with open(path, encoding="utf-8") as f:
            return json.load(f)
    except (OSError, PermissionError, json.JSONDecodeError):
        return {}


def save_device_configs(configs: dict[str, dict[str, Any]], path: Path | None = None) -> None:
    """Save device configs to JSON."""
    path = path or DEVICE_CONFIGS_PATH
    try:
        path.parent.mkdir(parents=True, exist_ok=True)
        with open(path, "w", encoding="utf-8") as f:
            json.dump(configs, f, indent=2)
    except (OSError, PermissionError):
        pass  # e.g. read-only mount in container
