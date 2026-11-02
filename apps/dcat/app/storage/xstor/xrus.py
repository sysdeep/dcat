#!/usr/bin/env python3
# -*- coding: utf-8 -*-


import os
import gzip
import xml.etree.ElementTree as etree


XFILE = "/home/nia/Development/_Python/_DCat/xrus.xml"
# GFILE = "/home/nia/Development/_Python/_DCat/xrus.xml.gz"
GFILE = "/home/nia/Development/_Python/_DCat/cmp_create.xml.gz"




# with open(XFILE, "r", encoding="utf-8") as fd:
# 	tree = etree.fromstring(fd.read())
#
# 	etree.dump(tree)

with gzip.open(GFILE, "rb") as fd:
	tree = etree.fromstring(fd.read())

	etree.dump(tree)



def create_file():

	root = etree.Element("catalog", {"name": "name", "description": "привет"})

	with gzip.open(GFILE, "wb") as fd:
		fd.write(etree.tostring(root, encoding="utf-8"))


# create_file()