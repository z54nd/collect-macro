"""Automation action states for UI display."""

from __future__ import annotations

from enum import Enum


class MacroAction(str, Enum):
    IDLE = "Idle"
    LAUNCHING_ROBLOX = "Launching Roblox"
    JOINING_GAME = "Joining game"
    SELECTING_TOOL = "Selecting tool"
    GRINDING = "Grinding"
    LEAVING = "Leaving"
    WAITING = "Waiting"
    ERROR = "Error"
