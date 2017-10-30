#!/usr/bin/env python3
# -*- coding: utf-8 -*-


import tkinter
from tkinter import ttk

from app.storage import get_storage
from app.lib import dbus

from ..utils import qicon, aqicon




class Find(tkinter.Toplevel):
	def __init__(self, master=None, *args, **kwargs):
		super(Find, self).__init__(master, *args, **kwargs)
		self.title("Поиск")
		
		self.minsize(400, 300)
		
		self.storage = get_storage()

		self.main_frame = ttk.Frame(self)
		self.main_frame.pack(expand=True, fill="both")



		self.volumes = []								# список томов
		self.volumes_name_map = {}						# карта id: name
		self.files = []									# список найденых файлов

		self.var_file = tkinter.IntVar()
		self.var_file.set(1)
		self.var_folder = tkinter.IntVar()

		self.icon_folder = qicon("folder.png")
		self.icon_file = qicon("empty.png")




		group_edit = ttk.LabelFrame(self.main_frame, text="Поиск", padding=5)
		group_edit.pack(padx=10, pady=10, fill="x")



		#--- edit controls ----------------------------------------------------
		left_frame = ttk.Frame(group_edit)
		left_frame.pack(side="left")


		__label_term = ttk.Label(left_frame, text="Фраза:")
		__label_volume = ttk.Label(left_frame, text="Том:")
		__label_options = ttk.Label(left_frame, text="Опции:")



		self.search_entry = tkinter.Entry(left_frame, width=30, justify="left")
		self.volume_box = ttk.Combobox(left_frame, state='readonly')


		__options_frame = ttk.Frame(left_frame)
		ttk.Checkbutton(__options_frame, text="File", variable=self.var_file).grid(row=0, column=0)
		ttk.Checkbutton(__options_frame, text="Folder", variable=self.var_folder).grid(row=0, column=1)



		row = 0
		__label_term.grid(row=row, column=0, sticky="e", pady=5, padx=5)
		self.search_entry.grid(row=row, column=1, sticky="w", pady=5, padx=5)



		row += 1
		__label_volume.grid(row=row, column=0, sticky="e", pady=5, padx=5)
		self.volume_box.grid(row=row, column=1, sticky="w", pady=5, padx=5)



		row += 1
		__label_options.grid(row=row, column=0, sticky="e", pady=5, padx=5)
		__options_frame.grid(row=row, column=1, sticky="w", pady=5, padx=5)





		#--- actions ----------------------------------------------------------
		frame_actions = ttk.Frame(group_edit)
		frame_actions.pack(side="right", fill="x", expand=True)

		self.__icon_start = qicon("go_next.png")
		ttk.Button(frame_actions, text="Запустить", image=self.__icon_start, compound="left", command=self.__act_start).pack(side="right")

		



		#--- tree result ------------------------------------------------------
		frame_result = ttk.Frame(self.main_frame)
		frame_result.pack(side="top", expand=True, fill="both")

		columns = ("volume", "path")
		self.__tree = ttk.Treeview(frame_result, show="tree headings", selectmode='browse', columns=columns)
		self.__tree.heading('#0', text='Название')
		self.__tree.heading("volume", text="Том")
		self.__tree.heading("path", text="Путь")
		self.__tree.column("#0", minwidth=200, width=200)
		self.__tree.pack(side="left", expand=True, fill="both")
		self.__tree.bind("<Button-3>", self.__make_cmenu)


		self.__icon_menu_info = aqicon("info")
		self.cmenu = tkinter.Menu(self, tearoff=0)
		self.cmenu.add_command(label="Свойства", command=self.__show_info, image=self.__icon_menu_info, compound="left")

		#--- vertical scroll
		ysb = ttk.Scrollbar(frame_result, orient="vertical", command= self.__tree.yview)
		self.__tree['yscroll'] = ysb.set
		ysb.pack(side="right", expand=False, fill="y")





		#--- controls ---------------------------------------------------------
		controls_frame = ttk.Frame(self.main_frame)
		controls_frame.pack(fill="both", side="bottom", padx=10, pady=10)

		self.__icon_close = aqicon("close")
		ttk.Button(controls_frame, text="Закрыть(Ctrl+w)", image=self.__icon_close, compound="left", command=self.destroy).pack(side="right")

		self.bind_all("<Control-w>", lambda e: self.destroy())




		#--- start ------------------------------------------------------------
		self.__load()





		#--- debug ------------------------------------------------------------
		# self.search_entry.insert(0, "pro.json")








	def __load(self):
		"""предзагрузка данных"""
		self.volumes = self.storage.fetch_volumes(iscache=True)
		vnames = [volume.name for volume in self.volumes]

		vnames.insert(0, "All")

		self.volume_box.config(values=vnames)
		self.volume_box.current(0)

		#--- делаем карту имён для послед. быстрого поиска
		self.volumes_name_map = {v.uuid : v.name for v in self.volumes}






	def __act_start(self):
		"""запуск поиска"""

		volume_index = self.volume_box.current()
		if volume_index == 0:
			volume_id = None
		else:
			volume = self.volumes[volume_index - 1]
			volume_id = volume.uuid


		search_text = self.search_entry.get()
		

		is_file = self.var_file.get() == 1
		is_folder = self.var_folder.get() == 1


		self.files = self.storage.find_items(search_text, is_file=is_file, is_folder=is_folder, volume_id=volume_id)

		self.__clear()

		for item in self.files:
			self.__insert_file(item)


	def __clear(self):
		"""очистка списка"""
		for row in self.__tree.get_children():
			self.__tree.delete(row)


	def __insert_file(self, fnode):
		"""добавление строки данных"""

		name_path = fnode.make_parents_path(is_self=False)
		volume_name = self.__find_volume_name(fnode.volume_id)

		ivalues = (volume_name, name_path)

		icon = self.icon_folder if fnode.is_dir() else self.icon_file
		
		
		self.__tree.insert("", 'end', fnode.uuid, text=fnode.name, tags=("simple", ), image=icon, values=ivalues)




	def destroy(self):
		"""???"""
		# self.status = False
		tkinter.Toplevel.destroy(self)




	def __find_volume_name(self, volume_id):
		"""поиск имени тома"""
		return self.volumes_name_map.get(volume_id, "---")



	def __find_fnode(self, fnode_id):
		"""поиск объекта файла"""
		fnode = None
		for n in self.files:
			if n.uuid == fnode_id:
				fnode = n
				break

		return fnode


	def __make_cmenu(self, e):
		"""отображение контекстного меню"""
		cmenu_selection = self.__tree.identify_row(e.y)		# тек. елемент под курсором

		if cmenu_selection:
			self.__tree.selection_set(cmenu_selection)				# выделяем его

			#--- отображение меню
			self.cmenu.tk_popup(e.x_root, e.y_root)




	def __show_info(self):
		"""отображение модала информации"""
		selection = self.__tree.selection()
		if len(selection) == 0:
			return False

		selected_item = self.__tree.selection()[0]
		fnode = self.__find_fnode(selected_item)

		dbus.emit(dbus.SHOW_ABOUT_FILE, fnode)



