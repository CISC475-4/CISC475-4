#!/usr/bin/env python2
import utility.file_utility
import database

"""
Controller Class for the application.
"""

class Controller:

    def __init__(self):
        self.db = database.DatabaseManager()
        self.db.connect() # this creates the cursor object

    def setup_db(self):
        # if the schema has already been loaded, don't perform the init operation
        if not self.db.check_db_setup():
            self.db.setup()

    def import_file_to_database(self, filename):
        self.db.import_file_to_database(filename)

    # TODO: Do we need to specify whether or not we want time data?
    def retrieve_graph_data(self, x_label, y_label, z_label):
        """
        retrieve_graph_data
        Description: by default, retrieve all data from Chunk tabel. No with no constraints
        """
        cursor = self.db.sql_conn.cursor()
        cursor.execute("SELECT " + x_label + "," + y_label + "," + z_label + "  FROM Chunk")  
        return cursor.fetchall() #a list of data rows


    #TODO: rename conditional_selects later
    def conditional_selects(select, conditions):
        '''
        considering select statements requesting certain conditions
        select - a list of columns we want all row data from
        conditions - a dictionary of columns mapped to a list of values 
        '''
        pass
