#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os.path
import threading
import time
from queue import Queue
import uuid
from datetime import datetime

import tkinter
from tkinter import ttk
from tkinter import filedialog

from app.storage import get_storage
from app.data import VOLUME_TYPE
from app.logic.SWalker import SWalker
from app.logic import scaner
from app.lib import dbus

from app.lib.fsize import naturalsize
from ..utils import qicon, conv


# def now_date():
# 	return time.strftime("%Y-%m-%d %H:%M:%S")








class Find(tkinter.Toplevel):
	def __init__(self, master=None, *args, **kwargs):
		super(Find, self).__init__(master, *args, **kwargs)
		self.title("Поиск")
		
		self.minsize(400, 300)
		
		self.storage = get_storage()
		# self.volume_path = None
		# self.volume_name = ""
		# self.volume_id = ""
		# self.volume_vtype = VOLUME_TYPE[0]
		# self.chan = Queue()
		# self.cb_complete = None

		self.main_frame = ttk.Frame(self)
		self.main_frame.pack(expand=True, fill="both")









		group_edit = tkinter.LabelFrame(self.main_frame, text="Поиск", padx=5, pady=5)
		group_edit.pack(padx=10, pady=10, fill="x")


		frame_edit = tkinter.Frame(group_edit)
		frame_edit.pack(side="top", fill="x", expand=True)


		tkinter.Label(frame_edit, text="Фраза: ").pack(side="left")
		self.search_entry = tkinter.Entry(frame_edit, width=30, justify="left")
		self.search_entry.pack(side="left")


		frame_options = tkinter.Frame(group_edit)
		frame_options.pack(side="top", fill="x", expand=True)

		tkinter.Label(frame_options, text="Опции: ").pack(side="left")




		self.var_file = tkinter.IntVar()
		self.var_file.set(1)
		self.var_folder = tkinter.IntVar()
		# self.var_register = tkinter.IntVar()



		self.cbutton_file = tkinter.Checkbutton(frame_options, text="File", variable=self.var_file)
		self.cbutton_file.pack(side="left")

		self.cbutton_folder = tkinter.Checkbutton(frame_options, text="Folder", variable=self.var_folder)
		self.cbutton_folder.pack(side="left")

		# self.cbutton_register = tkinter.Checkbutton(frame_options, text="Register", variable=self.var_register)
		# self.cbutton_register.pack(side="left")

		
		frame_actions = tkinter.Frame(group_edit)
		frame_actions.pack(side="top", fill="x", expand=True)





		tkinter.Button(frame_actions, text="Start", command=self.__act_start).pack(side="right")

		



		columns=(
			"path",
			'size', 
			# 'rights', "owner", "group", 
			"ctime", 
			# "atime", "mtime"
			)

		self.__tree = ttk.Treeview(self.main_frame, show="tree headings", selectmode='browse', columns=columns)
		
		# self.__tree.heading("size", text="Размер", command=lambda c="size": self.__sort(c))
		self.__tree.heading('#0', text='Название')
		self.__tree.heading("size", text="Размер")
		# self.__tree.heading("rights", text="Права")
		# self.__tree.heading("owner", text="Владелец")
		# self.__tree.heading("group", text="Группа")
		self.__tree.heading("path", text="Путь")
		self.__tree.heading("ctime", text="Создание")
		# self.__tree.heading("atime", text="Доступ")
		# self.__tree.heading("mtime", text="Модификация")


		self.__tree.column("#0", minwidth=200, width=200)
		self.__tree.column("size", minwidth=90, width=90)
		# self.__tree.column("rights", minwidth=40, width=50)
		# self.__tree.column("owner", minwidth=80, width=80)
		# self.__tree.column("group", minwidth=80, width=80)
		self.__tree.column("ctime", minwidth=200, width=200)
		# self.__tree.column("atime", minwidth=90, width=90)
		# self.__tree.column("mtime", minwidth=100, width=100)


		# for c in columns:
		# 	self.__tree.heading(c, text=c, command=lambda c=c: self.__sort(c))

		self.__tree.pack(side="top", expand=True, fill="both")



		#--- vertical scroll
		# ysb = ttk.Scrollbar(self, orient="vertical", command= self.__tree.yview)
		# self.__tree['yscroll'] = ysb.set
		# ysb.pack(side="right", expand=False, fill="y")

		# self.__tree.column("#0", width=300)
		# self.__tree.tag_bind("simple", "<<TreeviewSelect>>", self.__select_row)
		# self.__tree.bind("<Double-1>", self.__open_row)
		
		self.icon_folder = qicon("folder.png")
		self.icon_file = qicon("empty.png")



		# row = 0
		# ttk.Label(edit_frame, text="Каталог: ").grid(row=row, column=0, sticky="e")
		# self.scan_path_entry = ttk.Entry(edit_frame, width=30, justify="left")
		# self.scan_path_entry.grid(row=row, column=1, sticky="w")
		# ttk.Button(edit_frame, text="Выбрать каталог", command=self.__show_select_dir).grid(row=row, column=2, sticky="w")

		# row += 1
		# ttk.Label(edit_frame, text="Название тома: ").grid(row=row, column=0, sticky="e")
		# self.volume_name_entry = ttk.Entry(edit_frame, width=30, justify="left")
		# self.volume_name_entry.grid(row=row, column=1, sticky="w")

		# row += 1
		# ttk.Label(edit_frame, text="Иконка: ").grid(row=row, column=0, sticky="e")
		# self.volume_type_box = ttk.Combobox(edit_frame, values=VOLUME_TYPE, state='readonly')
		# self.volume_type_box.grid(row=row, column=1, sticky="w")
		# self.volume_type_box.set(self.volume_vtype)
		# self.volume_type_box.bind('<<ComboboxSelected>>', self.__update_volume_vtype)






		# results_frame = ttk.Frame(self.main_frame)
		# results_frame.pack(fill="x", side="top", padx=10, pady=10)

		# self.cur_file_operate = ttk.Label(results_frame, text="")
		# self.cur_file_operate.pack(side="left")


		controls_frame = ttk.Frame(self.main_frame)
		controls_frame.pack(fill="both", side="bottom", padx=10, pady=10)

		# ttk.Button(controls_frame, text="Закрыть(Ctrl+w)", image=get_icon("application-exit"), compound="left", command=self.destroy).pack(side="right")
		# ttk.Button(controls_frame, text="Запуск", command=self.__start_scan).pack(side="left")
		ttk.Button(controls_frame, text="Закрыть(Ctrl+w)", command=self.destroy).pack(side="right")

		self.bind_all("<Control-w>", lambda e: self.destroy())



		# self.stime_start = None
		# self.stime_finish = None
		# self.files_counter = 0

		self.search_entry.insert(0, "ant")



	def __act_start(self):


		search_text = self.search_entry.get()
		

		# print(self.var_file.get())
		# print(self.var_folder.get())
		# print(self.var_register.get())


		is_file = self.var_file.get() == 1
		is_folder = self.var_folder.get() == 1


		items = self.storage.find_items(search_text, is_file=is_file, is_folder=is_folder)

		self.__clear()
		for item in items:
			# print(item.name)

			self.__insert_file(item)


	def __clear(self):
		for row in self.__tree.get_children():
			self.__tree.delete(row)


	def __insert_file(self, fnode):

		if fnode.is_dir():
			ftype = "dir"
			icon = self.icon_folder
			size = ""
		else:
			ftype = "file"
			icon = self.icon_file
			size = naturalsize(fnode.size)



		name_path = fnode.make_parents_path(is_self=False)
		ivalues = (
			name_path,
				size,
				# file_row[FRow.RIGHTS],
				# file_row[FRow.OWNER],
				# file_row[FRow.GROUP],
				conv.convert_ctime(fnode.ctime),
				# conv.convert_ctime(file_row[FRow.ATIME]),
				# conv.convert_ctime(file_row[FRow.MTIME]),
			)


		
		
		self.__tree.insert("", 'end', fnode.uuid, text=fnode.name, tags=("simple", ), image=icon, values=ivalues)
		# self.__tree.insert("", 'end', fnode.uuid, text=name_text, tags=("simple", ), image=icon, values=ivalues)

		# self.litems[fnode.uuid] = fnode


	def destroy(self):
		# self.status = False
		tkinter.Toplevel.destroy(self)


	# def __update_volume_vtype(self, e):
	# 	self.volume_vtype = self.volume_type_box.get()
	# 	# print(self.volume_vtype)


	# def __show_select_dir(self):
	# 	spath = filedialog.askdirectory()
	# 	if spath:
	# 		spath = os.path.normpath(spath)
	# 		self.volume_path = spath
	# 		# self.select_label.config(text=self.volume_path)

	# 		volume_name = os.path.basename(self.volume_path)
	# 		self.volume_name_entry.delete(0, "end")
	# 		self.volume_name_entry.insert(0, volume_name)

	# 		self.scan_path_entry.delete(0, "end")
	# 		self.scan_path_entry.insert(0, self.volume_path)

	# 		# self.__start_scan(spath)



	# def __start_scan(self):
	# 	print("start scan dir: ", self.volume_path)
	# 	self.volume_name = self.volume_name_entry.get()
	# 	print("volume_name: ", self.volume_name)

	# 	self.stime_start = datetime.now()
	# 	print("start scan time: ", self.stime_start.isoformat())

	# 	self.files_counter = 0

	# 	self.__start_chan_reader()



		
	# 	self.volume_id = str(uuid.uuid4())
	# 	vdata = {
	# 		"name": self.volume_name,
	# 		"uuid": self.volume_id,
	# 		"path": self.volume_path,
	# 		"vtype": self.volume_vtype,
	# 		"created": now_date()
	# 	}
		
	# 	self.storage.create_volume_row(vdata)


	# 	# t = threading.Thread(target=scan_dir, args=(self.volume_path, self.chan))
	# 	t = threading.Thread(target=scaner.start_scan, args=(self.volume_path, self.chan))
	# 	t.start()



	# def __finish_scan(self):
	# 	self.storage.commit()

	# 	self.stime_finish = datetime.now()
	# 	print("finish scan time: ", self.stime_finish.isoformat())
	# 	delta = self.stime_finish - self.stime_start
	# 	print("Scan time: ", delta.seconds)


	# 	dbus.emit(dbus.SCAN_COMPLETE)
	# 	self.destroy()

	# 	#
	# 	# if self.cb_complete:
	# 	# 	self.cb_complete()
	# 	# 	self.destroy()







	# def __start_chan_reader(self):
	# 	try:
	# 		msg = self.chan.get(block=False)
	# 	except:
	# 		pass
	# 	else:
	# 		if msg["type"] == "finish":
	# 			self.__finish_scan()
	# 			return True
	# 		else:
	# 			# print("--->", msg)

	# 			#--- долгие операции - 17 сек(без них - 3 сек)
	# 			# full_path = os.path.join(msg["root"], msg["name"])
	# 			# self.cur_file_operate.config(text=full_path)
	# 			#--- долгие операции - 17 сек(без них - 3 сек)

	# 			self.files_counter += 1

	# 			# self.cur_file_operate.config(text=msg["name"])
	# 			self.cur_file_operate.config(text=self.files_counter)

	# 			msg["volume_id"] = self.volume_id
	# 			self.storage.create_file_row(msg)

	# 	self.after(1, self.__start_chan_reader)		

		

	# 	# swalker = SWalker()
	# 	# swalker.storage = self.storage
	# 	# swalker.set_scan_volume(spath)
	# 	# swalker.start_scan()


	# # def set_item(self, item):
	# # 	self.main_frame.set_item(item)

	# def set_cb_complete(self, cb):
	# 	self.cb_complete = cb





# def scan_dir(dir_path, chan):
# 	for root, dirs, files in os.walk(dir_path):

# 		for d in dirs:
# 			fpath = os.path.join(root, d)
# 			print(fpath)
# 			chan.put(fpath)


# 		for d in files:
# 			fpath = os.path.join(root, d)
# 			print(fpath)
# 			chan.put(fpath)

# 		# time.sleep(1)

# 	chan.put("finish")













if __name__ == "__main__":

	from app.rc import FILE_DB_TEST
	storage = get_storage()
	storage.open_storage(FILE_DB_TEST)

	root = tkinter.Tk()

	modal = Find(root)
	ttk.Button(root, text="quit", command=quit).pack()

	root.mainloop()