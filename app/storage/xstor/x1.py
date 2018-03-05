#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import gzip
import xml.etree.ElementTree as etree

SCAN_PATH = "/mnt/backup"
# SCAN_PATH = "/home/nia/Work/_LinuxServer"
XFILE = "/home/nia/Development/_Python/_DCat/x1.xml"
GFILE = "/home/nia/Development/_Python/_DCat/x1.xml.gz"




# xroot = etree.parse(XFILE)
# etree.dump(xroot)

#
# with open(XFILE, "br") as fd:
# 	xroot = etree.fromstring(fd.read())
#
# 	etree.dump(xroot)
#
#



with gzip.open(GFILE, "rb") as fd:
	xroot = etree.fromstring(fd.read())

	etree.dump(xroot)











xroot = etree.Element("volume")

rmap = {
	SCAN_PATH	: xroot
}



for root, dirs, files in os.walk(SCAN_PATH):



	x_el = rmap.get(root)


	for dir in dirs:
		node = etree.SubElement(x_el, "node", {"name": dir, "type": "d"})

		dir_path = os.path.join(root, dir)

		rmap[dir_path] = node



	for f in files:
		etree.SubElement(x_el, "node", {"name": f, "type": "f"})



	del rmap[root]



#
# with gzip.open(GFILE, "wb") as fd:
# 	fd.write(etree.tostring(xroot, encoding="utf-8"))


#
#
#
# with open(XFILE, "wb") as fd:
# 	fd.write(etree.tostring(xroot, encoding="utf-8"))
#

