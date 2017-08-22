#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import tkinter
from tkinter import ttk


class IRow(object):
    def __init__(self, parent, name, sname):
        self.parent = parent
        self.name = name
        self.sname = sname

        lkey_text = self.sname + ": "
        self.lkey = ttk.Label(self.parent, text=lkey_text)
        self.vkey = ttk.Label(self.parent, text="")

    def update(self, value):
        self.vkey.config(text=value)






class VInfo(ttk.Frame):
    def __init__(self, parent, *args, **kwargs):
        super(VInfo, self).__init__(parent, *args, **kwargs)


        ttk.Label(self, text="Volume info").pack(side="top")


        self.grid = ttk.Frame(self)
        self.grid.pack(side="top", expand=True, fill="both")


        self.items = (
            self.__make_irow("name", "Название"),
        )


        for i, irow in enumerate(self.items):

            irow.lkey.grid(row=i, column=0, sticky="e")
            irow.vkey.grid(row=i, column=1, sticky="w")
            





    def update_info(self, vnode):
        for irow in self.items:
            try:
                value = getattr(vnode, irow.name)
            except:
                value = "---"

            irow.update(value)








    def __make_irow(self, name, sname):
        return IRow(self.grid, name, sname)