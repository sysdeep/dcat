from typing import Callable
from logging import Logger
from app.storage.Storage import Storage
from app.lib import dbus


class ActionsController:
    def __init__(self, storage: Storage, logger: Logger, show_open_handler: Callable[[], None], show_create_handler: Callable[[], None],):
        self._storage = storage
        self._logger = logger
        self._show_open_handler = show_open_handler
        self._show_create_handler = show_create_handler

    def backup_db(self):
        self._logger.debug("action debug")
        self._storage.create_current_backup()

    def show_find_modal(self):
        # TODO: избавится от шины
        dbus.emit(dbus.SHOW_FIND)

    def show_open_db(self):
        self._show_open_handler()

    def show_create_db(self):
        self._show_create_handler()
