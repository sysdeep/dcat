#!/usr/bin/env python
# -*- coding: utf-8 -*-

from app.logic import get_tree, walker
import json


# DIR_SRC = "/home/nia/Temp"
DIR_SRC = "/home/nia/Documents"
tfile = "test.json"

tree = get_tree()


walker.start(DIR_SRC, tree)


print(tree.print_nodes())


with open(tfile, "w") as fd:
	fd.write(json.dumps(tree.export()))