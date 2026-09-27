"""Launch Roblox and join experience via normal OS / protocol methods."""

from __future__ import annotations

import subprocess
import sys
import webbrowser
from pathlib import Path
from typing import Callable

from collect_macro.config.defaults import GAME_URL, JOIN_PROTOCOL_URL, PLACE_ID
from collect_macro.roblox.process import expand_windows_path, is_roblox_running


def launch_roblox(exe_path: str, log: Callable[[str], None] | None = None) -> bool:
    if is_roblox_running():
        if log:
            log("Roblox is already running; skipping launch.")
        return True
    if sys.platform != "win32":
        if log:
            log("Auto-launch requires Windows.")
        return False
    resolved = Path(expand_windows_path(exe_path))
    if not resolved.is_file():
        if log:
            log(f"Roblox executable not found: {resolved}")
        return False
    try:
        subprocess.Popen([str(resolved)], close_fds=True)
        if log:
            log(f"Launched Roblox: {resolved}")
        return True
    except OSError as exc:
        if log:
            log(f"Failed to launch Roblox: {exc}")
        return False


def join_experience(log: Callable[[str], None] | None = None) -> bool:
    """Join via roblox:// protocol (primary) with browser URL fallback."""
    if log:
        log(f"Joining place {PLACE_ID}…")
    if sys.platform == "win32":
        try:
            os_startfile = getattr(__import__("os"), "startfile")
            os_startfile(JOIN_PROTOCOL_URL)
            if log:
                log(f"Opened join URI: {JOIN_PROTOCOL_URL}")
            return True
        except OSError:
            pass
    try:
        webbrowser.open(JOIN_PROTOCOL_URL)
        if log:
            log("Opened join URI via default handler.")
        return True
    except Exception as exc:
        if log:
            log(f"Protocol join failed ({exc}); trying browser URL.")
    try:
        webbrowser.open(GAME_URL)
        if log:
            log(f"Opened game page: {GAME_URL}")
        return True
    except Exception as exc:
        if log:
            log(f"Join failed: {exc}")
        return False
