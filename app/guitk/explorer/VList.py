#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import re
import tkinter
from tkinter import ttk
from tkinter import messagebox

# from vendor.natsort import natsorted
from app.storage import get_storage, sbus
from app.lib import dbus, sorting
from ..utils import ticons




class VList(tkinter.Frame):
	def __init__(self, parent, *args, **kwargs):
		super(VList, self).__init__(parent, *args, **kwargs)


		self.storage = get_storage()
		self.current_volume_id = None

		self.select_cb = None
		self.remove_cb = None
		self.cb_open_modal_add_volume = None


		self.__volumes_map = {}
		self.volume_icons = []



		list_frame = tkinter.Frame(self)
		list_frame.pack(side="top", expand=True, fill="both")

		self.__list = ttk.Treeview(list_frame, show="tree", selectmode='browse')
		self.__list.pack(side="left", expand=True, fill="both")
		self.__list.bind("<Button-3>", self.__make_cmenu)


		#--- vertical scroll
		ysb = ttk.Scrollbar(list_frame, orient="vertical", command= self.__list.yview)
		self.__list['yscroll'] = ysb.set
		ysb.pack(side="right", expand=False, fill="y")

		self.__list.column("#0", width=200)
		self.__list.tag_bind("simple", "<<TreeviewSelect>>", self.__select_row)
		# self.__list.bind("<Double-1>", self.__open_row)




		self.cmenu = tkinter.Menu(self, tearoff=0)
		self.cmenu.add_command(label="Свойства", command=self.__show_info, image=ticons.ticon(ticons.INFO), compound="left")
		self.cmenu.add_command(label="Удалить", command=self.__remove_volume, image=ticons.ticon(ticons.TRASH), compound="left")
		self.cmenu.add_command(label="Экспорт", command=self.__export_volume, image=ticons.ticon(ticons.I_EXPORT), compound="left")
		self.cmenu.add_command(label="Экспорт A", command=self.__export_volume_a, image=ticons.ticon(ticons.I_EXPORT), compound="left")
		self.cmenu.add_command(label="Экспорт B", command=self.__export_volume_b, image=ticons.ticon(ticons.I_EXPORT), compound="left")
		self.cmenu.add_command(label="Экспорт 10", command=self.__export_volume_10, image=ticons.ticon(ticons.I_EXPORT), compound="left")
		# self.cmenu.add_separator()
		# self.cmenu.add_command(label="Закрыть", command=self.__hide_cmenu)


		# self.toolbar = Toolbar(parent=self)
		# self.toolbar.pack(side="bottom", expand=False, fill="x")
		# self.toolbar.cb_add_volume = self.__add_volume
		# self.toolbar.cb_remove_volume = self.__remove_volume
		# self.toolbar.cb_show_info = self.__show_info
		# self.toolbar.cb_show_edit = self.__show_edit


		sbus.eon(sbus.STORAGE_VOLUME_UPDATED, self.__on_volume_updated)



	def __make_cmenu(self, e):
		"""отображение контекстного меню"""
		cmenu_selection = self.__list.identify_row(e.y)		# тек. елемент под курсором

		if cmenu_selection:
			self.__list.selection_set(cmenu_selection)				# выделяем его
			self.__select_row(None)									# выполняем действия по отображению выбора

			#--- отображение меню
			# self.cmenu.post(e.x_root, e.y_root)
			self.cmenu.tk_popup(e.x_root, e.y_root)					# автозакрытие при потере фокуса(https://stackoverflow.com/questions/21200516/python3-tkinter-popup-menu-not-closing-automatically-when-clicking-elsewhere)


	


	def reload_volumes(self):
		"""обновление списка томов"""
		self.__clear()
		self.current_volume_id = None
		self.__volumes_map = {}
		self.__insert_volumes()
		# self.is_locked = True




	


	def __insert_volumes(self):
		self.volume_icons = []
		volumes = self.storage.fetch_volumes()


		# abdig_sort = lambda var: [int(x) if x.isdigit() else x for x in re.findall(r'[^0-9]|[0-9]+', var.name)]

		# volumes.sort(key=lambda vnode: vnode.name)
		# volumes.sort(key=abdig_sort)
		convert = lambda text: int(text) if text.isdigit() else text
		alphanum_key = lambda key: [convert(c) for c in re.split(r'([0-9]+)', key.name)]
		volumes.sort(key=alphanum_key)


		#
		# names = [x.name for x in volumes]
		# print(natsorted(names))



		for vnode in volumes:
			# ivolume = volume_icon(vnode.vtype)
			ivolume = ticons.vicon(vnode.vtype)
			self.volume_icons.append(ivolume)
			self.__list.insert('', 'end', vnode.uuid, text=vnode.name, tags=("simple", ), image=ivolume)
			self.__volumes_map[vnode.uuid] = vnode



	def __clear(self):
		for row in self.__list.get_children():
			self.__list.delete(row)



	def __select_row(self, e):

		selection = self.__list.selection()

		#--- если ничего не выбрано - ничего не делаем
		if len(selection) == 0:
			return False
		

		vnode_uuid = self.__list.selection()[0]


		#--- если выбранный элемент равен текущему - ничего не делаем
		#--- 2017.10.27 - неудобно... нельзя быстро переместиться в корень...
		# if self.current_volume_id == vnode_uuid:
		# 	return False

		self.current_volume_id = vnode_uuid

		vnode = self.__volumes_map[vnode_uuid]

		if self.select_cb:
			self.select_cb(vnode)








	#--- toolbar actions ------------------------------------------------------
	def __remove_volume(self):
		

		if self.current_volume_id and self.remove_cb:
			result = messagebox.askyesno("Подтверждение удаления тома", "Удалить выбранный том?")
			if result:
				self.remove_cb(self.current_volume_id)



	# def __add_volume(self):
	# 	if self.cb_open_modal_add_volume:
	# 		self.cb_open_modal_add_volume()


	def __show_info(self):
		"""отображение модала о томе"""
		if self.current_volume_id is None:
			return False

		vnode = self.__volumes_map[self.current_volume_id]
		dbus.emit(dbus.SHOW_ABOUT_VOLUME, vnode)




	def __export_volume(self):
		"""отобразить окно экспорта заданного тома"""
		if self.current_volume_id is None:
			return False

		vnode = self.__volumes_map[self.current_volume_id]

		dbus.emit(dbus.SHOW_EXPORT_VOLUME, self.current_volume_id, vnode.name)



	def __export_volume_a(self):
		"""отобразить окно экспорта заданного тома"""
		if self.current_volume_id is None:
			return False

		vnode = self.__volumes_map[self.current_volume_id]

		dbus.emit(dbus.SHOW_EXPORT_VOLUME_A, self.current_volume_id, vnode.name)
		
		
	def __export_volume_b(self):
		"""отобразить окно экспорта заданного тома"""
		if self.current_volume_id is None:
			return False

		vnode = self.__volumes_map[self.current_volume_id]

		dbus.emit(dbus.SHOW_EXPORT_VOLUME_B, self.current_volume_id, vnode.name)

	def __export_volume_10(self):
		"""отобразить окно экспорта заданного тома"""
		if self.current_volume_id is None:
			return False

		vnode = self.__volumes_map[self.current_volume_id]

		dbus.emit(dbus.SHOW_EXPORT_VOLUME_10, self.current_volume_id, vnode.name)

	# def __show_edit(self):
	# 	"""отображение модала редактирования тома"""
	#
	# 	if self.current_volume_id is None:
	# 		return False
	#
	# 	vnode = self.__volumes_map[self.current_volume_id]
	# 	dbus.emit(dbus.SHOW_EDIT_VOLUME, vnode)
	#--- toolbar actions ------------------------------------------------------
		




	#--- set cbs --------------------------------------------------------------
	def set_select_cb(self, cb):
		self.select_cb = cb

	def set_remove_cb(self, cb):
		self.remove_cb = cb

	def set_cb_open_modal_add_volume(self, cb):
		self.cb_open_modal_add_volume = cb
	#--- set cbs --------------------------------------------------------------


	def __on_volume_updated(self, volume_uuid):
		"""событие об обновлении данных тома"""
		self.reload_volumes()						# обновляем весь список
		self.current_volume_id = volume_uuid
		self.__list.selection_set(volume_uuid)		# выделяем текуший








# class Toolbar(ttk.Frame):
# 	def __init__(self, parent, *args, **kwargs):
# 		super(Toolbar, self).__init__(parent, *args, **kwargs)

# 		self.cb_add_volume 		= None
# 		self.cb_remove_volume 	= None
# 		self.cb_show_info 		= None
# 		self.cb_show_edit 		= None

# 		self.icon_add 			= qicon("edit_add.png")
# 		self.icon_remove 		= qicon("edittrash.png")
# 		self.icon_info 			= aqicon("info")
# 		self.icon_edit 			= aqicon("edit")

# 		# self.btn_add_volume = tkinter.Button(self, text="add", command=self.__add_volume, image=self.icon_add, relief="flat")
# 		self.btn_add_volume = ttk.Button(self, text="add", command=self.__add_volume, image=self.icon_add)
# 		self.btn_add_volume.pack(side="left")

# 		# self.btn_show_edit = tkinter.Button(self, text="edit", command=self.__show_edit, image=self.icon_edit, relief="flat")
# 		self.btn_show_edit = ttk.Button(self, text="edit", command=self.__show_edit, image=self.icon_edit)
# 		self.btn_show_edit.pack(side="left")

# 		# self.btn_show_info = tkinter.Button(self, text="info", command=self.__show_info, image=self.icon_info, relief="flat")
# 		self.btn_show_info = ttk.Button(self, text="info", command=self.__show_info, image=self.icon_info)
# 		self.btn_show_info.pack(side="left")

# 		# self.btn_remove_volume = tkinter.Button(self, text="remove", command=self.__remove_volume, image=self.icon_remove, relief="flat")
# 		self.btn_remove_volume = ttk.Button(self, text="remove", command=self.__remove_volume, image=self.icon_remove)
# 		self.btn_remove_volume.pack(side="right")


# 	def __add_volume(self):
# 		self.cb_add_volume()

# 	def __remove_volume(self):
# 		# result = messagebox.askquestion("Remove", "Remove&&")
		
# 		self.cb_remove_volume()

# 	def __show_info(self):
# 		self.cb_show_info()

# 	def __show_edit(self):
# 		self.cb_show_edit()

