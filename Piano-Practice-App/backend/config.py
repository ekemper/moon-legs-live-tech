"""Configuration: ports, paths, defaults."""

import os
from pathlib import Path

# Project root (parent of backend/)
PROJECT_ROOT = Path(__file__).resolve().parent.parent

# Data paths
DATA_DIR = PROJECT_ROOT / "data"
LESSON_DEFINITIONS_PATH = DATA_DIR / "lesson_definitions.json"
DEVICE_CONFIGS_PATH = DATA_DIR / "device_configs.json"

# SuperCollider (SC_HOST for Docker: set to host.docker.internal so container reaches host scsynth)
SC_HOST = os.environ.get("SC_HOST", "127.0.0.1")
SC_PORT = int(os.environ.get("SC_PORT", "57120"))
SC_BOOT_TIMEOUT_SEC = 5.0
SC_PROGRAMS_DIR = PROJECT_ROOT / "sc_programs"
SC_BOOTSTRAP_SCRIPT = SC_PROGRAMS_DIR / "bootstrap.scd"

# Backend
WS_HTTP_PORT = 8765
WS_HOST = "0.0.0.0"

# Default volume (0-1); scaled with frontend value
DEFAULT_VOLUME = 0.8

# Keys for random lesson (12 keys)
KEYS = ["C", "C#", "D", "Eb", "E", "F", "F#", "G", "Ab", "A", "Bb", "B"]
