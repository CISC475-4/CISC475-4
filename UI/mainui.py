#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
sys.path.append("../")
from PySide import QtGui


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
        # TODO: Separate out components of UI in classes or separate functions. e.g. separate toolbar

        # set up exit action and its properties
        exit_action = QtGui.QAction(QtGui.QIcon('ui_assets/run.png'), '&XLStoCSV', self)
        exit_action.setShortcut('Ctrl+Q')
        exit_action.setStatusTip('Run Kelly\'s Script')
        exit_action.triggered.connect(self.close)

        # set up open file action and its properties
        open_file_action = QtGui.QAction(QtGui.QIcon('ui_assets/open.png'), 'Open', self)
        open_file_action.setShortcut('Ctrl+O')
        open_file_action.setStatusTip('Open new File')
        open_file_action.triggered.connect(use_open_file_dialog(self, self.controller.import_file_to_database))

        # add status bar
        self.statusBar()

        # create the menu bar, by default on Mac OS it is in top menu bar
        menubar = self.menuBar()
        file_menu = menubar.addMenu('&File')
        file_menu.addAction(exit_action)

        # add the toolbar and stick action on it
        toolbar = self.addToolBar('XLStoCSV')
        toolbar.addAction(exit_action)
        toolbar.addAction(open_file_action)

        # window props
        self.setWindowTitle('Data Visualization')
        self.showMaximized()

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
