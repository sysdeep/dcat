import json
import sys
import os

from .user_settings_model import UserSettingsModel, make_default, UpdateUserSettingsModel


class UserSettings:
    def __init__(self, file_path: str | None = None):
        self._file_path = file_path
        if self._file_path is None:
            self._file_path = self._make_os_file_path()

        self._settings: UserSettingsModel = self._try_load()
        self._check_bases_exists()

    # public ------------------------------------------------------------------
    def set_settings(self, payload: UpdateUserSettingsModel, write: bool = True):
        if payload.lastbases is not None:
            self._settings.lastbases = payload.lastbases

        if payload.open_last is not None:
            self._settings.open_last = payload.open_last

        if write:
            self._write()

    def get_settings(self) -> UserSettingsModel:
        return self._settings

    # private -----------------------------------------------------------------
    def _make_os_file_path(self):
        app_name = "dcat"
        file_name = "settings.json"
        if sys.platform == "win32":
            return os.path.join(os.environ["APPDATA"], app_name, file_name)
        else:
            return os.path.expanduser(os.path.join("~", "." + app_name, file_name))

    def _write(self):
        data_dict = self._settings.dump()

        with open(self._file_path, "w", encoding="utf-8") as fd:
            fd.write(json.dumps(data_dict, indent=4))

    def _try_load(self) -> UserSettingsModel:
        print(self._file_path)
        if os.path.exists(self._file_path):
            with open(self._file_path, "r", encoding="utf-8") as fd:
                settings_data = json.load(fd)
                return UserSettingsModel.fromDict(settings_data)
        else:
            return make_default()

    def _check_bases_exists(self):
        """проверка на существование баз в истории"""
        dbs: list[str] = []
        for item in self._settings.lastbases:
            if os.path.exists(item):
                dbs.append(item)

        self._settings.lastbases = dbs
