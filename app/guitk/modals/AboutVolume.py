#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import tkinter
from tkinter import ttk

from app.rc import ABOUT_NAME, ABOUT_AUTHOR_EMAIL, ABOUT_AUTHOR_NAME, ABOUT_DESCRIPTION, ABOUT_SLUG, VERSION
from ..utils import aqicon
from ..components import ButtonDefault


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






class AboutVolume(tkinter.Toplevel):
	def __init__(self, vnode, master=None, *args, **kwargs):
		super(AboutVolume, self).__init__(master, *args, **kwargs)
		self.title("Свойства тома")

		self.maxsize(400, 300)
		self.minsize(400, 300)

		self.vnode = vnode


		self.main_frame = ttk.Frame(self, padding=10)
		# self.main_frame.pack(expand=True, fill="both", side="top", padx=10, pady=20)
		self.main_frame.pack(expand=True, fill="both")


		self.grid = ttk.Frame(self.main_frame)
		self.grid.pack(side="top", expand=False, fill="x")


		self.items = (
			self.__make_irow("name", "Название"),
			self.__make_irow("created", "Создание"),
			self.__make_irow("updated", "Обновление"),
			self.__make_irow("path", "Путь"),
			self.__make_irow("vtype", "Тип"),
		)


		for i, irow in enumerate(self.items):

			irow.lkey.grid(row=i, column=0, sticky="e")
			irow.vkey.grid(row=i, column=1, sticky="w")



		self.desctiption = tkinter.Text(self.main_frame, height=6, width=20)
		self.desctiption.pack(side="top", fill="both", expand=True)
		# self.desctiption.insert(tkinter.END, "asfdafasdffsd")
		# self.desctiption.config(state=tkinter.NORMAL)
		# self.desctiption.config(state=tkinter.DISABLED)


		controls_frame = ttk.Frame(self.main_frame)
		controls_frame.pack(fill="both", side="bottom", padx=5, pady=5)

		self.icon_close = aqicon("close")
		# ttk.Button(controls_frame, text="Закрыть(Ctrl+w)", command=self.destroy, image=self.icon_close, compound="left").pack(side="right")
		# ButtonDefault(controls_frame, text="Закрыть(Ctrl+w)", command=self.destroy, image=self.icon_close, compound="left").pack(side="right")
		ttk.Button(controls_frame, text="Закрыть(Ctrl+w)", command=self.destroy, image=self.icon_close, compound="left").pack(side="right")

		self.bind_all("<Control-w>", lambda e: self.destroy())



		self.update_info(self.vnode)


	def __make_irow(self, name, sname):
		return IRow(self.grid, name, sname)


	def update_info(self, vnode):
		for irow in self.items:
			try:
				value = getattr(vnode, irow.name)
			except:
				value = "---"

			irow.update(value)


		if vnode.description:
			self.desctiption.insert(tkinter.END, vnode.description)
			# self.desctiption.insert(tkinter.END, "vnode.description")

		self.desctiption.config(state=tkinter.DISABLED)











if __name__ == "__main__":


	root = tkinter.Tk()

	modal = AboutVolume(root)
	ttk.Button(root, text="quit", command=quit).pack()

	root.mainloop()