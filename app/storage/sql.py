#!/usr/bin/env python3
# -*- coding: utf-8 -*-




CREATE_TABLE_FILES = """
    CREATE TABLE "files" (
        "id"            INTEGER PRIMARY KEY AUTOINCREMENT,
        "volume_id"     INTEGER NOT NULL,
        "uuid"          VARCHAR(64),
        "parent_id"     VARCHAR(64),
        "name"          VARCHAR(64) NOT NULL,
        "type"          INTEGER NOT NULL,
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
        "id"            INTEGER PRIMARY KEY AUTOINCREMENT,
        "uuid"       VARCHAR(64),
        "name"          VARCHAR(64)
    );
"""



CREATE_FILE_ROW = """
    INSERT INTO 
        files(volume_id, parent_id, uuid, name, type, rights, sowner, sgroup, size, ctime, atime, mtime, category, description) 
        VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?);
"""


GET_VOLUMES = """
    SELECT uuid, name FROM volumes;
"""


GET_FILES_ALL = """
    SELECT uuid, parent_id, volume_id, name, type, rights, sowner, sgroup, size, ctime, atime, mtime, category, description  
        FROM files;
"""


GET_VOLUME_ROOT_FILES = """
    SELECT uuid, parent_id, volume_id, name, type, rights, sowner, sgroup, size, ctime, atime, mtime, category, description 
        FROM files WHERE volume_id=? AND parent_id='0';
"""


GET_PARENT_FILES = """
    SELECT uuid, parent_id, volume_id, name, type, rights, sowner, sgroup, size, ctime, atime, mtime, category, description 
        FROM files WHERE parent_id=?;
"""



REMOVE_VOLUME_FILES = """
    DELETE FROM files WHERE volume_id=?
"""

REMOVE_VOLUME = """
    DELETE FROM volumes WHERE uuid=?
"""