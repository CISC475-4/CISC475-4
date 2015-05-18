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
        """
        set-up the qt elements on the main graph window
        """
        self.layout = QtGui.QVBoxLayout(self.window.main_widget)
        self.layout.setContentsMargins(0,0,0,0)

        seek_layout = QtGui.QHBoxLayout(self.window.main_widget)
        self.seek_slider = QtGui.QSlider(QtCore.Qt.Horizontal, self.window.main_widget)
        self.seek_slider.setGeometry(30, 40, 100, 30)

        seek_label = QtGui.QLabel(' Seek\t', self.window)

        seek_layout.addWidget(seek_label)
        seek_layout.addWidget(self.seek_slider)
        self.layout.addLayout(seek_layout)

        zoom_layout = QtGui.QHBoxLayout(self.window.main_widget)
        self.zoom_slider = QtGui.QSlider(QtCore.Qt.Horizontal, self.window.main_widget)
        self.zoom_slider.setGeometry(30, 40, 100, 30)
        zoom_label = QtGui.QLabel(' Zoom\t', self.window)

        zoom_layout.addWidget(zoom_label)
        zoom_layout.addWidget(self.zoom_slider)
        self.layout.addLayout(zoom_layout)

        self.layout.addStretch()

        self.window.main_widget.setFocus()
        self.window.setCentralWidget(self.window.main_widget)

    def add_graph_with_ids(self, child_id, session_id, behavior_id, color):
        """
        adds a graph to the window
        child_id:    (string) id for a child
        session_id:  (string) id for a session that the child attended
        behavior_id: (string) id for a behavior in the selected session
        color:       (string) the name of a matplotlib color map - see http://matplotlib.org/examples/color/colormaps_reference.html
        """
        behavior_data = self.window.controller.get_behaviors_for_child([behavior_id], child_id, session_id)
        b = []
        for i in behavior_data:
            b.append(i[1])
        self.add_graph(b, child_id, session_id, behavior_id, color)

    def add_multisystem_graph(self, child_id, session_id, color):
        """
        sum all behaviors into one and display it as a graph
        child_id:    (string) id for a child
        session_id:  (string) id for a session that the child attended
        color:       (string) the name of a matplotlib color map - see http://matplotlib.org/examples/color/colormaps_reference.html
        """

        behaviors = self.window.controller.get_behavior_types(child_id, session_id)
        num_behaviors = len(behaviors)
        behavior_data = self.window.controller.get_behaviors_for_child(behaviors, child_id, session_id)
        b = []
        for i in range(0, len(behavior_data), num_behaviors):
            total = 0
            for pair in range(0, num_behaviors):
                total += behavior_data[i + pair][1]
            b.append(total)
        self.add_graph(b, child_id, session_id, 'multi system', color)

    def add_graph(self, behavior_data, child_id_label="N/A", session_id_label="N/A", behavior_label="N/A", color="cool"):
        """
        add a graph to the window using a array of behavor data
        behavior_data:    (array of integers) data that represents the behavior(s) of a child in a session
        child_id_label:   (string) used to label the graph
        session_id_label: (string) used to label the graph
        behavior_label:   (string) used to label the graph
        color:            (string) the name of a matplotlib color map - see http://matplotlib.org/examples/color/colormaps_reference.html
        """
        
        # Outer layout for graph
        bar_layout = QtGui.QHBoxLayout()

        # add labels
        label_layout = QtGui.QVBoxLayout()
        child_id_label_qt = QtGui.QLabel('Child ID: %s' % child_id_label, self.window) 
        session_id_label_qt = QtGui.QLabel('Session ID: %s' % session_id_label, self.window)
        if behavior_label == 'multi system':
            behavior_label_qt = QtGui.QLabel('Multi System', self.window)
        else:
            behavior_label_qt = QtGui.QLabel('Behavior(s): %s' % behavior_label, self.window)

        label_layout.addWidget(child_id_label_qt)
        label_layout.addWidget(session_id_label_qt)
        label_layout.addWidget(behavior_label_qt)

        bar_layout.addLayout(label_layout)
        # add graph
        graph = ColorBarCanvas(behavior_data, color, self.window.main_widget, width=5, height=4, dpi=100)
        graph.set_seek_slider(self.seek_slider)
        graph.set_zoom_slider(self.zoom_slider)
        bar_layout.addWidget(graph)



        button_layout = QtGui.QVBoxLayout()

        # add close button
        close_btn = QtGui.QPushButton('X')
        button_layout.addWidget(close_btn)

        #add key button
        key_btn = QtGui.QPushButton('Show Key')
        button_layout.addWidget(key_btn)

        bar_layout.addLayout(button_layout)

        self.layout.addLayout(bar_layout)

        # Delete functionality
        close_btn.clicked.connect(
            lambda: self.delete_graph(
                close_btn, 
                key_btn,
                graph, 
                [ 
                    child_id_label_qt,
                    session_id_label_qt,
                    behavior_label_qt
                ]
            )
        )

        key_btn.clicked.connect(lambda: self.show_key(min(behavior_data), max(behavior_data), color))

    def show_key(self, min_val, max_val, color):
        """
        Show a dialog box with a pyplot displaying a color key (legend)
        min_val: (int) the smallest integer in the graph's behavior_data
        max_val: (int) the largest integer in the graph's behavior_data
        color:   (string) the name of a matplotlib color map - see http://matplotlib.org/examples/color/colormaps_reference.html
        """
        fig = pyplot.figure(figsize=(5,1))
        fig.canvas.set_window_title('Key')
        fig.canvas.toolbar.hide()
        ax1 = fig.add_axes([0.05, 0.2, 0.9, 0.7])
        cmap = pyplot.get_cmap(color)
        norm = mpl.colors.Normalize(vmin=min_val, vmax=max_val)
        cb1 = mpl.colorbar.ColorbarBase(ax1, cmap=cmap,
            norm=norm,
            orientation='horizontal')
        cb1.set_cmap(color)
        pyplot.show()

    def delete_graph(self, close_btn, key_btn, graph, labels):
        """
        Remove a graph and its related buttons and labels
        close_btn: (qt_widget) the close button
        key_btn:   (qt_widget) the show color key button
        graph:     (qt_widget) the graph
        labels:    (qt_widget array) an array of label widgets associated with the graph
        """
        close_btn.hide()
        close_btn.deleteLater()
        key_btn.hide()
        key_btn.deleteLater()
        graph.hide()
        graph.deleteLater()
        for label in labels:
            label.hide()
            label.deleteLater()





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

    def __init__(self, dataset, color, *args, **kwargs):
        """
        dataset:    (array of integers) data that represents the behavior(s) of a child in a session
        color:            (string) the name of a matplotlib color map - see http://matplotlib.org/examples/color/colormaps_reference.html
        """
        self.dataset = dataset
        self.graph_color = color
        MyMplCanvas.__init__(self, *args, **kwargs)

    def set_seek_slider(self, seek_slider):
        """
        give the graph a link to the seek slider
        """
        self.seek_slider = seek_slider
        self.seek_slider.valueChanged.connect(self.redraw)

    def set_zoom_slider(self, zoom_slider):
        """
        give the graph a link to the zoom slider
        """
        self.zoom_slider = zoom_slider
        self.zoom_slider.valueChanged.connect(self.redraw)

    def compute_initial_figure(self):
        """
        set-up the inital color list that links the behavior data to a color on the color bar
        add the color bar to the MplCanvas
        """
        data_min = min(self.dataset)
        data_max = max(self.dataset)
        self.data_range = data_max - data_min + 1 
        self.colors = []

        color_map = mpl.cm.ScalarMappable(mpl.colors.Normalize(data_min, data_max))
        color_map.set_cmap(self.graph_color)
        
        for i in range(0, self.data_range):
            color_tuple = color_map.to_rgba(i)
            self.colors.append([color_tuple[0], color_tuple[1], color_tuple[2]])

        self.color_list = []
        for i in self.dataset: 
            self.color_list.append(self.colors[i - data_min])

        self.cmap = mpl.colors.ListedColormap(self.color_list)
        self.cmap.set_over((1., 0., 0.))
        self.cmap.set_under((0., 0., 1.))
        # bounds will be the timestamps
        bounds = range(0, len(self.dataset))
        norm = mpl.colors.BoundaryNorm(bounds, self.cmap.N)
        self.colorbar = mpl.colorbar.ColorbarBase(self.axes, cmap=self.cmap,
                                   norm=norm,
                                   boundaries=bounds,
                                   orientation='horizontal')

    def redraw(self):
        """
        called when a slider's value is updated
        recalculates what portion of each graph to show
        """
        zoom = self.zoom_slider.value()
        seek = self.seek_slider.value()
        total_len = len(self.color_list)
        percent_viewed =  ((100 - zoom) / 100.0) ** 2
        window_size = int(total_len * percent_viewed)

        window_start = int((total_len - window_size) * (seek / 99.0))
        bounds = range(window_start, window_start + window_size)
        self.colorbar.boundaries = bounds
        self.draw()
        self.colorbar.draw_all()

