#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from app.lib import dbus

from . import AddVolume, AboutVolume, AboutFile, EditVolume

class ModalsCtrl(object):
	def __init__(self, main_win):
		self.main_win = main_win

		dbus.eon(dbus.SHOW_ABOUT_VOLUME, self.show_about_volume)
		dbus.eon(dbus.SHOW_ABOUT_FILE, self.show_about_file)
		dbus.eon(dbus.SHOW_EDIT_VOLUME, self.show_edit_volume)


	def show_about_volume(self, vnode):
		AboutVolume(vnode, master=self.main_win)

	def show_about_file(self, fnode):
		AboutFile(fnode, master=self.main_win)

	def show_edit_volume(self, vnode):
		EditVolume(vnode, master=self.main_win)
