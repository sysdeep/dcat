#!/usr/bin/env python
# -*- coding: utf-8 -*-



class Importer(object):
    def __init__(self, tree):
        self.tree = tree


    def start(self, data):
        self.tree.set_empty()
        data.sort(key = lambda x: x["id"])

        node = self.tree.get_root()
        for row in data:
            if row["id"] == 1: continue

            print(row["parent"])
            parent_node = self.tree.get_node_id(row["parent"])
            # print(parent_node)

            node = self.tree.get_empty_node()
            node.set_dict(row)
            self.tree.insert_node(parent_node, node)



            # node = self.tree.get_node_id(row["id"])
            # if node:
            #     node.set_dict(row)


    # def __make_node(self, row):
    #     pass