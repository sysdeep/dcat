#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
{
    "version": "0.1",
    "lastbases": [
        "/home/nia/Development/_Python/_DCat/reanimator.dcat",
        "/home/nia/Development/_Python/_DCat/3.dcat",
        "/home/nia/Development/_Python/_DCat/2.dcat",
        "/home/nia/Development/_Python/_DCat/1.dcat"
    ],
    "open_last": 1
}
"""

import tkinter
from tkinter import ttk

from app.lib.user_settings import UserSettings, UpdateUserSettingsModel


class FrameHistory(ttk.Frame):
    def __init__(self, master, us: UserSettings, *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        self._us = us

        self.config(padding=10)

        self._autoload_flag = False
        self._var_autoloading = tkinter.BooleanVar()

        settings_frame = ttk.Frame(self)
        settings_frame.pack(side="top", fill="x")

        ttk.Checkbutton(settings_frame, text="Автозагрузка базы:", variable=self._var_autoloading).pack(side="left")

        controls_frame = ttk.Frame(self)
        controls_frame.pack(side="bottom", fill="x")

        # TODO
        # ttk.Button(controls_frame, text="Очистить историю", command=self.__clear_history).pack(side="right")

        self.__load()

    def __load(self):
        self._autoload_flag = self._us.get_settings().open_last
        self._var_autoloading.set(self._autoload_flag)

    # TODO
    # def __clear_history(self):
    #     # self.usettings.clear_lastbases()
    #     pass

    def apply_changes(self, model: UpdateUserSettingsModel):
        autoload_flag = self._var_autoloading.get()
        if autoload_flag != self._autoload_flag:
            model.open_last = autoload_flag
