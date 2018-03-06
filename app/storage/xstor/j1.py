#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import time
from .nstree import NSTree

SCAN_PATH = "/home/nia/Documents/_Comcon"
SCAN_PATH = "/home/nia/Development/_Python/_DCat/sdir"
SCAN_PATH = "/home/nia/Development/_Python/_DCat"
SCAN_PATH = "/home/nia/Documents/_Comcon"



def start(scan_path, db_file, volume_name):


	tree = NSTree()

	rmap = {
		scan_path	: tree.root
	}



	for root, dirs, files in os.walk(scan_path):



		x_el = rmap.get(root)


		for dir in dirs:
			full_path = os.path.join(root, dir)				# полный путь
			if not os.path.exists(full_path):				# если нет - продолжаем...
				continue

			st = os.stat(full_path)							# статистика по файлу


			node = tree.create_node(x_el, dir)

			# row = make_frow(dir, "d", st)

			# node = etree.SubElement(x_el, "node", {"name": dir, "type": "d"})
			# node = etree.SubElement(x_el, "node", row)

			dir_path = os.path.join(root, dir)

			rmap[dir_path] = node



		for f in files:
			full_path = os.path.join(root, f)				# полный путь
			if not os.path.exists(full_path):				# если нет - продолжаем...
				continue

			st = os.stat(full_path)							# статистика по файлу

			# row = make_frow(f, "f", st)
			#
			# etree.SubElement(x_el, "node", row)
			# etree.SubElement(x_el, "node", {"name": f, "type": "f"})
			node = tree.create_node(x_el, f)



		del rmap[root]

	# print(tree.nodes)
	# tree.print_tree()
	print(len(tree.nodes))



	#
	# with gzip.open(db_file, "wb") as fd:
	# 	fd.write(etree.tostring(xroot, encoding="utf-8"))



ts = time.time()

start(SCAN_PATH, None, None)

te = time.time()

print("timeit: ", te - ts)

