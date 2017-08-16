#!/usr/bin/env python
# -*- coding: utf-8 -*-

from PyQt5.QtCore import QThread, QEvent


class Event(QEvent):
	EVENT_TYPE = QEvent.Type(QEvent.registerEventType())

	def __init__(self, data):
		#thread-safe
		QEvent.__init__(self, Event.EVENT_TYPE)
		self.data = data