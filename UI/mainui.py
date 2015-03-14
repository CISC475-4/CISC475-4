#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
from PySide import QtGui

class Example(QtGui.QMainWindow):
    
    def __init__(self):
        super(Example, self).__init__()
        
        self.initUI()
        
    def initUI(self):               

        exitAction = QtGui.QAction(QtGui.QIcon('run.png'), '&XLStoCSV', self)
        exitAction.setShortcut('Ctrl+Q')
        exitAction.setStatusTip('Run Kelly\'s Script')
        exitAction.triggered.connect(self.close)

        self.statusBar()

        menubar = self.menuBar()
        fileMenu = menubar.addMenu('&File')
        fileMenu.addAction(exitAction)

        toolbar = self.addToolBar('XLStoCSV')
        toolbar.addAction(exitAction)
        
        self.setGeometry(300, 300, 700, 500)
        self.setWindowTitle('Data Visualization')    
        self.show()
        
        
def main():
    
    app = QtGui.QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()