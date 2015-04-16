#!/usr/bin/env python2
import utility.file_utility
import database
import logging


class Controller:
    """
    The Controller class in an MVC Framework.  This class is meant to handle
    interactions between the UI and the backend (i.e. Data/Model).
    """

    def __init__(self):
        """
        Initializes the controller.  Creates an instance of the database.
        """
        self.db = database.DatabaseManager()
        self.db.connect()  # this creates the cursor object

    def setup_db(self):
        """
        TODO: write function header
        """
        # TODO: Answer why this can't be called in the DatabaseManager initialization
        # if the schema has already been loaded, don't perform the init operation
        if not self.db.check_db_setup():
            self.db.setup()

    def import_file_to_database(self, filename):
        """
        Given a full file path, imports that file into the database.

        input:
            filename (string) path and filename of the file
        """
        try:
            self.db.import_file_to_database(filename)
        # except IOError as e:
        #     logging.error(e)
        except Exception as e:
            # TODO: Get a modal to pop up in the UI displaying the error message
            logging.error(e)

    # TODO: Do we need to specify whether or not we want time data?
    def retrieve_graph_data(x_label, y_label, z_label):
        """
        TODO: write function header
        """
        pass
