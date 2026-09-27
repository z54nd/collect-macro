"""Global emergency stop hotkey via pynput."""

from __future__ import annotations

import threading
from typing import Callable

from pynput import keyboard


class EmergencyHotkey:
    def __init__(self, on_trigger: Callable[[], None]) -> None:
        self._on_trigger = on_trigger
        self._listener: keyboard.GlobalHotKeys | None = None
        self._lock = threading.Lock()
        self._hotkey_str = "<f9>"

    @staticmethod
    def normalize(hotkey: str) -> str:
        key = hotkey.strip().lower()
        if not key.startswith("<"):
            key = f"<{key}>"
        return key

    def start(self, hotkey: str) -> None:
        self.stop()
        self._hotkey_str = self.normalize(hotkey)
        mapping = {self._hotkey_str: self._trigger}
        self._listener = keyboard.GlobalHotKeys(mapping)
        self._listener.start()

    def stop(self) -> None:
        with self._lock:
            if self._listener is not None:
                try:
                    self._listener.stop()
                except Exception:
                    pass
                self._listener = None

    def _trigger(self) -> None:
        self._on_trigger()
