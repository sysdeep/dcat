#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os


class Walker(object):
	def __init__(self, tree, scan_dir):
		self.tree       = tree
		self.scan_dir   = scan_dir
		self.scan_items_count = 0




	def start(self):
		self.scan_items_count = 0
		folder_path_len = len(self.scan_dir)
		for root, dirs, files in os.walk(self.scan_dir):

			o_root = "root" + root[folder_path_len:]

			path_array = o_root.split(os.sep)
			node = self.tree.find_node(path_array)


			for d in dirs:
				self.tree.create_node(node, d)
				self.scan_items_count += 1

			for f in files:
				self.tree.create_node(node, f)
				self.scan_items_count += 1
