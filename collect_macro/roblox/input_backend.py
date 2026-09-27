"""Keyboard/mouse input abstraction (pynput + pyautogui)."""

from __future__ import annotations

import sys
from typing import Any

import pyautogui

pyautogui.FAILSAFE = True
pyautogui.PAUSE = 0.05

try:
    from pynput.keyboard import Controller as KeyboardController
    from pynput.keyboard import Key
except ImportError:  # pragma: no cover
    KeyboardController = None  # type: ignore[misc, assignment]
    Key = None  # type: ignore[misc, assignment]

_keyboard = KeyboardController() if KeyboardController else None

_KEY_ALIASES: dict[str, Any] = {}


def _init_aliases() -> None:
    global _KEY_ALIASES
    if _KEY_ALIASES or Key is None:
        return
    _KEY_ALIASES = {
        "esc": Key.esc,
        "escape": Key.esc,
        "enter": Key.enter,
        "return": Key.enter,
        "tab": Key.tab,
        "space": Key.space,
        "down": Key.down,
        "up": Key.up,
        "left": Key.left,
        "right": Key.right,
    }


def _resolve_key(name: str) -> Any:
    _init_aliases()
    key = name.strip().lower()
    if len(key) == 1:
        return key
    if Key is not None and key in _KEY_ALIASES:
        return _KEY_ALIASES[key]
    if key.startswith("f") and key[1:].isdigit():
        fnum = int(key[1:])
        if Key is not None and 1 <= fnum <= 20:
            return getattr(Key, f"f{fnum}", key)
    return key


def tap_key(name: str) -> None:
    resolved = _resolve_key(name)
    if _keyboard is not None:
        _keyboard.press(resolved)
        _keyboard.release(resolved)
    else:
        pyautogui.press(name if len(name) == 1 else name.lower())


def press_key(name: str) -> None:
    resolved = _resolve_key(name)
    if _keyboard is not None:
        _keyboard.press(resolved)
    else:
        pyautogui.keyDown(name)


def release_key(name: str) -> None:
    resolved = _resolve_key(name)
    if _keyboard is not None:
        _keyboard.release(resolved)
    else:
        pyautogui.keyUp(name)


def type_grind_key(key_name: str) -> None:
    tap_key(key_name)


def platform_note() -> str:
    if sys.platform != "win32":
        return "Input automation is intended for Windows; running in dry/stub mode may be limited."
    return ""
