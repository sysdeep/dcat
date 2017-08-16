#!/usr/bin/env python
# -*- coding: utf-8 -*-


from .guitk import MainWindow


class Application(object):
    def __init__(self):


        self.gui = MainWindow()


    def start(self):
        self.gui.mainloop()
