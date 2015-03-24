#!/usr/bin/env python2
# -*- coding: utf-8 -*-

import sys
from PySide import QtGui
import viztoolbar
import vizmenubar


class MainScreen(QtGui.QMainWindow):
    """
    UI class for the main screen, that will host the graphs and functionality for uploading data
    """

    def __init__(self, controller):
        """
        __init__
        Description: Creates an instance of MainScreen.
        Input:
        controller (Controller instance) initialized instance of the controller
        """
        super(MainScreen, self).__init__()

        self.controller = controller

        # Set up the initial UI
        self.init_ui()

    def init_ui(self):

        self.setup_actions()
        
        # add status bar
        self.statusBar()

        # create the menu bar, by default on Mac OS it is in top menu bar
        self.menubar = vizmenubar.VizMenuBar(self)
        
        # add the toolbar
        self.toolbar = viztoolbar.VizToolBar(self)

        # window props
        self.setWindowTitle('Data Visualization')
        self.showMaximized()   

    def setup_actions(self):

        # set up exit action and its properties
        self.exit_action = QtGui.QAction(QtGui.QIcon('ui/ui_assets/run.png'), '&XLStoCSV', self)
        self.exit_action.setShortcut('Ctrl+Q')
        self.exit_action.setStatusTip('XLStoCSV')
        self.exit_action.triggered.connect(self.close)

        # set up open file action and its properties
        self.open_file_action = QtGui.QAction(QtGui.QIcon('ui/ui_assets/open.png'), 'Open', self)
        self.open_file_action.setShortcut('Ctrl+O')
        self.open_file_action.setStatusTip('Open new file')
        self.open_file_action.triggered.connect(use_open_file_dialog(self, self.controller.import_file_to_database))

        self.save_file_action = QtGui.QAction(QtGui.QIcon('ui/ui_assets/save.png'), 'Save', self)
        self.save_file_action.setShortcut('Ctrl+S')
        self.save_file_action.setStatusTip('Save current file')
        self.save_file_action.triggered.connect(use_open_file_dialog(self, self.controller.import_file_to_database)) # need to refactor

# ----------------------------------------------------------------------------
# Other functions
# ----------------------------------------------------------------------------

def use_open_file_dialog(window, function_to_pass_filename):
    """
    showOpenFileDialog
    Description: returns a function that is able to open the file dialog, and then pass
    the filename returned to another function that can do something with the filename.
    This abstraction is done because we may need to trigger an open a file dialog for a lot of things,
    but what we do with that file may be different, so we want to allow ourselves to open
    a file, but call a different action after that.  The returned function is what the
    QT triggered.connect() method needs
    Input:
    window (QtGui.QtMainWindow) the window that the open file dialog originates from
    function_to_pass_filename (function) a function that has 1 parameter for a file path
    ending with the filename
    Output: (function) function that opens a file dialog, then calls a unique function that
    does something with a filename
    """
    def filename_handler():
        # show the open file dialog and get the filename
        filename, _ = QtGui.QFileDialog.getOpenFileName(window, 'Open file', '~/')
        # call the unique function that does something with the filename
        function_to_pass_filename(filename)

    return filename_handler
