#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
from .Node import Node


class Tree(object):
	def __init__(self):

		self.name       = "tree"
		self.root       = None
		

		self.__id_counter = 2
		self.__nodes_dict = {}

		self.__make_root()


	def __make_root(self):
		self.root       = Node()
		self.root.name  = "root"
		self.root.id    = 1
		self.root.level = 0

		self.__nodes_dict[self.root.id] = self.root
		

	def get_root(self):
		return self.root


	def set_empty(self):
		self.__nodes_dict = {}
		self.__make_root()



	def create_node(self, parent, node_name, node_type="d"):
		
		node            = Node()
		node.name       = node_name
		node.ntype      = node_type
		node.id_parent  = parent.id
		node.id         = self.__id_counter
		node.level      = parent.level + 1
		
		
		# parent.add_children(node.id)
		parent.add_children(node)
		self.__nodes_dict[node.id] = node
		self.__id_counter += 1
		
		return node


	def insert_node(self, parent_node, child_node):
		parent_node.add_children(child_node)
		child_node.parent = parent_node
		self.__nodes_dict[child_node.id] = child_node
		
	


	def find_node(self, path_array):
		path_array = path_array[1:]             # trim first("root")
		node = self.root
		for pi in path_array:
			node = node.get_children(pi)

		return node


	def get_node_id(self, id):
		node = self.__nodes_dict.get(id)

		return node


	 
	def get_nodes_count(self):
		return len(self.__nodes_dict)



	#--- prints ---------------------------------------------------------------
	def show(self):
		print(self.root.name)
		for node in self.root.childrens:
			self.__re_show(node)

	def __re_show(self, parent):
		print("  "*parent.level + parent.name)
		for node in parent.childrens:
			self.__re_show(node)

	#--- prints ---------------------------------------------------------------





	#--- scan -----------------------------------------------------------------
	def start_scan(self, scan_path):
		self.set_empty()
		folder_path_len = len(scan_path)
		for root, dirs, files in os.walk(scan_path):

			o_root = "root" + root[folder_path_len:]

			path_array = o_root.split(os.sep)
			node = self.find_node(path_array)


			for d in dirs:
				item = self.create_node(node, d)
				full_path = os.path.join(root, d)
				st = os.stat(full_path)
				item.ntype 		= "d"
				item.st_size 	= st.st_size
				item.st_atime 	= st.st_atime
				item.st_mtime 	= st.st_mtime
				item.st_ctime 	= st.st_ctime

			for f in files:
				item = self.create_node(node, f)
				full_path = os.path.join(root, f)
				st = os.stat(full_path)
				item.ntype 		= "f"
				item.st_size 	= st.st_size
				item.st_atime 	= st.st_atime
				item.st_mtime 	= st.st_mtime
				item.st_ctime 	= st.st_ctime
	#--- scan -----------------------------------------------------------------





	#--- export ---------------------------------------------------------------

	def start_export(self):
		items = []
		for item in self.__nodes_dict.values():
			items.append(item.get_dict())
		return items
	#--- export ---------------------------------------------------------------










	#--- import ---------------------------------------------------------------
	def start_import(self, data):
		self.set_empty()
		data.sort(key = lambda x: x["id"])

		for row in data:
			if row["id_parent"] == 0: continue         # root

			parent_node = self.get_node_id(row["id_parent"])

			node = Node()
			node.set_dict(row)
			self.insert_node(parent_node, node)

	#--- import ---------------------------------------------------------------

	