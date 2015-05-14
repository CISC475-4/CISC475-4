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

    #application = QtGui.QApplication(sys.argv)
    # Initialize the MainScreen (main window of the UI) and pass it our controller
    #this_screen = MainScreen(main_controller)

    ### This commented out code shows how perform a simple database query
    #all_data = main_controller.retrieve_graph_data('b1','b2','b3')

    ### The following displays the current query repertoire
    child_ids = main_controller.get_all_child_ids()
    #session_ids = main_controller.get_all_sessions_for_child("20274")
    #tables_names = main_controller.get_table_names()
    #column_names = main_controller.get_columns_from_table("Session_Meta")
    #max_behaviors = main_controller.get_max_behavior(['b3', 'b2'], '20274', 1)
    #max_behaviors_with_time = main_controller.ax_behavior(['b3', 'b2'], '20274', 1, 10, 15)
    #range_behaviors = main_controller.get_behaviors_for_child(['b1','b2','b3'], '20274', 1, 10, 15, True)
    nonrange_behaviors = main_controller.get_behaviors_for_child(['b1','b2','b3'], '20274', 1)
    print nonrange_behaviors
    nonrange_behaviors = main_controller.get_behaviors_for_child(['b1','b2','b3'], '40323', 1)
    print nonrange_behaviors
    #combo_indices = main_controller.get_all_combo_indexes('20274','1')
    #combo_data = main_controller.get_group_data_by_combo_index(['*'], 13, 20274, 1)
    #num_chunks = main_controller.get_num_chunks(13, 20274, 1)
    #chunk_max_dur = main_controller.get_chunk_max_duration(13, 20274, 1)
    #chunk_avg_dur = main_controller.get_chunk_avg_duration(13, 20274, 1)

    #sys.exit(application.exec_())

if __name__ == '__main__':
    main()
