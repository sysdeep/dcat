#!/usr/bin/env python3
# -*- coding: utf-8 -*-

class NSNode(object):
	def __init__(self):

		self.tree_lk 	= 0
		self.tree_rk 	= 0
		self.tree_level = 0

		self.name 		= ""			# название ноды







class NSTree(object):

	def __init__(self):
		self.nodes 		= []		# список нод
		self.root 		= NSNode()		# основная нода
		# self.nodes_map 	= {}		# {node_uuid: node}
		#
		# #--- инициализируем пустое дерево
		# self.__set_new()


		self.root.tree_lk 		= 0
		self.root.tree_rk 		= 1
		self.root.tree_level 	= 0
		self.root.name 			= "root"




	def create_node(self, parent_node, name=""):
		"""создание новой ноды от родителя"""


		new_node = NSNode()
		new_node.name = name

		self.__insert_node(parent_node, new_node)
		return new_node


	def __insert_node(self, parent_node, new_node):
		"""добавление новой ноды к родительской ветви"""

		parent_rk = parent_node.tree_rk
		# parent_lk = parent_node.tree_lk

		#--- 1 - update after
		for node in self.nodes:
			if node.tree_lk > parent_rk:
				node.tree_lk += 2
				node.tree_rk += 2

		#--- 2 - update parent
		for node in self.nodes:
			if node.tree_rk >= parent_rk and node.tree_lk < parent_rk:
				node.tree_rk += 2

		#--- 3 - add node
		new_node.tree_level = parent_node.tree_level + 1
		new_node.tree_lk = parent_rk
		new_node.tree_rk = parent_rk + 1


		self.nodes.append(new_node)
		# self.nodes_map[new_node.uuid] = new_node




	def __remove_branch(self, node):
		"""удаление заданной ноды(со всеми потомками)"""

		node_lk = node.tree_lk
		node_rk = node.tree_rk

		#--- 1 - find del nodes
		del_nodes = [n for n in self.nodes if n.tree_lk >= node_lk and n.tree_rk <= node_rk]
		# print(del_nodes)

		#--- 2 - remove nodes from list
		for n in del_nodes:
			self.nodes.remove(n)
			# del(self.nodes_map[n.uuid])

		#--- 3 - update nodes before
		for n in self.nodes:
			if n.tree_rk > node_rk and n.tree_lk < node_lk:
				n.tree_rk -= (node_rk - node_lk + 1)


		#--- 4 - update nodes after
		for n in self.nodes:
			if n.tree_lk > node_rk:
				n.tree_lk -= (node_rk - node_lk + 1)
				n.tree_rk -= (node_rk - node_lk + 1)


		return del_nodes