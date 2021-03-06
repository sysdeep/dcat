#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
from os.path import join, getsize

from app.rc import DIR_SCAN, FILE_JSON
from .nstree import NSTree, print_tree1







# def start(scan_path, tree):
# 	folder_path_len = len(scan_path)

# 	for root, dirs, files in os.walk(scan_path):
# 		o_root = root[folder_path_len:]
# 		if len(o_root) == 0:
# 			root_path = "root"
# 		else:
# 			root_path = "root" + o_root

# 		# print(root_path)
# 		root_path_array = root_path.split(os.sep)
# 		# print(root_path_array)

# 		node = tree.get_node_tree_path(root_path_array)
# 		# print("node_name ->", node.name)



# 		#--- add dirs
# 		for dir_item in dirs:
# 			# print("add dir", node.name, dir_item)
# 			tree.create_node_dir(node, dir_item)


# 		#--- add files
# 		for file_item in files:
# 			# print("add file", node.name, file_item)
# 			file_path = os.path.join(root, file_item)
# 			try:
# 				file_size = getsize(file_path)
# 			except:
# 				continue
# 			# print(file_size)
# 			node_item = tree.create_node_file(node, file_item)
# 			node_item.size = file_size















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

		for root, dirs, files in os.walk(self.folder_path):
			# print(root[root_size:])
			# print(root)

			o_root = root[self.folder_path_len:]
			# print(o_root)
			if len(o_root) == 0:
				root_path = "root"
			else:
				root_path = "root" + o_root

			# print(root_path)
			root_path_array = self.__unpack_path(root_path)
			# print(root_path_array)

			node = self.tree.get_node_tree_path(root_path_array)
			# print("node_name ->", node.name)



			#--- add dirs
			for dir_item in dirs:
				# print("add dir", node.name, dir_item)
				self.tree.create_node_dir(node, dir_item)


			#--- add files
			for file_item in files:
				# print("add file", node.name, file_item)
				file_size = getsize(os.path.join(root, file_item))
				# print(file_size)
				node_item = self.tree.create_node_file(node, file_item)
				node_item.size = file_size


	def __unpack_path(self, path):
		return path.split(os.sep)













if __name__ == '__main__':

	import json

	walker = Walker(DIR_SCAN)
	walker.start()

	# walker.tree.print_nodes()
	print_tree1(walker.tree.nodes)

	data = walker.tree.export()
	print()
	with open(FILE_JSON, "w") as fd:
		fd.write(json.dumps(data))

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