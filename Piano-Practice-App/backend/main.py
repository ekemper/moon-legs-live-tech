"""
Piano Practice App backend: FastAPI + WebSocket, MIDI -> OSC + validation, random lessons.
"""

from __future__ import annotations

import asyncio
import json
import logging
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

logging.basicConfig(level=logging.INFO)
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


async def send_ws(obj: dict) -> None:
    if active_ws is not None:
        try:
            await active_ws.send_text(json.dumps(obj))
        except Exception as e:
            logger.warning("send_ws: %s", e)


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
    note_generator = LessonNoteGenerator()
    # SuperCollider (only start sclang when on localhost; in Docker, SC runs on host)
    sc_running = await check_sc_running(config.SC_HOST, config.SC_PORT, timeout=2.0)
    if not sc_running:
        if config.SC_HOST in ("127.0.0.1", "localhost") and config.SC_BOOTSTRAP_SCRIPT.exists():
            logger.info("Starting SuperCollider...")
            proc = start_sc()
            if proc:
                await asyncio.sleep(config.SC_BOOT_TIMEOUT_SEC)
        else:
            logger.warning("SuperCollider not reachable at %s:%s (start scsynth on host if using Docker)", config.SC_HOST, config.SC_PORT)
    sc_client = SCClient(config.SC_HOST, config.SC_PORT)
    sc_client.set_volume(volume)
    midi_handler = MIDIHandler()
    # Initial lesson
    current_lesson = pick_random_lesson(lesson_catalog, note_generator)
    # Start MIDI consumer
    consumer_task = asyncio.create_task(midi_consumer())
    try:
        yield
    finally:
        consumer_task.cancel()
        try:
            await consumer_task
        except asyncio.CancelledError:
            pass
        if midi_handler:
            midi_handler.close()
        sc_client = None
        midi_handler = None


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
    global active_ws, current_lesson
    await websocket.accept()
    active_ws = websocket
    try:
        # Send initial state
        await send_ws({"type": "lesson", "lesson": current_lesson})
        await send_ws({"type": "midi_devices", "devices": midi_handler.list_devices() if midi_handler else []})
        if midi_handler:
            await send_ws({"type": "device_configs", "configs": midi_handler.get_all_device_configs()})
        await send_ws({"type": "volume", "value": volume})
        while True:
            raw = await websocket.receive_text()
            try:
                data = json.loads(raw)
            except json.JSONDecodeError:
                continue
            msg_type = data.get("type")
            if msg_type == "midi_device_select":
                device_id = data.get("deviceId") or data.get("deviceName")
                if not device_id and midi_handler:
                    devices = midi_handler.list_devices()
                    idx = data.get("deviceIndex", 0)
                    if 0 <= idx < len(devices):
                        device_id = devices[idx]
                if device_id and midi_handler:
                    err = midi_handler.open(device_id)
                    if err:
                        await send_ws({"type": "error", "message": err})
                    else:
                        cfg = midi_handler.get_device_config(device_id)
                        if cfg:
                            await send_ws({"type": "midi_device", "deviceId": device_id, "config": cfg})
                        else:
                            midi_handler.start_init_workflow(device_id)
                            await send_ws({"type": "init_workflow", "deviceId": device_id, "step": "low"})
            elif msg_type == "next_lesson":
                global current_lesson
                current_lesson = pick_random_lesson(lesson_catalog, note_generator)
                await send_ws({"type": "lesson", "lesson": current_lesson})
            elif msg_type == "set_volume":
                global volume
                v = data.get("value", volume)
                volume = max(0.0, min(1.0, float(v)))
                if sc_client:
                    sc_client.set_volume(volume)
                await send_ws({"type": "volume", "value": volume})
            elif msg_type == "virtual_note":
                # Mouse/touch on virtual keyboard: note (int), on (bool), velocity (optional)
                note = data.get("note")
                on = data.get("on", True)
                vel = int(data.get("velocity", 80))
                if note is not None and isinstance(note, int):
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
