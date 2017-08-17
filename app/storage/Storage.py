#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from .DB import DB

class Storage(object):
    def __init__(self):

        self.storage_path = None
        self.db = DB()
        self.is_open = False


    def open_storage(self, file_path):
        self.storage_path = file_path
        self.db.open_db(self.storage_path)
        self.is_open = True


    def close_storage(self):
        self.db.close_db()
        self.is_open = False


    def create_storage(self, file_path):

        if self.is_open:
            self.close_storage()

        self.storage_path = file_path
        self.db.create_db(self.storage_path)
        self.is_open = True


    def get_volumes(self):
        if not self.is_open:
            return []

        volumes = self.db.get_volumes()

        return volumes
        

    def get_files(self, volume=None):
        if not self.is_open:
            return []

        if volume:
            files = self.db.get_volume_files(volume)
        else:
            files = self.db.get_files_all()


        return files

    



    def create_volume_row(self, vdata, commit=False):
        volume_id = self.db.create_volume_row(vdata, commit)
        return volume_id


    def create_file_row(self, fdata, commit=False):
        file_id = self.db.create_file_row(fdata, commit)
        return file_id


    def commit(self):
        self.db.commit()