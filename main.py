#!/usr/bin/env python2

"""
Starting point for the application.
"""

import sys
from PySide import QtGui
import logging
from controller.controller import Controller
from ui.mainui import MainScreen
import argparse

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

    # Added argument parsing so we can optionally do utility tasks from the command-line
    p = argparse.ArgumentParser(description='run the application with different behavior')
    p.add_argument('-i', '--import-file', help='import file to database')
    args = p.parse_args()
    if args.import_file:
        main_controller.import_file_to_database(args.import_file)

    application = QtGui.QApplication(sys.argv)
    # Initialize the MainScreen (main window of the UI) and pass it our controller
    this_screen = MainScreen(main_controller)

    ### This commented out code shows how perform a simple database query

    ### The following displays the current query repertoire

    sys.exit(application.exec_())

if __name__ == '__main__':
    main()
