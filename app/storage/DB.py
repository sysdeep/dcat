#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sqlite3
from . import sql



class DB(object):
    def __init__(self, db_path=None):
        self.db_path = db_path
        self.connection = None
        self.cursor = None
        if db_path:
            self.connection = sqlite3.connect(db_path)


    def open_db(self, db_path):
        
        if self.connection:
            self.connection.close()

        self.db_path = db_path
        self.connection = sqlite3.connect(db_path)


    def close_db(self):
        if self.connection:
            self.connection.close()


    def create_db(self, db_path):
        self.db_path = db_path
        self.connection = sqlite3.connect(db_path)
        self.cursor = self.connection.cursor()
        self.cursor.execute(sql.CREATE_TABLE_FILES)
        self.cursor.execute(sql.CREATE_TABLE_VOLUMES)
        self.connection.commit()




    def get_volumes(self):
        cursor = self.connection.cursor()
        cursor.execute(sql.GET_VOLUMES)

        rows = cursor.fetchall()

        return rows


    def get_files_all(self):
        cursor = self.connection.cursor()
        cursor.execute(sql.GET_FILES_ALL)
        rows = cursor.fetchall()
        return rows


    def get_volume_files(self, volume_id):
        cursor = self.connection.cursor()
        cursor.execute("SELECT * FROM files WHERE volume_id=?", (volume_id, ))
        rows = cursor.fetchall()
        return rows


    def create_volume_row(self, vdata, commit=False):
        ivalues = (
            vdata["uuid"],
            vdata["name"]
        )
        cursor = self.connection.cursor()
        cursor.execute("INSERT INTO volumes(uuid, name) VALUES(?,?)", ivalues)
        volume_id = cursor.lastrowid
        
        if commit:
            self.connection.commit()

        return volume_id


    def create_file_row(self, fdata, commit=False):
        ivalues = (
            fdata["volume_id"],
            fdata["parent_id"],
            fdata["uuid"],
            fdata["name"],
            fdata["type"]
        )
        cursor = self.connection.cursor()
        cursor.execute("INSERT INTO files(volume_id, parent_id, uuid, name, type) VALUES(?,?,?,?,?)", ivalues)
        row_id = cursor.lastrowid

        if commit:
            self.connection.commit()

        return row_id



    def commit(self):
        self.connection.commit()

