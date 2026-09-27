"""Leave game using keyboard simulation (Esc menu navigation).

Roblox menu layout can vary by client version and resolution. Default sequence:
  Esc → wait → Down (highlight Leave) → Enter → wait

Users can tune delays in Settings. Document in README that manual verification is recommended.
"""

from __future__ import annotations

import time
from typing import Callable

from collect_macro.config.models import Settings
from collect_macro.roblox.input_backend import press_key, tap_key


def _wait_or_cancel(seconds: float, cancel_check: Callable[[], bool]) -> bool:
    """Sleep in short slices so an emergency stop is never held by a delay."""
    deadline = time.monotonic() + max(0.0, seconds)
    while time.monotonic() < deadline:
        if cancel_check():
            return False
        time.sleep(min(0.1, deadline - time.monotonic()))
    return not cancel_check()


def leave_game(settings: Settings, cancel_check: Callable[[], bool], log: Callable[[str], None]) -> bool:
    if cancel_check():
        return False
    if log:
        log("Leaving game (Esc menu sequence)…")
    if not _wait_or_cancel(settings.leave_delay_sec, cancel_check):
        return False

    tap_key("esc")
    if not _wait_or_cancel(settings.leave_esc_delay_sec, cancel_check):
        return False

    if settings.leave_use_leave_key_sequence:
        # Typical in-game menu: first item may be Resume; Leave is often below.
        tap_key("down")
        if not _wait_or_cancel(settings.leave_menu_nav_delay_sec, cancel_check):
            return False
        tap_key("enter")
        if not _wait_or_cancel(settings.leave_confirm_delay_sec, cancel_check):
            return False
    else:
        press_key("esc")

    if log:
        log("Leave sequence sent.")
    return True
