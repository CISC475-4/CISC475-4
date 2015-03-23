#!/usr/bin/env python2
# -*- coding: utf-8 -*-

import sys
import random
from PySide import QtGui, QtCore
import viztoolbar
import vizmenubar
from numpy import arange, sin, pi
import matplotlib
matplotlib.use('Qt4Agg')
matplotlib.rcParams['backend.qt4']='PySide'
from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

# copied from http://matplotlib.org/examples/user_interfaces/embedding_in_qt4.html
class MyMplCanvas(FigureCanvas):
    """Ultimately, this is a QWidget (as well as a FigureCanvasAgg, etc.)."""
    def __init__(self, parent=None, width=5, height=4, dpi=100):
        fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = fig.add_subplot(111)
        # We want the axes cleared every time plot() is called
        self.axes.hold(False)

        self.compute_initial_figure()

        #
        FigureCanvas.__init__(self, fig)
        self.setParent(parent)

        FigureCanvas.setSizePolicy(self,
                                   QtGui.QSizePolicy.Expanding,
                                   QtGui.QSizePolicy.Expanding)
        FigureCanvas.updateGeometry(self)

    def compute_initial_figure(self):
        pass


# copied from http://matplotlib.org/examples/user_interfaces/embedding_in_qt4.html
class MyStaticMplCanvas(MyMplCanvas):
    """Simple canvas with a sine plot."""
    def compute_initial_figure(self):
        t = arange(0.0, 3.0, 0.01)
        s = sin(2*pi*t)
        self.axes.plot(t, s)


# copied from http://matplotlib.org/examples/user_interfaces/embedding_in_qt4.html
class MyDynamicMplCanvas(MyMplCanvas):
    """A canvas that updates itself every second with a new plot."""
    def __init__(self, *args, **kwargs):
        MyMplCanvas.__init__(self, *args, **kwargs)
        timer = QtCore.QTimer(self)
        timer.timeout.connect(self.update_figure)
        timer.start(1000)

    def compute_initial_figure(self):
        self.axes.plot([0, 1, 2, 3], [1, 2, 0, 4], 'r')

    def update_figure(self):
        # Build a list of 4 random integers between 0 and 10 (both inclusive)
        l = [random.randint(0, 10) for i in range(4)]

        self.axes.plot([0, 1, 2, 3], l, 'r')
        self.draw()


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
        self.main_widget = QtGui.QWidget(self)

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


        # set-up matplotlib canvas
        l = QtGui.QVBoxLayout(self.main_widget)
        sc = MyStaticMplCanvas(self.main_widget, width=5, height=4, dpi=100)
        dc = MyDynamicMplCanvas(self.main_widget, width=5, height=4, dpi=100)
        l.addWidget(sc)
        l.addWidget(dc)

        self.main_widget.setFocus()
        self.setCentralWidget(self.main_widget)

    def setup_actions(self):

        # set up exit action and its properties
        self.exit_action = QtGui.QAction(QtGui.QIcon('ui/ui_assets/run.png'), '&XLStoCSV', self)
        self.exit_action.setShortcut('Ctrl+Q')
        self.exit_action.setStatusTip('Run Kelly\'s Script')
        self.exit_action.triggered.connect(self.close)

        # set up open file action and its properties
        self.open_file_action = QtGui.QAction(QtGui.QIcon('ui/ui_assets/open.png'), 'Open', self)
        self.open_file_action.setShortcut('Ctrl+O')
        self.open_file_action.setStatusTip('Open new File')
        self.open_file_action.triggered.connect(use_open_file_dialog(self, self.controller.import_file_to_database))     

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
