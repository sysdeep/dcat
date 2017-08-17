#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import uuid

class SWalker(object):
    def __init__(self):
        self.storage = None
        self.volume_path = None


    def set_scan_volume(self, volume_path):
        self.volume_path = volume_path


    def start_scan(self):
        print("start_scan")

        volume_name = os.path.basename(self.volume_path)
        volume_id = str(uuid.uuid4())
        print("volume_name: ", volume_name)
        vdata = {
            "name": volume_name,
            "uuid": volume_id
        }
        
        self.storage.create_volume_row(vdata)


        rmap = {
            self.volume_path    : "0"
        }

        # parent = "0"
        for root, dirs, files in os.walk(self.volume_path):
            # print(root)
            # rmap[root] = "0"
            parent = rmap[root]


            for d in dirs:
                fpath = os.path.join(root, d)
                rid = str(uuid.uuid4())
                rmap[fpath] = rid
                row = {
                    "volume_id" : volume_id,
                    "uuid"      : rid,
                    "parent_id" : parent,
                    "name"      : d,
                    "type"      : "d"
                }

                self.storage.create_file_row(row)



            for f in files:
                fpath = os.path.join(root, f)
                rid = str(uuid.uuid4())
                # rmap[fpath] = rid
                row = {
                    "volume_id" : volume_id,
                    "uuid"      : rid,
                    "parent_id" : parent,
                    "name"      : f,
                    "type"      : "f"
                }

                self.storage.create_file_row(row)

                # print(row)



            del rmap[root] 

            # break
        self.storage.commit()
        print(rmap)

if __name__ == "__main__":

    from app.storage import get_storage

    FILE_PATH = "/home/nia/Development/_Python/_DCat/dcat/tests/s1.db"
    SCAN_PATH = "/home/nia/Development/_Python/_DCat/sdir"
    # SCAN_PATH = "/home/nia/Development/_Python"
    
    swalker = SWalker()
    swalker.storage = get_storage()
    swalker.storage.open_storage(FILE_PATH)
    swalker.set_scan_volume(SCAN_PATH)
    swalker.start_scan()
