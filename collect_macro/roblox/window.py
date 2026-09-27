"""Focus Roblox window (Windows-only; stubs elsewhere)."""

from __future__ import annotations

import sys
from typing import Callable

from collect_macro.roblox.process import get_primary_roblox_pid

if sys.platform == "win32":
    try:
        import win32con
        import win32gui
        import win32process
    except ImportError:  # pragma: no cover - dev on Mac
        win32con = win32gui = win32process = None  # type: ignore[misc, assignment]
else:
    win32con = win32gui = win32process = None  # type: ignore[misc, assignment]


def _roblox_window_predicate(hwnd: int) -> bool:
    if not win32gui or not win32gui.IsWindowVisible(hwnd):
        return False
    title = win32gui.GetWindowText(hwnd) or ""
    if "Roblox" not in title:
        return False
    pid = get_primary_roblox_pid()
    if pid is None:
        return True
    try:
        _, window_pid = win32process.GetWindowThreadProcessId(hwnd)
        return window_pid == pid
    except Exception:
        return True


def find_roblox_hwnd() -> int | None:
    if sys.platform != "win32" or not win32gui:
        return None
    found: list[int] = []

    def enum_handler(hwnd: int, _: int) -> None:
        if _roblox_window_predicate(hwnd):
            found.append(hwnd)

    try:
        win32gui.EnumWindows(enum_handler, 0)
    except Exception:
        return None
    return found[0] if found else None


def focus_roblox_window(log: Callable[[str], None] | None = None) -> bool:
    if sys.platform != "win32":
        if log:
            log("Window focus is only supported on Windows.")
        return False
    if not win32gui or not win32con:
        if log:
            log("pywin32 is not installed; cannot focus Roblox window.")
        return False
    hwnd = find_roblox_hwnd()
    if hwnd is None:
        if log:
            log("Roblox window not found.")
        return False
    try:
        win32gui.ShowWindow(hwnd, win32con.SW_RESTORE)
        win32gui.SetForegroundWindow(hwnd)
        if log:
            log("Focused Roblox window.")
        return True
    except Exception as exc:
        if log:
            log(f"Failed to focus Roblox window: {exc}")
        return False
