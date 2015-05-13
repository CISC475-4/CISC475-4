#!/usr/bin/env python2
# -*- coding: utf-8 -*-

import sys
from PySide import QtGui

class VizToolBar():
    """
    Class for modifying the toolbar of our Main UI, broken up to increase cohesion of our UI components
    """
    def __init__(self, window):
        self.window = window
        self.init_toolbar()

    def init_toolbar(self):
        self.toolbar = self.window.addToolBar('main_toolbar')
        self.toolbar.addAction(self.window.open_file_action)
        self.toolbar.addAction(self.window.add_graph_action)
        # self.toolbar.addAction(self.window.export_action)

