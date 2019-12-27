#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import gzip
import uuid
import struct


# SCAN_PATH = "/mnt/backup"
# SCAN_PATH = "/home/nia/Android"
# SCAN_PATH = "/home/nia/Android"
SCAN_PATH = "/home/nia/Music"
# SCAN_PATH = "/home/nia/Work/_LinuxServer"
XFILE = "/home/nia/Development/_Python/_DCat/binvol.binvol"
# GFILE = "/home/nia/Development/_Python/_DCat/binvol.binvol.gz"
# GFILE = "/home/nia/Development/_Python/_DCat/x1.xml.gz"


def to_bstring(input: str):
    bstr = input.encode(encoding="utf-8")

    str_len = len(bstr)

    bdata = b""
    bdata += struct.pack("<I", str_len)
    bdata += bstr
    return bdata



def make_header():
	bdata = b""
       
	#--- 20b
	dataset = (
		1, 					#model.version,
		1, 					#model.created,
		1, 					#model.updated,
		1, 					#model.vtype,
		1					#model.total_blocks,
	)
	bdata  += struct.pack("<IIIII", *dataset)

	return bdata

def read_header(bdata):
	dataset = struct.unpack("<IIIII", bdata)
	print(dataset)



def make_frow(id, name, ftype, st, parent_id=0):
	
	dataset = (
		id, 			# int
		ftype, 			# int
		st.st_size,		# size int
		parent_id,				# parent id
		0, 				# rights
		0,				# uid
		0, 				# gid
		0,				# ctime
		0,				# atime
		0,				# mtime
	)
	bdata = b"";
	bdata  += struct.pack("<IIIIIIIIII", *dataset)

	bdata += to_bstring(name)
	return bdata


	# item = {


	# 	"id": str(uuid.uuid4()),
	# 	"name": name,
	# 	"type": ftype,

	# 	"rights": str(st.st_mode),

	# 	"owner": str(st.st_uid),
	# 	"group": str(st.st_gid),

	# 	"ctime": str(st.st_ctime),
	# 	"atime": str(st.st_atime),
	# 	"mtime": str(st.st_mtime),

	# 	"category": "",
	# 	"description": "",

	# 	"size": str(st.st_size)
	# }

	# return item
	# pass


def re_scan(spath, fid, parent_id, bdata):
	

	lid = fid
	for f in os.listdir(spath):
		full_path = os.path.join(spath, f)
		
		if os.path.isfile(full_path):
			
			st = os.stat(full_path)	

			brow = make_frow(lid, f, 2, st, parent_id)
			bdata += brow
			lid += 1

		else:
			
			
			st = os.stat(full_path)	

			brow = make_frow(lid, f, 1, st, parent_id)
			bdata += brow

			lid = re_scan(full_path, lid + 1, lid, bdata)

	return lid

def write_db(scan_path, out_path, is_gz=False):

	bdata = make_header()
	files_count = 0

	re_scan(scan_path, 1, 0, bdata)



def write_db_walk(scan_path, out_path, is_gz=False):
	

	bdata = make_header()
	files_count = 0
	
	for root, dirs, files in os.walk(scan_path):


		for dir in dirs:
			full_path = os.path.join(root, dir)				# полный путь
			if not os.path.exists(full_path):				# если нет - продолжаем...
				continue

			st = os.stat(full_path)							# статистика по файлу

			brow = make_frow(files_count + 1, dir, 1, st)
			bdata += brow
			files_count += 1

			# # node = etree.SubElement(x_el, "node", {"name": dir, "type": "d"})
			# node = etree.SubElement(x_el, "node", row)

			# dir_path = os.path.join(root, dir)

			# rmap[dir_path] = node



		for f in files:
			full_path = os.path.join(root, f)				# полный путь
			if not os.path.exists(full_path):				# если нет - продолжаем...
				continue

			st = os.stat(full_path)							# статистика по файлу

			row = make_frow(files_count +1, f, 2, st)
			bdata += brow
			files_count += 1


			# etree.SubElement(x_el, "node", row)
			# etree.SubElement(x_el, "node", {"name": f, "type": "f"})
	

	print("added files: ", files_count)

	if is_gz:
		with gzip.open(out_path + ".gz", "wb") as fd:
			fd.write(bdata)
	else:
		with open(out_path, "wb") as fd:
			fd.write(bdata)


def read_db(file_path, is_gz=False):

	if is_gz:
		with gzip.open(file_path + ".gz", "rb") as fd:
			bheader = fd.read(20)
			read_header(bheader)
	else:
		with open(file_path, "rb") as fd:
			bheader = fd.read(20)
			read_header(bheader)



if __name__ == "__main__":

	write_db(SCAN_PATH, XFILE, True)
	read_db(XFILE, True)


