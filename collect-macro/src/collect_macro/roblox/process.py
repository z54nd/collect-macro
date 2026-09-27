"""Roblox process detection via psutil."""

from __future__ import annotations

import os
import sys
from dataclasses import dataclass
from typing import Iterable

import psutil

ROBLOX_PROCESS_NAMES = ("RobloxPlayerBeta.exe", "RobloxPlayerBeta")


@dataclass(frozen=True)
class RobloxProcessInfo:
    pid: int
    name: str
    exe: str | None


def _normalize_name(name: str) -> str:
    return name.lower().replace(".exe", "")


def iter_roblox_processes() -> Iterable[RobloxProcessInfo]:
    targets = {_normalize_name(n) for n in ROBLOX_PROCESS_NAMES}
    for proc in psutil.process_iter(["pid", "name", "exe"]):
        try:
            info = proc.info
            name = info.get("name") or ""
            if _normalize_name(name) not in targets:
                continue
            yield RobloxProcessInfo(
                pid=int(info["pid"]),
                name=name,
                exe=info.get("exe"),
            )
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            continue


def is_roblox_running() -> bool:
    return next(iter_roblox_processes(), None) is not None


def get_primary_roblox_pid() -> int | None:
    procs = list(iter_roblox_processes())
    if not procs:
        return None
    return procs[0].pid


def expand_windows_path(path: str) -> str:
    if sys.platform != "win32":
        return os.path.expanduser(path)
    return os.path.expandvars(os.path.expanduser(path))
