#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
	scaner - сканирование заданной директории в потоке
	в процессе выполнения шлёт данные в очередь

	для windows - проблема с правами - пока отключено
"""

import os
import time
import uuid

from app.lib.tools import dtimeit
from app.storage import FType
from app import log

from .models import make_frow



#--- user perms ---------------------------------------------------------------
# from pwd import getpwuid, getpwall
# from grp import getgrgid, getgrall

# USERS = {}
# GROUPS = {}

# for item in getpwall():
#	USERS[item.pw_uid] = item.pw_name

# for item in getgrall():
#	GROUPS[item.gr_gid] = item.gr_name
#--- user perms ---------------------------------------------------------------






#--- типы пакетов, отправляемых в канал
ETYPE_START 	= "start"					# запуск
ETYPE_FINISH	= "finish"					# завершение
ETYPE_ERROR 	= "error"					# ошибка
ETYPE_FILE 		= "file"					# полезная нагрузка в виде файла
ETYPE_COUNT 	= "count"					# полезная нагрузка - кол-во файлов для сканирования









@dtimeit
def get_fcount(rpath):
	"""получить кол-во файлов для сканирования"""
	counter = 0
	for root, dirs, files in os.walk(rpath):
		counter += len(dirs)
		counter += len(files)

	return counter





def make_event(etype, payload=None):
	"""создать пакет для отправки"""
	return {
		"etype"		: etype,
		"payload"	: payload
	}



@dtimeit
def start_scan(dir_path, chan):
	log.info("запуск сканирования каталога")

	chan.put(make_event(ETYPE_START))


	files_count = get_fcount(dir_path)
	log.info("кол-во файлов: " + str(files_count))
	chan.put(make_event(ETYPE_COUNT, files_count))


	# # print(getpwall())




	#--- карта - path : id
	rmap = {
		# volume_path    : "0"
		dir_path		: "0"
	}



	for root, dirs, files in os.walk(dir_path):


		#--- id родителя
		parent_id = rmap[root]


		
		#--- каталоги
		for d in dirs:


			full_path = os.path.join(root, d)				# полный путь
			if not os.path.exists(full_path):				# если нет - продолжаем...
				continue

			rid = str(uuid.uuid4())							# id
			rmap[full_path] = rid							# сохраняем полный путь и id для получения id родителя

			st = os.stat(full_path)							# статистика по файлу

			row = make_frow(rid, d, parent_id, FType.DIR, st)
			row["root"]	= root


			chan.put(make_event(ETYPE_FILE, row))




		#--- файлы
		for f in files:

			full_path = os.path.join(root, f)
			if not os.path.exists(full_path):
				continue

			rid = str(uuid.uuid4())

			st = os.stat(full_path)

			row = make_frow(rid, f, parent_id, FType.FILE, st)

			row["root"]	= root

			chan.put(make_event(ETYPE_FILE, row))


		#--- очищаем карту...
		del rmap[root] 



	log.info("сканирование завершено")
	chan.put(make_event(ETYPE_FINISH))












def start_scan_for_storage(dir_path, storage, vol_id):
	"""!!! для тестов с прямой записью в базу"""


	#--- карта - path : id
	rmap = {
		dir_path		: "0"
	}



	for root, dirs, files in os.walk(dir_path):


		#--- id родителя
		parent_id = rmap[root]



		#--- каталоги
		for d in dirs:


			full_path = os.path.join(root, d)				# полный путь
			if not os.path.exists(full_path):				# если нет - продолжаем...
				continue

			rid = str(uuid.uuid4())							# id
			rmap[full_path] = rid							# сохраняем полный путь и id для получения id родителя

			st = os.stat(full_path)							# статистика по файлу

			row = make_frow(rid, d, parent_id, FType.DIR, st)
			row["root"]	= root
			row["volume_id"]	= vol_id

			storage.create_file_row(row)


			# chan.put(make_event(ETYPE_FILE, row))




		#--- файлы
		for f in files:

			full_path = os.path.join(root, f)
			if not os.path.exists(full_path):
				continue

			rid = str(uuid.uuid4())

			st = os.stat(full_path)

			row = make_frow(rid, f, parent_id, FType.FILE, st)

			row["root"]	= root

			row["volume_id"]	= vol_id
			# chan.put(make_event(ETYPE_FILE, row))

			storage.create_file_row(row)


		#--- очищаем карту...
		del rmap[root]





















if __name__ == "__main__":

	import time
	import sys
	import threading
	from queue import Queue
	from datetime import datetime



	PATH = "/mnt/data/_Devel/_Python/_DCat/dcat"
	CHAN = Queue()

	# print("counter")
	# aa = get_fcount(PATH)
	# print(aa)

	# print("main scan")
	# start_scan(PATH, CHAN)


	# sys.exit(0)



	# def resolve(row):
	# 	print(row)


	def start_worker():
		global PATH, CHAN
		t = threading.Thread(target=start_scan, args=(PATH, CHAN))
		t.start()


	tstart = datetime.now()
	start_worker()

	ccc = 0
	while True:
		msg = CHAN.get()

		if msg["etype"] == ETYPE_START:
			print("--- start ---")

		elif msg["etype"] == ETYPE_COUNT:
			count = msg["payload"]
			print("files:", count)

		elif msg["etype"] == ETYPE_FILE:
			# count = msg["pytload"]
			# print("files:", count)
			ccc += 1

		elif msg["etype"] == ETYPE_FINISH:
			print("--- finish ---")
			break

		else:
			print("!!! error !!!")
			break

		# ccc += 1

		# if msg["type"] == "finish":
		# 	break

		# print(msg)

		# print("loop")
		# time.sleep(1)

	# print("ccc:" , ccc)
	# tend = datetime.now()
	
	# print("--- finish ---")
	# dur = tend - tstart
	# print(dur.total_seconds())


	print("all finish")
	print("files:", ccc)


