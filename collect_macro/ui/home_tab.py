"""Home tab — concise live control centre and activity log."""

from __future__ import annotations

import customtkinter as ctk

from collect_macro.automation.states import MacroAction
from collect_macro.ui.theme import (
    ACCENT,
    DANGER,
    DANGER_HOVER,
    FONT_FAMILY,
    SUCCESS,
    SUCCESS_HOVER,
    TEXT_MUTED,
    TEXT_PRIMARY,
)
from collect_macro.ui.widgets import RoundedCard, StatCard


class HomeTab(ctk.CTkFrame):
    def __init__(self, master, on_start, on_stop, **kwargs) -> None:
        super().__init__(master, fg_color="transparent", **kwargs)
        self._on_start = on_start
        self._on_stop = on_stop
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(2, weight=1)

        self.status_var = ctk.StringVar(value="Ready to start")
        self.tool_var = ctk.StringVar(value="Conveyor")
        self.countdown_var = ctk.StringVar(value="—")
        self.cycles_var = ctk.StringVar(value="0")
        self.runtime_var = ctk.StringVar(value="0:00:00")
        self._is_running = False

        self._build_controls()
        self._build_stats()
        self._build_log()

    def _build_controls(self) -> None:
        controls = RoundedCard(self)
        controls.grid(row=0, column=0, sticky="ew", padx=8, pady=(8, 6))
        controls.grid_columnconfigure(0, weight=1)
        controls.grid_columnconfigure(1, weight=0)

        copy = ctk.CTkFrame(controls, fg_color="transparent")
        copy.grid(row=0, column=0, sticky="w", padx=20, pady=18)
        ctk.CTkLabel(
            copy, text="Automation control", font=(FONT_FAMILY, 20, "bold"), text_color=TEXT_PRIMARY,
        ).pack(anchor="w")
        ctk.CTkLabel(
            copy, text="Select a tool, then let the cycle handle the routine.",
            font=(FONT_FAMILY, 12), text_color=TEXT_MUTED,
        ).pack(anchor="w", pady=(3, 0))

        action_row = ctk.CTkFrame(controls, fg_color="transparent")
        action_row.grid(row=0, column=1, sticky="e", padx=18, pady=18)
        self.start_btn = ctk.CTkButton(
            action_row, text="Start macro", width=140, height=44,
            font=(FONT_FAMILY, 14, "bold"), fg_color=SUCCESS, hover_color=SUCCESS_HOVER,
            command=self._on_start,
        )
        self.start_btn.grid(row=0, column=0, padx=(0, 8))
        self.stop_btn = ctk.CTkButton(
            action_row, text="Stop", width=104, height=44,
            font=(FONT_FAMILY, 14, "bold"), fg_color=DANGER, hover_color=DANGER_HOVER,
            command=self._on_stop, state="disabled",
        )
        self.stop_btn.grid(row=0, column=1)

    def _build_stats(self) -> None:
        stat_row = ctk.CTkFrame(self, fg_color="transparent")
        stat_row.grid(row=1, column=0, sticky="ew", padx=8, pady=6)
        for col in range(5):
            stat_row.grid_columnconfigure(col, weight=1, uniform="stats")

        self._status_card = StatCard(stat_row, "Current action", self.status_var, ACCENT)
        self._status_card.grid(row=0, column=0, padx=(0, 5), sticky="ew")
        StatCard(stat_row, "Selected tool", self.tool_var, TEXT_PRIMARY).grid(row=0, column=1, padx=5, sticky="ew")
        StatCard(stat_row, "Cycle remaining", self.countdown_var, "#F7C65A").grid(row=0, column=2, padx=5, sticky="ew")
        StatCard(stat_row, "Completed cycles", self.cycles_var, "#58D59A").grid(row=0, column=3, padx=5, sticky="ew")
        StatCard(stat_row, "Total runtime", self.runtime_var, "#A99BFF").grid(row=0, column=4, padx=(5, 0), sticky="ew")

    def _build_log(self) -> None:
        log_card = RoundedCard(self)
        log_card.grid(row=2, column=0, sticky="nsew", padx=8, pady=(6, 8))
        log_card.grid_rowconfigure(1, weight=1)
        log_card.grid_columnconfigure(0, weight=1)

        heading = ctk.CTkFrame(log_card, fg_color="transparent")
        heading.grid(row=0, column=0, sticky="ew", padx=16, pady=(14, 7))
        heading.grid_columnconfigure(0, weight=1)
        ctk.CTkLabel(heading, text="Activity", font=(FONT_FAMILY, 15, "bold"), text_color=TEXT_PRIMARY).grid(
            row=0, column=0, sticky="w"
        )
        self._log_count_var = ctk.StringVar(value="LIVE LOG")
        ctk.CTkLabel(
            heading, textvariable=self._log_count_var, font=(FONT_FAMILY, 10, "bold"),
            text_color=TEXT_MUTED,
        ).grid(row=0, column=1, sticky="e")

        self.log_box = ctk.CTkTextbox(
            log_card, wrap="word", activate_scrollbars=True, fg_color="#121419",
            border_width=1, border_color="#252832", text_color="#C7CBD4", font=("Cascadia Mono", 11),
        )
        self.log_box.grid(row=1, column=0, sticky="nsew", padx=14, pady=(0, 14))
        self.log_box.configure(state="disabled")

    def set_running(self, running: bool) -> None:
        self._is_running = running
        self.start_btn.configure(state="disabled" if running else "normal")
        self.stop_btn.configure(state="normal" if running else "disabled")
        if not running and self.status_var.get() == "Idle":
            self.status_var.set("Ready to start")

    def set_action(self, action: MacroAction) -> None:
        label = "Ready to start" if action is MacroAction.IDLE else action.value
        self.status_var.set(label)

    def set_grind_tool(self, name: str) -> None:
        self.tool_var.set(name)

    def set_countdown(self, seconds: float) -> None:
        self.countdown_var.set("—" if seconds <= 0 else f"{seconds:.1f}s")

    def set_stats(self, cycles: int, runtime_sec: float, countdown: float) -> None:
        self.cycles_var.set(str(cycles))
        self.runtime_var.set(self._format_runtime(runtime_sec))
        self.set_countdown(countdown)

    @staticmethod
    def _format_runtime(sec: float) -> str:
        sec = int(sec)
        h, rem = divmod(sec, 3600)
        m, s = divmod(rem, 60)
        return f"{h}:{m:02d}:{s:02d}"

    def append_log(self, line: str) -> None:
        self.log_box.configure(state="normal")
        self.log_box.insert("end", line + "\n")
        self.log_box.see("end")
        self.log_box.configure(state="disabled")

    def load_log_snapshot(self, lines: list[str]) -> None:
        self.log_box.configure(state="normal")
        self.log_box.delete("1.0", "end")
        self.log_box.insert("end", "\n".join(lines) + ("\n" if lines else ""))
        self.log_box.configure(state="disabled")
