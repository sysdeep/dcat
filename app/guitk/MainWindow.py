#!/usr/bin/env python
# -*- coding: utf-8 -*-


import tkinter

from app.storage import get_storage

from .Menu import BarMenu
# from .TreeFrame import TreeFrame
# from .DataFrame import DataFrame
from .explorer import Explorer
# from .InfoFrame import InfoFrame
from .modals.AddVolume import AddVolume

from app.logic import load_tree_demo

class MainWindow(tkinter.Tk):
	def __init__(self):
		super(MainWindow, self).__init__()


		self.title("DCat")
		# self.iconphoto(self, get_icon("gnome-app-install-star"))


		self.storage = get_storage()

		self.menu_bar = BarMenu(self)

		# self.tree_frame = TreeFrame(self, width=800)
		# self.tree_frame.pack(side="left", fill="both", expand=False)

		self.explorer_frame = Explorer(self)
		self.explorer_frame.pack(side="left", fill="both", expand=False)
		self.explorer_frame.v_list.set_cb_open_modal_add_volume(self.__on_open_modal_add_volume)


		self.modal_add_volume = None

		# self.info_frame = InfoFrame(self)
		# self.info_frame.pack(side="right", fill="both", expand=True)

		# self.__main_bar = None						# main bar - top
		# self.__mnemo_bar = None
		# self.footer_bar = None
		# self.__ioaction_bar = None

		# status bar
		self.status_bar_text = tkinter.StringVar()
		self.status_bar_text.set("--")


		self.menu_bar.set_cb_create(self.__on_create_db)
		self.menu_bar.set_cb_open(self.__on_open_db)

		self.menu_bar.set_cb_open_modal_add_volume(self.__on_open_modal_add_volume)

		# load_tree_demo()

	def __on_create_db(self, db_path):
		print(db_path)

		self.storage.close_storage()
		self.storage.create_storage(db_path)

		self.explorer_frame.refresh()


	def __on_open_db(self, db_path):
		self.storage.close_storage()
		self.storage.open_storage(db_path)

		self.explorer_frame.refresh()




	def __on_open_modal_add_volume(self):
		self.modal_add_volume = AddVolume(self)
		self.modal_add_volume.set_cb_complete(self.__on_scan_complete)


	def __on_scan_complete(self):
		self.explorer_frame.refresh()
		self.modal_add_volume = None















if __name__ == "__main__":


	# from .dummyloop import dummyloop

	# from base.iodum import iodum
	# from base.sender import sender


	app = MainWindow()
	app.mainloop()



# 	# root.geometry("350x250+300+300")
