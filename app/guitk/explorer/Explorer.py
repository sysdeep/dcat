#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import tkinter

from app.storage import get_storage
from app.lib import dbus


from .VList import VList
from .FList import FList
from .info_frame import InfoFrame



class Explorer(tkinter.Frame):
	def __init__(self, parent, *args, **kwargs):
		super(Explorer, self).__init__(parent, *args, **kwargs)


		#--- volumes
		self.v_list = VList(self)
		self.v_list.pack(side="left", expand=False, fill="y")
		self.v_list.set_select_cb(self.__on_volume_selected)
		self.v_list.set_remove_cb(self.__on_volume_do_remove)

		#--- volume/file info frame
		self.__info_frame = InfoFrame(self, width=500, height=500)
		self.__info_frame.pack(side="right", expand=True, fill="both")

		#--- files
		self.__f_list = FList(self)
		self.__f_list.signal_file_selected.connect(self.__on_fnode_selected)
		self.__f_list.pack(side="right", expand=True, fill="both")


		
		#

		self.storage = get_storage()





		
		# self.history_stack = []
		# self.current_volume = None
		self.current_vnode = None


		self.v_list.reload_volumes()
		

		dbus.eon(dbus.SCAN_COMPLETE, self.refresh)



	def refresh(self):
		"""полное обновление"""
		self.__f_list.clear()										# очистка списка файлов
		self.__info_frame.drop_volume()								# сброс информации о томе
		self.v_list.reload_volumes()								# обновление списка томов



	#--- volume actions -------------------------------------------------------
	def __on_volume_selected(self, vnode):
		"""событие выбора тома"""
		self.current_vnode = vnode
		
		self.__f_list.show_volume(self.current_vnode)				# обновляем список файлов
		self.__info_frame.update_volume(vnode)						# обновляем инфо о томе
		self.__info_frame.drop_file()								# т.к. том новый - файлов нет
		



	def __on_volume_do_remove(self, volume_uuid):
		"""запрос на удаление тома"""
		self.storage.remove_volume(volume_uuid)
		self.refresh()
	#--- volume actions -------------------------------------------------------





	#--- events ---------------------------------------------------------------
	def __on_fnode_selected(self, fnode):
		"""событие о выборе ноды"""
		self.__info_frame.update_file(fnode)			# обновляем инфо ноды
	#--- events ---------------------------------------------------------------












