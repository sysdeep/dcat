#!/usr/bin/env python
# -*- coding: utf-8 -*-


class Node(object):
    def __init__(self):
        self.name   = ""
        self.ntype  = ""
        
        self.st_size    = 0     # size
        self.st_atime   = 0     # access time
        self.st_mtime   = 0     # modification time
        self.st_ctime   = 0     # create time

        self.id         = 0
        self.id_parent  = 0
        self.childrens  = []
        self.level      = 0
        self.parent     = None


    def add_children(self, children):
        self.childrens.append(children)
        children.parent = self


    def get_children(self, name):
        result = [ch for ch in self.childrens if ch.name == name]
        # print(result)
        # if len(result):
        return result[0]



    def get_dict(self):
        row = {
            "id"            : self.id,
            "id_parent"     : self.id_parent,
            "level"         : self.level,
            "ntype"         : self.ntype,
            "name"          : self.name,
            "st_size"       : self.st_size,
            "st_atime"      : self.st_atime,
            "st_mtime"      : self.st_mtime,
            "st_ctime"      : self.st_ctime,
        }

        return row

    def set_dict(self, row):
        self.id         = row["id"]
        self.id_parent  = row["id_parent"]
        self.level      = row["level"]
        self.ntype      = row["ntype"]
        self.name       = row["name"]
        self.st_size    = row["st_size"]
        self.st_atime   = row["st_atime"]
        self.st_mtime   = row["st_mtime"]
        self.st_ctime   = row["st_ctime"]