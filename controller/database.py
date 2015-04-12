#!/usr/bin/env python2
import utility.file_utility
import sqlite3
import os
import sys

'''Database Wrapper Class
Responsible for all interactions with the embedded sqlite3 DB
'''

'''
Jamie's notes
can we use a connection.create_aggregate() for certain things?
should replace the loading code with a 'cur.executemany' call that loops with her iter
'''

class DatabaseManager(object):
    # if you're setting the address or timeout, USE NAMED PARAMS
    def __init__(self, address=':memory:', timeout=2):
        self.address = address
        self.sql_conn = None
        self.timeout = timeout

    def connect(self):
        self.sql_conn = sqlite3.connect(self.address)
        self.sql_conn.text_factory = str
        return self.sql_conn.cursor()

    def disconnect(self):
        self.sql_conn.commit()
        self.sql_conn.close()

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
        datasets = utility.file_utility.get_data_from_xls(filename) # tuple of DataSet objects
        cur = self.connect()
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
        self.disconnect()

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
