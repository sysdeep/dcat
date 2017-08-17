#!/usr/bin/env python3
# -*- coding: utf-8 -*-




CREATE_TABLE_FILES = """
    CREATE TABLE "files" (
        "id"            INTEGER PRIMARY KEY AUTOINCREMENT,
        "volume_id"     INTEGER NOT NULL,
        "uuid"          VARCHAR(64),
        "parent_id"     VARCHAR(64),
        "name"          VARCHAR(64) NOT NULL,
        "type"          INTEGER NOT NULL
    );
"""


CREATE_TABLE_VOLUMES = """
    CREATE TABLE "volumes" (
        "id"            INTEGER PRIMARY KEY AUTOINCREMENT,
        "uuid"       VARCHAR(64),
        "name"          VARCHAR(64)
    );
"""


GET_VOLUMES = """
    SELECT uuid, name FROM volumes;
"""


GET_FILES_ALL = """
    SELECT uuid, parent_id, volume_id, name, type FROM files;
"""