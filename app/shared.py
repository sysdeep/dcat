#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from .lib.USettings import USettings

DATA = {
	"usettings"	: USettings(),
}




def get_usettings() -> USettings:
	# usettings = DATA.get("usettings")
	# if usettings is None:
	# 	usettings = USettings()
	# 	usettings.open_settings()
	# 	DATA["usettings"] = usettings
	return DATA["usettings"]

