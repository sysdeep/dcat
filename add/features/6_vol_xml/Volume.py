#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import os.path
import xml.etree.ElementTree as etree
import gzip

class VolumeHeader(object):
	def __init__(self):
		self.name = ""
		self.description = ""
		self.scan_path = ""
		self.version = "1"

	def to_dict(self) -> dict:

		return {
			"name"			: self.name,
			"description"	: self.description,
			"scan_path"		: self.scan_path,
			"version"		: self.version
		}



def make_frow(name, ftype, st):
	"""используется при обходе файловой системы"""
	item = {


		# "id": str(uuid.uuid4()),
		"n": name,
		"t": ftype,

		"r": str(st.st_mode),

		"o": str(st.st_uid),
		"g": str(st.st_gid),

		"c": str(st.st_ctime),
		"a": str(st.st_atime),
		"m": str(st.st_mtime),

		
		"s": str(st.st_size)

		# "name": name,
		# "type": ftype,

		# "rights": str(st.st_mode),

		# "owner": str(st.st_uid),
		# "group": str(st.st_gid),

		# "ctime": str(st.st_ctime),
		# "atime": str(st.st_atime),
		# "mtime": str(st.st_mtime),

		# "category": "",
		# "description": "",

		# "size": str(st.st_size)
	}
	return item


def start_scan(xroot, scan_path):

	rmap = {
		scan_path	: xroot
	}

	files_count = 0
	for root, dirs, files in os.walk(scan_path):

		x_el = rmap.get(root)

		for dir in dirs:
			full_path = os.path.join(root, dir)
			if not os.path.exists(full_path):				# если нет - продолжаем...
				continue

			st = os.stat(full_path)							# статистика по файлу

			row = make_frow(dir, "d", st)
			files_count += 1

			node = etree.SubElement(x_el, "node", row)

			rmap[full_path] = node


		for f in files:
			full_path = os.path.join(root, f)				# полный путь
			if not os.path.exists(full_path):				# если нет - продолжаем...
				continue

			st = os.stat(full_path)							# статистика по файлу

			row = make_frow(f, "f", st)
			files_count += 1

			etree.SubElement(x_el, "node", row)

		del rmap[root]

	print("total files: ", files_count)


class Volume(object):
	def __init__(self, db_path: str):
		self.__db_path = db_path




	def create(self, volume_name, scan_path) -> bool:

		volume_header = VolumeHeader()
		volume_header.name = volume_name
		volume_header.description = "new volume"
		volume_header.scan_path = scan_path

		new_name = volume_name + ".gz"
		full_path = os.path.join(self.__db_path, new_name)

		xroot = etree.Element("catalog", volume_header.to_dict())

		start_scan(xroot, scan_path)

		with gzip.open(full_path, "wb") as fd:
			fd.write(etree.tostring(xroot, encoding="utf-8"))

		return True