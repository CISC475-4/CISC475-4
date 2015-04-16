#!/usr/bin/env python2

"""
Starting point for the application.
"""

import sys
from PySide import QtGui
import logging
from controller.controller import Controller
from ui.mainui import MainScreen


def main():
    """
    Starting point for the application
    """
    # Set up log format and streams
    logging.basicConfig(
        format='%(asctime)s:%(filename)s:%(levelname)s:%(message)s',
        stream=sys.stderr,
        level=logging.INFO)

    # Initialize the controller
    main_controller = Controller()

    # This method sets up the DB and should therefore be called before any DB interactions
    main_controller.setup_db()

    application = QtGui.QApplication(sys.argv)
    # Initialize the MainScreen (main window of the UI) and pass it our controller
    this_screen = MainScreen(main_controller)
    sys.exit(application.exec_())


if __name__ == '__main__':
    main()
