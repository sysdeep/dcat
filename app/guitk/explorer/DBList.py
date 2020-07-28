#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import re
import tkinter
from tkinter import ttk
from tkinter import messagebox

# from vendor.natsort import natsorted
from app.storage import get_storage, sbus
from app.lib import dbus, sorting
from ..utils import ticons

from app import shared



# TODO: добавить обработку изменения конфига
class DBList(tkinter.Frame):
	def __init__(self, parent, *args, **kwargs):
		super(DBList, self).__init__(parent, *args, **kwargs)


		self.storage = get_storage()
		self.current_volume_id = None

		self.select_cb = None
		self.remove_cb = None
		self.cb_open_modal_add_volume = None


		self.__volumes_map = {}
		self.volume_icons = []

		# self.configure(width=50)

		list_frame = tkinter.Frame(self)
		list_frame.pack(side="top", expand=True, fill="both")

		self.__list = ttk.Treeview(list_frame, show="tree", selectmode='browse')
		# self.__list.pack(side="left", expand=True, fill="both")
		self.__list.grid(row=0, column=0, sticky='NSEW')
		# self.__list.bind("<Button-3>", self.__make_cmenu)
		# self.__list.column("#0", width=200)
		self.__list.column("#0", minwidth=800, stretch=True)
		# self.tree.column("#0",minwidth=1080, stretch=True)
		self.__list.tag_bind("simple", "<<TreeviewSelect>>", self.__select_row)
		# self.__list.bind("<Double-1>", self.__open_row)


		#--- vertical scroll
		ysb = ttk.Scrollbar(list_frame, orient="vertical", command=self.__list.yview)
		self.__list['yscroll'] = ysb.set
		# ysb.pack(side="right", expand=False, fill="y")
		ysb.grid(row=0, column=1, sticky="NS")
		
		
		#--- horisontal scroll
		hsb = ttk.Scrollbar(list_frame, orient="horizontal", command=self.__list.xview)
		self.__list['xscroll'] = hsb.set
		# hsb.pack(side="right", expand=False, fill="y")
		hsb.grid(row=1, column=0, sticky="WE")

		
		self.__update()
		
		
		
		
		
	def __update(self):
		#--- очистка
		self.__clear()

		#--- очистка от несуществующих баз
		usettings = shared.get_usettings()
		usettings.check_bases_exists()

		#--- отображение
		# self.__show_items()
		
		items = usettings.data["lastbases"]

		for item_path in items:
			self.__list.insert('', 'end', item_path, text=item_path, tags=("simple", ))
		
		# self.__list.insert('', 'end', vnode.uuid, text=vnode.name, tags=("simple", ), image=ivolume)
		
		
	def __clear(self):
		for row in self.__list.get_children():
			self.__list.delete(row)
		
		
		
		

	def __select_row(self, e):

		selection = self.__list.selection()
		
		# print(selection)
		
		
		#--- если ничего не выбрано - ничего не делаем
		if len(selection) == 0:
			return False
		
		
		item_path = selection[0]

		dbus.emit(dbus.REQUEST_OPEN_DB, item_path)

		







