"""Settings model."""

from __future__ import annotations

from dataclasses import asdict, dataclass, field
from typing import Any

from collect_macro.config.defaults import DEFAULT_SETTINGS, GRIND_TOOLS


@dataclass
class Settings:
    grind_tool: str = "Conveyor"
    conveyor_duration_sec: int = 32
    magnet_duration_sec: int = 17
    grind_tool_key: str = "1"
    tool_activation_key: str = "e"
    tool_activation_delay_sec: float = 0.35
    join_delay_sec: float = 25.0
    leave_delay_sec: float = 2.0
    rejoin_delay_sec: float = 8.0
    roblox_exe_path: str = DEFAULT_SETTINGS["roblox_exe_path"]
    auto_launch_roblox: bool = True
    auto_rejoin: bool = True
    emergency_stop_hotkey: str = "f9"
    start_minimized: bool = False
    remember_settings: bool = True
    join_retry_count: int = 3
    join_retry_delay_sec: float = 10.0
    leave_esc_delay_sec: float = 0.8
    leave_menu_nav_delay_sec: float = 0.4
    leave_confirm_delay_sec: float = 0.5
    leave_use_leave_key_sequence: bool = True

    def grind_duration_sec(self) -> float:
        if self.grind_tool == "Magnet":
            return float(self.magnet_duration_sec)
        return float(self.conveyor_duration_sec)

    def validate(self) -> list[str]:
        errors: list[str] = []
        if self.grind_tool not in GRIND_TOOLS:
            errors.append(f"Invalid grind tool: {self.grind_tool}")
        if not self.grind_tool_key.strip():
            errors.append("Grind tool key cannot be empty.")
        if not self.tool_activation_key.strip():
            errors.append("Tool activation key cannot be empty.")
        if self.tool_activation_delay_sec < 0:
            errors.append("Tool activation delay cannot be negative.")
        if self.conveyor_duration_sec < 1 or self.magnet_duration_sec < 1:
            errors.append("Grind durations must be at least 1 second.")
        return errors

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> Settings:
        merged = {**DEFAULT_SETTINGS, **(data or {})}
        known = {f.name for f in cls.__dataclass_fields__.values()}  # type: ignore[attr-defined]
        filtered = {k: v for k, v in merged.items() if k in known}
        return cls(**filtered)

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)
