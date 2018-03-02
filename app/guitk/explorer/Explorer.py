#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import tkinter

from app.storage import get_storage
from app.lib import dbus


from .VList import VList
from .FList import FList




class Explorer(tkinter.Frame):
	def __init__(self, parent, *args, **kwargs):
		super(Explorer, self).__init__(parent, *args, **kwargs)



		self.v_list = VList(self)
		self.v_list.pack(side="left", expand=False, fill="y")
		self.v_list.set_select_cb(self.__on_select_volume)
		self.v_list.set_remove_cb(self.__on_remove_volume)

		self.f_list = FList(self)
		self.f_list.pack(side="right", expand=True, fill="both")


		# self.info_frame = InfoFrame(self, width=500, height=500)
		# self.info_frame.pack(side="right", expand=True, fill="both")
		#

		self.storage = get_storage()





		
		# self.history_stack = []
		# self.current_volume = None
		self.current_vnode = None


		self.v_list.reload_volumes()
		

		dbus.eon(dbus.SCAN_COMPLETE, self.refresh)



	def refresh(self):
		self.f_list.clear()
		self.v_list.reload_volumes()



	#--- volume actions -------------------------------------------------------
	def __on_select_volume(self, vnode):
		self.current_vnode = vnode
		# self.f_list.update_volume(self.current_vnode.uuid)
		self.f_list.show_volume(self.current_vnode)



	def __on_remove_volume(self, volume_uuid):
		
		self.storage.remove_volume(volume_uuid)
		self.refresh()
	#--- volume actions -------------------------------------------------------


















