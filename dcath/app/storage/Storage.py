#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
# from .volume.Volume import Volume

from app.lib.models.Volume import Volume


class Storage(object):
	def __init__(self):
		self.volumes = []
		self.volume = None
	
	# def read_dir(self, storage_path):
	# 	files = os.listdir(storage_path)
	# 	for file in files:
	# 		full_path = os.path.join(storage_path, file)
	# 		print(full_path)
	#
	# 		vol = self.open_volume(full_path)
	# 		self.volumes.append(vol)
	#
	
	
	def open_volume(self, volume_path: str) -> Volume:
		
		
		
		self.volume = Volume()
		
		self.volume.load(volume_path)
		
		
		return self.volume