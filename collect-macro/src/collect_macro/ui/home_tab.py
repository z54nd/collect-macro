"""Home tab — start/stop, status, log."""

from __future__ import annotations

import customtkinter as ctk

from collect_macro.automation.states import MacroAction
from collect_macro.ui.theme import ACCENT, DANGER, FONT_FAMILY, SUCCESS
from collect_macro.ui.widgets import RoundedCard


class HomeTab(ctk.CTkFrame):
    def __init__(self, master, on_start, on_stop, **kwargs) -> None:
        super().__init__(master, fg_color="transparent", **kwargs)
        self._on_start = on_start
        self._on_stop = on_stop
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(2, weight=1)

        controls = RoundedCard(self)
        controls.grid(row=0, column=0, sticky="ew", padx=8, pady=(8, 4))
        controls.grid_columnconfigure((0, 1), weight=1)

        self.start_btn = ctk.CTkButton(
            controls,
            text="▶  Start",
            height=52,
            font=(FONT_FAMILY, 18, "bold"),
            fg_color=SUCCESS,
            hover_color="#16A34A",
            command=self._on_start,
        )
        self.start_btn.grid(row=0, column=0, padx=12, pady=12, sticky="ew")

        self.stop_btn = ctk.CTkButton(
            controls,
            text="■  Stop",
            height=52,
            font=(FONT_FAMILY, 18, "bold"),
            fg_color=DANGER,
            hover_color="#DC2626",
            command=self._on_stop,
            state="disabled",
        )
        self.stop_btn.grid(row=0, column=1, padx=12, pady=12, sticky="ew")

        status_card = RoundedCard(self)
        status_card.grid(row=1, column=0, sticky="ew", padx=8, pady=4)
        for i in range(4):
            status_card.grid_columnconfigure(i, weight=1)

        self.status_var = ctk.StringVar(value="Idle")
        self.tool_var = ctk.StringVar(value="—")
        self.countdown_var = ctk.StringVar(value="—")
        self.cycles_var = ctk.StringVar(value="0")
        self.runtime_var = ctk.StringVar(value="0:00:00")

        self._stat_block(status_card, 0, "Status", self.status_var)
        self._stat_block(status_card, 1, "Grind tool", self.tool_var)
        self._stat_block(status_card, 2, "Countdown", self.countdown_var)
        self.cycles_runtime_var = ctk.StringVar(value="0 · 0:00:00")
        self._stat_block(status_card, 3, "Cycles / Runtime", self.cycles_runtime_var)

        log_card = RoundedCard(self)
        log_card.grid(row=2, column=0, sticky="nsew", padx=8, pady=(4, 8))
        log_card.grid_rowconfigure(1, weight=1)
        log_card.grid_columnconfigure(0, weight=1)

        ctk.CTkLabel(
            log_card,
            text="Activity log",
            font=(FONT_FAMILY, 14, "bold"),
            anchor="w",
        ).grid(row=0, column=0, sticky="w", padx=14, pady=(12, 4))

        self.log_box = ctk.CTkTextbox(log_card, wrap="word", activate_scrollbars=True)
        self.log_box.grid(row=1, column=0, sticky="nsew", padx=12, pady=(0, 12))
        self.log_box.configure(state="disabled")

    def _stat_block(self, parent, col: int, title: str, var: ctk.StringVar) -> None:
        frame = ctk.CTkFrame(parent, fg_color="transparent")
        frame.grid(row=0, column=col, sticky="nsew", padx=8, pady=12)
        ctk.CTkLabel(frame, text=title, text_color="#9CA3AF", font=(FONT_FAMILY, 12)).pack(anchor="w")
        ctk.CTkLabel(
            frame,
            textvariable=var,
            font=(FONT_FAMILY, 16, "bold"),
            text_color=ACCENT,
            anchor="w",
        ).pack(anchor="w")

    def set_running(self, running: bool) -> None:
        self.start_btn.configure(state="disabled" if running else "normal")
        self.stop_btn.configure(state="normal" if running else "disabled")

    def set_action(self, action: MacroAction) -> None:
        self.status_var.set(action.value)

    def set_grind_tool(self, name: str) -> None:
        self.tool_var.set(name)

    def set_countdown(self, seconds: float) -> None:
        if seconds <= 0:
            self.countdown_var.set("—")
        else:
            self.countdown_var.set(f"{seconds:.1f}s")

    def set_stats(self, cycles: int, runtime_sec: float, countdown: float) -> None:
        self.cycles_var.set(str(cycles))
        runtime_text = self._format_runtime(runtime_sec)
        self.runtime_var.set(runtime_text)
        self.cycles_runtime_var.set(f"{cycles} · {runtime_text}")
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
        for line in lines:
            self.log_box.insert("end", line + "\n")
        self.log_box.configure(state="disabled")
