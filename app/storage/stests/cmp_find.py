#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""

"""



import time
import uuid
import gzip
import xml.etree.ElementTree as etree

from .. import get_storage
from ..xstor import x1
from app.logic import scaner

from .defs import *







def find_xml():
	"""
		test1	: 0.06995248794555664

	"""
	print("remove volume xml: ", SCAN_PATH)
	ts = time.time()

	with gzip.open(XDB_FILE, "rb") as fd:
		tree = etree.fromstring(fd.read())


		# result = tree.findall("[@attrib='0_un']")
		result = tree.find(".//node[@name='manual_dos_eng.pdf']")

		print(result.attrib["name"])


		print("childrens")
		for ch in result:
			print(ch)

		print("parent")
		parent = result.find("..")												# not working...
		# parent = tree.find(".//node[@name='manual_dos_eng.pdf']/..")			# working
		print(parent)

		# etree.dump(result)

		# vol_el = tree.find("volume")
		# # etree.dump(vol_el)
		#
		# tree.remove(vol_el)
		#
		# etree.dump(tree)

	# vol_el = tree.find("volume")
	# print(vol_el)



	te = time.time()

	print("timeit: ", te - ts)




find_xml()

