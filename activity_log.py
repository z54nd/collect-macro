"""Thread-safe activity log for UI display."""

from __future__ import annotations

import threading
from collections import deque
from dataclasses import dataclass
from datetime import datetime
from typing import Callable


@dataclass(frozen=True)
class LogLine:
    timestamp: str
    message: str

    def formatted(self) -> str:
        return f"[{self.timestamp}] {self.message}"


class ActivityLog:
    def __init__(self, max_lines: int = 500) -> None:
        self._lock = threading.Lock()
        self._lines: deque[LogLine] = deque(maxlen=max_lines)
        self._listeners: list[Callable[[LogLine], None]] = []

    def add_listener(self, callback: Callable[[LogLine], None]) -> None:
        with self._lock:
            self._listeners.append(callback)

    def remove_listener(self, callback: Callable[[LogLine], None]) -> None:
        with self._lock:
            if callback in self._listeners:
                self._listeners.remove(callback)

    def log(self, message: str) -> None:
        line = LogLine(datetime.now().strftime("%H:%M:%S"), message)
        listeners: list[Callable[[LogLine], None]]
        with self._lock:
            self._lines.append(line)
            listeners = list(self._listeners)
        for cb in listeners:
            try:
                cb(line)
            except Exception:
                pass

    def snapshot(self) -> list[str]:
        with self._lock:
            return [ln.formatted() for ln in self._lines]
