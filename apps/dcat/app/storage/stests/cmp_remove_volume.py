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







def remove_volume_xml():
	"""
		test1	: 0.06995248794555664

	"""
	print("remove volume xml: ", SCAN_PATH)
	ts = time.time()

	with gzip.open(XDB_FILE, "rb") as fd:
		tree = etree.fromstring(fd.read())

		vol_el = tree.find("volume")
		# etree.dump(vol_el)

		tree.remove(vol_el)

		etree.dump(tree)

	# vol_el = tree.find("volume")
	# print(vol_el)



	te = time.time()

	print("timeit: ", te - ts)




remove_volume_xml()

