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
from collect_macro.ui.theme import ACCENT, APP_BG, CARD_BORDER, CARD_FG, FONT_FAMILY, TEXT_MUTED, TEXT_PRIMARY


class CollectMacroApp(ctk.CTk):
    def __init__(self) -> None:
        super().__init__()
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")

        self.title("Collect Macro")
        self.geometry("980x700")
        self.minsize(820, 580)
        self.configure(fg_color=APP_BG)

        self._settings = load_settings()
        self._last_state = MacroAction.IDLE
        self._activity = ActivityLog()
        self._activity.add_listener(self._on_log_line)

        self._engine = MacroEngine(
            settings_provider=lambda: self._settings,
            activity_log=self._activity,
            on_state=self._on_engine_state,
            on_stats=self._on_engine_stats,
            on_finished=self._on_engine_finished,
        )
        self._hotkey = EmergencyHotkey(self._emergency_stop)

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)

        header = ctk.CTkFrame(self, fg_color="transparent")
        header.grid(row=0, column=0, sticky="ew", padx=22, pady=(18, 7))
        header.grid_columnconfigure(0, weight=1)
        ctk.CTkLabel(header, text="COLLECT MACRO", font=(FONT_FAMILY, 21, "bold"), text_color=TEXT_PRIMARY).grid(
            row=0, column=0, sticky="w"
        )
        ctk.CTkLabel(
            header, text="Simple desktop automation", font=(FONT_FAMILY, 12), text_color=TEXT_MUTED,
        ).grid(row=1, column=0, sticky="w", pady=(2, 0))
        self._mode_badge = ctk.CTkLabel(
            header, text="  READY  ", height=26, corner_radius=13,
            fg_color="#20372B", text_color="#71DA9D", font=(FONT_FAMILY, 10, "bold"),
        )
        self._mode_badge.grid(row=0, column=1, rowspan=2, sticky="e")

        self.tabs = ctk.CTkTabview(
            self, fg_color=APP_BG, segmented_button_fg_color=CARD_FG,
            segmented_button_selected_color=ACCENT, segmented_button_selected_hover_color="#6848E8",
            segmented_button_unselected_color=CARD_FG, segmented_button_unselected_hover_color="#242730",
            border_width=1, border_color=CARD_BORDER,
        )
        self.tabs.grid(row=1, column=0, sticky="nsew", padx=14, pady=(0, 14))
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
        def update() -> None:
            self._last_state = state
            self.home.set_action(state)
            if state is MacroAction.ERROR:
                self._mode_badge.configure(text="  CHECK LOG  ", fg_color="#41242A", text_color="#FF9BA5")
            elif state is MacroAction.IDLE:
                self._mode_badge.configure(text="  READY  ", fg_color="#20372B", text_color="#71DA9D")
            else:
                self._mode_badge.configure(text="  RUNNING  ", fg_color="#2D2750", text_color="#B9AEFF")

        self.after(0, update)

    def _on_engine_finished(self) -> None:
        def update() -> None:
            self.home.set_running(False)
            if self._last_state is not MacroAction.ERROR:
                self._mode_badge.configure(text="  READY  ", fg_color="#20372B", text_color="#71DA9D")

        self.after(0, update)

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
        try:
            current_settings = self.settings_tab.collect()
        except ValueError:
            self.tabs.set("Settings")
            self.settings_tab.show_error("Check the numeric values in Settings before starting.")
            return
        errors = current_settings.validate()
        if errors:
            self.tabs.set("Settings")
            self.settings_tab.show_error("; ".join(errors))
            return
        self._settings = current_settings
        self.home.set_grind_tool(self._settings.grind_tool)
        self._restart_hotkey()
        if self._settings.remember_settings:
            save_settings(self._settings)
        self.home.set_running(True)
        self._engine.start()

    def _stop(self) -> None:
        self._engine.stop()
        self.home.set_running(False)
        self._mode_badge.configure(text="  READY  ", fg_color="#20372B", text_color="#71DA9D")

    def _emergency_stop(self) -> None:
        self.after(0, lambda: (self._activity.log("Emergency stop hotkey pressed."), self._stop()))

    def _on_close(self) -> None:
        self._hotkey.stop()
        self._engine.stop()
        if self._settings.remember_settings:
            save_settings(self._settings)
        self.destroy()
