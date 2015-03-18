#!/usr/bin/env python2

"""
The entry point for the application.  Starts the UI.
"""

import sys
from PySide import QtGui

from Controller.controller import Controller
from UI.mainui import MainScreen


def main():
    # Initialize the controller
    main_controller = Controller()

    application = QtGui.QApplication(sys.argv)
    # Initialize the MainScreen (main window of the UI) and pass it our controller
    this_screen = MainScreen(main_controller)
    sys.exit(application.exec_())


if __name__ == '__main__':
    main()
