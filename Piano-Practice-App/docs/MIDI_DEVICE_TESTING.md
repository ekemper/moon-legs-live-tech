# Testing: Connect a New MIDI Device While the App Is Running

How the flow works and how to debug it.

---

## Flow

1. **App is running** — Backend and frontend are up; WebSocket is connected.
2. **You plug in a MIDI keyboard** (or turn it on).
3. **Device list updates automatically:** A background task polls `mido.get_input_names()` every **3 seconds**. When the list changes, the backend sends `{ type: "midi_devices", devices: [...] }` to the frontend and the dropdown updates.
4. **You select the new device** in the dropdown. The frontend sends `{ type: "midi_device_select", deviceId: "<port name>" }`.
5. **Backend opens the port** via `midi_handler.open(device_id)` and either:
   - Sends `{ type: "midi_device", deviceId, config }` if the device was used before (saved config), or
   - Sends `{ type: "init_workflow", deviceId, step: "low" }` and waits for you to play lowest then highest note to save key range.

---

## How to Test

1. **Start the app** (backend + frontend). Leave the MIDI device **unplugged** or off.
2. **Confirm dropdown** shows current devices (e.g. empty or existing ports).
3. **Plug in (or turn on) the keyboard.**
4. **Wait up to ~3 seconds:** The dropdown should update (backend log: `MIDI device list changed: ... -> [...]`). To confirm the poller is running when nothing changes, look for `MIDI device poller: list unchanged (N devices), next check in 3s` every ~30 seconds.
5. **Select the new device** in the dropdown.
6. **Backend logs:** You should see `midi_device_select: ...`, then either `connected ... with saved config` or `connected ..., starting init_workflow`.
7. **If init_workflow:** Play lowest key, then highest key; backend logs `MIDI init_workflow: completed for ...`.
8. **Play notes** — they should trigger sound and green/red feedback.

---

## Backend Logs to Watch

| When | Log (INFO) |
|------|------------|
| Backend import | `MIDI backend: mido.backends.rtmidi` then `MIDI at startup: N input port(s) [...]` |
| In Docker (Mac) | `Backend is running in Docker. USB MIDI devices on the host are not visible here. ...` |
| Poller started | `MIDI device poller started (interval=3.0s)` |
| Poller sees new list | `MIDI device list changed: <old> -> <new>, pushing to client` |
| Poller running, list unchanged | `MIDI device poller: list unchanged (N devices), next check in 3s` (every ~30s) |
| You select a device | `WS recv: type=midi_device_select ...` then `midi_device_select: deviceId=...` |
| Open succeeds (saved config) | `midi_device_select: connected "<name>" with saved config {...}` |
| Open succeeds (first time) | `midi_device_select: connected "<name>", starting init_workflow (no saved config)` |
| Init: press lowest/highest | `MIDI init_workflow: started for device ...` then `MIDI init_workflow: completed for ...` |
| Open fails | `midi_device_select: open failed for "<name>": ...` and `MIDI open: failed to open ...` |

MIDI listing is also logged: `MIDI list_devices: found N port(s) [...]` when the list is fetched (each poll). If listing fails (e.g. no `python-rtmidi`), you get a one-time warning: `MIDI list_devices failed: ...`.

---

## Troubleshooting

- **USB device not found (polling always shows 0 ports):**
  - **Running backend in Docker?** On macOS, the container cannot see the host’s USB or CoreMIDI. You’ll see a startup log: `Backend is running in Docker. USB MIDI devices on the host are not visible here.` **Fix:** Run the backend on the host (e.g. `uvicorn backend.main:app --reload` from the project root). Keep the frontend in Docker or run it with `npm run dev`; point it at the host backend.
  - **Backend on host (macOS):** The app forces `mido.backends.rtmidi/MACOSX_CORE` on macOS so CoreMIDI is used (avoids the `API_UNSPECIFIED` bug in some mido/python-rtmidi combos). Check startup for `MIDI backend: mido.backends.rtmidi/MACOSX_CORE` and `MIDI at startup: N input port(s) [...]`. If you see `0 input port(s) []`, plug in the USB keyboard and wait a few seconds for the next poll. Confirm the device appears in **Audio MIDI Setup** (Applications → Utilities → Window → Show MIDI Studio). If it’s not there, macOS isn’t seeing the device (cable/port/power). Ensure `python-rtmidi` is installed (`pip install python-rtmidi`).
- **Device in System Report (USB) but not in Audio MIDI Setup:** macOS sees the USB device but CoreMIDI doesn’t. Try: (1) **Plug directly into the Mac** — avoid USB hubs; many keyboards (e.g. Alesis Recital) only show up in MIDI Studio when connected directly. (2) **Audio MIDI Setup → Window → Show MIDI Studio → Rescan MIDI**. (3) **Reset MIDI configuration:** unplug all MIDI devices, Audio MIDI Setup → Configuration → New Configuration…, name it, OK, then plug the keyboard in and click Rescan MIDI. (4) Try a different USB cable (must be data-capable) and another port.
- **Dropdown doesn’t update after plugging in:** Wait up to 3 seconds for the next poll. Check backend logs for `MIDI device list changed` or `MIDI device poller: list unchanged` to confirm the poller is running, and for `MIDI list_devices failed` (install `python-rtmidi` if needed).
- **Device appears but selecting it does nothing:** Check backend for `midi_device_select: open failed` or `no device_id resolved`. Ensure the `deviceId` in the dropdown matches a port name from `mido.get_input_names()`.
- **Init workflow doesn’t complete:** Play one note for “lowest”, then a higher note for “highest”. Backend must see two distinct note-on events. Check for `MIDI init_workflow: completed` in the logs.
