#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
	модал со списком баз
"""
import os
import tkinter
from tkinter import ttk

from ..utils import ticons
from app.storage import get_storage, defs
from app.lib.fsize import naturalsize

from app import shared
from app.lib import dbus




class DataBases(tkinter.Toplevel):
	def __init__(self, master=None, *args, **kwargs):
		super(DataBases, self).__init__(master, *args, **kwargs)
		self.title("Базы данных")

		self.maxsize(450, 350)
		self.minsize(450, 350)


		self.usettings = shared.get_usettings()







		self.main_frame = ttk.Frame(self, padding=10)
		self.main_frame.pack(expand=True, fill="both")


		list_frame = tkinter.Frame(self.main_frame)
		list_frame.pack(side="top", expand=True, fill="both")


		self.__list = ttk.Treeview(list_frame, show="tree", selectmode='browse')
		self.__list.pack(side="left", expand=True, fill="both")
		# self.__list.bind("<Button-3>", self.__make_cmenu)


		#--- vertical scroll
		ysb = ttk.Scrollbar(list_frame, orient="vertical", command= self.__list.yview)
		self.__list['yscroll'] = ysb.set
		ysb.pack(side="right", expand=False, fill="y")

		self.__list.column("#0", width=200)
		# self.__list.tag_bind("simple", "<<TreeviewSelect>>", self.__select_row)
		self.__list.bind("<Double-1>", self.__open_row)






		#--- controls
		controls_frame = ttk.Frame(self.main_frame)
		controls_frame.pack(fill="both", side="bottom", padx=5, pady=5)


		ttk.Button(controls_frame, text="Закрыть(Ctrl+w)", command=self.destroy, image=ticons.ticon(ticons.CLOSE), compound="left").pack(side="right")

		# ttk.Button(controls_frame, text="Сохранить", command=self.__do_save, image=ticons.ticon(ticons.SAVE), compound="left").pack(side="left")
		# ttk.Button(controls_frame, text="Уплотнить", command=self.do_vacuum, image=ticons.ticon(ticons.I_BOOKMARK), compound="left").pack(side="left")

		self.bind_all("<Control-w>", lambda e: self.destroy())



		self.update_view()





	def update_view(self):
		"""обновление вида"""
		#--- очистка
		self.__clear()

		#--- очистка от несуществующих баз
		self.usettings.check_bases_exists()

		#--- отображение
		self.__show_items()


	def __clear(self):
		for row in self.__list.get_children():
			self.__list.delete(row)


	def __show_items(self):
		items = self.usettings.data["lastbases"]

		for item_path in items:
			self.__list.insert('', 'end', item_path, text=item_path, tags=("simple", ))




	def __open_row(self, e):

		selection = self.__list.selection()

		#--- если ничего не выбрано - ничего не делаем
		if len(selection) == 0:
			return False


		item_path = selection[0]

		dbus.emit(dbus.REQUEST_OPEN_DB, item_path)

		self.destroy()








if __name__ == "__main__":


	root = tkinter.Tk()

	modal = DataBases(root)
	ttk.Button(root, text="quit", command=quit).pack()

	root.mainloop()

