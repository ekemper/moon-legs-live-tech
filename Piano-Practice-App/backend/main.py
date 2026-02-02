"""
Piano Practice App backend: FastAPI + WebSocket, MIDI -> OSC + validation, random lessons.
"""

from __future__ import annotations

import asyncio
import json
import logging
import sys
from contextlib import asynccontextmanager
from pathlib import Path

from fastapi import FastAPI, WebSocket, WebSocketDisconnect

from backend import config
from backend.lesson_generator import pick_random_lesson
from backend.lesson_loader import load_lesson_definitions, load_device_configs
from backend.lesson_notes import LessonNoteGenerator
from backend.midi_handler import MIDIHandler
from backend.sc_manager import SCClient, check_sc_running, start_sc
from backend.validator import is_note_in_lesson

logging.basicConfig(
    level=config.LOG_LEVEL_VALUE,
    format="%(levelname)s:%(name)s:%(message)s",
)
logger = logging.getLogger(__name__)

# --- State (set in lifespan) ---
lesson_catalog: dict = {}
device_configs: dict = {}
sc_client: SCClient | None = None
midi_handler: MIDIHandler | None = None
note_generator: LessonNoteGenerator | None = None
current_lesson: dict | None = None
active_ws: WebSocket | None = None
volume: float = config.DEFAULT_VOLUME
# For MIDI device change detection: last list we sent to the client (or None)
_last_midi_devices_sent: list[str] | None = None
MIDI_DEVICE_POLL_INTERVAL = 3.0  # seconds


async def _midi_device_poller() -> None:
    """When MIDI port list changes, push midi_devices to the connected client. Polls every MIDI_DEVICE_POLL_INTERVAL."""
    global _last_midi_devices_sent
    logger.info("MIDI device poller started (interval=%.1fs)", MIDI_DEVICE_POLL_INTERVAL)
    while True:
        await asyncio.sleep(MIDI_DEVICE_POLL_INTERVAL)
        if midi_handler is None:
            logger.warning("MIDI device poll: midi_handler is None, skip")
            continue
        current = midi_handler.list_devices()
        # Log every poll with the device list so we can see what the system reports
        logger.info("MIDI device poll: %d device(s) %s", len(current), current)
        if current != _last_midi_devices_sent:
            logger.info("MIDI device list changed: %s -> %s, pushing to client", _last_midi_devices_sent, current)
            _last_midi_devices_sent = current
            if active_ws is not None:
                await send_ws({"type": "midi_devices", "devices": current})
        elif active_ws is None:
            logger.info("MIDI device poll: no WebSocket client connected, not pushing")


# Log WebSocket traffic (type + brief summary; avoid flooding for lesson / midi_note)
def _ws_log_send(obj: dict) -> None:
    t = obj.get("type", "?")
    if t == "lesson":
        logger.info("WS send: type=lesson key=%s", (obj.get("lesson") or {}).get("key"))
    elif t == "midi_note":
        logger.debug("WS send: type=midi_note note=%s on=%s", obj.get("note"), obj.get("on"))
    else:
        logger.info("WS send: type=%s %s", t, {k: v for k, v in obj.items() if k != "type"})


async def send_ws(obj: dict) -> None:
    _ws_log_send(obj)
    if active_ws is not None:
        try:
            await active_ws.send_text(json.dumps(obj))
        except Exception:
            pass


async def midi_consumer() -> None:
    """Consume MIDI queue: note on/off -> OSC + validation -> WebSocket."""
    global current_lesson
    while midi_handler is not None:
        msg = await midi_handler.get_message()
        if msg is None:
            await asyncio.sleep(0.001)
            continue
        if msg.type == "note_on" and msg.velocity == 0:
            msg = type(msg)("note_off", note=msg.note, velocity=0, time=msg.time, channel=msg.channel)
        if msg.type == "note_on":
            note, vel, ch = msg.note, msg.velocity or 80, msg.channel
            logger.debug("MIDI note_on note=%s vel=%s ch=%s", note, vel, ch)
            if sc_client:
                sc_client.note_on(note, vel, ch)
            # Init workflow
            init_state = midi_handler.get_init_state() if midi_handler else None
            if init_state:
                completed = midi_handler.handle_init_note(note) if midi_handler else None
                if completed:
                    await send_ws({"type": "init_complete", "config": completed})
                else:
                    await send_ws({"type": "init_step", "step": midi_handler.get_init_state().get("step") if midi_handler else "high"})
            else:
                # Normal: validate and send feedback
                lesson_midi = (current_lesson or {}).get("midiNotes") or []
                correct = is_note_in_lesson(note, lesson_midi)
                await send_ws({"type": "midi_note", "note": note, "velocity": vel, "on": True, "isCorrect": correct})
        elif msg.type == "note_off":
            note, ch = msg.note, msg.channel
            logger.debug("MIDI note_off note=%s ch=%s", note, ch)
            if sc_client:
                sc_client.note_off(note, ch)
            if not (midi_handler and midi_handler.get_init_state()):
                lesson_midi = (current_lesson or {}).get("midiNotes") or []
                correct = is_note_in_lesson(note, lesson_midi)
                await send_ws({"type": "midi_note", "note": note, "velocity": 0, "on": False, "isCorrect": correct})


@asynccontextmanager
async def lifespan(app: FastAPI):
    global lesson_catalog, device_configs, sc_client, midi_handler, note_generator, current_lesson
    # Load data
    config.DATA_DIR.mkdir(parents=True, exist_ok=True)
    lesson_catalog = load_lesson_definitions()
    device_configs = load_device_configs()
    n_chords = len(lesson_catalog.get("chords", []))
    n_scales = len(lesson_catalog.get("scales", []))
    n_arpeggios = len(lesson_catalog.get("arpeggios", []))
    n_devices = len(device_configs)
    logger.info("Startup: lessons chords=%d scales=%d arpeggios=%d, device_configs=%d", n_chords, n_scales, n_arpeggios, n_devices)
    note_generator = LessonNoteGenerator()
    # SuperCollider (only start sclang when on localhost; in Docker, SC must be running on host)
    sc_running = await check_sc_running(config.SC_HOST, config.SC_PORT, timeout=2.0)
    if not sc_running:
        logger.warning("SuperCollider not running at %s:%s", config.SC_HOST, config.SC_PORT)
        if config.SC_HOST in ("127.0.0.1", "localhost") and config.SC_BOOTSTRAP_SCRIPT.exists():
            logger.info("Starting SuperCollider: %s", config.SC_BOOTSTRAP_SCRIPT)
            proc = start_sc()
            if proc:
                await asyncio.sleep(config.SC_BOOT_TIMEOUT_SEC)
                logger.info("SuperCollider started (PID %s)", proc.pid)
            else:
                logger.error("Failed to start SuperCollider (sclang not found?)")
        else:
            # Docker / remote: require SC on host so startup fails fast with obvious error
            msg = (
                "SuperCollider is not reachable at %s:%s. "
                "Start scsynth on the host (e.g. run 'sclang bootstrap.scd' in sc_programs), then restart the backend."
            ) % (config.SC_HOST, config.SC_PORT)
            logger.error(msg)
            print(msg, file=sys.stderr)
            sys.exit(1)
    else:
        logger.info("SuperCollider already running at %s:%s", config.SC_HOST, config.SC_PORT)
    sc_client = SCClient(config.SC_HOST, config.SC_PORT)
    sc_client.set_volume(volume)
    midi_handler = MIDIHandler()
    # Initial lesson
    current_lesson = pick_random_lesson(lesson_catalog, note_generator)
    if current_lesson:
        logger.info("Initial lesson: %s %s (%s)", current_lesson.get("key"), current_lesson.get("name"), current_lesson.get("type"))
    # Start MIDI consumer and MIDI device poller (push device list changes to client)
    consumer_task = asyncio.create_task(midi_consumer())
    poller_task = asyncio.create_task(_midi_device_poller())
    logger.info("Backend ready: MIDI consumer and device poller started")
    try:
        yield
    finally:
        logger.info("Shutting down: stopping MIDI consumer and poller")
        consumer_task.cancel()
        poller_task.cancel()
        try:
            await consumer_task
        except asyncio.CancelledError:
            pass
        try:
            await poller_task
        except asyncio.CancelledError:
            pass
        if midi_handler:
            midi_handler.close()
        sc_client = None
        midi_handler = None
        logger.info("Shutdown complete")


app = FastAPI(title="Piano Practice App", lifespan=lifespan)


@app.get("/health")
def health():
    return {"status": "ok"}


@app.get("/api/midi/devices")
def api_midi_devices():
    if midi_handler is None:
        return {"devices": []}
    return {"devices": midi_handler.list_devices()}


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    global active_ws, current_lesson, volume, _last_midi_devices_sent
    await websocket.accept()
    active_ws = websocket
    try:
        # Send initial state
        devices = midi_handler.list_devices() if midi_handler else []
        logger.info("WebSocket connected: sending initial state (lesson, %d MIDI device(s))", len(devices))
        await send_ws({"type": "lesson", "lesson": current_lesson})
        await send_ws({"type": "midi_devices", "devices": devices})
        _last_midi_devices_sent = devices  # so poller doesn't immediately re-send
        if midi_handler:
            await send_ws({"type": "device_configs", "configs": midi_handler.get_all_device_configs()})
        await send_ws({"type": "volume", "value": volume})
        while True:
            raw = await websocket.receive_text()
            try:
                data = json.loads(raw)
            except json.JSONDecodeError:
                logger.warning("WS recv: invalid JSON (len=%d)", len(raw))
                continue
            msg_type = data.get("type")
            if msg_type in ("midi_note", "virtual_note"):
                logger.debug("WS recv: type=%s %s", msg_type, {k: v for k, v in data.items() if k != "type"})
            else:
                logger.info("WS recv: type=%s %s", msg_type, {k: v for k, v in data.items() if k != "type"})
            if msg_type == "midi_device_select":
                device_id = data.get("deviceId") or data.get("deviceName")
                device_index = data.get("deviceIndex")
                logger.info("midi_device_select: deviceId=%r deviceName=%r deviceIndex=%r", data.get("deviceId"), data.get("deviceName"), device_index)
                if not device_id and midi_handler:
                    devices = midi_handler.list_devices()
                    idx = device_index if device_index is not None else 0
                    if 0 <= idx < len(devices):
                        device_id = devices[idx]
                        logger.info("midi_device_select: resolved by index to %r", device_id)
                    else:
                        logger.warning("midi_device_select: no deviceId and index %s out of range (devices=%s)", idx, devices)
                if device_id and midi_handler:
                    err = midi_handler.open(device_id)
                    if err:
                        logger.warning("midi_device_select: open failed for %r: %s", device_id, err)
                        await send_ws({"type": "error", "message": err})
                    else:
                        cfg = midi_handler.get_device_config(device_id)
                        if cfg:
                            logger.info("midi_device_select: connected %r with saved config %s", device_id, cfg)
                            await send_ws({"type": "midi_device", "deviceId": device_id, "config": cfg})
                        else:
                            logger.info("midi_device_select: connected %r, starting init_workflow (no saved config)", device_id)
                            midi_handler.start_init_workflow(device_id)
                            await send_ws({"type": "init_workflow", "deviceId": device_id, "step": "low"})
                elif not device_id:
                    logger.warning("midi_device_select: no device_id resolved, ignoring")
            elif msg_type == "next_lesson":
                try:
                    new_lesson = pick_random_lesson(lesson_catalog, note_generator)
                    if new_lesson is not None:
                        current_lesson = new_lesson
                    await send_ws({"type": "lesson", "lesson": current_lesson})
                except Exception:
                    await send_ws({"type": "lesson", "lesson": current_lesson})
            elif msg_type == "set_volume":
                try:
                    v = float(data.get("value", volume))
                    volume = max(0.0, min(1.0, v))
                    if sc_client:
                        sc_client.set_volume(volume)
                    await send_ws({"type": "volume", "value": volume})
                except (TypeError, ValueError):
                    await send_ws({"type": "volume", "value": volume})
            elif msg_type == "virtual_note":
                # Mouse/touch on virtual keyboard: note (int), on (bool), velocity (optional)
                raw_note = data.get("note")
                on = data.get("on", True)
                vel = int(data.get("velocity", 80))
                try:
                    note = int(raw_note) if raw_note is not None else None
                except (TypeError, ValueError):
                    note = None
                if note is not None and 0 <= note <= 127:
                    if sc_client:
                        if on:
                            sc_client.note_on(note, vel, 0)
                        else:
                            sc_client.note_off(note, 0)
                    lesson_midi = (current_lesson or {}).get("midiNotes") or []
                    correct = is_note_in_lesson(note, lesson_midi)
                    await send_ws({"type": "midi_note", "note": note, "velocity": vel if on else 0, "on": on, "isCorrect": correct})
    except WebSocketDisconnect:
        pass
    finally:
        active_ws = None


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host=config.WS_HOST, port=config.WS_HTTP_PORT)
