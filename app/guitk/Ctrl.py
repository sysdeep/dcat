#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from tkinter.filedialog import *
from tkinter import messagebox

from app.lib import dbus
from app.storage import get_storage

class Ctrl(object):
	def __init__(self):





		#--- bind events
		dbus.eon(dbus.SHOW_EXPORT_VOLUME, self.__on_show_export_volume)
		dbus.eon(dbus.SHOW_EXPORT_VOLUME_OK, self.__on_show_export_volume_ok)




	def __on_show_export_volume(self, volume_id):
		"""запрос на сохранение экспорта тома"""
		title = "Расположение файла экспорта тома"
		export_file_path = asksaveasfilename(defaultextension=".json", title=title)
		# print(export_file_path)

		if export_file_path:
			storage = get_storage()
			storage.export_volume(volume_id, export_file_path)



	def __on_show_export_volume_ok(self):
		"""отображение модала успешного экспорта тома"""
		messagebox.showinfo("Результат", "Экспорт выполнен")