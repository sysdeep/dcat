#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import gzip
import uuid
import xml.etree.ElementTree as etree

SCAN_PATH = "/mnt/backup"
# SCAN_PATH = "/home/nia"
# SCAN_PATH = "/home/nia/Work/_LinuxServer"
XFILE = "/home/nia/Development/_Python/_DCat/x1.xml"
GFILE = "/home/nia/Development/_Python/_DCat/x1.xml.gz"




# xroot = etree.parse(XFILE)
# etree.dump(xroot)

#
# with open(XFILE, "br") as fd:
# 	xroot = etree.fromstring(fd.read())
#
# 	etree.dump(xroot)
#
#


#
# with gzip.open(GFILE, "rb") as fd:
# 	xroot = etree.fromstring(fd.read())
#
# 	print(xroot)
	# etree.dump(xroot)
	# root = xroot.getroot()
	# fff = xroot.findall("*/node")
	# print(fff)



def make_frow(name, ftype, st):
	"""используется при обходе файловой системы"""
	item = {


		"id": str(uuid.uuid4()),
		"name": name,
		"type": ftype,

		"rights": str(st.st_mode),

		"owner": str(st.st_uid),
		"group": str(st.st_gid),

		"ctime": str(st.st_ctime),
		"atime": str(st.st_atime),
		"mtime": str(st.st_mtime),

		"category": "",
		"description": "",

		"size": str(st.st_size)
	}
	return item



def start(scan_path, db_file, volume_name):



	xroot = etree.Element("catalog", {"name": volume_name, "description": "catalog description"})
	# description = etree.SubElement(xroot, "description")
	# description.text = "catalog description"
	# volumes = etree.SubElement(xroot, "volumes")
	volume = etree.SubElement(xroot, "volume", {"name": volume_name, "description": "volume description"})

	rmap = {
		scan_path	: volume
	}



	for root, dirs, files in os.walk(scan_path):



		x_el = rmap.get(root)


		for dir in dirs:
			full_path = os.path.join(root, dir)				# полный путь
			if not os.path.exists(full_path):				# если нет - продолжаем...
				continue

			st = os.stat(full_path)							# статистика по файлу

			row = make_frow(dir, "d", st)

			# node = etree.SubElement(x_el, "node", {"name": dir, "type": "d"})
			node = etree.SubElement(x_el, "node", row)

			dir_path = os.path.join(root, dir)

			rmap[dir_path] = node



		for f in files:
			full_path = os.path.join(root, f)				# полный путь
			if not os.path.exists(full_path):				# если нет - продолжаем...
				continue

			st = os.stat(full_path)							# статистика по файлу

			row = make_frow(f, "f", st)

			etree.SubElement(x_el, "node", row)
			# etree.SubElement(x_el, "node", {"name": f, "type": "f"})



		del rmap[root]




	with gzip.open(db_file, "wb") as fd:
		fd.write(etree.tostring(xroot, encoding="utf-8"))


	# with gzip.open(GFILE, "wb") as fd:
	# 	fd.write(etree.tostring(xroot, encoding="utf-8"))


	#
	#
	#
	# with open(XFILE, "wb") as fd:
	# 	fd.write(etree.tostring(xroot, encoding="utf-8"))
	#

