#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
fat = 16M
slim v1 = 2.5Mb
slim v2 = 4Mb
"""
import sqlite3

NEW_DB = "slim.sqlite"
OLD_DB = "fat.dcat"

CREATE_TABLE_FILES = """
    CREATE TABLE "files" (
        "id"            INTEGER PRIMARY KEY AUTOINCREMENT,
        "volume_id"     INTEGER NOT NULL,
        "parent_id"     INTEGER,
        "name"          VARCHAR(64) NOT NULL,
        "type"          INTEGER,
        "rights"        INTEGER,
        "sowner"        VARCHAR(64),
        "sgroup"        VARCHAR(64),
        "ctime"         INTEGER,
        "atime"         INTEGER,
        "mtime"         INTEGER,
        "category"      INTEGER,
        "description"   TEXT,
        "size"          INTEGER

    );
"""


CREATE_TABLE_VOLUMES = """
    CREATE TABLE "volumes" (
        "id"        INTEGER PRIMARY KEY AUTOINCREMENT,
        "name"      VARCHAR(64),
        "path"      VARCHAR(256),
        "created"   DATETIME,
        "vtype"     INTEGER,
        "description"   TEXT
    );
""" 


def create_db():
	connection = sqlite3.connect(NEW_DB)
	cursor = connection.cursor()
	cursor.execute(CREATE_TABLE_FILES)
	cursor.execute(CREATE_TABLE_VOLUMES)
	connection.commit()
	connection.close()



def start():
	fat_conn = sqlite3.connect(OLD_DB)
	slim_conn = sqlite3.connect(NEW_DB)

	fat_cursor = fat_conn.cursor()
	slim_cursor = slim_conn.cursor()

	#--- volumes
	fat_cursor.execute("""SELECT name, path, created, description FROM volumes;""")
	fat_rows = fat_cursor.fetchall()
	
	
	for i, row in enumerate(fat_rows):
		irow = (*row, i)
		slim_cursor.execute("""INSERT INTO volumes(name, path, created, description, vtype) VALUES(?,?,?,?,?)""", irow)
		


		

	#--- files
	fat_cursor.execute("""SELECT name, size, description FROM files;""")
	fat_rows = fat_cursor.fetchall()
	
	
	for i, row in enumerate(fat_rows):
		irow = (i, i, row[0], i, i, str(i), str(i), i, i, i, i, row[1], row[2])
		slim_cursor.execute("""INSERT INTO files(volume_id, parent_id, name, type, rights, sowner, sgroup, ctime, atime, mtime, category, size, description) VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?)""", irow)
	


	fat_conn.close()
	slim_conn.commit()
	slim_conn.close()



if __name__ == "__main__":
	create_db()
	start()