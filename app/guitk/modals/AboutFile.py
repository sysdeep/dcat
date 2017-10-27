#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import tkinter
from tkinter import ttk

from app.lib.fsize import naturalsize
from ..utils import aqicon
from app.storage import get_storage


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






class AboutFile(tkinter.Toplevel):
	def __init__(self, fnode, master=None, *args, **kwargs):
		super(AboutFile, self).__init__(master, *args, **kwargs)
		self.title("Свойства файла")

		self.maxsize(400, 300)
		self.minsize(400, 300)

		self.fnode = fnode


		self.main_frame = ttk.Frame(self, padding=10)
		self.main_frame.pack(expand=True, fill="both")


		self.grid = ttk.Frame(self.main_frame)
		self.grid.pack(side="top", expand=True, fill="both")


		self.items = (
			self.__make_irow("name", "Название"),
			self.__make_irow("size", "Размер"),
			self.__make_irow("ctime", "Создание"),
			self.__make_irow("mtime", "Модификация"),
			self.__make_irow("volume", "Том"),
		)


		for i, irow in enumerate(self.items):

			irow.lkey.grid(row=i, column=0, sticky="e")
			irow.vkey.grid(row=i, column=1, sticky="w")


		controls_frame = ttk.Frame(self.main_frame)
		controls_frame.pack(fill="both", side="bottom", padx=5, pady=5)

		self.icon_close = aqicon("close")
		ttk.Button(controls_frame, text="Закрыть(Ctrl+w)", command=self.destroy, image=self.icon_close, compound="left").pack(side="right")

		self.bind_all("<Control-w>", lambda e: self.destroy())



		self.update_info(self.fnode)


	def __make_irow(self, name, sname):
		return IRow(self.grid, name, sname)


	def update_info(self, fnode):
		for irow in self.items:

			if irow.name == "ctime":
				irow.update(fnode.fctime())
				continue

			if irow.name == "mtime":
				irow.update(fnode.fmtime())
				continue

			if irow.name == "size":
				irow.update(naturalsize(fnode.size))
				continue

			if irow.name == "volume":
				volume_name = self.__find_volume_name(fnode.volume_id)
				irow.update(volume_name)
				continue

			try:
				value = getattr(fnode, irow.name)
			except:
				value = "---"

			irow.update(value)



	def __find_volume_name(self, volume_id):
		storage = get_storage()
		if storage.is_open is False:
			return "---"

		volumes = storage.get_volumes_cache()

		result = [v.name for v in volumes if v.uuid == volume_id]

		return result[0] if result else "---"
















if __name__ == "__main__":


	root = tkinter.Tk()

	modal = AboutFile(root)
	ttk.Button(root, text="quit", command=quit).pack()

	root.mainloop()