#!/usr/bin/env python3
# -*- coding: utf-8 -*-


#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import tkinter
from tkinter import ttk

from app.guitk.utils import ticons
from app import shared

from .FrameHistory import FrameHistory
from .FrameStyle import FrameStyle


class Settings(tkinter.Toplevel):
	def __init__(self, master=None, *args, **kwargs):
		super(Settings, self).__init__(master, *args, **kwargs)
		self.title("Настройкие")

		self.maxsize(400, 300)
		self.minsize(400, 300)


		self.usettings = shared.get_usettings()


		self.main_frame = ttk.Frame(self, padding=10)
		self.main_frame.pack(expand=True, fill="both", side="top")



		self.tabs = ttk.Notebook(self.main_frame)
		self.tabs.pack(fill="both", expand=True)



		self.frame_history = FrameHistory(self.tabs, self.usettings)
		self.tabs.add(self.frame_history, text="История")

		self.frame_style = FrameStyle(self.tabs)
		self.tabs.add(self.frame_style, text="Стиль")





		#--- controls
		controls_frame = ttk.Frame(self.main_frame)
		controls_frame.pack(fill="both", side="bottom", padx=5, pady=5)

		ttk.Button(controls_frame, text="Закрыть(Ctrl+w)", command=self.destroy, image=ticons.ticon(ticons.CLOSE), compound="left").pack(side="right")

		ttk.Button(controls_frame, text="Сохранить", command=self.apply, image=ticons.ticon(ticons.SAVE), compound="left").pack(side="left")

		self.bind_all("<Control-w>", lambda e: self.destroy())




	def apply(self):

		self.frame_history.apply()
		self.frame_style.apply()

		self.usettings.save()










if __name__ == "__main__":


	root = tkinter.Tk()

	modal = Settings(root)
	ttk.Button(root, text="quit", command=quit).pack()

	root.mainloop()