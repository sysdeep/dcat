#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import tkinter
from tkinter import ttk
from tkinter.filedialog import *

from app.storage import get_storage
from app.lib import dbus
from app.lib.USettings import USettings
from app import shared

from .modals.ModalsCtrl import ModalsCtrl
from .Menu import BarMenu
from .explorer import Explorer
from .DBInfo import DBInfo
from .ToolBar import ToolBar












class MainWindow(tkinter.Tk):
	def __init__(self):
		super(MainWindow, self).__init__()

		self.name = "DCat"
		self.title(self.name)
		self.minsize(800, 400)
		# self.iconphoto(self, get_icon("gnome-app-install-star"))

		# self.usettings = USettings()
		# self.usettings.open_settings()

		self.usettings = shared.get_usettings()

		
		self.storage = get_storage()


		

		#--- menu
		self.menu_bar = BarMenu(self)
		self.menu_bar.add_last_files(self.usettings.data["lastbases"])
		self.menu_bar.cb_show_open			= self.__on_show_open_db
		self.menu_bar.cb_show_create 		= self.__on_create_db
		self.menu_bar.cb_open_last 			= self.__on_open_db
		self.menu_bar.cb_show_add_volume 	= self.__on_show_modal_add_volume
		self.menu_bar.cb_create_db_backup	= self.act_db_backup


		#--- toolbar
		self.tool_bar = ToolBar(self)
		self.tool_bar.pack(side="top", expand=False, fill="x")
		self.tool_bar.cb_open_db 			= self.__on_show_open_db
		self.tool_bar.cb_create_db 			= self.__on_create_db
		self.tool_bar.cb_create_db_backup	= self.act_db_backup
		self.tool_bar.cb_show_find_modal	= self.act_show_find_modal


		#--- explorer
		self.explorer_frame = Explorer(self)
		self.explorer_frame.pack(side="top", fill="both", expand=True)
		# self.explorer_frame.v_list.set_cb_open_modal_add_volume(self.__on_show_modal_add_volume)


		#--- db info
		self.db_info = DBInfo(self)
		self.db_info.pack(side="bottom", fill="x", expand=False)

		self.modal_add_volume = None


		self.modals_ctrl = ModalsCtrl(self)

		style = ttk.Style()
		# print(style.theme_names())
		# print(style.theme_use())
		style.theme_use("clam")

		# self.tk.eval("source themes/pkgIndex.tcl")
		# self.tk.call("package", "require", "ttkthemes")
		# self.tk.call("ttk::setTheme", "plastik")
		# self.tk.call("ttk::setTheme", "aquativo")
		# self.tk.call("ttk::setTheme", "arc")
		# self.tk.call("ttk::setTheme", "elegance")
		# self.tk.call("ttk::setTheme", "blue")
		# self.tk.call("ttk::setTheme", "clearlooks")
		# self.tk.call("ttk::setTheme", "radiance")
		# self.tk.call("ttk::setTheme", "winxpblue")



		#--- открываем последний
		self.__check_open_last()



	def __check_open_last(self):
		#--- если в настройках флаг открывать последний
		is_open_last = self.usettings.data["open_last"]
		if is_open_last == 0:
			return False

		last = self.usettings.get_last_base()

		if last:
			self.__on_open_db(last)




	def __update_db_info(self):
		"""обновление информации по базе"""
		self.db_info.set_path(self.storage.storage_path)
		# self.db_info.set_sysinfo(self.storage.fetch_system())






	def __on_create_db(self):
		"""запрос создания базы"""

		title = 'Расположение новой базы'
		db_path = asksaveasfilename(defaultextension=".dcat", title=title)
		if db_path:

			self.storage.close_storage()
			self.storage.create_storage(db_path)

			self.explorer_frame.refresh()
			self.__update_db_info()
			self.usettings.update_last_base(db_path)
			self.__update_title(db_path)





	def __on_open_db(self, db_path):
		"""запрос на открытие базы по заданному пути"""

		#--- проверка существования базы
		if not os.path.exists(db_path):
			self.usettings.remove_last(db_path)
			return False

		self.storage.close_storage()
		self.storage.open_storage(db_path)

		self.explorer_frame.refresh()
		self.__update_db_info()

		self.usettings.update_last_base(db_path)
		self.__update_title(db_path)
		



	def __on_show_modal_add_volume(self):
		"""вызов события для отоьражения модала добавления тома"""
		dbus.emit(dbus.SHOW_ADD_VOLUME)



	def __on_show_open_db(self):
		"""отобразить модал выбора базы для открытия"""
		inpath = askopenfilename(
				title=u"Выбор базы",
				defaultextension=u".dcat", filetypes=[('DCat files', '.dcat')])

		if inpath:
			inpath = os.path.normpath(inpath)
			self.__on_open_db(inpath)




	def __update_title(self, db_path):
		text = "{}: {}".format(self.name, db_path)
		self.title(text)



	def act_show_find_modal(self):
		dbus.emit(dbus.SHOW_FIND)


	def act_db_backup(self):
		self.storage.create_current_backup();


	def act_exit(self):
		self.quit()



if __name__ == "__main__":

	app = MainWindow()
	app.mainloop()
