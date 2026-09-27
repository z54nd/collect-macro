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


def leave_game(settings: Settings, cancel_check: Callable[[], bool], log: Callable[[str], None]) -> bool:
    if cancel_check():
        return False
    if log:
        log("Leaving game (Esc menu sequence)…")
    time.sleep(max(0.0, settings.leave_delay_sec))
    if cancel_check():
        return False

    tap_key("esc")
    time.sleep(settings.leave_esc_delay_sec)
    if cancel_check():
        return False

    if settings.leave_use_leave_key_sequence:
        # Typical in-game menu: first item may be Resume; Leave is often below.
        tap_key("down")
        time.sleep(settings.leave_menu_nav_delay_sec)
        if cancel_check():
            return False
        tap_key("enter")
        time.sleep(settings.leave_confirm_delay_sec)
    else:
        press_key("esc")

    if log:
        log("Leave sequence sent.")
    return True
