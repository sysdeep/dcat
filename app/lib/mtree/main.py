#!/usr/bin/env python
# -*- coding: utf-8 -*-


import os
import os.path
from .Tree import Tree
from app.rc import DIR_SCAN
from datetime import datetime
from .Render import Render

def t2():
    DIR_SCAN = "/home/nia/Documents"
    tree = Tree()
    root_node = tree.get_root()
    ds_len = len(DIR_SCAN)
    tstart = datetime.now()
    for root, dirs, files in os.walk(DIR_SCAN):
        o_root = "root" + root[ds_len:]
        # o_root = root[ds_len:]

        path_array = o_root.split(os.sep)

        # if len(o_root) == 0:
        #     node = root_node
        # else:
            
        node = tree.find_node(path_array)


        for d in dirs:
            tree.create_node(node, d)

        for f in files:
            tree.create_node(node, f)

        # print(o_root)
        # print(os.path.join("root", o_root))
    tend = datetime.now()
    # tree.show()

    r = Render(tree)
    r.show()

    dur = tend - tstart
    print(dur.seconds)





# t2()


def t1():


    tree = Tree()

    root_node = tree.get_root()

    dir1 = tree.create_node(root_node, "dir1")
    dir2 = tree.create_node(root_node, "dir2")
    dir3 = tree.create_node(root_node, "dir3")

    d1_1 = tree.create_node(dir1, "dir1.1")
    tree.create_node(dir1, "dir1.2")
    tree.create_node(dir1, "dir1.3")

    tree.create_node(d1_1, "d.1.1.1")

    tree.show()


    print("-----------------------")
    r = Render(tree)
    r.show()



def t3():
    from .. import anytree
    
    root = anytree.Node("Root")
    d1 = anytree.Node("d1", parent=root)
    d2 = anytree.Node("d2", parent=root)
    d1_1 = anytree.Node("d1.1", parent=d1)
    d1_1_1 = anytree.Node("d1.1.1", parent=d1_1)

    for pre, fill, node in anytree.RenderTree(root):
        print(pre, node.name)



if __name__ == '__main__':
    
    
    
    t2()
    
    
    # t3()
