"""MIDI input: mido callback -> asyncio.Queue; device list; open/close; init workflow (lowest/highest note)."""

from __future__ import annotations

import asyncio
import logging
import os
import sys
import threading
from pathlib import Path
from typing import Any

import mido
from mido import Message

from backend.config import DEVICE_CONFIGS_PATH
from backend.lesson_loader import load_device_configs, save_device_configs

logger = logging.getLogger(__name__)

# Log MIDI list failure only once to avoid poller flooding (e.g. missing rtmidi)
_midi_list_failure_logged = False
_no_ports_hint_logged = False


def _init_mido_backend() -> None:
    """Use rtmidi (CoreMIDI on macOS) so USB MIDI devices are enumerated. Log backend and initial ports."""
    backend_name = os.environ.get("MIDO_BACKEND")
    if backend_name:
        try:
            mido.set_backend(backend_name)
            logger.info("MIDI backend: %s (from MIDO_BACKEND)", backend_name)
        except Exception as e:
            logger.warning("MIDI backend %s failed: %s; trying defaults", backend_name, e)
            backend_name = None
    if not backend_name:
        # On macOS, mido's default rtmidi path can hit API_UNSPECIFIED (missing in python-rtmidi).
        # Forcing MACOSX_CORE avoids that and uses CoreMIDI so USB MIDI devices are visible.
        candidates = (
            ("mido.backends.rtmidi/MACOSX_CORE", "mido.backends.portmidi")
            if sys.platform == "darwin"
            else ("mido.backends.rtmidi", "mido.backends.portmidi")
        )
        for candidate in candidates:
            try:
                mido.set_backend(candidate)
                logger.info("MIDI backend: %s", candidate)
                break
            except Exception as e:
                logger.debug("MIDI backend %s failed: %s", candidate, e)
        else:
            logger.warning("MIDI: no backend loaded; device list may be empty")
    # Force backend load and log initial device count
    try:
        names = mido.get_input_names()
        backend_loaded = getattr(mido.backend, "__module__", str(mido.backend))
        logger.info("MIDI loaded backend: %s", backend_loaded)
        logger.info("MIDI at startup: %d input port(s) %s", len(names), names)
    except Exception as e:
        logger.warning("MIDI get_input_names at startup failed: %s", e)


def _is_running_in_docker() -> bool:
    """Heuristic: we're in a container if /.dockerenv exists or cgroup has docker."""
    if Path("/.dockerenv").exists():
        return True
    try:
        cgroup = Path("/proc/self/cgroup").read_text()
        return "docker" in cgroup or "containerd" in cgroup
    except Exception:
        return False


# Set backend and log once at import
_init_mido_backend()
if _is_running_in_docker():
    logger.warning(
        "Backend is running in Docker. USB MIDI devices on the host are not visible here. "
        "To use a USB MIDI keyboard on macOS, run the backend on the host (e.g. uvicorn backend.main:app)."
    )


def get_input_names() -> list[str]:
    """Return list of available MIDI input port names. Returns [] if unavailable (e.g. in Docker)."""
    global _midi_list_failure_logged, _no_ports_hint_logged
    try:
        names = mido.get_input_names()
        logger.info("MIDI list_devices: found %d port(s) %s", len(names), names)
        if not names and not _is_running_in_docker() and not _no_ports_hint_logged:
            _no_ports_hint_logged = True
            logger.info(
                "MIDI: no input ports. On macOS: confirm the USB device appears in Audio MIDI Setup "
                "(Applications → Utilities). Plug in the keyboard and wait a few seconds for the next poll."
            )
        return names
    except (OSError, RuntimeError, Exception) as e:
        if not _midi_list_failure_logged:
            _midi_list_failure_logged = True
            logger.warning("MIDI list_devices failed: %s (install python-rtmidi for real MIDI ports)", e)
        else:
            logger.debug("MIDI list_devices failed: %s", e)
        return []


def open_input(port_name: str):
    """Open MIDI input port by name. Returns mido port or None."""
    try:
        logger.info("MIDI open_input: opening %r", port_name)
        port = mido.open_input(port_name)
        logger.info("MIDI open_input: opened %r", port_name)
        return port
    except (OSError, IOError) as e:
        logger.warning("MIDI open_input failed for %r: %s", port_name, e)
        return None


def make_midi_queue(loop: asyncio.AbstractEventLoop | None = None):
    """
    Create a callback and an async iterator that yields MIDI messages.
    Callback pushes to a queue via call_soon_threadsafe; consumer uses async for.
    """
    loop = loop or asyncio.get_event_loop()
    queue: asyncio.Queue[Message] = asyncio.Queue()

    def callback(msg: Message):
        loop.call_soon_threadsafe(queue.put_nowait, msg)

    async def stream():
        while True:
            yield await queue.get()

    return callback, stream()


class MIDIHandler:
    """
    One selected device; pushes note on/off to queue; optional init workflow state
    (waiting for lowest, then highest note) and device config persistence.
    """

    def __init__(self):
        self._port = None
        self._callback = None
        self._thread: threading.Thread | None = None
        self._queue: asyncio.Queue[Message] | None = None
        self._loop: asyncio.AbstractEventLoop | None = None
        try:
            self._device_configs = load_device_configs()
        except Exception:
            self._device_configs = {}
        self._init_state: dict[str, Any] | None = None  # { "step": "low"|"high", "lowNote"?: int }

    def get_device_config(self, device_id: str) -> dict[str, Any] | None:
        """Return stored config for device (lowNote, highNote, keyCount) or None."""
        return self._device_configs.get(device_id)

    def list_devices(self) -> list[str]:
        return get_input_names()

    def open(self, port_name: str) -> str | None:
        """Open port by name; start a thread that pushes messages to queue. Returns error string or None."""
        if self._port is not None:
            logger.info("MIDI open: closing previous port %r", getattr(self, "_current_port_name", None))
            self.close()
        logger.info("MIDI open: connecting to %r", port_name)
        port = open_input(port_name)
        if port is None:
            logger.warning("MIDI open: failed to open %r", port_name)
            return f"Could not open MIDI port: {port_name}"
        self._port = port
        self._loop = asyncio.get_event_loop()
        self._queue = asyncio.Queue()

        def put(msg: Message):
            self._loop.call_soon_threadsafe(self._queue.put_nowait, msg)

        def thread_target():
            for msg in port:
                put(msg)

        self._thread = threading.Thread(target=thread_target, daemon=True)
        self._thread.start()
        self._current_port_name = port_name
        logger.info("MIDI open: connected %r, read thread started", port_name)
        return None

    def close(self) -> None:
        if self._port is not None:
            name = getattr(self, "_current_port_name", None)
            logger.info("MIDI close: closing port %r", name)
            try:
                self._port.close()
            except Exception as e:
                logger.warning("MIDI close: exception %s", e)
            self._port = None
        self._thread = None
        self._current_port_name = None

    async def get_message(self) -> Message | None:
        """Get next MIDI message (for use in a consumer task). Returns None if closed."""
        if self._queue is None:
            return None
        try:
            return await asyncio.wait_for(self._queue.get(), timeout=0.1)
        except asyncio.TimeoutError:
            return None

    def start_init_workflow(self, device_id: str) -> None:
        """Begin init workflow for device: waiting for lowest note."""
        logger.info("MIDI init_workflow: started for device %r (press lowest key)", device_id)
        self._init_state = {"deviceId": device_id, "step": "low", "lowNote": None, "highNote": None}

    def cancel_init_workflow(self) -> None:
        self._init_state = None

    def get_init_state(self) -> dict[str, Any] | None:
        return self._init_state

    def handle_init_note(self, note: int) -> dict[str, Any] | None:
        """
        If in init workflow, record lowest or highest note. Returns completed config
        { lowNote, highNote, keyCount } when both received, else None.
        """
        if not self._init_state:
            return None
        step = self._init_state["step"]
        if step == "low":
            self._init_state["lowNote"] = note
            self._init_state["step"] = "high"
            return None
        if step == "high":
            low = self._init_state.get("lowNote")
            high = note
            if low is not None:
                low, high = min(low, high), max(low, high)
                key_count = high - low + 1
                device_id = self._init_state["deviceId"]
                self._device_configs[device_id] = {"lowNote": low, "highNote": high, "keyCount": key_count}
                save_device_configs(self._device_configs)
                logger.info("MIDI init_workflow: completed for %r -> lowNote=%s highNote=%s keyCount=%s", device_id, low, high, key_count)
                self._init_state = None
                return {"lowNote": low, "highNote": high, "keyCount": key_count}
        return None

    def get_config_for_device(self, device_id: str) -> dict[str, Any] | None:
        return self._device_configs.get(device_id)

    def get_all_device_configs(self) -> dict[str, dict[str, Any]]:
        """Return copy of stored device configs (device_id -> { lowNote, highNote, keyCount })."""
        return dict(self._device_configs)
