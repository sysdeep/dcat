#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sqlite3
import os.path
from app.lib.volume import Volume
from app.lib.volume.FileRecord import FileRecord

SQLITE_DB = "/home/nia/2.dcat"
OUT_PATH = "/home/nia/Temp/dcat_export"


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

for vol_data in rows:
	
	vol = Volume()
	
	vol.volume_header.icon = VOLUME_ICONS.get(vol_data["vtype"], 14)			# or other
	vol.volume_header.name = vol_data["name"] if vol_data["name"] else ""
	vol.volume_header.scan_path = vol_data["path"] if vol_data["path"] else ""
	vol.volume_header.description = vol_data["description"] if vol_data["description"] else ""

	
	
	
	cursor.execute(GET_VOLUME_FILES, (vol_data["uuid"], ))
	frows = cursor.fetchall()
	
	for frow in frows:
		record = FileRecord()
		record.name = frow["name"]
		# record.description = frow["description"]
		record.size = frow["size"]
	
		vol.records.append(record)
	
	vol.save(os.path.join(OUT_PATH, vol_data["name"] + ".hmap.gz"))
	
	# break
	
	
	
	
connection.close()