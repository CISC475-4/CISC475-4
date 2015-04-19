#!/usr/bin/env python2
# -*- coding: utf-8 -*-

import sys
from PySide import QtGui, QtCore
from numpy import arange, sin, pi
import matplotlib as mpl
mpl.use('Qt4Agg')
mpl.rcParams['backend.qt4']='PySide'
from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from matplotlib import pyplot


class VizGraphing():
    """
    Class for setting up the matplotlib graphs for the user_interfaces
    """

    def __init__(self, window):
        self.window = window
        self.init_graphs() 

    def init_graphs(self):
        # set-up matplotlib canvas
        l = QtGui.QVBoxLayout(self.window.main_widget)
        sc = MyStaticMplCanvas(self.window.main_widget, width=5, height=4, dpi=100)
        l.addWidget(sc)
        sc2 = MyStaticMplCanvas(self.window.main_widget, width=5, height=4, dpi=100)
        l.addWidget(sc2)
        sc3 = MyStaticMplCanvas(self.window.main_widget, width=5, height=4, dpi=100)
        l.addWidget(sc3)
        sc4 = MyStaticMplCanvas(self.window.main_widget, width=5, height=4, dpi=100)
        l.addWidget(sc4)

        self.window.main_widget.setFocus()
        self.window.setCentralWidget(self.window.main_widget)


# copied from http://matplotlib.org/examples/user_interfaces/embedding_in_qt4.html
class MyMplCanvas(FigureCanvas):
    """Ultimately, this is a QWidget (as well as a FigureCanvasAgg, etc.)."""
    def __init__(self, parent=None, width=5, height=4, dpi=100):
        self.fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = self.fig.add_subplot(111)
        # We want the axes cleared every time plot() is called
        self.axes.hold(False)

        self.compute_initial_figure()

        FigureCanvas.__init__(self, self.fig)
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
        # The four colors in order from left to right
        # cmap will hold the data
        cmap = mpl.colors.ListedColormap([[0., .4, 1.], [0., .8, 1.],
            [1., .8, 0.], [1., .4, 0.]])
        cmap.set_over((1., 0., 0.))
        cmap.set_under((0., 0., 1.))
        # bounds will be the timestamps
        bounds = [1, 2, 3, 4, 5]
        norm = mpl.colors.BoundaryNorm(bounds, cmap.N)
        colorbar = mpl.colorbar.ColorbarBase(self.axes, cmap=cmap,
                                   norm=norm,
                                   boundaries=bounds,
                                   orientation='horizontal')

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

