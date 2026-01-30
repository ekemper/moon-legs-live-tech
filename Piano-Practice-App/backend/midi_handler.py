"""MIDI input: mido callback -> asyncio.Queue; device list; open/close; init workflow (lowest/highest note)."""

from __future__ import annotations

import asyncio
import threading
from typing import Any

import mido
from mido import Message

from backend.config import DEVICE_CONFIGS_PATH
from backend.lesson_loader import load_device_configs, save_device_configs


def get_input_names() -> list[str]:
    """Return list of available MIDI input port names. Returns [] if unavailable (e.g. in Docker)."""
    try:
        return mido.get_input_names()
    except (OSError, RuntimeError, Exception):
        return []


def open_input(port_name: str):
    """Open MIDI input port by name. Returns mido port or None."""
    try:
        return mido.open_input(port_name)
    except (OSError, IOError):
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
            self.close()
        port = open_input(port_name)
        if port is None:
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
        return None

    def close(self) -> None:
        if self._port is not None:
            try:
                self._port.close()
            except Exception:
                pass
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
                self._init_state = None
                return {"lowNote": low, "highNote": high, "keyCount": key_count}
        return None

    def get_config_for_device(self, device_id: str) -> dict[str, Any] | None:
        return self._device_configs.get(device_id)

    def get_all_device_configs(self) -> dict[str, dict[str, Any]]:
        """Return copy of stored device configs (device_id -> { lowNote, highNote, keyCount })."""
        return dict(self._device_configs)
