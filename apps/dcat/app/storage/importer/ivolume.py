#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import json




def api_1(data):
	pass




def import_volume(file_path):

	try:
		fd = open(file_path, "r", encoding="utf-8")
		jdata = fd.read()
	except:
		return True, "Can not read file: " + file_path

	fd.close()


	try:
		data = json.loads(jdata)
	except:
		return True, "Can not parse file: " + file_path


	ftype = data.get("type")

	if ftype != "volume":
		return True, "File is not volume type"

	api = data.get("api")

	if api == 1:
		api_1(data)
	else:
		return True, "Api not supported: " + str(api)

	return False, None