import tkinter

from app.storage import Storage
from app.lib import dbus
from app.lib.user_settings import UserSettings

from .volumes_list import VolumesList
from .DBList import DBList
from .FList import FList
# from .info_frame import InfoFrame


class Explorer(tkinter.Frame):
    def __init__(self, parent, storage: Storage, us: UserSettings, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)

        self._storage = storage

        # left side ---------------------------------------
        _left_side = tkinter.Frame(self)
        _left_side.pack(side="left", expand=False, fill="y")

        # volumes
        self.v_list = VolumesList(_left_side)
        self.v_list.pack(side="top", expand=True, fill="y")
        self.v_list.set_select_cb(self.__on_volume_selected)
        self.v_list.set_remove_cb(self.__on_volume_do_remove)

        # databases ---------------------------------------
        tkinter.Label(master=_left_side, text="Последние базы").pack(side="top", fill="y", anchor="w")
        self.__dblist = DBList(parent=_left_side, us=us)
        self.__dblist.pack(side="top", expand=False, fill="y")

        # volume/file info frame --------------------------
        # NOTE: при использовании скачет... больше вредит чем помогает
        # self.__info_frame = InfoFrame(self, width=500, height=500)
        # self.__info_frame.pack(side="right", expand=False, fill="both")

        # files -------------------------------------------
        self.__f_list = FList(self)
        self.__f_list.signal_file_selected.connect(self.__on_fnode_selected)
        self.__f_list.pack(side="right", expand=True, fill="both")

        # self.history_stack = []
        # self.current_volume = None
        self.current_vnode = None

        self.v_list.reload_volumes()

        dbus.eon(dbus.SCAN_COMPLETE, self.refresh)

    def refresh(self):
        """полное обновление"""
        self.__f_list.clear()  # очистка списка файлов
        # self.__info_frame.drop_volume()  # сброс информации о томе
        self.v_list.reload_volumes()  # обновление списка томов

    # volume actions ----------------------------------------------------------
    def __on_volume_selected(self, vnode):
        """событие выбора тома"""
        self.current_vnode = vnode

        self.__f_list.show_volume(self.current_vnode)  # обновляем список файлов
        # self.__info_frame.update_volume(vnode)  # обновляем инфо о томе
        # self.__info_frame.drop_file()  # т.к. том новый - файлов нет

    def __on_volume_do_remove(self, volume_uuid):
        """запрос на удаление тома"""
        self._storage.remove_volume(volume_uuid)
        self.refresh()

    # events ------------------------------------------------------------------
    def __on_fnode_selected(self, fnode):
        """событие о выборе ноды"""
        # self.__info_frame.update_file(fnode)  # обновляем инфо ноды
        pass
