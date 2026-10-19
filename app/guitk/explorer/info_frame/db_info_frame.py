from dataclasses import dataclass
import os
from tkinter import ttk

from app.storage import Storage, defs
from app.lib.fsize import naturalsize


class IRow(object):
    def __init__(self, parent, title: str):
        self._parent = parent
        self._title = title

        lkey_text = self._title + ": "
        self.lkey = ttk.Label(self._parent, text=lkey_text)
        self.vkey = ttk.Label(self._parent, text="")

    def update(self, value: str):
        self.vkey.config(text=value)


@dataclass
class DBInfo:
    db_path: str
    size: int
    version: str
    created_at: str
    updated_at: str


class DBInfoFrame(ttk.Frame):
    """database info"""

    def __init__(self, parent, storage: Storage, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)

        self._storage = storage

        # title -------------------------------------------
        ttk.Label(self, text="Свойства базы").pack(side="top")

        # table -------------------------------------------
        self.__grid = ttk.Frame(self)
        self.__grid.pack(side="top", expand=True, fill="both")

        self._r_path = IRow(self.__grid, "Название")
        self._r_size = IRow(self.__grid, "Размер")
        self._r_version = IRow(self.__grid, "Версия")
        self._r_created = IRow(self.__grid, "Создание")
        self._r_updated = IRow(self.__grid, "Обновление")

        items = [
            self._r_path,
            self._r_size,
            self._r_version,
            self._r_created,
            self._r_updated,
        ]

        for i, irow in enumerate(items):
            irow.lkey.grid(row=i, column=0, sticky="e")
            irow.vkey.grid(row=i, column=1, sticky="w")

        # connect -----------------------------------------
        self._storage.connect(Storage.Event.opened, self._on_db_opened_event)

    # private -------------------------------------------------------
    def _on_db_opened_event(self):
        db_info = self.extract_dbinfo(self._storage)
        db_name = os.path.basename(db_info.db_path)

        view_size = naturalsize(db_info.size)

        self._r_path.update(db_name)
        self._r_size.update(view_size)
        self._r_version.update(db_info.version)
        self._r_created.update(db_info.created_at)
        self._r_updated.update(db_info.updated_at)

    @classmethod
    def extract_dbinfo(cls, storage: Storage) -> DBInfo:
        if storage.is_open:
            st = os.stat(storage.storage_path)

            return DBInfo(
                db_path=storage.storage_path,
                size=st.st_size,
                version=storage.get_system_value(defs.SYS_KEY_VERSION),
                created_at=storage.get_system_value(defs.SYS_KEY_CREATED),
                updated_at=storage.get_system_value(defs.SYS_KEY_UPDATED),
            )

        return DBInfo(
            db_path="",
            size=0,
            version="",
            created_at="",
            updated_at="",
        )
