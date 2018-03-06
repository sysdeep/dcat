#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import time
import uuid

from .. import get_storage
from ..xstor import x1
from app.logic import scaner

from .defs import *







def make_xml():
	"""
		test1	: 0.3789064884185791
				: 0.4810817241668701
		size	: 72kb
	"""
	print("make xml: ", SCAN_PATH)
	ts = time.time()
	x1.start(SCAN_PATH, XDB_FILE, "cmp_tests")
	te = time.time()

	print("timeit: ", te - ts)



def make_sql():
	"""
		test1	: 0.7755308151245117
				: 0.7381277084350586
		size	: 753kb
	"""
	print("make xml: ", SCAN_PATH)
	ts = time.time()


	storage = get_storage()
	storage.create_storage(SDB_FILE)

	vol_id = str(uuid.uuid4())
	vol_row = {
			"uuid"	: vol_id,
			"name"	: "cmp_tests",
			"path"	: SCAN_PATH,
			"vtype"	: "cd",
			"created"	: "",
			"description"	: ""
	}

	storage.create_volume_row(vol_row)

	scaner.start_scan_for_storage(SCAN_PATH, storage, vol_id)

	storage.commit()

	te = time.time()

	print("timeit: ", te - ts)



make_xml()
# make_sql()

