#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import json

API_VERSION = 1
DATA = {
	"db_info"	: {},
	"volumes"	: []
}



def reset():
	global DATA
	DATA = {
		"db_info"	: {},
		"volumes"	: []
	}



def add_db_info(db_info):
	DATA["db_info"] = {
		"api"	: API_VERSION,
		"name"	: "qqq",
	}



def add_volume(vnode, fnodes_list):

	row = vnode.make_data_dict()

	files_array = []
	for fnode in fnodes_list:
		files_array.append(fnode.make_data_dict())

	row["files"] = files_array
	DATA["volumes"].append(row)



def make(file_export_path):

	pass

	with open(file_export_path, "w", encoding="utf-8") as fd:
		jdata = json.dumps(DATA, indent=4, ensure_ascii=False)
		fd.write(jdata)

	reset()

