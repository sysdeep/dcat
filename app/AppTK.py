#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import signal
from .guitk import MainWindow
from app.lib.user_settings import UserSettings


class AppTK(object):
    def __init__(self):
        # --- перехват системных сигналов
        signal.signal(signal.SIGINT, self.__signal_handler)  # обработка Ctrl+C

        # NOTE: use system settings
        user_settings = UserSettings(file_path=None)

        # --- главное окно
        self.gui = MainWindow(us=user_settings)

    def start(self):
        self.gui.mainloop()

        sys.exit(0)

    def __signal_handler(self, signum, frame):
        """обработчик сигнала завершения от системы"""
        print("перехвачен сигнал SIGINT(Ctrl+C)")
        print("запрос на выход из cmd")
        self.gui.act_exit()
