#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import uuid

from app.storage import FType, make_frow

# from pwd import getpwuid, getpwall
# from grp import getgrgid, getgrall


USERS = {}
GROUPS = {}

# for item in getpwall():
#	USERS[item.pw_uid] = item.pw_name

# for item in getgrall():
#	GROUPS[item.gr_gid] = item.gr_name






class SWalker(object):
	def __init__(self):
		self.storage = None
		self.volume_path = None


	def set_scan_volume(self, volume_path):
		self.volume_path = volume_path


	def start_scan(self):
		print("start_scan")

		# print(getpwall())

		# return False


		volume_name = os.path.basename(self.volume_path)
		volume_id = str(uuid.uuid4())
		print("volume_name: ", volume_name)
		vdata = {
			"name": volume_name,
			"uuid": volume_id
		}
		
		self.storage.create_volume_row(vdata)


		rmap = {
			self.volume_path    : "0"
		}

		# parent = "0"
		for root, dirs, files in os.walk(self.volume_path):
			# print(root)
			# rmap[root] = "0"
			parent = rmap[root]


			

			for d in dirs:
				fpath = os.path.join(root, d)
				rid = str(uuid.uuid4())
				rmap[fpath] = rid
				# row = {
				#     "volume_id" : volume_id,
				#     "uuid"      : rid,
				#     "parent_id" : parent,
				#     "name"      : d,
				#     "type"      : FType.DIR
				# }

				full_path = os.path.join(root, d)
				if not os.path.exists(full_path):
					continue

				st = os.stat(full_path)

				row = make_frow()
				row["volume_id"] = volume_id
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

				self.storage.create_file_row(row)



			for f in files:
				fpath = os.path.join(root, f)
				rid = str(uuid.uuid4())
				# rmap[fpath] = rid
				# row = {
				#     "volume_id" : volume_id,
				#     "uuid"      : rid,
				#     "parent_id" : parent,
				#     "name"      : f,
				#     "type"      : FType.FILE
				# }

				full_path = os.path.join(root, f)
				if not os.path.exists(full_path):
					continue

				st = os.stat(full_path)

				row = make_frow()
				row["volume_id"] = volume_id
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

				self.storage.create_file_row(row)

				# print(row)



			del rmap[root] 

			# break
		self.storage.commit()
		print(rmap)

if __name__ == "__main__":

	from app.storage import get_storage
	
	from app.rc import FILE_DB_TEST
	
	
	# FILE_PATH = "/home/nia/Development/_Python/_DCat/dcat/tests/s1.db"
	FILE_PATH = FILE_DB_TEST
	SCAN_PATH = "/home/nia/Development/_Python/_DCat/sdir"
	SCAN_PATH = "/home/nia/Development/_Python"
	SCAN_PATH = "G:\_Wrk\_Python\_DCat\sdir"
	
	swalker = SWalker()
	swalker.storage = get_storage()
	swalker.storage.open_storage(FILE_PATH)
	swalker.set_scan_volume(SCAN_PATH)
	swalker.start_scan()
