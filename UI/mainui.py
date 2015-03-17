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
        exit_action = QtGui.QAction(QtGui.QIcon('ui_assets/run.png'), '&XLStoCSV', self)
        exit_action.setShortcut('Ctrl+Q')
        exit_action.setStatusTip('Run Kelly\'s Script')
        exit_action.triggered.connect(self.close)

        # set up open file action and its props
        open_file_action = QtGui.QAction(QtGui.QIcon('ui_assets/open.png'), 'Open', self)
        open_file_action.setShortcut('Ctrl+O')
        open_file_action.setStatusTip('Open new File')
        open_file_action.triggered.connect(self.showOpenFileDialog)
 
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
        
    def showOpenFileDialog(self):

        file_name, _ = QtGui.QFileDialog.getOpenFileName(self, 'Open file',
                    '~/')
        
        f = open(file_name)
        print(f.name)
        
        # this is where we will need to send the retrieved path to Matt's script

def main():
    
    application = QtGui.QApplication(sys.argv)
    this_screen = MainScreen()
    sys.exit(application.exec_())


if __name__ == '__main__':
    main()