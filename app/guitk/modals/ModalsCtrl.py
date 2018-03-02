#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from app.lib import dbus

from . import AddVolume, AboutFile, AboutVolume, AboutBase, Find
from .settings.Settings import Settings
from .DataBases import DataBases

class ModalsCtrl(object):
	def __init__(self, main_win):
		self.main_win = main_win

		dbus.eon(dbus.SHOW_ABOUT_VOLUME, self.show_about_volume)
		dbus.eon(dbus.SHOW_ABOUT_FILE, self.show_about_file)
		dbus.eon(dbus.SHOW_ADD_VOLUME, self.show_add_volume)
		dbus.eon(dbus.SHOW_ABOUT_BASE, self.show_about_base)
		dbus.eon(dbus.SHOW_FIND, self.show_find)
		dbus.eon(dbus.SHOW_SETTINGS, self.show_settings)
		dbus.eon(dbus.SHOW_DATABASES, self.show_databases)


	def show_about_volume(self, vnode):
		AboutVolume(vnode, master=self.main_win)

	def show_about_file(self, fnode):
		AboutFile(fnode, master=self.main_win)

	def show_add_volume(self):
		AddVolume(master=self.main_win)

	def show_about_base(self):
		AboutBase(master=self.main_win)

	def show_find(self):
		Find(master=self.main_win)

	def show_settings(self):
		Settings(master=self.main_win)


	def show_databases(self):
		DataBases(master=self.main_win)

