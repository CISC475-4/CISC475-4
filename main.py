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

    # Added argument parsing so we can optionally do utility tasks from the command-line
    p = argparse.ArgumentParser(description='run the application with different behavior')
    p.add_argument('-i', '--import-file', help='import file to database')
    p.add_argument('-r', '--reset-db', help='recreate the DB fresh', action='store_true')
    p.add_argument('-t', '--tests', help='run all our nosetests', action='store_true')
    args = p.parse_args()
    if args.tests:
        import nose
        # ok yeah reassigning argv is hacky, but it allows tests to run. trust me. -j
        sys.argv = sys.argv[:1]
        nose.main()
    else:
        # Initialize the controller
        with Controller() as main_controller:
            if args.import_file:
                main_controller.import_file_to_database(args.import_file)
            elif args.reset_db:
                main_controller.reset_db()
            else:
                application = QtGui.QApplication(sys.argv)
                # Initialize the MainScreen (main window of the UI) and pass it our controller
                this_screen = MainScreen(main_controller)

                ### This commented out code shows how perform a simple database query

                ### The following displays the current query repertoire

                # k's database testing stuff
                #avg_bh = main_controller.get_avg_behavior('b1', 20274) #works
                #bh = main_controller.get_behaviors_for_child(['b1','b2'],20274,1)
                #types = main_controller.get_behavior_types(20274)

                sys.exit(application.exec_())

if __name__ == '__main__':
    main()
