"""Default configuration values."""

from __future__ import annotations

PLACE_ID = 133363783004873
GAME_URL = "https://www.roblox.com/games/133363783004873/Collect-1-Million-Items"
JOIN_PROTOCOL_URL = f"roblox://experiences/start?placeId={PLACE_ID}"

DEFAULT_ROBLOX_EXE = r"%LOCALAPPDATA%\Roblox\Versions\RobloxPlayerBeta.exe"

GRIND_TOOLS = ("Conveyor", "Magnet")

DEFAULT_SETTINGS: dict = {
    "grind_tool": "Conveyor",
    "conveyor_duration_sec": 32,
    "magnet_duration_sec": 17,
    "grind_tool_key": "1",
    "tool_activation_key": "e",
    "tool_activation_delay_sec": 0.35,
    "join_delay_sec": 25.0,
    "leave_delay_sec": 2.0,
    "rejoin_delay_sec": 8.0,
    "roblox_exe_path": DEFAULT_ROBLOX_EXE,
    "auto_launch_roblox": True,
    "auto_rejoin": True,
    "emergency_stop_hotkey": "f9",
    "start_minimized": False,
    "remember_settings": True,
    "join_retry_count": 3,
    "join_retry_delay_sec": 10.0,
    "leave_esc_delay_sec": 0.8,
    "leave_menu_nav_delay_sec": 0.4,
    "leave_confirm_delay_sec": 0.5,
    "leave_use_leave_key_sequence": True,
}
