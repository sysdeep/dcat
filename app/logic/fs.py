#!/usr/bin/env python
# -*- coding: utf-8 -*-
import json

from app import log


def load_file(file_path):
    log.info("load file: " + file_path)
    with open(file_path, "r", encoding="utf-8") as fd:
        data_json = fd.read()
        data = json.loads(data_json)
        return data


def store_file(file_path, data):
    with open(file_path, "w", encoding="utf-8") as fd:
        data_json = json.dumps(data)
        fd.write(data_json)


        




if __name__ == '__main__':
    from app.rc import FILE_JSON



    data = load_file(FILE_JSON)

    print(data)