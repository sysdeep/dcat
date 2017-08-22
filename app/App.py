#!/usr/bin/env python
# -*- coding: utf-8 -*-


from .guitk import MainWindow
from app.rc import FILE_DB_TEST
from app.storage import get_storage



# storage = get_storage()
# storage.open_storage(FILE_DB_TEST)



class Application(object):
    def __init__(self):



        self.gui = MainWindow()


    def start(self):
        self.gui.mainloop()
