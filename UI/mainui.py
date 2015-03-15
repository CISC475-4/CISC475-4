#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
import imp
from PySide import QtGui

"""
UI class for the main screen, that will host the graphs and functionality for uploading data
"""

class MainScreen(QtGui.QMainWindow):

    # not sure how to load using relative path yet, but kelly needs to add xlrd library anyway so commented for now
    # fu = imp.load_source('FileUtility.py', '/Users/brandontrautmann/GoogleDrive/development/cisc475/CISC475-4/Utility/FileUtility.py')
    # fu.XLStoCSV('Workbook1.xlsx')
    
    def __init__(self):
        super(MainScreen, self).__init__()
        
        self.initUI()
        
    def initUI(self):               

        # set up exit action and its props
        exitAction = QtGui.QAction(QtGui.QIcon('run.png'), '&XLStoCSV', self)
        exitAction.setShortcut('Ctrl+Q')
        exitAction.triggered.connect(self.close)
        
        # status for status bar
        exitAction.setStatusTip('Run Kelly\'s Script')
        self.statusBar()

        # create the menu bar, by default on Mac OS it is in top menu bar
        menubar = self.menuBar()
        fileMenu = menubar.addMenu('&File')
        fileMenu.addAction(exitAction)

        # add the toolbar and stick action on it
        toolbar = self.addToolBar('XLStoCSV')
        toolbar.addAction(exitAction)
        
        # window props
        self.setWindowTitle('Data Visualization')    
        self.showMaximized()
        
        
def main():
    
    app = QtGui.QApplication(sys.argv)
    ex = MainScreen()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()