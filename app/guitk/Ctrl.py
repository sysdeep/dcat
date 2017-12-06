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

		dbus.eon(dbus.SHOW_IMPORT_VOLUME, self.__on_show_import_volume)



	def __on_show_export_volume(self, volume_id, volume_name):
		"""запрос на сохранение экспорта тома"""
		title = "Расположение файла экспорта тома: " + volume_name
		file_name = volume_name + ".json"
		export_file_path = asksaveasfilename(defaultextension=".json", title=title, initialfile=file_name)
		# print(export_file_path)

		if export_file_path:
			storage = get_storage()
			storage.export_volume(volume_id, export_file_path)



	def __on_show_export_volume_ok(self):
		"""отображение модала успешного экспорта тома"""
		messagebox.showinfo("Результат", "Экспорт выполнен")






	def __on_show_import_volume(self):
		"""запрос на открытие импорта тома"""
		title = "Расположение файла импорта тома"

		messagebox.showwarning("Внимание", "В процессе разработки")

		# import_file_path = askopenfilename(
		# 		title=title,
		# 		defaultextension=".json", filetypes=[('DCat volume files', '.json')])
		#
		#
		# if import_file_path:
		# 	storage = get_storage()
		# 	storage.import_volume(import_file_path)