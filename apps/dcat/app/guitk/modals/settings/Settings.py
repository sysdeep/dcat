import tkinter
from tkinter import ttk

from app.guitk.utils import ticons
from app.lib.user_settings import UserSettings, UpdateUserSettingsModel

from .FrameHistory import FrameHistory
from .FrameStyle import FrameStyle


class Settings(tkinter.Toplevel):
    def __init__(self, master, us: UserSettings, *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        self._us = us
        self.title("Настройкие")

        self.maxsize(400, 300)
        self.minsize(400, 300)

        self.main_frame = ttk.Frame(self, padding=10)
        self.main_frame.pack(expand=True, fill="both", side="top")

        self.tabs = ttk.Notebook(self.main_frame)
        self.tabs.pack(fill="both", expand=True)

        self.frame_history = FrameHistory(self.tabs, self._us)
        self.tabs.add(self.frame_history, text="История")

        self.frame_style = FrameStyle(self.tabs)
        self.tabs.add(self.frame_style, text="Стиль")

        # --- controls
        controls_frame = ttk.Frame(self.main_frame)
        controls_frame.pack(fill="both", side="bottom", padx=5, pady=5)

        ttk.Button(
            controls_frame,
            text="Закрыть(Ctrl+w)",
            command=self.destroy,
            image=ticons.ticon(ticons.CLOSE),
            compound="left",
        ).pack(side="right")

        ttk.Button(
            controls_frame, text="Сохранить", command=self.apply, image=ticons.ticon(ticons.SAVE), compound="left"
        ).pack(side="left")

        self.bind_all("<Control-w>", lambda e: self.destroy())

    def apply(self):
        model = UpdateUserSettingsModel()

        self.frame_history.apply_changes(model)
        self.frame_style.apply_changes(model)

        self._us.set_settings(model)
