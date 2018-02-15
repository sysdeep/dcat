#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
	модал с информацией о базе
"""
import os
import tkinter
from tkinter import ttk

from ..utils import ticons
from app.storage import get_storage, defs
from app.lib.fsize import naturalsize







class AboutBase(tkinter.Toplevel):
	def __init__(self, master=None, *args, **kwargs):
		super(AboutBase, self).__init__(master, *args, **kwargs)
		self.title("Свойства базы")

		self.maxsize(450, 350)
		self.minsize(450, 350)

		self.storage = get_storage()


		self.main_frame = ttk.Frame(self, padding=10)
		self.main_frame.pack(expand=True, fill="both")


		#--- main info grid
		self.grid = ttk.Frame(self.main_frame)
		self.grid.pack(side="top", expand=True, fill="x")

		self.__current_row = 0
		self.label_path = self.__append_kv_row("путь")
		self.label_size = self.__append_kv_row("размер")
		self.label_version = self.__append_kv_row("версия")
		self.label_created = self.__append_kv_row("создание")
		self.label_updated = self.__append_kv_row("обновление")



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
		ttk.Button(controls_frame, text="Уплотнить", command=self.do_vacuum, image=ticons.ticon(ticons.I_BOOKMARK), compound="left").pack(side="left")

		self.bind_all("<Control-w>", lambda e: self.destroy())



		#--- start
		self.__load()



	def __load(self):
		"""загрузить данные"""

		if self.storage.is_open:
			self.label_path.config(text=self.storage.storage_path)

			self.__update_size()

		self.label_version.config(text=self.storage.get_system_value(defs.SYS_KEY_VERSION))
		self.label_created.config(text=self.storage.get_system_value(defs.SYS_KEY_CREATED))
		self.label_updated.config(text=self.storage.get_system_value(defs.SYS_KEY_UPDATED))

		description = self.storage.get_system_value(defs.SYS_KEY_DESCRIPTION)
		self.description.insert(tkinter.END, description)



	def __make_kv_row(self, name, row):
		"""создать строку ключ-значение"""
		ttk.Label(self.grid, text=name).grid(row=row, column=0, sticky="e", pady=2, padx=5)

		label = ttk.Label(self.grid)
		label.grid(row=row, column=1, sticky="w", pady=2, padx=5)
		return label


	def __append_kv_row(self, name):
		"""добавить строку со смещением вниз"""
		row = self.__current_row
		self.__current_row += 1
		return self.__make_kv_row(name, row)



	def __do_save(self):
		"""сохранить изменения"""
		description = self.description.get(1.0, tkinter.END)

		self.storage.update_system(defs.SYS_KEY_DESCRIPTION, description)
		self.storage.commit()



	def do_vacuum(self):
		"""уплотнить базу"""

		if self.storage.is_open:
			self.storage.vacuum()				# уплотняем
			self.__update_size()				# обновляем инфо о размере

		else:
			print("storage not open")


	def __update_size(self):
		"""обновить информацию о размере базы"""
		st = os.stat(self.storage.storage_path)
		size = naturalsize(st.st_size)
		self.label_size.config(text=size)















if __name__ == "__main__":


	root = tkinter.Tk()

	modal = AboutBase(root)
	ttk.Button(root, text="quit", command=quit).pack()

	root.mainloop()