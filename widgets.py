"""Reusable UI widgets."""

from __future__ import annotations

import customtkinter as ctk

from collect_macro.ui.theme import CARD_BORDER, CARD_FG, TEXT_MUTED


class RoundedCard(ctk.CTkFrame):
    def __init__(self, master, **kwargs) -> None:
        kwargs.setdefault("fg_color", CARD_FG)
        kwargs.setdefault("corner_radius", 16)
        kwargs.setdefault("border_width", 1)
        kwargs.setdefault("border_color", CARD_BORDER)
        super().__init__(master, **kwargs)


class StatCard(RoundedCard):
    def __init__(self, master, label: str, variable, accent: str, **kwargs) -> None:
        super().__init__(master, **kwargs)
        ctk.CTkLabel(
            self, text=label.upper(), text_color=TEXT_MUTED,
            font=("Segoe UI", 10, "bold"), anchor="w",
        ).pack(anchor="w", padx=14, pady=(12, 2))
        ctk.CTkLabel(
            self, textvariable=variable, text_color=accent,
            font=("Segoe UI", 18, "bold"), anchor="w",
        ).pack(anchor="w", padx=14, pady=(0, 13))
