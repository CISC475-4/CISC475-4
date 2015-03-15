#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
from PySide import QtGui

class Example(QtGui.QMainWindow):
    
    def __init__(self):
        super(Example, self).__init__()
        
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
        self.setGeometry(300, 300, 700, 500) # needs to not be hard-coded
        self.setWindowTitle('Data Visualization')    
        self.show()
        
        
def main():
    
    app = QtGui.QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()