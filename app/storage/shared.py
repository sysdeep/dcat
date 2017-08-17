#!/usr/bin/env python3
# -*- coding: utf-8 -*-


DATA = {
    "storage"       : None
}




def set_storage(storage):
    DATA["storage"] = storage


def get_storage():
    return DATA["storage"]