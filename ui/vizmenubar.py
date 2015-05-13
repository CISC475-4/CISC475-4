#!/usr/bin/env python2
# -*- coding: utf-8 -*-

import sys
from PySide import QtGui

class VizMenuBar():
    """
    Class for modifying the menubar of our Main UI, broken up to increase cohesion of our UI components
    """
    def __init__(self, window):
        self.window = window
        self.init_menubar()

    def init_menubar(self):
        # add a menu bar
        self.menubar = self.window.menuBar()

        # make an actions menu
        action_menu = self.menubar.addMenu('&Actions')
        # add open file action
        action_menu.addAction(self.window.open_file_action)
        # add add graph action
        action_menu.addAction(self.window.add_graph_action)

        # make a database menu
        database_menu = self.menubar.addMenu('&Database')
        # add clear database action
        database_menu.addAction(self.window.clear_database_action)
        

        # action_menu.addAction(self.window.export_action)