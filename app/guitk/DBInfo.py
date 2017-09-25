#!/usr/bin/env python3
# -*- coding: utf-8 -*-


import tkinter 
from tkinter import ttk

from .utils import aqicon


class DBInfo(tkinter.Frame):
	def __init__(self, master, *args, **kwargs):
		super(DBInfo, self).__init__(master, *args, **kwargs)

		tkinter.Label(self, text="version:").pack(side="left")

		self.label_version = tkinter.Label(self, text="---")
		self.label_version.pack(side="left")

		tkinter.Label(self, text=" | ").pack(side="left")

		tkinter.Label(self, text="path:").pack(side="left")

		self.label_path = tkinter.Label(self, text="---")
		self.label_path.pack(side="left")

		tkinter.Label(self, text=" | ").pack(side="left")

		tkinter.Label(self, text="created:").pack(side="left")

		self.label_created = tkinter.Label(self, text="---")
		self.label_created.pack(side="left")

		self.icon_close = aqicon("close")
		tkinter.Button(self, text="Close", image=self.icon_close, compound="left", relief="flat", command=self.__on_exit).pack(side="right")


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


	def __on_exit(self):
		self.master.quit()