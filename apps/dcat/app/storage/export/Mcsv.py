#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import gzip
import re
import base64
from app.lib import tools

def __kv(key, value):
	return "{}:{}\n".format(key, value)


def __str2base(data: str) -> str:
	return base64.standard_b64encode(data.encode()).decode("utf-8")

def __vol_info(data: dict):
	"""
	{'created': '2017-09-27 11:05:42', 'name': 'oxygen_16x16', 'description': None,
	'updated': None, 'uuid': '3a618114-f766-4767-a058-79d3a1b1da07', 'vtype': 'cd', 'path': '/home/nia/Development/_Python/_DCat/oxygen_16x16'}
	
	
	313057 - 9.1m
	replace 313057 - 12s - 10.2m
	base64 313057 - 3.3s - 13.2m
	
	
	"""
	
	# safe_description = data["description"].replace("\n", "___LF___").replace(":", "___TERM___")
	# safe_name = data["name"]
	
	safe_description = __str2base(data["description"])
	safe_name = __str2base(data["name"])
	
	
	result = ""
	result += __kv("version", 1)
	result += __kv("name", safe_name)
	# result += __kv("name", data["name"])
	# result += __kv("description", data["description"])
	result += __kv("description", safe_description)
	# result += __kv("description", re.escape(data["description"]))
	# result += __kv("description", data["description"].encode())
	result += __kv("created", data["created"])
	result += __kv("vtype", data["vtype"])
	return result


def __format_row(row_data: dict) -> str:
	"""
	{'name': 'k3b.png', 'size': 998,
	'rights': 0, 'group': '',
	'category': 0, 'owner': '', 'ctime': 1481536946.5915499,
	'ftype': 1,
	'volume_id': '3a618114-f766-4767-a058-79d3a1b1da07',
	'parent_id': '73fc11a5-5c81-4f05-83b5-3b42baadc91c', 'uuid': '90d897f9-9803-4fe3-a006-7df326438a4c',
	'description': '', 'mtime': 0, 'atime': 0}
	"""
	
	# safe_description = row_data["description"].replace("|", ":")
	# safe_name = row_data["name"].replace("|", ":")
	# safe_parent_id = row_data["parent_id"]
	# safe_uuid = row_data["uuid"]
	
	safe_description = __str2base(row_data["description"])
	safe_name = __str2base(row_data["name"])
	safe_parent_id = __str2base(row_data["parent_id"])
	safe_uuid = __str2base(row_data["uuid"])
	
	dataset = (
		# "'" + row_data["name"] + "'",
		safe_name,							# 0
		str(row_data["size"]),										# 1
		str(row_data["ctime"]),										# 2
		str(row_data["mtime"]),										# 3
		str(row_data["atime"]),										# 4
		str(row_data["rights"]),									# 5
		row_data["group"],											# 6
		row_data["owner"],											# 7
		safe_description,					# 8
		safe_parent_id,										# 9
		safe_uuid,											# 10
	)
	
	result = "|".join(dataset)
	
	return result + "\n"

@tools.dtimeit
def start_export(vol_info: dict, files_list: list, file_path: str):
	
	
	
	fd = gzip.open(file_path + ".gz", "wt", encoding="utf-8")
	header = __vol_info(vol_info)
	print("header len: ", len(header))
	fd.write(header)
	fd.write("-"*10)
	fd.write("\n")
	
	for fdata in files_list:
		# print(__format_row(fdata))
		fd.write(__format_row(fdata))
	
	fd.flush()
	fd.close()
	
	# with open(file_path, "w", encoding="utf-8") as fd:
	# 	fd.write(__vol_info(vol_info))
	# 	fd.write("-"*10)
	# 	fd.write("\n")
	#
	# 	for fdata in files_list:
	# 		# print(__format_row(fdata))
	# 		fd.write(__format_row(fdata))
	#