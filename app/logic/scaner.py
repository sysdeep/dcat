#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import time
import uuid

from app.storage import FType, make_frow

# from pwd import getpwuid, getpwall
# from grp import getgrgid, getgrall


USERS = {}
GROUPS = {}


#--- типы пакетов, отправляемых в канал
ETYPE_START 	= "start"					# запуск
ETYPE_FINISH	= "finish"					# завершение
ETYPE_ERROR 	= "error"					# ошибка
ETYPE_FILE 		= "file"					# полезная нагрузка в виде файла
ETYPE_COUNT 	= "count"					# полезная нагрузка - кол-во файлов для сканирования
# ETYPE_PCR 		= "pcr"




# for item in getpwall():
#	USERS[item.pw_uid] = item.pw_name

# for item in getgrall():
#	GROUPS[item.gr_gid] = item.gr_name



def dtimeit(func):

	def timed(*args, **kwargs):
		ts = time.time()
		result = func(*args, **kwargs)
		te = time.time()

		print("timeit: ", te - ts)
		return result

	return timed






@dtimeit
def get_fcount(rpath):
	counter = 0
	for root, dirs, files in os.walk(rpath):
		counter += len(dirs)
		counter += len(files)

	return counter





def make_event(etype, payload=None):
	return {
		"etype"		: etype,
		"payload"	: payload
	}



@dtimeit
def start_scan(dir_path, chan):
	print("start_scan")

	chan.put(make_event(ETYPE_START))


	files_count = get_fcount(dir_path)
	chan.put(make_event(ETYPE_COUNT, files_count))


	# f_holder = int(files_count / 100)
	# print("f_holder:", f_holder)

	# # print(getpwall())

	# # return False


	# volume_name = os.path.basename(self.volume_path)
	# volume_id = str(uuid.uuid4())
	# print("volume_name: ", volume_name)
	# vdata = {
	# 	"name": volume_name,
	# 	"uuid": volume_id
	# }
	
	# self.storage.create_volume_row(vdata)


	rmap = {
		# volume_path    : "0"
		dir_path		: "0"
	}



	# current_holder = 0

	# parent = "0"
	for root, dirs, files in os.walk(dir_path):
		
		parent = rmap[root]


		

		for d in dirs:
			fpath = os.path.join(root, d)
			rid = str(uuid.uuid4())
			rmap[fpath] = rid
			

			full_path = os.path.join(root, d)
			if not os.path.exists(full_path):
				continue

			st = os.stat(full_path)

			row = make_frow()
			# row["volume_id"] = volume_id
			row["root"]	= root
			row["uuid"] = rid
			row["parent_id"] = parent
			row["name"] = d
			row["type"] = FType.DIR
			row["size"] = st.st_size
			row["ctime"] = st.st_ctime
			row["atime"] = st.st_atime
			row["mtime"] = st.st_mtime
			# row["rights"] = oct(st.st_mode & 777)
			row["rights"] = st.st_mode

			row["owner"] = st.st_uid
			row["group"] = st.st_gid
			#row["owner"] = USERS[st.st_uid]
			#row["group"] = GROUPS[st.st_gid]

			# self.storage.create_file_row(row)
			# chan.put(row)
			chan.put(make_event(ETYPE_FILE, row))
			# time.sleep(0.1)

			# current_holder += 1
			# if current_holder > f_holder:
			# 	current_holder = 0
			# 	chan.put(make_event(ETYPE_PCR))


		for f in files:
			fpath = os.path.join(root, f)
			rid = str(uuid.uuid4())
			
			full_path = os.path.join(root, f)
			if not os.path.exists(full_path):
				continue

			st = os.stat(full_path)

			row = make_frow()
			# row["volume_id"] = volume_id
			row["root"]	= root
			row["uuid"] = rid
			row["parent_id"] = parent
			row["name"] = f
			row["type"] = FType.FILE
			row["size"] = st.st_size
			row["ctime"] = st.st_ctime
			row["atime"] = st.st_atime
			row["mtime"] = st.st_mtime
			row["rights"] = st.st_mode

			row["owner"] = st.st_uid
			row["group"] = st.st_gid
			#row["owner"] = USERS[st.st_uid]
			#row["group"] = GROUPS[st.st_gid]

			# self.storage.create_file_row(row)

			# print(row)
			# chan.put(row)
			chan.put(make_event(ETYPE_FILE, row))
			# time.sleep(0.1)

			# current_holder += 1
			# if current_holder > f_holder:
			# 	current_holder = 0
			# 	chan.put(make_event(ETYPE_PCR))



		del rmap[root] 

		# break
	# self.storage.commit()
	
	#--- !!! windows error
	#  File "G:\_Wrk\_Python\_DCat\DCat\app\logic\scaner.py", line 135, in start_scan
	#
	# 	print(rmap)
	#	File "g:\Python35\lib\encodings\cp866.py", line 19, in encode
    #	return codecs.charmap_encode(input,self.errors,encoding_map)[0]
	#	UnicodeEncodeError: 'charmap' codec can't encode character '\xeb' in position 10
	#	89: character maps to <undefined>
	
	
	# print(rmap)


	# row = {
	# 	"type"	: "finish"
	# }
	# chan.put(row)
	chan.put(make_event(ETYPE_FINISH))


















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


