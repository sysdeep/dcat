#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from .storage.Storage import Storage

__data = {
	"storage"	: Storage()
}




def get_storage() -> Storage:
	return __data["storage"]


