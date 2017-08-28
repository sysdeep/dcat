#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import tkinter
from tkinter import ttk
from tkinter.filedialog import *

from app.storage import get_storage

from .Menu import BarMenu
# from .TreeFrame import TreeFrame
# from .DataFrame import DataFrame
from .explorer import Explorer
from .DBInfo import DBInfo
# from .InfoFrame import InfoFrame
from .modals.AddVolume import AddVolume
# from .ToolBar import ToolBar

from app.lib.USettings import USettings

class MainWindow(tkinter.Tk):
	def __init__(self):
		super(MainWindow, self).__init__()


		self.title("DCat")
		self.minsize(1100, 400)
		# self.iconphoto(self, get_icon("gnome-app-install-star"))

		self.usettings = USettings()
		self.usettings.open_settings()

		
		self.storage = get_storage()

		self.menu_bar = BarMenu(self)
		self.menu_bar.add_last_files(self.usettings.data["lastbases"])


		# self.tool_bar = ToolBar(self)
		# self.tool_bar.pack(side="top", expand=False, fill="x")

		self.explorer_frame = Explorer(self)
		self.explorer_frame.pack(side="top", fill="both", expand=True)
		self.explorer_frame.v_list.set_cb_open_modal_add_volume(self.__on_open_modal_add_volume)
		self.explorer_frame.v_list.set_cb_open_db(self.__on_show_open_db)

		self.db_info = DBInfo(self)
		self.db_info.pack(side="bottom", fill="x", expand=False)

		self.modal_add_volume = None



		self.menu_bar.set_cb_create(self.__on_create_db)
		self.menu_bar.set_cb_show_open_db(self.__on_show_open_db)

		self.menu_bar.set_cb_open_modal_add_volume(self.__on_open_modal_add_volume)


		#--- если в настройках флаг открывать последний
		is_open_last = self.usettings.data["open_last"]
		if is_open_last == 1:
			if len(self.usettings.data["lastbases"]) > 0:
				last = self.usettings.data["lastbases"][-1]
				if os.path.exists(last):
					self.__on_open_db(last)


		style = ttk.Style()
		print(style.theme_names())
		print(style.theme_use())
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

		# load_tree_demo()


	def __update_db_info(self):
		"""обновление информации по базе"""
		self.db_info.set_path(self.storage.storage_path)
		self.db_info.set_sysinfo(self.storage.fetch_system())


	def __update_lastbases(self, db_path):
		"""обновление списка недавних баз"""
		if db_path not in self.usettings.data["lastbases"]:
			if len(self.usettings.data["lastbases"]) > 10:
				self.usettings.data["lastbases"].pop()
			self.usettings.data["lastbases"].append(db_path)
			self.usettings.save()



	def __on_create_db(self, db_path):
		"""запрос создания базы по заданному пути"""
		self.storage.close_storage()
		self.storage.create_storage(db_path)

		self.explorer_frame.refresh()
		self.__update_db_info()
		self.__update_lastbases(db_path)


	def __on_open_db(self, db_path):
		"""запрос на открытие базы по заданному пути"""
		self.storage.close_storage()
		self.storage.open_storage(db_path)

		self.explorer_frame.refresh()
		self.__update_db_info()

		self.__update_lastbases(db_path)
		



	def __on_open_modal_add_volume(self):
		self.modal_add_volume = AddVolume(self)
		self.modal_add_volume.set_cb_complete(self.__on_scan_complete)


	def __on_scan_complete(self):
		self.explorer_frame.refresh()
		self.modal_add_volume = None


	def __on_show_open_db(self):
		"""отобразить модал выбора базы для открытия"""
		inpath = askopenfilename(
				title=u"Select ADEPT-encrypted PDF file to decrypt",
				defaultextension=u".dcat", filetypes=[('DCat files', '.dcat')])

		if inpath:
			inpath = os.path.normpath(inpath)
			self.__on_open_db(inpath)















if __name__ == "__main__":

	app = MainWindow()
	app.mainloop()
