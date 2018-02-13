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

from app import log
from app.storage import get_storage
from app.data import VOLUME_TYPE
from app.logic import scaner
from app.lib import dbus


from ..utils import ticons


def now_date():
	return time.strftime("%Y-%m-%d %H:%M:%S")






class AddVolume(tkinter.Toplevel):
	def __init__(self, master=None, *args, **kwargs):
		super(AddVolume, self).__init__(master, *args, **kwargs)
		self.title("Добавление тома")
		self.minsize(400, 300)

		self.storage = get_storage()
		self.volume_path = None
		self.volume_name = ""
		self.volume_description = ""
		self.volume_id = ""
		self.volume_vtype = VOLUME_TYPE[0]
		self.chan = Queue()
		self.cb_complete = None

		self.is_started = False

		self.main_frame = ttk.Frame(self)
		self.main_frame.pack(expand=True, fill="both")

		# select_frame = ttk.Frame(self.main_frame)
		# select_frame.pack(fill="x", side="top", padx=10, pady=10)

		# ttk.Button(select_frame, text="Выбрать каталог", command=self.__show_select_dir).pack(side="left")
		# self.select_label = ttk.Label(select_frame, text="--")
		# self.select_label.pack(side="left")


		edit_frame = ttk.Frame(self.main_frame)
		edit_frame.pack(fill="x", side="top", padx=10, pady=10)



		row = 0
		ttk.Label(edit_frame, text="Каталог: ").grid(row=row, column=0, sticky="e", pady=5, padx=5)
		self.scan_path_entry = ttk.Entry(edit_frame, width=30, justify="left")
		self.scan_path_entry.grid(row=row, column=1, sticky="w", pady=5, padx=5)
		ttk.Button(edit_frame, text="Выбрать каталог", command=self.__show_select_dir, image=ticons.ticon(ticons.OPEN_FOLDER)).grid(row=row, column=2, sticky="w", padx=5)
		# ttk.Button(edit_frame, text="Выбрать каталог", command=self.__show_select_dir, image=self.__icon_open_folder, compound="left").grid(row=row, column=2, sticky="w", padx=5)

		row += 1
		ttk.Label(edit_frame, text="Название тома: ").grid(row=row, column=0, sticky="e", pady=5, padx=5)
		self.volume_name_entry = ttk.Entry(edit_frame, width=30, justify="left")
		self.volume_name_entry.grid(row=row, column=1, sticky="w", pady=5, padx=5)

		row += 1
		ttk.Label(edit_frame, text="Иконка: ").grid(row=row, column=0, sticky="e", pady=5, padx=5)
		self.volume_type_box = ttk.Combobox(edit_frame, values=VOLUME_TYPE, state='readonly')
		self.volume_type_box.grid(row=row, column=1, sticky="w", pady=5, padx=5)
		self.volume_type_box.set(self.volume_vtype)
		self.volume_type_box.bind('<<ComboboxSelected>>', self.__update_volume_vtype)
		self.__label_vtype_icon = ttk.Label(edit_frame, text="icon")
		self.__label_vtype_icon.grid(row=row, column=2, sticky="w", pady=5, padx=5)
		self.__vtype_icon = None

		self.__update_volume_icon()



		self.description = tkinter.Text(self.main_frame, height=6, width=20)
		self.description.pack(side="top", fill="both", expand=True)


		# col_count, row_count = edit_frame.grid_size()
		# edit_frame.grid_columnconfigure(0, minsize=160)
		
		# for row in range(row_count):
		# 	edit_frame.grid_rowconfigure(row, minsize=30)

		# print(edit_frame.grid_size())



		results_frame = ttk.Frame(self.main_frame)
		results_frame.pack(fill="x", side="top", padx=10, pady=10)

		self.cur_file_operate = ttk.Label(results_frame, text="0")
		self.cur_file_operate.pack(side="left")

		ttk.Label(results_frame, text="/").pack(side="left")

		self.total_files = ttk.Label(results_frame, text="0")
		self.total_files.pack(side="left")
		self.total_files_count = 0
		self.current_prc = 0
		self.current_hold = 0



		self.progress_val = tkinter.IntVar()

		self.progress = ttk.Progressbar(results_frame, orient='horizontal', mode='determinate', variable=self.progress_val)
		self.progress.pack(side="left", expand=True, fill="both")

		# self.progress.start(50)
		self.progress_val.set(self.current_prc)


		

		#--- controls
		controls_frame = ttk.Frame(self.main_frame)
		controls_frame.pack(fill="both", side="bottom", padx=10, pady=10)



		# ttk.Button(controls_frame, text="Закрыть(Ctrl+w)", image=get_icon("application-exit"), compound="left", command=self.destroy).pack(side="right")
		self.__btn_start = ttk.Button(controls_frame, text="Запуск", command=self.__start_scan, image=ticons.ticon(ticons.GO_NEXT), compound="left")
		self.__btn_start.pack(side="left")

		self.__btn_close = ttk.Button(controls_frame, text="Закрыть(Ctrl+w)", command=self.destroy, image=ticons.ticon(ticons.CLOSE), compound="left")
		self.__btn_close.pack(side="right")


		#--- error label
		self.__label_error = ttk.Label(self.main_frame, text="", foreground="red")
		self.__label_error.pack(side="bottom", fill="x", padx=20)


		self.bind_all("<Control-w>", lambda e: self.destroy())



		self.stime_start = None
		self.stime_finish = None
		self.files_counter = 0


		self.__update_state()


	def destroy(self):
		# self.status = False
		tkinter.Toplevel.destroy(self)



	def __update_state(self):
		if self.is_started:
			self.__btn_start.config(state="disabled")
			self.__btn_close.config(state="disabled")
		else:
			self.__btn_start.config(state="enabled")
			self.__btn_close.config(state="enabled")


	def __update_volume_vtype(self, e):
		self.volume_vtype = self.volume_type_box.get()
		self.__update_volume_icon()


	def __update_volume_icon(self):
		# self.__vtype_icon = volume_icon(self.volume_vtype)
		self.__vtype_icon = ticons.vicon(self.volume_vtype)
		self.__label_vtype_icon.config(image=self.__vtype_icon)



	def __update_err(self, err_text):
		self.__label_error.config(text=err_text)
		

	def __show_select_dir(self):
		spath = filedialog.askdirectory()
		if spath:
			spath = os.path.normpath(spath)
			self.volume_path = spath
			# self.select_label.config(text=self.volume_path)

			volume_name = os.path.basename(self.volume_path)
			self.volume_name_entry.delete(0, "end")
			self.volume_name_entry.insert(0, volume_name)

			self.scan_path_entry.delete(0, "end")
			self.scan_path_entry.insert(0, self.volume_path)

			# self.__start_scan(spath)




	def __prepare_scan(self):

		if not os.path.exists(self.volume_path):
			return False, "выбранный каталог не существует"

		if len(self.volume_name) == 0:
			return False, "название не должно быть пустым"

		return True, None


	def __start_scan(self):
		"""запуск сканирования"""
		log.info("запуск сканирования")

		self.volume_path = self.scan_path_entry.get()
		self.volume_name = self.volume_name_entry.get()
		self.volume_description = self.description.get(1.0, tkinter.END)


		log.info("каталог для сканирования: " + self.volume_path)
		log.info("название: " + self.volume_name)

		#--- проверка входных данных
		self.__update_err("")
		result, err = self.__prepare_scan()

		if result is False:
			log.warning(err)
			self.__update_err(err)
			return False


		#--- обновляем статус
		self.is_started = True
		self.__update_state()


		self.stime_start = datetime.now()
		log.info("начало сканирования: " + now_date())



		#--- create volume record
		self.__create_volume_record()




		self.files_counter = 0


		#--- запуск канала чтения потока
		self.__start_chan_reader()


		# t = threading.Thread(target=scan_dir, args=(self.volume_path, self.chan))
		t = threading.Thread(target=scaner.start_scan, args=(self.volume_path, self.chan))
		t.start()





	def __create_volume_record(self):
		log.info("создание записи о томе")
		self.volume_id = str(uuid.uuid4())
		vdata = {
			"name" 			: self.volume_name,
			"uuid" 			: self.volume_id,
			"path" 			: self.volume_path,
			"vtype" 		: self.volume_vtype,
			"description"	: self.volume_description,
			"created" 		: now_date()
		}
		
		self.storage.create_volume_row(vdata)














	def __finish_scan(self):
		self.storage.commit()

		self.stime_finish = datetime.now()
		print("finish scan time: ", self.stime_finish.isoformat())
		delta = self.stime_finish - self.stime_start
		print("Scan time: ", delta.seconds)


		dbus.emit(dbus.SCAN_COMPLETE)
		self.destroy()

		#
		# if self.cb_complete:
		# 	self.cb_complete()
		# 	self.destroy()







	def __start_chan_reader(self):
		# log.info("запуск канала чтения потока")
		try:
			msg = self.chan.get(block=False)
		except:
			pass
		else:
			if msg["etype"] == scaner.ETYPE_START:
				pass

			elif msg["etype"] == scaner.ETYPE_FINISH:
				self.current_prc = 100
				self.progress_val.set(self.current_prc)
				self.__finish_scan()
				return True
			
			elif msg["etype"] == scaner.ETYPE_ERROR:
				pass
			
			elif msg["etype"] == scaner.ETYPE_COUNT:
				self.total_files_count = msg["payload"]
				self.total_files.config(text=str(self.total_files_count))
				self.current_hold = self.total_files_count/100
				self.current_prc = 0
				self.progress_val.set(self.current_prc)


			elif msg["etype"] == scaner.ETYPE_FILE:

				file_row = msg["payload"]
				# print("--->", msg)

				#--- долгие операции - 17 сек(без них - 3 сек)
				# full_path = os.path.join(msg["root"], msg["name"])
				# self.cur_file_operate.config(text=full_path)
				#--- долгие операции - 17 сек(без них - 3 сек)

				self.files_counter += 1

				# self.cur_file_operate.config(text=msg["name"])
				self.cur_file_operate.config(text=self.files_counter)

				file_row["volume_id"] = self.volume_id
				self.storage.create_file_row(file_row)


				self.current_prc = int(self.files_counter / self.current_hold)
				self.progress_val.set(self.current_prc)

			else:
				print("ERROR!!!!!!!!")

		self.after(1, self.__start_chan_reader)		

		


	def set_cb_complete(self, cb):
		self.cb_complete = cb










if __name__ == "__main__":

	from app.rc import FILE_DB_TEST
	# storage = get_storage()
	# storage.open_storage(FILE_DB_TEST)

	root = tkinter.Tk()

	modal = AddVolume(root)
	ttk.Button(root, text="quit", command=quit).pack()

	root.mainloop()
