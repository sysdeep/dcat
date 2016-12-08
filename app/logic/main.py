#!/usr/bin/env python
# -*- coding: utf-8 -*-

from .nstree import NSTree
from .fs import load_file
from app.rc import FILE_JSON

TREE = NSTree()



def get_tree():
	global TREE
	return TREE



def load_tree(file):
	file_data = load_file(file)
	global TREE
	TREE.set_nodes(file_data)


def load_tree_demo():
	load_tree(FILE_JSON)