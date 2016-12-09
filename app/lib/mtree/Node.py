#!/usr/bin/env python
# -*- coding: utf-8 -*-


class Node(object):
    def __init__(self):
        self.name   = ""
        self.ntype  = ""
        self.size   = 0

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