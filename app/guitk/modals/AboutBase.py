#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import tkinter
from tkinter import ttk

from ..utils import aqicon
from app.storage import get_storage
from app.lib.fsize import naturalsize
from ..components import ButtonDefault







class AboutBase(tkinter.Toplevel):
	def __init__(self, master=None, *args, **kwargs):
		super(AboutBase, self).__init__(master, *args, **kwargs)
		self.title("Свойства базы")

		self.maxsize(400, 300)
		self.minsize(400, 300)

		self.storage = get_storage()


		self.main_frame = tkinter.Frame(self,)
		self.main_frame.pack(expand=True, fill="both", side="top", padx=10, pady=20)


		self.grid = tkinter.Frame(self.main_frame)
		self.grid.pack(side="top", expand=True, fill="both")





		#--- path
		self.items = [
			IRow(self.grid, "path", self.storage.storage_path),
		]

		#--- file os stat
		for key, value in self.__get_db_stat(self.storage.storage_path).items():
			self.items.append(IRow(self.grid, key, value))

		#--- db sys info
		for row in self.storage.fetch_system():
			self.items.append(IRow(self.grid, row["key"], row["value"]))


		#--- draw
		for i, irow in enumerate(self.items):

			irow.lkey.grid(row=i, column=0, sticky="e")
			irow.vkey.grid(row=i, column=1, sticky="w")


		#--- controls
		controls_frame = tkinter.Frame(self.main_frame)
		controls_frame.pack(fill="both", side="bottom", padx=5, pady=5)

		self.icon_close = aqicon("close")
		ButtonDefault(controls_frame, text="Закрыть(Ctrl+w)", command=self.destroy, image=self.icon_close, compound="left").pack(side="right")

		self.bind_all("<Control-w>", lambda e: self.destroy())






	def __get_db_stat(self, db_path):
		"""получить информацию о файле базы"""
		st = os.stat(db_path)

		result = {
			"size"	: naturalsize(st.st_size)					# нормальный вид размера
		}

		return result






class IRow(object):
	def __init__(self, parent, name, value):
		self.parent = parent
		self.name = name
		self.value = value

		lkey_text = self.name + ": "
		self.lkey = ttk.Label(self.parent, text=lkey_text)
		self.vkey = ttk.Label(self.parent, text=value)

	def update(self, value):
		self.vkey.config(text=value)






if __name__ == "__main__":


	root = tkinter.Tk()

	modal = AboutBase(root)
	ttk.Button(root, text="quit", command=quit).pack()

	root.mainloop()