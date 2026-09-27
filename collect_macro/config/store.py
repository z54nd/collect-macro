"""Load and save settings JSON."""

from __future__ import annotations

import json
from pathlib import Path

from collect_macro.config.defaults import DEFAULT_SETTINGS
from collect_macro.config.models import Settings
from collect_macro.config.paths import config_file_path, ensure_config_parent


def load_settings() -> Settings:
    path = config_file_path()
    if not path.is_file():
        return Settings.from_dict(DEFAULT_SETTINGS)
    try:
        with path.open("r", encoding="utf-8") as f:
            data = json.load(f)
        return Settings.from_dict(data)
    except (json.JSONDecodeError, OSError, TypeError):
        return Settings.from_dict(DEFAULT_SETTINGS)


def save_settings(settings: Settings) -> Path:
    path = ensure_config_parent()
    payload = settings.to_dict()
    with path.open("w", encoding="utf-8") as f:
        json.dump(payload, f, indent=2)
    return path
