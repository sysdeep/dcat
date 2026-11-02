#!/usr/bin/env python
# -*- coding: utf-8 -*-

# from app.lib.nstree import NSTree
# from app.lib.mtree import Tree
from .fs import load_file, store_file
from app.rc import FILE_JSON





# TREE = NSTree()
TREE = Tree()



def get_tree():
	global TREE
	return TREE



def load_tree(file):
	file_data = load_file(file)
	global TREE
	TREE.start_import(file_data)
	# TREE.set_nodes(file_data)



def store_tree(file_path):
	global TREE
	data = TREE.start_export()
	store_file(file_path, data)



def load_tree_demo():
	load_tree(FILE_JSON)