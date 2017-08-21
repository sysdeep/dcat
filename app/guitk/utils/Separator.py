#!/usr/bin/env python
# -*- coding: utf-8 -*-

import tkinter
from tkinter import ttk


class SeparatorH(tkinter.Frame):
	def __init__(self, parent=None):
		super(SeparatorH, self).__init__(parent)
		self.config(relief="raised", bd=2, height=2)
		self.pack(fill="x", padx=5, pady=5)


class SeparatorV(tkinter.Frame):
	def __init__(self, parent=None):
		super(SeparatorV, self).__init__(parent)
		self.config(relief="raised", bd=0, width=2)
		self.pack(fill="y", padx=5, pady=5)