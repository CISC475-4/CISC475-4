#!/usr/bin/env python2
import utility.file_utility
import controller.database
import sqlite3
import os
import sys

"""
Controller Class for the application.
"""

class Controller:

    def __init__(self):
        self.db = DatabaseManager()

    def import_file_to_database(self, filename):
        self.db.import_file_to_database(filename)

    # TODO: Do we need to specify whether or not we want time data?
    def retrieve_graph_data(x_label, y_label, z_label):
        """
        retrieve_graph_data
        Description:
        """
        pass
