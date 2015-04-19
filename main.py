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
    #main_controller.import_file_to_database('Output_20274_Training_D1_.xlsx')
    #main_controller.import_file_to_database('Output_40323_Training_D1_.xlsx')

    application = QtGui.QApplication(sys.argv)
    # Initialize the MainScreen (main window of the UI) and pass it our controller
    this_screen = MainScreen(main_controller)

    ### This commented out code shows how perform a simple database query
    #all_data = main_controller.retrieve_graph_data('b1','b2','b3')

    sys.exit(application.exec_())




if __name__ == '__main__':
    main()
