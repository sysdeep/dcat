#!/usr/bin/env python
# -*- coding: utf-8 -*-

import tkinter




STYLES = {
	# name			(color_normal, color_hover, color_active, border_color, text_color)
	# "default"	: ("#BDBD5E", "#a5a543", "#92923c", "#92923c", "black"),
	"primary"	: ("#337ab7", "#286090", "#204d74", "#204d74", "white"),
	"success"	: ("#5cb85c", "#449d44", "#398439", "#398439", "white"),
	"info"		: ("#5bc0de", "#31b0d5", "#269abc", "#269abc", "white"),
	"warning"	: ("#f0ad4e", "#ec971f", "#d58512", "#d58512", "white"),
	"danger"	: ("#d9534f", "#c9302c", "#ac2925", "#ac2925", "white"),
}



class ButtonDefault(tkinter.Button):
	def __init__(self, parent, *args, **kwargs):
		super(ButtonDefault, self).__init__(parent, *args, **kwargs)

		self.text = ""
		self.cb = None

		self.config(bd=0)
		self.config(highlightthickness=0)
		# relief="flat"
		# self.config(font=('play', 16, 'bold'))
		# self.config(height=2)


	def set_my_style(self, style):

		bg_normal = style[0]
		bg_active = style[2]
		text_color = style[4]

		self.config(bg=bg_normal)
		self.config(activebackground=bg_active)
		self.config(fg=text_color)
		self.config(activeforeground=text_color)




class ButtonPrimary(ButtonDefault):
	def __init__(self, parent, *args, **kwargs):
		super(ButtonPrimary, self).__init__(parent, *args, **kwargs)
	
		self.set_my_style(STYLES["primary"])
		

class ButtonSuccess(ButtonDefault):
	def __init__(self, parent, *args, **kwargs):
		super(ButtonSuccess, self).__init__(parent, *args, **kwargs)

		self.set_my_style(STYLES["success"])


class ButtonInfo(ButtonDefault):
	def __init__(self, parent, *args, **kwargs):
		super(ButtonInfo, self).__init__(parent, *args, **kwargs)

		self.set_my_style(STYLES["info"])


class ButtonWarning(ButtonDefault):
	def __init__(self, parent, *args, **kwargs):
		super(ButtonWarning, self).__init__(parent, *args, **kwargs)

		self.set_my_style(STYLES["warning"])


class ButtonError(ButtonDefault):
	def __init__(self, parent, *args, **kwargs):
		super(ButtonError, self).__init__(parent, *args, **kwargs)

		self.set_my_style(STYLES["error"])