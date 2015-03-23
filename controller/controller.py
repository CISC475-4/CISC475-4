#!/usr/bin/env python2
import utility.file_utility
import sqlite3
import os
import sys

"""
Controller Class for the application.
"""

class Controller:

    def __init__(self):
        self.db = None

    def db_connect(self):
        self.db = sqlite3.connect('')
        # Use bytestrings instead of Unicode in the results
        self.db.text_factory = str

    def import_file_to_database(self, filename):
        """
        import_file_to_database
        Description: Will take a filename and import the contents of the file into the DB
        Input: filename (string) the full path of the file
        Output: TODO
        """
        if not os.path.isfile(filename):
            print >> sys.stderr, "Controller: Error: Tried to import a nonexistent file"
            sys.exit(1)
        dataset = file_utility.get_data_from(filename)
        if self.db is None:
            self.db_connect()
        cur = self.db.cursor()
        # iterate through dataset rows and insert
        # 1. Insert new row in Session
        session_insert = "INSERT INTO Session values('{cid}','{sid}')".format(cid=dataset.child_id,sid=dataset.session_id)
        cur.execute(session_insert)
        # 2. Insert new Session_Meta
        meta_insert = "INSERT INTO Session_Meta values('{cid}','{sid}','{time_load}','{time_mod}','{filename}')".format(cid=dataset.child_id, sid=dataset.session_id, time_load=dataset.time_accessed, time_mod=dataset.time_accessed, filename=dataset.file_name)
        cur.execute(meta_insert)
        # 3. TODO: Insert new GroupData
        # 4. TODO: Iterate through rows and insert into Chunk
        self.db.commit()

    def import_excel_to_database(self, filename):
        """
        import_excel_to_database
        Description:
        """
        pass

    def import_csv_to_database(self, filename):
        """
        import_csv_to_database
        Description:
        """
        pass


    # TODO: Do we need to specify whether or not we want time data?
    def retrieve_graph_data(x_label, y_label, z_label):
        """
        retrieve_graph_data
        Description:
        """
        pass
