"""Reusable UI widgets."""

from __future__ import annotations

import customtkinter as ctk

from collect_macro.ui.theme import CARD_BORDER, CARD_FG


class RoundedCard(ctk.CTkFrame):
    def __init__(self, master, **kwargs) -> None:
        kwargs.setdefault("fg_color", CARD_FG)
        kwargs.setdefault("corner_radius", 14)
        kwargs.setdefault("border_width", 1)
        kwargs.setdefault("border_color", CARD_BORDER)
        super().__init__(master, **kwargs)
