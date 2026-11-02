#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import tkinter
from tkinter import ttk

from app.lib.fsize import naturalsize
from ..utils import ticons
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
		self.cb_updated = None


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






		#--- edit description field
		frame_description = ttk.Frame(self.main_frame, padding=5)
		frame_description.pack(side="top", expand=True, fill="both")


		ttk.Label(frame_description, text="описание").pack(fill="x", side="top")
		self.description = tkinter.Text(frame_description, height=6, width=20)
		self.description.pack(side="left", fill="both", expand=True)

		#- vertical scroll
		ysb = ttk.Scrollbar(frame_description, orient="vertical", command=self.description.yview)
		self.description['yscroll'] = ysb.set
		ysb.pack(side="right", expand=False, fill="y")




		#--- controls
		controls_frame = ttk.Frame(self.main_frame)
		controls_frame.pack(fill="both", side="bottom", padx=5, pady=5)

		ttk.Button(controls_frame, text="Закрыть(Ctrl+w)", command=self.destroy, image=ticons.ticon(ticons.CLOSE), compound="left").pack(side="right")

		ttk.Button(controls_frame, text="Сохранить", command=self.__do_save, image=ticons.ticon(ticons.SAVE), compound="left").pack(side="left")

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

		self.description.insert(tkinter.END, fnode.description)


	def __find_volume_name(self, volume_id):
		storage = get_storage()
		if storage.is_open is False:
			return "---"

		volumes = storage.fetch_volumes(iscache=True)

		result = [v.name for v in volumes if v.uuid == volume_id]

		return result[0] if result else "---"





	def __do_save(self):
		"""сохранить изменения"""
		description = self.description.get(1.0, tkinter.END)

		storage = get_storage()

		storage.update_file_description(self.fnode.uuid, description, commit=True)

		if self.cb_updated:
			self.cb_updated()








if __name__ == "__main__":


	root = tkinter.Tk()

	modal = AboutFile(root)
	ttk.Button(root, text="quit", command=quit).pack()

	root.mainloop()