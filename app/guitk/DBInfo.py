#!/usr/bin/env python3
# -*- coding: utf-8 -*-


import tkinter 
from tkinter import ttk

from app.lib import dbus
from .utils import aqicon

from .components import ButtonDefault, ButtonInfo


class DBInfo(ttk.Frame):
	def __init__(self, master, *args, **kwargs):
		super(DBInfo, self).__init__(master, *args, **kwargs)


		# self.cb_show_info = None
		self.configure(padding=5)


		# ttk.Label(self, text="version:").pack(side="left")
		#
		# self.label_version = ttk.Label(self, text="---")
		# self.label_version.pack(side="left")
		#
		# ttk.Label(self, text=" | ").pack(side="left")
		#
		# ttk.Label(self, text="path:").pack(side="left")

		self.label_path = ttk.Label(self, text="---")
		self.label_path.pack(side="left")

		# ttk.Label(self, text=" | ").pack(side="left")
		#
		# ttk.Label(self, text="created:").pack(side="left")
		#
		# self.label_created = ttk.Label(self, text="---")
		# self.label_created.pack(side="left")



		self.icon_close = aqicon("close")
		# tkinter.Button(self, text="Закрыть", image=self.icon_close, compound="left", relief="flat", command=self.__on_exit).pack(side="right")
		# ButtonDefault(self, text="Закрыть", image=self.icon_close, compound="left", command=self.__on_exit).pack(side="right")
		ttk.Button(self, text="Закрыть", image=self.icon_close, compound="left", command=self.__on_exit).pack(side="right")


		self.icon_info = aqicon("info")
		ttk.Button(self, text="Info", image=self.icon_info, compound="left", command=self.__show_info).pack(side="right", padx=5)




	def set_path(self, value):
		self.label_path.config(text=value)


	# def set_version(self, value):
	# 	self.label_version.config(text=value)
	#
	# def set_created(self, value):
	# 	self.label_created.config(text=value)


	# def set_sysinfo(self, sqlite_rows):
	# 	for row in sqlite_rows:
	# 		if row["key"] == "version":
	# 			self.set_version(row["value"])
	# 		elif row["key"] == "created":
	# 			self.set_created(row["value"])
	# 		else:
	# 			pass








	def __on_exit(self):
		self.master.quit()


	def __show_info(self):
		dbus.emit(dbus.SHOW_ABOUT_BASE)

