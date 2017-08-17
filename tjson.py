#!/usr/bin/env python3
# -*- coding: utf-8 -*-



import os, json


DIR_SELF = os.path.dirname(os.path.abspath(__file__))
DIR_SCAN = os.path.normpath(os.path.join(DIR_SELF, "..", "sdir"))
DIR_DEST = os.path.join(DIR_SELF, "tests")

FILES = []


for root, dirs, files in os.walk(DIR_SCAN):
    # print(root)

    for d in dirs:
        row = {
            "parent": root,
            "name"  : d,
            "type"  : "d"
        }
        FILES.append(row)

    for f in files:
        row = {
            "parent": root,
            "name"  : f,
            "type"  : "f"
        }
        FILES.append(row)


# print(FILES)

with open(os.path.join(DIR_DEST, "tjson.json"), "w", encoding="utf-8") as fd:
    fd.write(json.dumps(FILES))
