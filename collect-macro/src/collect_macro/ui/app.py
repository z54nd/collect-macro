"""Main application window."""

from __future__ import annotations

import customtkinter as ctk

from collect_macro.automation.engine import EngineStats
from collect_macro.automation.hotkeys import EmergencyHotkey
from collect_macro.automation.states import MacroAction
from collect_macro.automation.engine import MacroEngine
from collect_macro.config.store import load_settings, save_settings
from collect_macro.config.models import Settings
from collect_macro.logging_util.activity_log import ActivityLog, LogLine
from collect_macro.ui.home_tab import HomeTab
from collect_macro.ui.settings_tab import SettingsTab


class CollectMacroApp(ctk.CTk):
    def __init__(self) -> None:
        super().__init__()
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")

        self.title("Collect Macro")
        self.geometry("720x640")
        self.minsize(640, 520)

        self._settings = load_settings()
        self._activity = ActivityLog()
        self._activity.add_listener(self._on_log_line)

        self._engine = MacroEngine(
            settings_provider=lambda: self._settings,
            activity_log=self._activity,
            on_state=self._on_engine_state,
            on_stats=self._on_engine_stats,
        )
        self._hotkey = EmergencyHotkey(self._emergency_stop)

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)

        header = ctk.CTkLabel(
            self,
            text="🎮  Collect Macro",
            font=("Segoe UI", 22, "bold"),
            anchor="w",
        )
        header.grid(row=0, column=0, sticky="ew", padx=16, pady=(14, 4))

        self.tabs = ctk.CTkTabview(self)
        self.tabs.grid(row=1, column=0, sticky="nsew", padx=12, pady=8)
        self.tabs.add("Home")
        self.tabs.add("Settings")

        self.home = HomeTab(self.tabs.tab("Home"), on_start=self._start, on_stop=self._stop)
        self.home.pack(fill="both", expand=True)

        self.settings_tab = SettingsTab(self.tabs.tab("Settings"), on_save=self._save_settings)
        self.settings_tab.pack(fill="both", expand=True)
        self.settings_tab.populate(self._settings)

        self.home.set_grind_tool(self._settings.grind_tool)
        self.home.load_log_snapshot(self._activity.snapshot())
        self._activity.log("Collect Macro ready.")

        self._restart_hotkey()
        if self._settings.start_minimized:
            self.after(100, self.iconify)

        self.protocol("WM_DELETE_WINDOW", self._on_close)

    def _restart_hotkey(self) -> None:
        self._hotkey.start(self._settings.emergency_stop_hotkey)

    def _on_log_line(self, line: LogLine) -> None:
        self.after(0, lambda: self.home.append_log(line.formatted()))

    def _on_engine_state(self, state: MacroAction) -> None:
        self.after(0, lambda: self.home.set_action(state))

    def _on_engine_stats(self, stats: EngineStats) -> None:
        def update() -> None:
            self.home.set_stats(stats.completed_cycles, stats.total_runtime_sec, stats.cycle_countdown_sec)

        self.after(0, update)

    def _save_settings(self, settings: Settings) -> None:
        self._settings = settings
        self.home.set_grind_tool(settings.grind_tool)
        if settings.remember_settings:
            path = save_settings(settings)
            self._activity.log(f"Settings saved to {path}.")
        self._restart_hotkey()

    def _start(self) -> None:
        if self._settings.remember_settings:
            self._settings = self.settings_tab.collect()
            save_settings(self._settings)
        self.home.set_running(True)
        self._engine.start()

    def _stop(self) -> None:
        self._engine.stop()
        self.home.set_running(False)

    def _emergency_stop(self) -> None:
        self.after(0, lambda: (self._activity.log("Emergency stop hotkey pressed."), self._stop()))

    def _on_close(self) -> None:
        self._hotkey.stop()
        self._engine.stop()
        if self._settings.remember_settings:
            save_settings(self._settings)
        self.destroy()
