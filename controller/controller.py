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
        datasets = file_utility.get_data_from_xls(filename) # tuple of DataSet objects
        if self.db is None:
            self.db_connect()
        cur = self.db.cursor()
        # iterate through dataset rows and insert
        # 1. Insert new row in Session
        allgroup = datasets[0] # all group data goes here
        session_insert = "INSERT INTO Session values('{cid}','{sid}')".format(cid=allgroup.child_id,sid=allgroup.session_id)
        cur.execute(session_insert)
        # 2. Insert new Session_Meta
        meta_insert = "INSERT INTO Session_Meta values('{cid}','{sid}','{time_load}','{time_mod}','{filename}')".format(cid=allgroup.child_id, sid=allgroup.session_id, time_load=allgroup.time_accessed, time_mod=allgroup.time_accessed, filename=allgroup.file_name)
        cur.execute(meta_insert)
        # 3. Insert new GroupData
        for record in allgroup.get_next_instance():
            combo_insert = "INSERT INTO GroupData values('{cid}','{sid}','{combo_index}','{duration}','{num_chunks}','{cad}','{cmd}','{rpc}','{rps}')".format(cid=allgroup.child_id, sid=allgroup.session_id, combo_index=record['INDEX'], duration=record['DURATION'], num_chunks=record['NUM-CHUNKS'], cad=record['CHUNK-AVG-DUR'], cmd=record['CHUNK-MAX-DUR'], rpc=record['CHUNK-RATE(CHUNK-DUR)'], rps=record['CHUNK-RATE(TOTAL-DUR)'])
            cur.execute(combo_insert)
        # 4. Iterate through rows and insert into Chunk
        timeseries = datasets[2]
        for record in timeseries.get_next_instance():
            chunk_insert = "INSERT INTO Chunk values('{cid}','{sid}','{exp_time}','{b1}','{b2}','{b3}')".format(cid=timeseries.child_id, sid=timeseries.session_id, exp_time=record['TIME [SEC]'], b1=record['BEHAV 1 LEVEL'], b2=record['BEHAV 2 LEVEL'], b3=record['BEHAV 3 LEVEL'])
            cur.execute(chunk_insert)
        self.db.commit()
        self.db.close()

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
