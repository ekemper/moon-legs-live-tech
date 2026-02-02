"""SuperCollider: check if running, start if not, OSC client for note on/off."""

from __future__ import annotations

import asyncio
import logging
import socket
import subprocess
from pathlib import Path
from collections import defaultdict

from pythonosc import udp_client

from backend.config import SC_BOOT_TIMEOUT_SEC, SC_BOOTSTRAP_SCRIPT, SC_HOST, SC_PORT

logger = logging.getLogger(__name__)


def _make_osc_client(host: str = SC_HOST, port: int = SC_PORT) -> udp_client.SimpleUDPClient:
    return udp_client.SimpleUDPClient(host, port)


def _osc_status_bytes() -> bytes:
    """Build OSC /status message (address + type tag, no args). OSC 1.0: 4-byte aligned."""
    # Address "/status" + null = 8 bytes; type tag "," + null, pad to 4 = 4 bytes
    return b"/status\x00" + b",\x00\x00\x00"


def _check_sc_running_sync(host: str = SC_HOST, port: int = SC_PORT, timeout: float = 2.0) -> bool:
    """Sync: send OSC /status, wait for reply. Used from asyncio.to_thread."""
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind(("0.0.0.0", 0))
    sock.settimeout(timeout)
    try:
        sock.sendto(_osc_status_bytes(), (host, port))
        sock.recv(1024)
        return True
    except (socket.timeout, OSError):
        return False
    finally:
        sock.close()


async def check_sc_running(host: str = SC_HOST, port: int = SC_PORT, timeout: float = 2.0) -> bool:
    """Return True if scsynth responds to /status within timeout."""
    loop = asyncio.get_event_loop()
    result = await loop.run_in_executor(None, _check_sc_running_sync, host, port, timeout)
    logger.info("check_sc_running %s:%s -> %s", host, port, result)
    return result


def start_sc(bootstrap_script: str | Path | None = None) -> subprocess.Popen | None:
    """Start SuperCollider by running sclang bootstrap.scd. Returns Popen or None on failure."""
    script = Path(bootstrap_script or SC_BOOTSTRAP_SCRIPT)
    if not script.exists():
        logger.warning("start_sc: script does not exist %s", script)
        return None
    try:
        proc = subprocess.Popen(
            ["sclang", str(script)],
            stdin=subprocess.DEVNULL,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            cwd=str(script.parent),
        )
        logger.info("start_sc: started sclang %s (PID %s)", script, proc.pid)
        return proc
    except FileNotFoundError as e:
        logger.warning("start_sc: sclang not found: %s", e)
        return None


class SCClient:
    """OSC client for Rhodes: note on/off with velocity and volume-scaled amp."""

    def __init__(self, host: str = SC_HOST, port: int = SC_PORT):
        self._client = _make_osc_client(host, port)
        self._volume = 0.8  # 0-1
        self._node_id = 1000
        # (channel, note) -> list of node ids (LIFO for note off)
        self._active_nodes: dict[tuple[int, int], list[int]] = defaultdict(list)

    def set_volume(self, value: float) -> None:
        self._volume = max(0.0, min(1.0, value))

    def _next_node_id(self) -> int:
        n = self._node_id
        self._node_id += 1
        if self._node_id > 0x7FFF:
            self._node_id = 1000
        return n

    def note_on(self, note: int, velocity: int, channel: int = 0) -> None:
        vel = velocity / 127.0 if velocity else 0.5
        amp = 0.3 * self._volume * (0.3 + 0.7 * vel)
        node_id = self._next_node_id()
        self._active_nodes[(channel, note)].append(node_id)
        logger.debug("SC note_on note=%s vel=%s ch=%s node_id=%s", note, velocity, channel, node_id)
        # /s_new defName nodeID addAction targetID [paramName paramValue ...]
        self._client.send_message(
            "/s_new",
            ["rhodes", node_id, 0, 0, "note", note, "gate", 1, "vel", vel, "amp", amp],
        )

    def note_off(self, note: int, channel: int = 0) -> None:
        key = (channel, note)
        if not self._active_nodes[key]:
            return
        node_id = self._active_nodes[key].pop()
        logger.debug("SC note_off note=%s ch=%s node_id=%s", note, channel, node_id)
        self._client.send_message("/n_set", [node_id, "gate", 0])
        if not self._active_nodes[key]:
            del self._active_nodes[key]
