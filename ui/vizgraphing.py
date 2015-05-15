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
import random #included to create test data TODO remove when not used

class VizGraphing():
    """
    Class for setting up the matplotlib graphs for the user_interfaces
    """

    def __init__(self, window):
        self.window = window
        self.init_graphs() 

    def init_graphs(self):
        # testdata = self.window.controller.get_behaviors_for_child(['b1'], '20274')
        b1 = []
        # for i in testdata:
        #     b1.append(i[0])

        self.layout = QtGui.QVBoxLayout(self.window.main_widget)
        self.layout.setContentsMargins(0,0,0,0)

        self.seek_slider = QtGui.QSlider(QtCore.Qt.Horizontal, self.window.main_widget)
        self.seek_slider.setGeometry(30, 40, 100, 30)
        self.layout.addWidget(self.seek_slider)

        self.zoom_slider = QtGui.QSlider(QtCore.Qt.Horizontal, self.window.main_widget)
        self.zoom_slider.setGeometry(30, 40, 100, 30)
        self.layout.addWidget(self.zoom_slider)

        # btn = QtGui.QPushButton('Test Button', self.window.main_widget)
        # btn.clicked.connect(lambda: self.add_graph(b1))
        # self.layout.addWidget(btn)

        self.layout.addStretch()

        self.window.main_widget.setFocus()
        self.window.setCentralWidget(self.window.main_widget)

    def add_graph(self, behavior):
        bar_layout = QtGui.QHBoxLayout()

        btn = QtGui.QPushButton('X')
        #btn.clicked.connect(ChildLayout)
        bar_layout.addWidget(btn)

        sc = ColorBarCanvas(behavior, self.window.main_widget, width=5, height=4, dpi=100)
        sc.set_seek_slider(self.seek_slider)
        sc.set_zoom_slider(self.zoom_slider)
        bar_layout.addWidget(sc)
        self.layout.addLayout(bar_layout)




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


# copied from http://matplotlib.org/examples/user_interfaces/embedding_in_qt4.html
class ColorBarCanvas(MyMplCanvas):

    def __init__(self, dataset, *args, **kwargs):
        self.dataset = dataset
        MyMplCanvas.__init__(self, *args, **kwargs)

    def set_seek_slider(self, seek_slider):
        self.seek_slider = seek_slider
        self.seek_slider.valueChanged.connect(self.redraw)

    def set_zoom_slider(self, zoom_slider):
        self.zoom_slider = zoom_slider
        self.zoom_slider.valueChanged.connect(self.redraw)

    """Simple canvas with a sine plot."""
    def compute_initial_figure(self):
        # The four colors in order from left to right
        # cmap will hold the data
        #self.test_data = [int(10*random.random()) for i in xrange(10000)]
        #self.test_data = range(0, 1000)
        self.test_data = self.dataset
        data_min = min(self.test_data)
        data_max = max(self.test_data)
        self.data_range = data_max - data_min + 1 # possible efficiency problem
        self.colors = []
        for i in range(0, self.data_range):
            #self.colors.append([0., .4, i / float(self.data_range)])
            self.colors.append([i / float(self.data_range), 1 - (i / float(self.data_range)), .4])

        self.color_list = []
        for i in self.test_data: 
            self.color_list.append(self.colors[i - data_min])

        self.cmap = mpl.colors.ListedColormap(self.color_list)
        self.cmap.set_over((1., 0., 0.))
        self.cmap.set_under((0., 0., 1.))
        # bounds will be the timestamps
        bounds = range(0, len(self.test_data))
        norm = mpl.colors.BoundaryNorm(bounds, self.cmap.N)
        self.colorbar = mpl.colorbar.ColorbarBase(self.axes, cmap=self.cmap,
                                   norm=norm,
                                   boundaries=bounds,
                                   orientation='horizontal')

    def redraw(self):
        window_size = 100 * (self.zoom_slider.value() / 10.0)
        window_size = int(window_size)

        if window_size == 0:
            window_size = 10
        if window_size > len(self.color_list) or self.zoom_slider.value() == 99:
            window_size = len(self.color_list)

        window_start = int((len(self.color_list) - window_size) * self.seek_slider.value() / 99.0)
        bounds = range(window_start, window_start + window_size)
        self.colorbar.boundaries = bounds
        self.draw()
        self.colorbar.draw_all()

