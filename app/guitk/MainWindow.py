#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import logging
import tkinter
from tkinter import ttk
from tkinter.filedialog import *

from app.storage import get_storage
from app.lib import dbus
from app.lib.user_settings import UserSettings, UpdateUserSettingsModel
from app.rc import VERSION

from .modals.ModalsCtrl import ModalsCtrl
from .main_menu import MainMenu, MainMenuHandler
from .explorer import Explorer
from .DBInfo import DBInfo
from .toolbar import ToolBar, ToolbarHandler
from .utils import ticons


from .Ctrl import Ctrl


class MainWindow(tkinter.Tk, ToolbarHandler, MainMenuHandler):
    def __init__(self, us: UserSettings):
        super().__init__()

        self._us = us

        self.name = "DCat"
        self.title(self.name)
        self.minsize(800, 400)

        self.app_icon = ticons.real_icon("app.png")
        # self.option_add("*Font", ("Play", 12))				# до создания виджетов
        self.iconphoto(self, self.app_icon)

        self.storage = get_storage()
        self.ctrl = Ctrl()

        self._logger = logging.getLogger("app")

        # --- menu
        self.menu_bar = MainMenu(parent=self, actions_controller=self)

        # --- toolbar
        self.tool_bar = ToolBar(parent=self, actions_controller=self)
        self.tool_bar.pack(side="top", expand=False, fill="x")

        # --- explorer
        self.explorer_frame = Explorer(parent=self, us=self._us)
        self.explorer_frame.pack(side="top", fill="both", expand=True)
        # self.explorer_frame.v_list.set_cb_open_modal_add_volume(self.__on_show_modal_add_volume)

        # --- db info
        self.db_info = DBInfo(self)
        self.db_info.pack(side="bottom", fill="x", expand=False)

        self.modal_add_volume = None

        self.modals_ctrl = ModalsCtrl(main_win=self, us=self._us)

        # TODO: use user settings for theme
        style = ttk.Style()
        # print(style.theme_names())
        # print(style.theme_use())
        style.theme_use("clam")

        # self.tk.eval("source themes/pkgIndex.tcl")
        # self.tk.call("package", "require", "ttkthemes")
        # self.tk.call("ttk::setTheme", "plastik")
        # self.tk.call("ttk::setTheme", "aquativo")
        # self.tk.call("ttk::setTheme", "arc")
        # self.tk.call("ttk::setTheme", "elegance")
        # self.tk.call("ttk::setTheme", "blue")
        # self.tk.call("ttk::setTheme", "clearlooks")
        # self.tk.call("ttk::setTheme", "radiance")
        # self.tk.call("ttk::setTheme", "winxpblue")

        # style.configure("TButton", font=("Play", 12))
        # style.configure(".", font=("Play", 10))
        # style.configure(".", font=("Ubuntu", 10))

        # --- открываем последний
        self._check_open_last()

        # --- events
        dbus.eon(dbus.REQUEST_OPEN_DB, self.__on_open_db)  # открытие заданной базы

    # interfaces --------------------------------------------------------------
    def backup_db(self):
        self._logger.debug("action backup")
        self.storage.create_current_backup()

    def show_find_modal(self):
        # TODO: избавится от шины
        dbus.emit(dbus.SHOW_FIND)

    def show_open_db(self):
        self.__on_show_open_db()

    def show_create_db(self):
        self.__on_create_db()

    def show_add_volume(self):
        dbus.emit(dbus.SHOW_ADD_VOLUME)

    # private -----------------------------------------------------------------
    def _check_open_last(self):
        # если в настройках флаг открывать последний
        settings = self._us.get_settings()
        if not settings.open_last:
            return

        if len(settings.lastbases) == 0:
            return

        last = settings.lastbases[-1]
        self.__on_open_db(last)

    def __update_db_info(self):
        """обновление информации по базе"""
        self.db_info.set_path(self.storage.storage_path)
        # self.db_info.set_sysinfo(self.storage.fetch_system())

    def __on_create_db(self):
        """запрос создания базы"""

        title = "Расположение новой базы"
        db_path = asksaveasfilename(defaultextension=".dcat", title=title)
        if db_path:
            self.storage.close_storage()
            self.storage.create_storage(db_path)

            self.explorer_frame.refresh()
            self.__update_db_info()
            self._update_last_base(db_path)
            self.__update_title(db_path)

    def __on_open_db(self, db_path):
        """запрос на открытие базы по заданному пути"""

        self.storage.close_storage()
        self.storage.open_storage(db_path)

        self.explorer_frame.refresh()
        self.__update_db_info()

        self._update_last_base(db_path)
        self.__update_title(db_path)

    def __on_show_modal_add_volume(self):
        """вызов события для отоьражения модала добавления тома"""
        dbus.emit(dbus.SHOW_ADD_VOLUME)

    def __on_show_open_db(self):
        """отобразить модал выбора базы для открытия"""
        inpath = askopenfilename(title="Выбор базы", defaultextension=".dcat", filetypes=[("DCat files", ".dcat")])

        if inpath:
            inpath = os.path.normpath(inpath)
            self.__on_open_db(inpath)

    def __update_title(self, db_path):
        text = "{} v{} - {}".format(self.name, VERSION, db_path)
        self.title(text)

    def act_exit(self):
        self.quit()

    def _update_last_base(self, db_path: str):
        """
        обновление списка последних баз.
                если база есть в списке - удалем её и добавляем в конец
                если кол-во записей больше максимального - очищаем старые
        Args:
                value 	[string] - путь до базы
        """

        settings = self._us.get_settings()

        # удаляем если есть
        new_bases = [b for b in settings.lastbases if b != db_path]

        # урезаем если привысили лимит
        if len(new_bases) > 15:
            new_bases = new_bases[1:]

        # добавляем
        new_bases.append(db_path)

        save_settings = UpdateUserSettingsModel(lastbases=new_bases)
        self._us.set_settings(save_settings)
