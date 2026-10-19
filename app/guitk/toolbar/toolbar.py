from tkinter import ttk
from typing import Callable

from app import log
from ..utils import ticons
from .tootlbar_handler import ToolbarHandler


class ToolBar(ttk.Frame):
    def __init__(self, parent, actions_controller: ToolbarHandler, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)

        self._actions_controller = actions_controller

        self.buttons = (
            ToolBarButton(
                self,
                text="Открыть",
                image=ticons.ticon(ticons.I_OPEN_FILE),
                compound="left",
                command=self.__open_db,
            ),
            ToolBarButton(
                self,
                text="Создать",
                command=self.__create_db,
                image=ticons.ticon(ticons.I_CREATE_FILE),
                compound="left",
            ),
            ToolBarButton(
                self,
                text="Добавить том",
                command=self.__show_add_volume,
                image=ticons.ticon(ticons.I_ADD_ITEM),
                compound="left",
            ),
            # ToolBarButton(self, text="Импортировать том", command=self.__show_import_volume, image=ticons.ticon(ticons.I_IMPORT), compound="left"),
            ToolBarButton(
                self,
                text="BackUP",
                command=self._create_db_backup,
                image=ticons.ticon(ticons.I_SAVE_AS),
                compound="left",
            ),
            ToolBarButton(
                self,
                text="Поиск",
                command=self._show_find_modal,
                image=ticons.ticon(ticons.I_FIND),
                compound="left",
            ),
        )

        for btn in self.buttons:
            btn.pack(side="left", ipadx=10, ipady=10)

    def __open_db(self):
        self._actions_controller.show_open_db()

    def __create_db(self):
        self._actions_controller.show_create_db()

    def _create_db_backup(self):
        self._actions_controller.backup_db()

    def _show_find_modal(self):
        self._actions_controller.show_find_modal()

    def __show_add_volume(self):
        self._actions_controller.show_add_volume()

    # def __show_import_volume(self):
    #     dbus.emit(dbus.SHOW_IMPORT_VOLUME)


class ToolBarButton(ttk.Label):
    def __init__(self, master, command: Callable[[], None], **kwargs):
        super(ToolBarButton, self).__init__(master, **kwargs)

        self._command = command

        self.bind("<Button-1>", self._on_click)

    def _on_click(self, event):
        try:
            self._command()
        except Exception as e:
            log.exception(e)
