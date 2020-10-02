#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from app.lib.volume import Volume

# VOL_PATH = "/home/nia/Temp/dcat_export/Video.hmap.gz"
VOL_PATH = "/home/nia/Temp/dcat_export/oxygen_16x16.hmap.gz"


vol = Volume()
vol.load(VOL_PATH)