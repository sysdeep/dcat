#!/usr/bin/env python
# -*- coding: utf-8 -*-
from app import log


class NSTree(object):
	def __init__(self):
		self.nodes = []
		self.root = None

		self.__set_new()

	def set_nodes(self, nodes_list):
		# print(nodes_list)
		nodes_list.sort(key=lambda a: a["tree_lk"])

		for node_data in nodes_list:
			if node_data["ntype"] == "f":
				node = NodeFile()

			elif node_data["ntype"] == "d":
				node = NodeDir()
			else:
				log.error("set_nodes - неизвестный тип ноды: {}".format(node_data["ntype"]))
				node = None


			if node:
				node.load(node_data)
				self.nodes.append(node)




		# self.nodes = sorted(nodes_list, key=lambda a: a["tree_lk"])
		# self.nodes = nodes_list


	def print_nodes(self):
		for node in sorted(self.nodes, key=lambda a: a.tree_lk):
			print(self.__fill_tabs(node.tree_level) + node.name + " - " + str(node.tree_lk) + " - " + str(node.tree_rk))

	def __fill_tabs(self, num):
		return "\t"*num



	def insert(self, parent_node, new_node):
		
		parent_rk = parent_node.tree_rk
		parent_lk = parent_node.tree_lk

		# // 1 - update after
		for node in self.nodes:
			if node.tree_lk > parent_rk:
				node.tree_lk += 2
				node.tree_rk += 2

		# // 2 - update parent
		for node in self.nodes:
			if node.tree_rk >= parent_rk and node.tree_lk < parent_rk:
				node.tree_rk += 2

		# // 3 - add node
		new_node.tree_level = parent_node.tree_level + 1
		new_node.tree_lk = parent_rk
		new_node.tree_rk = parent_rk + 1

		self.nodes.append(new_node)
		
	



	def create_node_dir(self, parent_node, new_node_name):
		new_node = NodeDir()
		new_node.name = new_node_name
		self.insert(parent_node, new_node)
		return new_node

	def create_node_file(self, parent_node, new_node_name):
		new_node = NodeFile()
		new_node.name = new_node_name
		self.insert(parent_node, new_node)
		return new_node





	def __set_new(self):
		root_node = NodeDir()
		root_node.tree_lk = 0
		root_node.tree_rk = 1
		root_node.tree_level = 0
		root_node.name = "root"

		self.nodes = [root_node]
		self.root = root_node




	def get_node_tree_path(self, path_array):
		# print("----------------------")
		pa = path_array[1:]
		node = self.root
		# print(pa)



		for path_item in pa:
			childrens = self.get_childrens(node)

			nodes = [node for node in childrens if node.name == path_item]

			# print(nodes)
			# print(nodes)
			if len(nodes) > 0:
				node = nodes[0]

		# print("----------------------")
		return node



	def get_childrens(self, parent_node):
		childrens = [node for node in self.nodes 
				if node.tree_lk > parent_node.tree_lk 
				and node.tree_rk < parent_node.tree_rk 
				and node.tree_level - 1 == parent_node.tree_level]
		return childrens

	def get_nodes_level(self, level):

		return [node for node in self.nodes if node.tree_level == level]

	def export(self):
		data = []
		for node in self.nodes:
			row = node.export()
			data.append(row)

		return data






class Node(object):
	def __init__(self):
		self.tree_lk = 0
		self.tree_rk = 0
		self.tree_level = 0
		self.name = ""
		self.ntype = "b"
		self.size = 0

	def export(self):
		data = {
			"tree_lk" 		: self.tree_lk,
			"tree_rk"		: self.tree_rk,
			"tree_level"	: self.tree_level,
			"name"			: self.name,
			"ntype" 		: self.ntype
		}

		return data

	def load(self, data):
		self.tree_lk 	= data["tree_lk"]
		self.tree_rk 	= data["tree_rk"]
		self.tree_level = data["tree_level"]
		self.name 		= data["name"]

class NodeDir(Node):
	def __init__(self):
		super(NodeDir, self).__init__()
		self.ntype = "d"

class NodeFile(Node):
	def __init__(self):
		super(NodeFile, self).__init__()
		self.ntype = "f"
		
	




















def get_childrens(items, root):
	childrens = [node for node in items 
				if node.tree_lk > root.tree_lk 
				and node.tree_rk < root.tree_rk 
				and node.tree_level - 1 == root.tree_level]
	return childrens


def print_tree1(items):
	prefix = []
	for node in sorted(items, key=lambda a: a.tree_lk):
		prefix = []
		# if node.tree_level == 0:
		# 	prefix = []		

		for x in range(node.tree_level):
			prefix.append("  ")

		# print(prefix + node.name)
		# print("\u02EA"+"  "*node.tree_level + "|-" + node.name + " - " + str(node.tree_lk) + " - " + str(node.tree_rk))
		# print("  "*node.tree_level + "|-" + node.name + " - " + str(node.tree_lk) + " - " + str(node.tree_rk))

		prefix_str = "".join(prefix)


		sss = "{} [{}] {}".format(prefix_str, node.ntype, node.name)

		if node.ntype == "f":
			sss += " ({})".format(node.size)

		print(sss)
		# print(prefix_str + node.name)

		# childrens = get_childrens(items, node)
		# if len(childrens) > 0:
		# 	prefix = "  "*node.tree_level +  "|-"



# def print_tree1(items):
# 	prefix = ""
# 	for node in sorted(items, key=lambda a: a.tree_lk):
		

# 		# print(prefix + node.name)
# 		# print("\u02EA"+"  "*node.tree_level + "|-" + node.name + " - " + str(node.tree_lk) + " - " + str(node.tree_rk))
# 		print("  "*node.tree_level + "|-" + node.name + " - " + str(node.tree_lk) + " - " + str(node.tree_rk))


# 		# childrens = get_childrens(items, node)
# 		# if len(childrens) > 0:
# 		# 	prefix = "  "*node.tree_level +  "|-"





if __name__ == '__main__':

	tree = NSTree()

	root_node = Node()
	root_node.tree_lk = 0
	root_node.tree_rk = 1
	root_node.tree_level = 0
	root_node.name = "root"


	tree.set_nodes([root_node])

	tree.print_nodes()


	print("-------------------------")
	new_node1 = Node()
	new_node1.name = "new 1"
	tree.insert(root_node, new_node1)


	new_node2 = Node()
	new_node2.name = "new 2"
	tree.insert(root_node, new_node2)

	new_node1_1 = Node()
	new_node1_1.name = "new 1.1"
	tree.insert(new_node1, new_node1_1)

	tree.print_nodes()


	ch = tree.get_childrens(root_node)
	print(ch)


	