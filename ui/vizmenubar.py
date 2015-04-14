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
        self.menubar = self.window.menuBar()
        action_menu = self.menubar.addMenu('&Actions')
        action_menu.addAction(self.window.exit_action)
        action_menu.addAction(self.window.open_file_action)
        action_menu.addAction(self.window.export_action)