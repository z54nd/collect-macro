"""Resolve config and resource paths for dev and PyInstaller frozen builds."""

from __future__ import annotations

import os
import sys
from pathlib import Path


def is_frozen() -> bool:
    return getattr(sys, "frozen", False) and hasattr(sys, "_MEIPASS")


def app_data_dir() -> Path:
    if sys.platform == "win32":
        base = os.environ.get("APPDATA")
        if base:
            return Path(base) / "CollectMacro"
    return Path.home() / ".collect-macro"


def config_file_path() -> Path:
    """Prefer config beside exe when frozen; otherwise APPDATA (or home on Mac dev)."""
    if is_frozen():
        exe_dir = Path(sys.executable).resolve().parent
        beside = exe_dir / "config.json"
        if beside.exists() or not app_data_dir().joinpath("config.json").exists():
            return beside
    return app_data_dir() / "config.json"


def ensure_config_parent() -> Path:
    path = config_file_path()
    path.parent.mkdir(parents=True, exist_ok=True)
    return path
