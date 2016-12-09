#!/usr/bin/env python
# -*- coding: utf-8 -*-
from .Node import Node


class Tree(object):
    def __init__(self):

        self.name = "tree"

        self.root       = Node()
        self.root.name  = "root"
        self.root.id    = 0
        self.root.level = 0

        self.__id_counter = 1


    def get_root(self):
        return self.root






    def create_node(self, parent, node_name, node_type="d"):
        
        node            = Node()
        node.name       = node_name
        node.ntype      = node_type
        node.id_parent  = parent.id
        node.id         = self.__id_counter
        node.level      = parent.level + 1
        
        
        # parent.add_children(node.id)
        parent.add_children(node)
        self.__id_counter += 1
        
        return node





    def find_node(self, path_array):
        path_array = path_array[1:]             # trim first("root")
        node = self.root
        for pi in path_array:
            node = node.get_children(pi)

        return node










    #--- prints ---------------------------------------------------------------
    def show(self):

        print(self.root.name)
        for node in self.root.childrens:
            # print(node.name)
            self.__re_show(node)



    def __re_show(self, parent):
        print("  "*parent.level + parent.name)
        for node in parent.childrens:
            # print(node.name)
            self.__re_show(node)