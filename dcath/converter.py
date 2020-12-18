#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sqlite3
import os.path
from app.lib.models import Volume
from app.lib.models.FileRecord import FileRecord
# from app.lib.db_worker.HmapWorker import HmapWorker
from app.lib.logger import log

#--- lin
SQLITE_DB = "/home/nia/2.dcat"
OUT_PATH = "/home/nia/Development/_Python/_DCat/Export10/app2"

# #--- win
# SQLITE_DB = "E:\\_Wrk\\_Python\\_DCat\\Bin10Test\\P50-61.dcat"
# OUT_PATH = "E:\\_Wrk\\_Python\\_DCat\\Bin10Test\\files"


VOLUME_ICONS = {
	"cd"        : 1,
	"dvd"       : 2,
	"bdrom"		: 3,
	"crypted"	: 4,
	"folder"    : 5,
	
	"audio_cd"  : 6,
	"hdd"       : 7,
	"hdd_usb"   : 8,
	"flash"     : 9,
	"sd"        : 10,
	"floppy"    : 11,
	"net"       : 12,
	"tape"      : 13,
	"other"     : 14,
	
}




def __convert_files(files: list):
	"""переводим файлы в новую структуру"""
		
	omap = {
		"0"	: 0,
	}			# uuid: new id
	
	
	new_id = 1
	
	#--- fix root parent
	# for row in files:
	# 	if row["parent_id"] == "0":
	# 		row["parent_id"] = 0
	
	#--- update fid
	for row in files:
		omap[row["uuid"]] = new_id
		row["uuid"] = new_id
		new_id += 1
		
	#--- update parents
	for row in files:
		try:
			new_parent_id = omap[row["parent_id"]]
		except:
			print("!!! no found parent in omap")
			continue
			
		row["parent_id"] = new_parent_id



GET_VOLUME_FILES = """
	SELECT uuid, parent_id, volume_id, name, type, rights, sowner, sgroup, size, ctime, atime, mtime, category, description
		FROM files WHERE volume_id=?;
"""




connection = sqlite3.connect(SQLITE_DB)
connection.row_factory = sqlite3.Row

cursor = connection.cursor()




cursor.execute("""SELECT * FROM volumes;""")
rows = cursor.fetchall()
# result = make_volumes(rows)
# result = loader.make_vnodes(rows)



# hmap_worker = HmapWorker()

for vol_data in rows:
	
	vol = Volume()
	
	vol.volume_header.icon = VOLUME_ICONS.get(vol_data["vtype"], 14)			# or other
	vol.volume_header.name = vol_data["name"] if vol_data["name"] else ""
	vol.volume_header.scan_path = vol_data["path"] if vol_data["path"] else ""
	vol.volume_header.description = vol_data["description"] if vol_data["description"] else ""

	
	
	
	cursor.execute(GET_VOLUME_FILES, (vol_data["uuid"], ))
	frows = cursor.fetchall()
	# __convert_files(frows)
	


	omap = {
		"0"	: 0,
	}			# uuid: new id
	
	new_id = 1
	#--- update fid
	for frow in frows:
		omap[frow["uuid"]] = new_id
		new_id += 1

	

	
	for frow in frows:
		record = FileRecord()
		record.name = frow["name"]
		record.description = frow["description"]
		record.size = frow["size"]
		record.ftype = frow["type"]
		record.ctime = int(frow["ctime"])
		record.rights = frow["rights"]

		# #--- fid 			[uint 4]	- id записи
		# # bdata += uint4(0)					# TODO
		record.fid = omap[frow["uuid"]]
		
		# #--- pid 			[uint 4]	- id родителя(0 - корень)
		# # bdata += uint4(0)					# TODO
		record.pid = omap[frow["parent_id"]]
	
		vol.records.append(record)
	


	file_path = os.path.join(OUT_PATH, vol_data["name"] + ".hmap.gz")

	vol.save(file_path)


	# hmap_worker.write_volume(vol, file_path)


	
	# break
	
	
	
	
connection.close()