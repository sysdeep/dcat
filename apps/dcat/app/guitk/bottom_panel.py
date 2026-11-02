from tkinter import ttk

from app.lib import dbus
from app.storage import Storage
from .utils import ticons


class BottomPanel(ttk.Frame):
    """BottomPanel - нижняя панель с информацией"""

    def __init__(self, master, storage: Storage, app_version: str):
        super().__init__(master)
        self._storage = storage

        self.configure(padding=5)

        # app version -------------------------------------
        self._label_app_version = ttk.Label(self, text=f"v {app_version}")
        self._label_app_version.pack(side="left")

        # database path -----------------------------------
        self._label_db_path = ttk.Label(self, text="---")
        self._label_db_path.pack(side="left", padx=10)

        # buttons -----------------------------------------
        # close
        ttk.Button(
            self,
            text="Закрыть",
            image=ticons.ticon(ticons.CLOSE),
            compound="left",
            command=self.__on_exit,
        ).pack(side="right")

        # dbinfo
        ttk.Button(
            self,
            text="Info",
            image=ticons.ticon(ticons.INFO),
            compound="left",
            command=self.__show_info,
        ).pack(side="right", padx=5)

        # show databases
        ttk.Button(
            self,
            text="DBs",
            image=ticons.ticon(ticons.I_FOLDER_HOME),
            compound="left",
            command=self.__show_dbs,
        ).pack(side="right", padx=5)

        # connect to events -------------------------------
        self._storage.connect(Storage.Event.opened, self._on_storage_changed)
        self._storage.connect(Storage.Event.created, self._on_storage_changed)

    def __on_exit(self):
        # TODO: вынести из зоны ответственности этого компонента
        self.master.quit()

    def __show_info(self):
        # TODO: вынести из зоны ответственности этого компонента
        dbus.emit(dbus.SHOW_ABOUT_BASE)

    def __show_dbs(self):
        # TODO: вынести из зоны ответственности этого компонента
        dbus.emit(dbus.SHOW_DATABASES)

    def _on_storage_changed(self):
        self._label_db_path.config(text=self._storage.storage_path)
