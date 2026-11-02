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



		# # self.__text = tkinter.Text(self, width=60)
		# self.__text = tkinter.Text(self)
		# self.__text.pack(side="top", expand=False)
		# self.__text.insert(tkinter.END, "Bye Bye..... sljkhlkajs j;laks j;ak ja;lk j;alk ja;lskdj; a;s ;laks jd;laksjd ;a sj;'akj;aksjd;alksjd;alksjd")
		#
		# #--- horisontal scroll
		# hsb = ttk.Scrollbar(self, orient="horizontal", command=self.__text.xview)
		# self.__text['xscroll'] = hsb.set
		# # hsb.pack(side="right", expand=False, fill="y")
		# hsb.pack(expand=True, fill="x")



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
		
		self.__add_items = (
			self.__make_irow("fnodes_count", "Кол-во элементов"),
		)

		gi = 0
		for i, irow in enumerate(self.__items):
			gi = gi + i
			irow.lkey.grid(row=gi, column=0, sticky="e")
			irow.vkey.grid(row=gi, column=1, sticky="w")
		
		gi += 1
		for i, irow in enumerate(self.__add_items):
			gi = gi + i
			irow.lkey.grid(row=gi, column=0, sticky="e")
			irow.vkey.grid(row=gi, column=1, sticky="w")
			
		#--- description
		# self.__description = tkinter.Label(self, wraplength=20, text="very long description")
		# self.__description.pack(side="top")
		
		#--- controls
		# self.__controls = ttk.Frame(self)
		# self.__controls.pack(side="bottom", fill="x", expand=True)
		#
		# ttk.Button(self.__controls, text="Edit").pack()



	#--- public ---------------------------------------------------------------
	def update_info(self, vnode, elements_count=0):
		"""обновление данных"""
		for irow in self.__items:
			try:
				value = getattr(vnode, irow.name)
			except:
				value = "---"

			irow.update(value)
			
		# TODO: да да... очень криво...
		# print(elements_count)
		for irow in self.__add_items:
			if irow.name == "fnodes_count":
				irow.update(str(elements_count))

	def drop_info(self):
		"""очистка данных"""
		for irow in self.__items:
			irow.drop()
			
		for irow in self.__add_items:
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
