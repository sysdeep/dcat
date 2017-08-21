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







def start_scan(dir_path, chan):
	print("start_scan")

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
			chan.put(row)



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
			chan.put(row)



		del rmap[root] 

		# break
	# self.storage.commit()
	print(rmap)


	row = {
		"type"	: "finish"
	}
	chan.put(row)

