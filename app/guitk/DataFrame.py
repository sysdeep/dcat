#!/usr/bin/env python
# -*- coding: utf-8 -*-

import tkinter
from tkinter import ttk

class DataFrame(tkinter.Frame):
	def __init__(self, parent, *args, **kwargs):
		super(DataFrame, self).__init__(parent, *args, **kwargs)


		label = tkinter.Label(self, text="data")
		label.pack()

		

