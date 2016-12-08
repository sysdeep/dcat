#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
	walk on tree in thread
"""
import threading
import time
from queue import Queue
import os
import os.path

from app.rc import QUE_WALKER
from app import log
from app.logic import get_tree

from datetime import datetime
import math












class TWalker(threading.Thread):
	def __init__(self, *args, **kwargs):
		super(TWalker, self).__init__(*args, **kwargs)
		self.daemon 		= True

		self.scan_path 		= ""
		self.tree 			= get_tree()

		self.__start_time 	= None
		self.__scan_items 	= []
		self.__scan_items_count = 0
		self.__progress 	= 0





	def run(self):
		log.info("starting scan")
		self.__event_start()
		self.tree.set_empty()


		self.__scan()
		self.__make_tree()
		self.__event_finish()







	def __scan(self):
		self.__start_time 		= datetime.now()
		self.__event_start_scan()

		folder_path_len = len(self.scan_path)
		for root, dirs, files in os.walk(self.scan_path):

			# log.warn(root)


			o_root = root[folder_path_len:]
			if len(o_root) == 0:
				o_root = "root"
			else:
				o_root = "root" + o_root

			#--- add dirs
			for dir_item in dirs:
				item = os.path.join(o_root, dir_item)

				self.__scan_items.append((item, 0))


			#--- add files
			for file_item in files:
				item = os.path.join(o_root, file_item)
				self.__scan_items.append((item, 1))


			# continue
			#
			# o_root = root[folder_path_len:]
			# if len(o_root) == 0:
			# 	o_root = "root"
			# else:
			# 	o_root = "root" + o_root
			#
			# root_path_array = o_root.split(os.sep)
			# parent_node = self.tree.get_node_tree_path(root_path_array)
			#
			#
			# #--- add dirs
			# for dir_item in dirs:
			# 	self.tree.create_node_dir(parent_node, dir_item)
			# 	item = os.path.join(o_root, dir_item)
			# 	# print(item)
			# 	# self.__push_dir(item)
			# 	# print("add dir", node.name, dir_item)
			# 	# tree.create_node_dir(node, dir_item)
			#
			#
			# #--- add files
			# for file_item in files:
			# 	self.tree.create_node_file(parent_node, file_item)
			# 	item = os.path.join(o_root, file_item)
			# 	# print(item)
			# 	# self.__push_file(item)
			# 	# print("add file", node.name, file_item)
			# 	# file_path = os.path.join(root, file_item)
			# 	# try:
			# 	# 	file_size = getsize(file_path)
			# 	# except:
			# 	# 	continue
			# 	# # print(file_size)
			# 	# node_item = tree.create_node_file(node, file_item)
			# 	# node_item.size = file_size


		end_time = datetime.now()


		qqq = end_time - self.__start_time
		items_count = len(self.__scan_items)
		self.__scan_items_count = items_count


		log.info("finish scan: {}".format(qqq.seconds))
		log.info("items: {}".format(items_count))
		self.__event_finish_scan(qqq.seconds, items_count)





	def __make_tree(self):
		self.__start_time 		= datetime.now()
		self.__event_start_tree()

		chunk = math.floor(self.__scan_items_count/10)
		log.warn(chunk)



		chunk_group = 0
		for item in self.__scan_items:
			path = item[0]
			ntype = item[1]


			item_array = path.split(os.sep)

			item_name = item_array[-1]
			item_path = item_array[:-1]

			parent_node = self.tree.get_node_tree_path(item_path)


			if ntype == 0:
				node = self.tree.create_node_dir(parent_node, item_name)
			elif ntype == 1:
				node = self.tree.create_node_file(parent_node, item_name)

			chunk_group += 1
			if chunk_group == chunk:
				chunk_group = 0
				self.__progress += 10
				self.__event_progress(self.__progress)


		end_time = datetime.now()
		qqq = end_time - self.__start_time

		self.__event_finish_tree(qqq.seconds)






	#--- events ---------------------------------------------------------------
	def __event_start(self):
		data = {
			"event"		: "start",
		}
		self.__push_que(data)

	def __event_finish(self):
		data = {
			"event"		: "finish",
		}
		self.__push_que(data)


	def __event_start_scan(self):
		data = {
			"event"		: "start_scan",
		}
		self.__push_que(data)


	def __event_finish_scan(self, sec, items_count):
		data = {
			"event"			: "finish_scan",
			"sec"			: sec,
			"items_count"	: items_count
		}
		self.__push_que(data)


	def __event_start_tree(self):
		data = {
			"event"		: "start_tree",
		}
		self.__push_que(data)


	def __event_finish_tree(self, sec):
		data = {
			"event"			: "finish_tree",
			"sec"			: sec
		}
		self.__push_que(data)


	def __event_progress(self, prc):
		data = {
			"event"			: "progress",
			"prc"			: prc
		}
		self.__push_que(data)
	#--- events ---------------------------------------------------------------









	def __push_que(self, data):
		QUE_WALKER.put(data)

	#
	#
	# def __push_start(self):
	# 	data = {
	# 		"event"		: "start_scan"
	# 	}
	# 	QUE_WALKER.put(data)
	#
	# def __push_end(self, sec):
	# 	data = {
	# 		"event"		: "finish_scan",
	# 		"sec"		: sec
	# 	}
	# 	QUE_WALKER.put(data)

	# def __push_dir(self, item):
	# 	data = {
	# 		"event"		: "data",
	# 		"ntype" 	: "d",
	# 		"item"		: item
	# 	}
	# 	QUE_WALKER.put(data)
	#
	# def __push_file(self, item):
	# 	data = {
	# 		"event"		: "data",
	# 		"ntype" 	: "f",
	# 		"item"		: item
	# 	}
	# 	QUE_WALKER.put(data)






def start(scan_path):
	log.debug("start twalker " + scan_path)
	w = TWalker()
	w.scan_path = scan_path
	w.start()







if __name__ == "__main__":

	w = TWalker()
	w.scan_path = "media"
	w.start()

	for x in range(6):
		print("root: {}".format(x))
		time.sleep(1)