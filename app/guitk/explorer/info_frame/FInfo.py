#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import tkinter
from tkinter import ttk

from app.storage.models.FNode import FNode


class IRow(object):
    def __init__(self, parent, name, sname):
        self.parent = parent
        self.name = name
        self.sname = sname

        lkey_text = self.sname + ": "
        self.lkey = ttk.Label(self.parent, text=lkey_text)
        self.vkey = ttk.Label(self.parent, text="")

    #--- public ---------------------------------------------------------------
    def update(self, value):
        """установка значения"""
        self.vkey.config(text=value)


    def drop(self):
        """сброс"""
        self.vkey.config(text="")
    #--- public ---------------------------------------------------------------





class FInfo(ttk.Frame):
    def __init__(self, parent, *args, **kwargs):
        super(FInfo, self).__init__(parent, *args, **kwargs)


        ttk.Label(self, text="File info").pack(side="top")


        self.grid = ttk.Frame(self)
        self.grid.pack(side="top", expand=True, fill="both")


        self.items = (
            self.__make_irow("name", "Название"),
            self.__make_irow("size", "Размер"),
            self.__make_irow("ctime", "Создание"),
            self.__make_irow("mtime", "Модификация"),
        )


        for i, irow in enumerate(self.items):

            irow.lkey.grid(row=i, column=0, sticky="e")
            irow.vkey.grid(row=i, column=1, sticky="w")
            




    #--- public ---------------------------------------------------------------
    def update_info(self, fnode: FNode):
        """обновление данных"""

        for irow in self.items:

            if irow.name == "ctime":
                irow.update(fnode.fctime())
                continue

            if irow.name == "mtime":
                irow.update(fnode.fmtime())
                continue

            try:
                value = getattr(fnode, irow.name)
            except:
                value = "---"

            irow.update(value)

    def drop_info(self):
        """очистка данных"""

        for irow in self.items:
            irow.drop()
    #--- public ---------------------------------------------------------------







    def __make_irow(self, name, sname):
        return IRow(self.grid, name, sname)