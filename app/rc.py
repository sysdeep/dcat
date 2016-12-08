#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os.path

DIR_SELF = os.path.dirname(os.path.abspath(__file__))
DIR_MEDIA = os.path.normpath(os.path.join(DIR_SELF, "..", "media"))

DIR_ICONS = os.path.join(DIR_MEDIA, "icons")

DIR_SCAN = os.path.normpath(os.path.join(DIR_SELF, "..", "..", "sdir"))
FILE_JSON = os.path.normpath(os.path.join(DIR_SELF, "..", "..", "sdir.json"))







def get_icon_path(*icon_subpath):
    return os.path.join(DIR_ICONS, *icon_subpath)