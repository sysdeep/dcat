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
from app.logic.SWalker import SWalker
from app.logic import scaner

class AddVolume(tkinter.Toplevel):
	def __init__(self, master=None, *args, **kwargs):
		super(AddVolume, self).__init__(master, *args, **kwargs)
		self.title("Добавление тома")
		# self.option_add("*Font", (GUI_FONT_NAME, GUI_FONT_SIZE))
		self.minsize(400, 300)
		# self.item = item
		# self.status = True
		# self.main_frame = SFrame(self, item=self.item)
		# self.main_frame.pack(fill="both", expand=True)

		self.storage = get_storage()
		self.volume_path = None
		self.volume_name = ""
		self.volume_id = ""
		self.chan = Queue()
		self.cb_complete = None

		self.main_frame = ttk.Frame(self)
		self.main_frame.pack(expand=True, fill="both")

		select_frame = ttk.Frame(self.main_frame)
		select_frame.pack(fill="x", side="top", padx=10, pady=10)

		ttk.Button(select_frame, text="Выбрать каталог", command=self.__show_select_dir).pack(side="left")
		self.select_label = ttk.Label(select_frame, text="--")
		self.select_label.pack(side="left")


		edit_frame = ttk.Frame(self.main_frame)
		edit_frame.pack(fill="x", side="top", padx=10, pady=10)

		self.volume_name_entry = ttk.Entry(edit_frame, width=30, justify="left")
		self.volume_name_entry.pack(side="left")
		ttk.Button(edit_frame, text="Запуск", command=self.__start_scan).pack(side="right")



		results_frame = ttk.Frame(self.main_frame)
		results_frame.pack(fill="x", side="top", padx=10, pady=10)

		self.cur_file_operate = ttk.Label(results_frame, text="")
		self.cur_file_operate.pack(side="left")


		controls_frame = ttk.Frame(self.main_frame)
		controls_frame.pack(fill="both", side="bottom", padx=10, pady=10)

		# ttk.Button(controls_frame, text="Закрыть(Ctrl+w)", image=get_icon("application-exit"), compound="left", command=self.destroy).pack(side="right")
		ttk.Button(controls_frame, text="Закрыть(Ctrl+w)", command=self.destroy).pack(side="right")

		self.bind_all("<Control-w>", lambda e: self.destroy())



		self.stime_start = None
		self.stime_finish = None
		self.files_counter = 0



	def destroy(self):
		# self.status = False
		tkinter.Toplevel.destroy(self)




	def __show_select_dir(self):
		spath = filedialog.askdirectory()
		if spath:
			spath = os.path.normpath(spath)
			self.volume_path = spath
			self.select_label.config(text=self.volume_path)

			volume_name = os.path.basename(self.volume_path)
			self.volume_name_entry.delete(0, "end")
			self.volume_name_entry.insert(0, volume_name)

			# self.__start_scan(spath)



	def __start_scan(self):
		print("start scan dir: ", self.volume_path)
		self.volume_name = self.volume_name_entry.get()
		print("volume_name: ", self.volume_name)

		self.stime_start = datetime.now()
		print("start scan time: ", self.stime_start.isoformat())

		self.files_counter = 0

		self.__start_chan_reader()



		
		self.volume_id = str(uuid.uuid4())
		vdata = {
			"name": self.volume_name,
			"uuid": self.volume_id
		}
		
		self.storage.create_volume_row(vdata)


		# t = threading.Thread(target=scan_dir, args=(self.volume_path, self.chan))
		t = threading.Thread(target=scaner.start_scan, args=(self.volume_path, self.chan))
		t.start()



	def __finish_scan(self):
		self.storage.commit()

		self.stime_finish = datetime.now()
		print("finish scan time: ", self.stime_finish.isoformat())
		delta = self.stime_finish - self.stime_start
		print("Scan time: ", delta.seconds)


		if self.cb_complete:
			self.cb_complete()
			self.destroy()

	def __start_chan_reader(self):
		try:
			msg = self.chan.get(block=False)
		except:
			pass
		else:
			if msg["type"] == "finish":
				self.__finish_scan()
				return True
			else:
				# print("--->", msg)

				#--- долгие операции - 17 сек(без них - 3 сек)
				# full_path = os.path.join(msg["root"], msg["name"])
				# self.cur_file_operate.config(text=full_path)
				#--- долгие операции - 17 сек(без них - 3 сек)

				self.files_counter += 1

				# self.cur_file_operate.config(text=msg["name"])
				self.cur_file_operate.config(text=self.files_counter)

				msg["volume_id"] = self.volume_id
				self.storage.create_file_row(msg)

		self.after(1, self.__start_chan_reader)		

		

		# swalker = SWalker()
		# swalker.storage = self.storage
		# swalker.set_scan_volume(spath)
		# swalker.start_scan()


	# def set_item(self, item):
	# 	self.main_frame.set_item(item)

	def set_cb_complete(self, cb):
		self.cb_complete = cb





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

	modal = AddVolume(root)
	ttk.Button(root, text="quit", command=quit).pack()

	root.mainloop()