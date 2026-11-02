#!/usr/bin/env python
# -*- coding: utf-8 -*-
import json


class Exporter(object):
    def __init__(self, tree):
        self.tree = tree
        self.items = []


    def export(self):
        root = self.tree.get_root()
        self.__fill_node(root)

        # result = json.dumps(self.items)
        # return result
        return self.items



    def __fill_node(self, node):
        row = node.get_dict()
        self.items.append(row)

        for n in node.childrens:
            self.__fill_node(n)


        
