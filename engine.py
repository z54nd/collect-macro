"""Cancellable macro cycle engine."""

from __future__ import annotations

import threading
import time
from dataclasses import dataclass, field
from typing import Callable

from collect_macro.automation.states import MacroAction
from collect_macro.config.models import Settings
from collect_macro.logging_util.activity_log import ActivityLog
from collect_macro.roblox import focus_roblox_window, is_roblox_running, join_experience, launch_roblox
from collect_macro.roblox.input_backend import type_grind_key
from collect_macro.roblox.leave import leave_game


@dataclass
class EngineStats:
    completed_cycles: int = 0
    total_runtime_sec: float = 0.0
    cycle_countdown_sec: float = 0.0


class MacroEngine:
    def __init__(
        self,
        settings_provider: Callable[[], Settings],
        activity_log: ActivityLog,
        on_state: Callable[[MacroAction], None] | None = None,
        on_stats: Callable[[EngineStats], None] | None = None,
    ) -> None:
        self._settings_provider = settings_provider
        self._log = activity_log
        self._on_state = on_state
        self._on_stats = on_stats
        self._cancel = threading.Event()
        self._thread: threading.Thread | None = None
        self._stats = EngineStats()
        self._stats_lock = threading.Lock()
        self._running = False
        self._session_start: float | None = None

    @property
    def is_running(self) -> bool:
        return self._running

    def get_stats(self) -> EngineStats:
        with self._stats_lock:
            runtime = self._stats.total_runtime_sec
            if self._session_start is not None:
                runtime += time.monotonic() - self._session_start
            return EngineStats(
                completed_cycles=self._stats.completed_cycles,
                total_runtime_sec=runtime,
                cycle_countdown_sec=self._stats.cycle_countdown_sec,
            )

    def start(self) -> None:
        if self._running:
            return
        self._cancel.clear()
        self._session_start = time.monotonic()
        self._running = True
        self._thread = threading.Thread(target=self._run, name="MacroEngine", daemon=True)
        self._thread.start()
        self._log.log("Macro started.")

    def stop(self) -> None:
        if not self._running:
            return
        self._cancel.set()
        self._log.log("Stop requested.")
        if self._thread and self._thread.is_alive():
            self._thread.join(timeout=5.0)
        self._finalize_session()
        self._set_state(MacroAction.IDLE)

    def _finalize_session(self) -> None:
        if self._session_start is not None:
            with self._stats_lock:
                self._stats.total_runtime_sec += time.monotonic() - self._session_start
            self._session_start = None
        self._running = False
        self._push_stats()

    def _set_state(self, state: MacroAction) -> None:
        if self._on_state:
            self._on_state(state)

    def _push_stats(self) -> None:
        if self._on_stats:
            self._on_stats(self.get_stats())

    def _wait(self, seconds: float, state: MacroAction = MacroAction.WAITING) -> bool:
        """Wait with countdown; return False if cancelled."""
        self._set_state(state)
        end = time.monotonic() + max(0.0, seconds)
        while time.monotonic() < end:
            if self._cancel.is_set():
                return False
            remaining = end - time.monotonic()
            with self._stats_lock:
                self._stats.cycle_countdown_sec = max(0.0, remaining)
            self._push_stats()
            time.sleep(min(0.25, remaining))
        with self._stats_lock:
            self._stats.cycle_countdown_sec = 0.0
        self._push_stats()
        return True

    def _join_with_retries(self, settings: Settings) -> bool:
        attempts = max(1, settings.join_retry_count)
        for attempt in range(1, attempts + 1):
            if self._cancel.is_set():
                return False
            self._set_state(MacroAction.JOINING_GAME)
            self._log.log(f"Join attempt {attempt}/{attempts}.")
            if not join_experience(self._log.log):
                self._log.log("Join command failed.")
            if self._wait(settings.join_delay_sec, MacroAction.JOINING_GAME):
                if is_roblox_running():
                    return True
            if attempt < attempts:
                self._log.log(f"Join may have failed; retrying in {settings.join_retry_delay_sec}s.")
                if not self._wait(settings.join_retry_delay_sec):
                    return False
        self._set_state(MacroAction.ERROR)
        self._log.log("Join failed after all retries.")
        return False

    def _run_cycle(self, settings: Settings) -> bool:
        if settings.auto_launch_roblox:
            self._set_state(MacroAction.LAUNCHING_ROBLOX)
            if not is_roblox_running():
                if not launch_roblox(settings.roblox_exe_path, self._log.log):
                    self._set_state(MacroAction.ERROR)
                    return False
                if not self._wait(5.0, MacroAction.LAUNCHING_ROBLOX):
                    return False
            else:
                self._log.log("Roblox already running.")

        if not self._join_with_retries(settings):
            return False

        if self._cancel.is_set():
            return False

        focus_roblox_window(self._log.log)

        self._set_state(MacroAction.SELECTING_TOOL)
        self._log.log(f"Selecting grind tool key '{settings.grind_tool_key}'.")
        type_grind_key(settings.grind_tool_key)
        time.sleep(0.3)

        grind_sec = settings.grind_duration_sec()
        self._log.log(f"Grinding with {settings.grind_tool} for {grind_sec:.0f}s.")
        if not self._wait(grind_sec, MacroAction.GRINDING):
            return False

        self._set_state(MacroAction.LEAVING)
        focus_roblox_window(self._log.log)
        leave_game(settings, lambda: self._cancel.is_set(), self._log.log)

        if self._cancel.is_set():
            return False

        if not self._wait(settings.rejoin_delay_sec):
            return False

        with self._stats_lock:
            self._stats.completed_cycles += 1
        self._push_stats()
        self._log.log(f"Cycle complete ({self._stats.completed_cycles}).")
        return True

    def _run(self) -> None:
        try:
            while not self._cancel.is_set():
                settings = self._settings_provider()
                errors = settings.validate()
                if errors:
                    self._set_state(MacroAction.ERROR)
                    self._log.log("; ".join(errors))
                    break

                if not self._run_cycle(settings):
                    break

                if not settings.auto_rejoin:
                    self._log.log("Auto rejoin disabled; stopping after one cycle.")
                    break

                if self._cancel.is_set():
                    break

                if not is_roblox_running():
                    self._set_state(MacroAction.ERROR)
                    self._log.log("Roblox closed unexpectedly.")
                    if settings.auto_launch_roblox:
                        self._log.log("Will attempt relaunch on next cycle.")
                    else:
                        break
        except Exception as exc:
            self._set_state(MacroAction.ERROR)
            self._log.log(f"Engine error: {exc}")
        finally:
            self._finalize_session()
            self._log.log("Macro stopped.")
