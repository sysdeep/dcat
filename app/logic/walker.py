#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
from os.path import join, getsize

from app.rc import DIR_SCAN
from .nstree import NSTree



class Walker(object):
    def __init__(self, folder_path=""):
        self.folder_path = folder_path
        self.folder_path_len = len(folder_path)
        self.tree = NSTree()




    def set_path(self, folder_path):
        """"""
        self.folder_path = folder_path
        self.folder_path_len = len(folder_path)



    def start(self):
        print("start")
        for root, dirs, files in os.walk(self.folder_path):
            # print(root[root_size:])
            print(root)

            o_root = root[self.folder_path_len:]
            # print(o_root)
            if len(o_root) == 0:
                root_path = "root"
            else:
                root_path = "root" + o_root

            print(root_path)
            root_path_array = self.__unpack_path(root_path)
            print(root_path_array)

            node = self.tree.get_node_tree_path(root_path_array)
            print("node_name ->", node.name)
            


            #--- add dirs
            for dir_item in dirs:
                self.tree.create_node_dir(node, dir_item)


            #--- add files
            for file_item in files:
                self.tree.create_node_file(node, file_item)


    def __unpack_path(self, path):
        return path.split(os.sep)








if __name__ == '__main__':
    walker = Walker(DIR_SCAN)
    walker.start()

    walker.tree.print_nodes()

    # root_size = len(DIR_SCAN)
    # for root, dirs, files in os.walk(DIR_SCAN):
    #     # print(root)
    #     print(root[root_size:])
    #     print(dirs)
    #     print(files)
    #     # print(root, "consumes", end="")
    #     print(sum(getsize(join(root, name)) for name in files), end=" ")
    #     print("bytes in", len(files), "non-directory files")
    #     if 'CVS' in dirs:
    #         dirs.remove('CVS')  # don't visit CVS directories