#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
import os
from . import events
from app import log
from app.rc import set_scan_dir, get_scan_dir
from app.logic import walker, twalker
from app.logic import get_tree, load_tree
from .utils.WalkerDispatcher import WalkerDispatcher



class Controller(object):
	def __init__(self):


		self.tree = get_tree()

		# self.walker_dispatcher = WalkerDispatcher(self)
		# self.walker_dispatcher.msg.connect(self.__handle_new_node)
		#



		# events.on("set_scan_path", self.set_scan_path)
		events.on("set_save_file", self.set_save_file)
		events.on("set_open_file", self.set_open_file)
		# events.on("start_scan", self.start_scan)


	# def set_scan_path(self, path):
	# 	log.info(path)
	# 	set_scan_dir(path)


	# def start_scan(self):
	# 	log.info("start scaning")
	#
	#
	#
	# 	self.walker_dispatcher.start()
	#
	#
	#
	#
	#
	# 	scan_dir = get_scan_dir()
	# 	log.debug("scan_dir: " + scan_dir)
	# 	self.tree.set_empty()
	#
	#
	# 	# walker.start(scan_dir, self.tree)
	# 	twalker.start(scan_dir)
	#
	# 	log.debug("done")
	#
	# 	# self.tree.print_nodes()
	# 	events.update_tree()


	def set_save_file(self, path):


		data = self.tree.export()

		with open(path, "w") as fd:
			fd.write(json.dumps(data))



	def set_open_file(self, path):
		log.info("open db file: " + path)
		load_tree(path)

		self.tree.print_nodes()

		events.update_tree()




	# def __handle_new_node(self, data):
	#
	#
	# 	log.warning(data)
	#
	# 	# return False
	#
	#
	#
	# 	# if data["event"] == "data":
	# 	# 	item = data["item"]
	# 	# 	item_array = item.split(os.sep)
	# 	#
	# 	# 	item_name = item_array[-1]
	# 	# 	item_path = item_array[:-1]
	# 	#
	# 	# 	parent_node = self.tree.get_node_tree_path(item_path)
	# 	#
	# 	# 	# log.debug(root_node)
	# 	# 	log.debug(item_path)
	# 	# 	log.debug(item_name)
	# 	#
	# 	# 	if data["ntype"] == "d":
	# 	# 		node = self.tree.create_node_dir(parent_node, item_name)
	# 	#
	# 	# 	elif data["ntype"] == "f":
	# 	# 		node = self.tree.create_node_file(parent_node, item_name)
	# 	#
	# 	# 	# print(node.name)
	#
	# 	if data["event"] == "end":
	#
	# 		print("end ------")
	# 		self.tree.print_nodes()
	#
	# 		events.update_tree()