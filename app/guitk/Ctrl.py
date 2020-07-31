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
		dbus.eon(dbus.SHOW_EXPORT_VOLUME_A, self.__on_show_export_volume_a)
		dbus.eon(dbus.SHOW_EXPORT_VOLUME_B, self.__on_show_export_volume_b)
		dbus.eon(dbus.SHOW_EXPORT_VOLUME_OK, self.__on_show_export_volume_ok)

		dbus.eon(dbus.SHOW_IMPORT_VOLUME, self.__on_show_import_volume)


		dbus.eon(dbus.SHOW_EXPORT_FTREE, self.show_export_ftree)
		# dbus.eon(dbus.SHOW_REMOVE_FTREE, self.show_remove_ftree)


	def __on_show_export_volume(self, volume_id, volume_name):
		"""запрос на сохранение экспорта тома"""
		title = "Расположение файла экспорта тома: " + volume_name
		file_name = volume_name + ".json"
		export_file_path = asksaveasfilename(defaultextension=".json", title=title, initialfile=file_name)
		# print(export_file_path)

		if export_file_path:
			storage = get_storage()
			storage.export_volume(volume_id, export_file_path)

	def __on_show_export_volume_a(self, volume_id, volume_name):
		"""запрос на сохранение экспорта тома"""
		title = "Расположение файла экспорта тома: " + volume_name
		file_name = volume_name + ".sson"
		export_file_path = asksaveasfilename(defaultextension=".sson", title=title, initialfile=file_name)
		# print(export_file_path)

		if export_file_path:
			storage = get_storage()
			storage.export_volume_a(volume_id, export_file_path)


	def __on_show_export_volume_b(self, volume_id, volume_name):
		"""запрос на сохранение экспорта тома"""
		title = "Расположение файла экспорта тома: " + volume_name
		file_name = volume_name + ".bss"
		export_file_path = asksaveasfilename(defaultextension=".bss", title=title, initialfile=file_name)
		# print(export_file_path)

		if export_file_path:
			storage = get_storage()
			storage.export_volume_b(volume_id, export_file_path)
			

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



	def show_export_ftree(self, fnode):
		"""запрос на сохранение экспорта ветви дерева"""


		items = [fnode]
		storage = get_storage()
		for item in storage.fetch_parent_files_all(fnode.uuid):
			items.append(item)


		print(len(items))



	# def show_remove_ftree(self, fnode):
	# 	"""запрос удаления ветви файлов"""
	#
	#
	# 	result = messagebox.askyesno("Подтверждение удаления", "Удалить выбранный элемент?")
	# 	if result is False:
	# 		return False
	#
	# 	storage = get_storage()
	#
	# 	#--- удаляем заданный
	# 	storage.remove_file(fnode.uuid)
	#
	# 	#--- удаляем все вложенные элементы
	# 	for item in storage.fetch_parent_files_all(fnode.uuid):
	# 		storage.remove_file(item.uuid)
	#
	# 	#--- сохраняем изменения
	# 	storage.commit()
	#
	# 	#--- сообщение об окончании
	# 	dbus.emit(dbus.SHOW_REMOVE_FTREE_OK)
