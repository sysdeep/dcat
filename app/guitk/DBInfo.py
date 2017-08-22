#!/usr/bin/env python3
# -*- coding: utf-8 -*-


import tkinter 
from tkinter import ttk


class DBInfo(ttk.Frame):
    def __init__(self, master, *args, **kwargs):
        super(DBInfo, self).__init__(master, *args, **kwargs)

        ttk.Label(self, text="version:").pack(side="left")

        self.label_version = ttk.Label(self, text="---")
        self.label_version.pack(side="left")
        
        ttk.Label(self, text=" | ").pack(side="left")
        
        ttk.Label(self, text="path:").pack(side="left")
        
        self.label_path = ttk.Label(self, text="---")
        self.label_path.pack(side="left")
        
        ttk.Label(self, text=" | ").pack(side="left")
        
        ttk.Label(self, text="created:").pack(side="left")

        self.label_created = ttk.Label(self, text="---")
        self.label_created.pack(side="left")

    
    def update_info(self):
        pass


    def set_path(self, value):
        self.label_path.config(text=value)


    def set_version(self, value):
        self.label_version.config(text=value)

    def set_created(self, value):
        self.label_created.config(text=value)


    def set_sysinfo(self, sqlite_rows):
        for row in sqlite_rows:
            if row["key"] == "version":
                self.set_version(row["value"])
            elif row["key"] == "created":
                self.set_created(row["value"])
            else:
                pass