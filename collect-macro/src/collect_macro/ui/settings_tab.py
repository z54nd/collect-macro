"""Settings tab."""

from __future__ import annotations

import sys
from tkinter import filedialog

import customtkinter as ctk

from collect_macro.config.defaults import GRIND_TOOLS
from collect_macro.config.models import Settings
from collect_macro.ui.theme import ACCENT, FONT_FAMILY
from collect_macro.ui.widgets import RoundedCard


class SettingsTab(ctk.CTkFrame):
    def __init__(self, master, on_save, **kwargs) -> None:
        super().__init__(master, fg_color="transparent", **kwargs)
        self._on_save = on_save
        self.grid_columnconfigure(0, weight=1)

        scroll = ctk.CTkScrollableFrame(self, fg_color="transparent")
        scroll.grid(row=0, column=0, sticky="nsew")
        scroll.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        card = RoundedCard(scroll)
        card.grid(row=0, column=0, sticky="ew", padx=8, pady=8)
        card.grid_columnconfigure(1, weight=1)

        row = 0
        self.grind_tool = self._combo(card, row, "Grind tool", GRIND_TOOLS)
        row += 1
        self.conveyor_duration = self._entry(card, row, "Conveyor duration (sec)", "32")
        row += 1
        self.magnet_duration = self._entry(card, row, "Magnet duration (sec)", "17")
        row += 1
        self.grind_tool_key = self._entry(card, row, "Grind tool key", "1")
        row += 1
        self.join_delay = self._entry(card, row, "Delay after joining (sec)", "25")
        row += 1
        self.leave_delay = self._entry(card, row, "Delay before leaving (sec)", "2")
        row += 1
        self.rejoin_delay = self._entry(card, row, "Delay before next cycle (sec)", "8")
        row += 1
        self.roblox_path = self._entry(card, row, "Roblox executable path", "")
        if sys.platform == "win32":
            ctk.CTkButton(
                card,
                text="Browse…",
                width=90,
                command=self._browse_roblox,
            ).grid(row=row, column=2, padx=8, pady=6)
        row += 1
        self.auto_launch = self._switch(card, row, "Auto launch Roblox")
        row += 1
        self.auto_rejoin = self._switch(card, row, "Auto rejoin after leaving")
        row += 1
        self.emergency_hotkey = self._entry(card, row, "Emergency stop hotkey", "f9")
        row += 1
        self.start_minimized = self._switch(card, row, "Start minimized")
        row += 1
        self.remember_settings = self._switch(card, row, "Remember settings", default=True)
        row += 1
        self.join_retry_count = self._entry(card, row, "Join retry count", "3")
        row += 1
        self.join_retry_delay = self._entry(card, row, "Join retry delay (sec)", "10")
        row += 1
        self.leave_esc_delay = self._entry(card, row, "Leave: Esc menu delay (sec)", "0.8")
        row += 1
        self.leave_nav_delay = self._entry(card, row, "Leave: menu nav delay (sec)", "0.4")
        row += 1

        ctk.CTkButton(
            scroll,
            text="Save settings",
            fg_color=ACCENT,
            command=self._save_clicked,
        ).grid(row=1, column=0, pady=12, padx=8, sticky="ew")

        self.status_label = ctk.CTkLabel(scroll, text="", text_color="#9CA3AF")
        self.status_label.grid(row=2, column=0, padx=8, pady=(0, 8), sticky="w")

    def _browse_roblox(self) -> None:
        path = filedialog.askopenfilename(
            title="Select RobloxPlayerBeta.exe",
            filetypes=[("Roblox Player", "RobloxPlayerBeta.exe"), ("Executables", "*.exe")],
        )
        if path:
            self.roblox_path.delete(0, "end")
            self.roblox_path.insert(0, path)

    def _label(self, parent, row: int, text: str) -> None:
        ctk.CTkLabel(parent, text=text, anchor="w", font=(FONT_FAMILY, 13)).grid(
            row=row, column=0, sticky="w", padx=14, pady=8
        )

    def _entry(self, parent, row: int, label: str, default: str) -> ctk.CTkEntry:
        self._label(parent, row, label)
        entry = ctk.CTkEntry(parent)
        entry.insert(0, default)
        entry.grid(row=row, column=1, sticky="ew", padx=8, pady=6)
        return entry

    def _combo(self, parent, row: int, label: str, values: tuple[str, ...]) -> ctk.CTkComboBox:
        self._label(parent, row, label)
        combo = ctk.CTkComboBox(parent, values=list(values))
        combo.set(values[0])
        combo.grid(row=row, column=1, sticky="ew", padx=8, pady=6)
        return combo

    def _switch(self, parent, row: int, label: str, default: bool = False) -> ctk.CTkSwitch:
        self._label(parent, row, label)
        var = ctk.StringVar(value="on" if default else "off")
        sw = ctk.CTkSwitch(parent, text="", variable=var, onvalue="on", offvalue="off")
        if default:
            sw.select()
        sw.grid(row=row, column=1, sticky="w", padx=8, pady=6)
        sw._cm_var = var  # type: ignore[attr-defined]
        return sw

    @staticmethod
    def _switch_val(sw: ctk.CTkSwitch) -> bool:
        try:
            return int(sw.get()) == 1
        except (TypeError, ValueError):
            var = getattr(sw, "_cm_var", None)
            return bool(var and var.get() == "on")

    def populate(self, settings: Settings) -> None:
        self.grind_tool.set(settings.grind_tool)
        self._set_entry(self.conveyor_duration, settings.conveyor_duration_sec)
        self._set_entry(self.magnet_duration, settings.magnet_duration_sec)
        self.grind_tool_key.delete(0, "end")
        self.grind_tool_key.insert(0, settings.grind_tool_key)
        self._set_entry(self.join_delay, settings.join_delay_sec)
        self._set_entry(self.leave_delay, settings.leave_delay_sec)
        self._set_entry(self.rejoin_delay, settings.rejoin_delay_sec)
        self.roblox_path.delete(0, "end")
        self.roblox_path.insert(0, settings.roblox_exe_path)
        self._set_switch(self.auto_launch, settings.auto_launch_roblox)
        self._set_switch(self.auto_rejoin, settings.auto_rejoin)
        self.emergency_hotkey.delete(0, "end")
        self.emergency_hotkey.insert(0, settings.emergency_stop_hotkey)
        self._set_switch(self.start_minimized, settings.start_minimized)
        self._set_switch(self.remember_settings, settings.remember_settings)
        self._set_entry(self.join_retry_count, settings.join_retry_count)
        self._set_entry(self.join_retry_delay, settings.join_retry_delay_sec)
        self._set_entry(self.leave_esc_delay, settings.leave_esc_delay_sec)
        self._set_entry(self.leave_nav_delay, settings.leave_menu_nav_delay_sec)

    @staticmethod
    def _set_entry(entry: ctk.CTkEntry, value) -> None:
        entry.delete(0, "end")
        entry.insert(0, str(value))

    @staticmethod
    def _set_switch(sw: ctk.CTkSwitch, on: bool) -> None:
        if on:
            sw.select()
        else:
            sw.deselect()

    def collect(self) -> Settings:
        return Settings(
            grind_tool=self.grind_tool.get(),
            conveyor_duration_sec=int(float(self.conveyor_duration.get())),
            magnet_duration_sec=int(float(self.magnet_duration.get())),
            grind_tool_key=self.grind_tool_key.get().strip() or "1",
            join_delay_sec=float(self.join_delay.get()),
            leave_delay_sec=float(self.leave_delay.get()),
            rejoin_delay_sec=float(self.rejoin_delay.get()),
            roblox_exe_path=self.roblox_path.get().strip(),
            auto_launch_roblox=self._switch_val(self.auto_launch),
            auto_rejoin=self._switch_val(self.auto_rejoin),
            emergency_stop_hotkey=self.emergency_hotkey.get().strip().lower() or "f9",
            start_minimized=self._switch_val(self.start_minimized),
            remember_settings=self._switch_val(self.remember_settings),
            join_retry_count=int(float(self.join_retry_count.get())),
            join_retry_delay_sec=float(self.join_retry_delay.get()),
            leave_esc_delay_sec=float(self.leave_esc_delay.get()),
            leave_menu_nav_delay_sec=float(self.leave_nav_delay.get()),
        )

    def _save_clicked(self) -> None:
        settings = self.collect()
        errors = settings.validate()
        if errors:
            self.status_label.configure(text="; ".join(errors), text_color="#EF4444")
            return
        self._on_save(settings)
        self.status_label.configure(text="Settings saved.", text_color="#22C55E")
