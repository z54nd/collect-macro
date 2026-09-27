"""Settings tab, grouped around the macro's actual flow."""

from __future__ import annotations

import sys
from tkinter import filedialog

import customtkinter as ctk

from collect_macro.config.defaults import GRIND_TOOLS
from collect_macro.config.models import Settings
from collect_macro.ui.theme import ACCENT, ACCENT_HOVER, FONT_FAMILY, TEXT_MUTED, TEXT_PRIMARY
from collect_macro.ui.widgets import RoundedCard


class SettingsTab(ctk.CTkFrame):
    def __init__(self, master, on_save, **kwargs) -> None:
        super().__init__(master, fg_color="transparent", **kwargs)
        self._on_save = on_save
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        scroll = ctk.CTkScrollableFrame(self, fg_color="transparent")
        scroll.grid(row=0, column=0, sticky="nsew")
        scroll.grid_columnconfigure(0, weight=1)

        intro = ctk.CTkFrame(scroll, fg_color="transparent")
        intro.grid(row=0, column=0, sticky="ew", padx=12, pady=(10, 4))
        ctk.CTkLabel(intro, text="Settings", font=(FONT_FAMILY, 20, "bold"), text_color=TEXT_PRIMARY).pack(anchor="w")
        ctk.CTkLabel(
            intro, text="Tune the timing to your machine and keep the routine predictable.",
            font=(FONT_FAMILY, 12), text_color=TEXT_MUTED,
        ).pack(anchor="w", pady=(2, 0))

        routine = self._section(scroll, 1, "Grind routine", "Tool selection and the interaction that starts it.")
        self.grind_tool = self._combo(routine, 0, "Grind tool", GRIND_TOOLS)
        self.conveyor_duration = self._entry(routine, 1, "Conveyor duration", "32", "seconds")
        self.magnet_duration = self._entry(routine, 2, "Magnet duration", "17", "seconds")
        self.grind_tool_key = self._entry(routine, 3, "Tool slot key", "1", "for example: 1")
        self.tool_activation_key = self._entry(routine, 4, "Activate tool key", "e", "sent after selecting the slot")
        self.tool_activation_delay = self._entry(routine, 5, "Activation delay", "0.35", "seconds after slot key")

        timing = self._section(scroll, 2, "Cycle timing", "Waiting and retry behavior between each run.")
        self.join_delay = self._entry(timing, 0, "Delay after joining", "25", "seconds")
        self.leave_delay = self._entry(timing, 1, "Delay before leaving", "2", "seconds")
        self.rejoin_delay = self._entry(timing, 2, "Delay before next cycle", "8", "seconds")
        self.join_retry_count = self._entry(timing, 3, "Join retry count", "3", "attempts")
        self.join_retry_delay = self._entry(timing, 4, "Retry delay", "10", "seconds")

        roblox = self._section(scroll, 3, "Roblox", "Choose how the app opens and exits the game.")
        self.roblox_path = self._entry(roblox, 0, "Roblox executable", "", "RobloxPlayerBeta.exe")
        if sys.platform == "win32":
            ctk.CTkButton(roblox, text="Browse", width=82, height=30, command=self._browse_roblox).grid(
                row=self._content_row(roblox, 0), column=3, padx=(0, 12), pady=7
            )
        self.auto_launch = self._switch(roblox, 1, "Launch Roblox when needed")
        self.auto_rejoin = self._switch(roblox, 2, "Rejoin after leaving")
        self.leave_esc_delay = self._entry(roblox, 3, "Leave menu delay", "0.8", "seconds after Esc")
        self.leave_nav_delay = self._entry(roblox, 4, "Leave navigation delay", "0.4", "seconds")

        app = self._section(scroll, 4, "Application", "Safety and local preferences.")
        self.emergency_hotkey = self._entry(app, 0, "Emergency stop hotkey", "f9", "for example: f9")
        self.start_minimized = self._switch(app, 1, "Start minimized")
        self.remember_settings = self._switch(app, 2, "Remember settings", default=True)

        ctk.CTkButton(
            scroll, text="Save settings", height=42, font=(FONT_FAMILY, 14, "bold"),
            fg_color=ACCENT, hover_color=ACCENT_HOVER, command=self._save_clicked,
        ).grid(row=5, column=0, pady=(8, 4), padx=12, sticky="ew")
        self.status_label = ctk.CTkLabel(scroll, text="", text_color=TEXT_MUTED, font=(FONT_FAMILY, 12))
        self.status_label.grid(row=6, column=0, padx=14, pady=(2, 12), sticky="w")

    def _section(self, parent, row: int, title: str, subtitle: str) -> RoundedCard:
        card = RoundedCard(parent)
        card.grid(row=row, column=0, sticky="ew", padx=12, pady=6)
        card.grid_columnconfigure(1, weight=1)
        ctk.CTkLabel(card, text=title, font=(FONT_FAMILY, 15, "bold"), text_color=TEXT_PRIMARY).grid(
            row=0, column=0, columnspan=4, padx=14, pady=(13, 0), sticky="w"
        )
        ctk.CTkLabel(card, text=subtitle, font=(FONT_FAMILY, 11), text_color=TEXT_MUTED).grid(
            row=1, column=0, columnspan=4, padx=14, pady=(1, 8), sticky="w"
        )
        card._content_row_offset = 2  # type: ignore[attr-defined]
        return card

    @staticmethod
    def _content_row(parent, row: int) -> int:
        return row + int(getattr(parent, "_content_row_offset", 0))

    def _browse_roblox(self) -> None:
        path = filedialog.askopenfilename(
            title="Select RobloxPlayerBeta.exe",
            filetypes=[("Roblox Player", "RobloxPlayerBeta.exe"), ("Executables", "*.exe")],
        )
        if path:
            self._set_entry(self.roblox_path, path)

    def _label(self, parent, row: int, text: str) -> None:
        row = self._content_row(parent, row)
        ctk.CTkLabel(parent, text=text, anchor="w", font=(FONT_FAMILY, 12), text_color=TEXT_PRIMARY).grid(
            row=row, column=0, sticky="w", padx=(14, 8), pady=7
        )

    def _entry(self, parent, row: int, label: str, default: str, hint: str) -> ctk.CTkEntry:
        self._label(parent, row, label)
        row = self._content_row(parent, row)
        entry = ctk.CTkEntry(parent, height=30)
        entry.insert(0, default)
        entry.grid(row=row, column=1, sticky="ew", padx=8, pady=7)
        ctk.CTkLabel(parent, text=hint, font=(FONT_FAMILY, 10), text_color=TEXT_MUTED).grid(
            row=row, column=2, sticky="w", padx=(0, 14), pady=7
        )
        return entry

    def _combo(self, parent, row: int, label: str, values: tuple[str, ...]) -> ctk.CTkComboBox:
        self._label(parent, row, label)
        row = self._content_row(parent, row)
        combo = ctk.CTkComboBox(parent, values=list(values), height=30)
        combo.set(values[0])
        combo.grid(row=row, column=1, sticky="ew", padx=8, pady=7)
        ctk.CTkLabel(parent, text="active duration is set below", font=(FONT_FAMILY, 10), text_color=TEXT_MUTED).grid(
            row=row, column=2, sticky="w", padx=(0, 14), pady=7
        )
        return combo

    def _switch(self, parent, row: int, label: str, default: bool = False) -> ctk.CTkSwitch:
        self._label(parent, row, label)
        row = self._content_row(parent, row)
        var = ctk.StringVar(value="on" if default else "off")
        sw = ctk.CTkSwitch(parent, text="", variable=var, onvalue="on", offvalue="off", width=42)
        if default:
            sw.select()
        sw.grid(row=row, column=1, sticky="w", padx=8, pady=7)
        sw._cm_var = var  # type: ignore[attr-defined]
        return sw

    @staticmethod
    def _switch_val(sw: ctk.CTkSwitch) -> bool:
        var = getattr(sw, "_cm_var", None)
        return bool(var and var.get() == "on")

    def populate(self, settings: Settings) -> None:
        self.grind_tool.set(settings.grind_tool)
        self._set_entry(self.conveyor_duration, settings.conveyor_duration_sec)
        self._set_entry(self.magnet_duration, settings.magnet_duration_sec)
        self._set_entry(self.grind_tool_key, settings.grind_tool_key)
        self._set_entry(self.tool_activation_key, settings.tool_activation_key)
        self._set_entry(self.tool_activation_delay, settings.tool_activation_delay_sec)
        self._set_entry(self.join_delay, settings.join_delay_sec)
        self._set_entry(self.leave_delay, settings.leave_delay_sec)
        self._set_entry(self.rejoin_delay, settings.rejoin_delay_sec)
        self._set_entry(self.roblox_path, settings.roblox_exe_path)
        self._set_switch(self.auto_launch, settings.auto_launch_roblox)
        self._set_switch(self.auto_rejoin, settings.auto_rejoin)
        self._set_entry(self.emergency_hotkey, settings.emergency_stop_hotkey)
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
            tool_activation_key=self.tool_activation_key.get().strip() or "e",
            tool_activation_delay_sec=float(self.tool_activation_delay.get()),
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

    def show_error(self, message: str) -> None:
        self.status_label.configure(text=message, text_color="#FF8D99")

    def _save_clicked(self) -> None:
        try:
            settings = self.collect()
        except ValueError:
            self.show_error("Use valid numbers for durations, delays, and retry counts.")
            return
        errors = settings.validate()
        if errors:
            self.show_error("; ".join(errors))
            return
        self._on_save(settings)
        self.status_label.configure(text="Settings saved locally.", text_color="#65D99A")
