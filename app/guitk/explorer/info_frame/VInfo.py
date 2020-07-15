#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import tkinter
from tkinter import ttk



# s = ttk.Style()
# s.configure('new.TFrame', background='#7AC5CD')


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






class VInfo(ttk.Frame):
	def __init__(self, parent, *args, **kwargs):
		super(VInfo, self).__init__(parent, *args, **kwargs)

		# self.relief = "groove"
		# self.configure(width=500, relief="groove", style="new.TFrame")
		# self.configure(style="new.TFrame")

		#--- title
		ttk.Label(self, text="Свойства тома").pack(side="top")


		#--- table
		self.__grid = ttk.Frame(self)
		self.__grid.pack(side="top", expand=True, fill="both")


		self.__items = (
			self.__make_irow("name", "Название"),
			self.__make_irow("created", "Создание"),
			self.__make_irow("path", "Путь"),
			self.__make_irow("vtype", "Тип"),
		)


		for i, irow in enumerate(self.__items):

			irow.lkey.grid(row=i, column=0, sticky="e")
			irow.vkey.grid(row=i, column=1, sticky="w")
			




	#--- public ---------------------------------------------------------------
	def update_info(self, vnode):
		"""обновление данных"""
		for irow in self.__items:
			try:
				value = getattr(vnode, irow.name)
			except:
				value = "---"

			irow.update(value)

	def drop_info(self):
		"""очистка данных"""
		for irow in self.__items:
			irow.drop()
	#--- public ---------------------------------------------------------------








	def __make_irow(self, name, sname):
		return IRow(self.__grid, name, sname)






if __name__ == "__main__":

	import tkinter

	root = tkinter.Tk()


	view = VInfo(parent=root)
	view.pack()

	
	root.mainloop()
