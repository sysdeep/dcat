#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from abc import ABC, abstractmethod

from app.lib.models.Volume import Volume


class FileWorkerAbstract(ABC):
	"""интерфейси загрузки и сохранения файла тома"""
	
	@abstractmethod
	def load(self, model: Volume, file_path: str):
		pass
	
	@abstractmethod
	def save(self, model: Volume, file_path: str):
		pass


