#!/usr/bin/env python2
import utility.file_utility
import sqlite3
import os
import sys

'''
Jamie's notes
can we use a connection.create_aggregate() for certain things?
should replace the loading code with a 'cur.executemany' call that loops with her iter
'''

''' Database Wrapper Class
Responsible for all interactions with the embedded sqlite3 DB
'''
class DatabaseManager(object):

    def __init__(self, address='data.sqlite3', timeout=2):
        ''' create a DatabaseManager class
        Must call connect() for use.
        if you're setting the address or timeout, USE NAMED PARAMS
        TODO: make this truly in memory instead of flushing to data.sqlite3
        '''
        self.address = address
        self.sql_conn = None
        self.cursor = None
        self.timeout = timeout

    def connect(self):
        ''' inits the cursor and sql_conn objects
        Should only be called once per program run
        '''
        self.sql_conn = sqlite3.connect(self.address)
        # Makes the output from cursor.fetch*() into 'Row' objects (like dicts)
        self.sql_conn.row_factory = sqlite3.Row
        # Use bytestrings instead of Unicode in the results
        self.sql_conn.text_factory = str
        self.cursor = self.sql_conn.cursor()

    def disconnect(self):
        ''' removes the connection to the database
        Should only be called once per program run
        '''
        self.sql_conn.commit()
        self.sql_conn.close()
        self.cursor = None

    def check_db_setup(self):
        ''' check to make sure that all tables exist in the database already
        Return: bool. True if the database has already been setup
        '''
        temp_conn = sqlite3.connect(self.address)
        temp_conn.text_factory = str
        temp_cur = temp_conn.cursor()
        existence = True
        tablenames = ['Chunk','Session','GroupData','Session_Meta']
        for table in tablenames:
            temp_cur.execute("SELECT name FROM sqlite_master WHERE type='table' and name='{tbl}'".format(tbl=table))
            potential = temp_cur.fetchone()
            if potential is not None:
                existence = (potential[0] == table) # if the 'Chunk' table exists, it is set up
            else:
                existence = False
        temp_conn.close()
        return existence

    def setup(self, sql_filename='controller/schemata/main.sql'):
        ''' reads in the initial database schema and creates all necessary tables
        Params: filename to load up. Default is the saved schema we already wrote
        '''
        with open(sql_filename, 'r') as schema:
            self.cursor.executescript(schema.read())  # catch 'em all
        changes = self.commit()
        print 'DatabaseManager: loaded schema {fn} successfully'.format(fn=sql_filename)

    def commit(self):
        ''' commits any pending changes and returns the total number of updated rows
        note that no rows will be updated on a CREATE TABLE operation, etc
        Return: number of rows updated
        '''
        self.sql_conn.commit()
        amt_changes = self.sql_conn.total_changes
        return amt_changes

    def import_file_to_database(self, filename):
        """
        Params: filename (string) the relative path of the file
        Return: none
        Will raise an exception or error if the data is already in the DB
        TODO: Exception handling for existing data
        """
        if not os.path.isfile(filename):
            print >> sys.stderr, "DatabaseManager: Error: Tried to import a nonexistent file"
            sys.exit(1)
        datasets = utility.file_utility.get_data_from_xls(filename) # tuple of DataSet objects
        # iterate through dataset rows and insert
        # 1. Insert new row in Session
        allgroup = datasets[0] # all group data goes here
        session_insert = "INSERT INTO Session values('{cid}','{sid}')".format(cid=allgroup.child_id,sid=allgroup.session_id)
        self.cursor.execute(session_insert)
        # 2. Insert new Session_Meta
        meta_insert = "INSERT INTO Session_Meta values('{cid}','{sid}','{time_load}','{time_mod}','{filename}')".format(cid=allgroup.child_id, sid=allgroup.session_id, time_load=allgroup.time_accessed, time_mod=allgroup.time_accessed, filename=allgroup.file_name)
        self.cursor.execute(meta_insert)
        # 3. Insert new GroupData
        for record in allgroup.get_next_instance():
            combo_insert = "INSERT INTO GroupData values('{cid}','{sid}','{combo_index}','{duration}','{num_chunks}','{cad}','{cmd}','{rpc}','{rps}')".format(cid=allgroup.child_id, sid=allgroup.session_id, combo_index=record['INDEX'], duration=record['DURATION'], num_chunks=record['NUM-CHUNKS'], cad=record['CHUNK-AVG-DUR'], cmd=record['CHUNK-MAX-DUR'], rpc=record['CHUNK-RATE(CHUNK-DUR)'], rps=record['CHUNK-RATE(TOTAL-DUR)'])
            self.cursor.execute(combo_insert)
        # 4. Iterate through rows and insert into Chunk
        timeseries = datasets[2]
        for record in timeseries.get_next_instance():
            chunk_insert = "INSERT INTO Chunk values('{cid}','{sid}','{exp_time}','{b1}','{b2}','{b3}')".format(cid=timeseries.child_id, sid=timeseries.session_id, exp_time=record['TIME [SEC]'], b1=record['BEHAV 1 LEVEL'], b2=record['BEHAV 2 LEVEL'], b3=record['BEHAV 3 LEVEL'])
            self.cursor.execute(chunk_insert)
        # if we've already loaded this file in, an IntegrityError will be raised
        changes = self.commit()
        if changes == 0:
            raise Exception('Inserted 0 rows into the DB on filename {fn}! Was this intentional?'.format(fn=filename))
        else:
            print 'DatabaseManager: Successfully loaded {fn}'.format(fn=filename)

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
