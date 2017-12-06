#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import json

API_VERSION = 1
DATA = {
	"db_info"		: {},
	"volume_info"	: {},
	"files"			: []
}

def get_default():
	return {
		"api"			: 1,
		"db_info"		: {},
		"volume_info"	: {},
		"files"			: []
	}




def export(db_info, volume_info, files_info, export_file_path):

	row = get_default()
	row["db_info"] = db_info
	row["volume_info"] = volume_info
	row["files"]	= files_info


	jdata = json.dumps(row, indent=4, ensure_ascii=False)

	try:
		with open(export_file_path, "w", encoding="utf-8") as fd:
			fd.write(jdata)

		return True
	except:
		return False

