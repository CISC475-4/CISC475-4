#!/usr/bin/env python2
import utility.file_utility
import sqlite3
import os
import sys
import logging

class DatabaseManager(object):
    '''
    Database Wrapper Class
    Responsible for all interactions with the embedded sqlite3 DB
    '''

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
        May be called multiple times per program run, but
        only if disconnect() was called first
        '''
        if self.sql_conn is not None:
            logging.error('DatabaseManager: called connect() on a connected DB!')
            return
        self.sql_conn = sqlite3.connect(self.address, timeout=self.timeout)
        # Makes the output from cursor.fetch*() into 'Row' objects (like dicts)
        self.sql_conn.row_factory = sqlite3.Row
        # Use bytestrings instead of Unicode in the results
        self.sql_conn.text_factory = str
        self.cursor = self.sql_conn.cursor()
        # if the schema has already been loaded, don't perform the init operation
        logging.info('DatabaseManager: connected to DB')
        if not self.check_db_setup():
            self.setup()

    def disconnect(self):
        ''' removes the connection to the database
        Should only be called once per program run
        '''
        self.sql_conn.commit()
        self.sql_conn.close()
        self.cursor = None
        self.sql_conn = None
        logging.info('DatabaseManager: closed DB connection')

    def check_db_setup(self):
        ''' check to make sure that all tables exist in the database already
        Return: bool. True if the database has already been setup
        '''
        existence = True
        tablenames = ['Chunk', 'Session', 'GroupData', 'Session_Meta']
        for table in tablenames:
            self.cursor.execute("SELECT name FROM sqlite_master WHERE type='table' and name='{tbl}'".format(tbl=table))
            potential = self.cursor.fetchone()
            if potential is not None:
                existence = (potential[0] == table)  # if the 'Chunk' table exists, it is set up
            else:
                existence = False
        logging.info('DatabaseManager: check_db_setup returned {e}'.format(e=existence))
        return existence

    def setup(self, sql_filename='controller/schemata/main.sql'):
        ''' reads in the initial database schema and creates all necessary tables
        Params: filename to load up. Default is the saved schema we already wrote
        Cursor must exist in order to do this operation
        '''
        changes = 0
        with open(sql_filename, 'r') as schema:
            self.cursor.executescript(schema.read())  # catch 'em all
            changes = self.commit()
        logging.info('DatabaseManager: loaded schema {fn} successfully'.format(fn=sql_filename))
        return changes

    def clear(self):
        tablenames = ['Chunk', 'Session', 'GroupData', 'Session_Meta']
        for table in tablenames:
            self.cursor.execute('DELETE FROM {n}'.format(n=table))
        changes = self.commit()
        logging.info('DatabaseManager: truncated all tables with {n} changes'.format(n=changes))
        return changes

    def commit(self):
        ''' commits any pending changes and returns the total number of updated rows
        note that no rows will be updated on a CREATE TABLE operation, etc
        Return: number of rows updated
        '''
        self.sql_conn.commit()
        amt_changes = self.sql_conn.total_changes
        return amt_changes

    def import_file_to_database(self, filename, num_behaviors=3):
        '''
        Params: filename (string) the relative path of the file
        Return: none
        Will raise an exception or error if the data is already in the DB
        To change the amount of behaviors in the file, change the param here.
        TODO: Exception handling for existing data
        '''
        if not os.path.isfile(filename):
            raise IOError("File does not exist!")
        # determine if the file is a csv or xls[x]
        # 0. snag datasets into memoriy
        datasets = None
        if '.csv' in os.path.splitext(filename)[1]:
            datasets = self.import_csv_to_database(filename)
        elif '.xls' in os.path.splitext(filename)[1]:
            datasets = self.import_excel_to_database(filename)
        else:
            raise IOError("Incorrect file type! Expected .csv or .xls")

        # iterate through dataset rows and insert
        # 1. Insert new row in Session
        allgroup = datasets[0]  # all group data goes here
        session_insert = "INSERT INTO Session values('{cid}','{sid}')".format(cid=allgroup.child_id, sid=allgroup.session_id)
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
            for i in range(1, num_behaviors + 1):
                chunk_insert = "INSERT INTO Chunk values('{cid}','{sid}','{exp_time}','{l}','{b}')".format(cid=timeseries.child_id, sid=timeseries.session_id, exp_time=record['TIME [SEC]'], l=i, b=record['BEHAV {i} LEVEL'.format(i=i)])
                self.cursor.execute(chunk_insert)
        # if we've already loaded this file in, an IntegrityError will be raised
        changes = self.commit()
        if changes == 0:
            raise Exception('Inserted 0 rows into the DB on filename {fn}! Was this intentional?'.format(fn=filename))
        else:
            logging.info('DatabaseManager: Successfully loaded {fn}'.format(fn=filename))

    def import_excel_to_database(self, filename):
        '''
        import_excel_to_database
        Description: returns a the imported datasets
        '''
        datasets = utility.file_utility.get_data_from_xls(filename)  # tuple of DataSet objects
        return datasets

    def import_csv_to_database(self, filename):
        '''
        import_csv_to_database
        Description:
        '''
        datasets = utility.file_utility.get_data_from_csv(filename)  # tuple of DataSet objects
        return datasets

    def execute_query(self, query):
        '''
        This functions servers to actually query the database. 
        '''
        cursor = self.sql_conn.cursor()
        cursor.execute(query)  
        return cursor.fetchall() #a list of data rows

    def create_condition_query(self, conditions):
        '''
        This functions serves as logic to create the sub-query with conditional syntax
        '''
        #TODO: handle other conditions that are not plainly equivalent cases
        qry = " WHERE "
        for pair in conditions.iteritems():
            # TODO: distinguish between numeric and non-numeric keys
            if type(pair[1]) == type(list()): #To Allow Multiple values 
                qry += '(' 
                for value in pair[1]:
                    qry += pair[0]  + ' = ' + str(value) + " OR "  
                qry = qry.rstrip(' OR ') + ') AND '
            else:
                qry += pair[0] + " = " + str(pair[1]) + " AND " # pair = (key, value)
        qry = qry.rstrip(' AND ')
        return qry 
        
    def create_range_condition_query(self, range_conditions):
        '''
        Function to create the range condition query
        Will not prepend a WHERE, must be added manually
        '''
        qry = ""
        for key, val in range_conditions.iteritems():
            # key here is the columnname to be restricted, val is the dictionary of conditions
            if 'min' in val:
                qry += '{k} >= {m} '.format(k=key, m=val['min'])
                if 'max' in val:
                    qry += 'AND {k} <= {m} '.format(k=key, m=val['max'])
            elif 'max' in val:
                qry += '{k} <= {m} '.format(k=key, m=val['max'])
            qry += " AND " 
        qry = qry.rstrip(' AND ')
        return qry

    def retrieve_db_info(self, table=""):
        '''
        performs queries for such information as table names and full table info
        '''
        qry = ""
        if table == "":
            qry = "SELECT name FROM sqlite_master WHERE type='table'"
        else:
            # results as (col_num, col_name, type, ?, ?, ?)
            qry = "PRAGMA table_info(" + table + ")"
        return self.execute_query(qry)

    def retrieve_distinct_by_name(self, column, table, equality_condition={}):
        '''
        call the database to query for all unique values of a given column from the specified table
        ie: use to retrive all session_ids or child_ids from Session table
        '''
        qry = "SELECT DISTINCT " + column + " FROM " + table
        if equality_condition != {}:
            qry += self.create_condition_query(equality_condition)

        return self.execute_query(qry)
        
    def query_single(self, column, table, conditions={}):
        '''
        column - a single column header to be retrieved from the database OR 
        conditions (Optional) - a dictionary of column headers to the target value
                - wil be used to create conditional statements in the query
        NOTE: use this if for a 'SELECT *' statement
        '''     
        qry = "SELECT " + column + " FROM " + table
        if conditions != {}:
            qry += self.create_condition_query(conditions)
        return self.execute_query(qry)

    def query_multiple(self, columns, table, conditions={}):
        '''
        columns - a list of colums to be retrieved
        conditions (optional) - a dictionary of column headers to target value
                - will be used to create conditional statements in the query 
        '''
        qry = "SELECT " 
        for col in columns:
            qry += col + ", "
        qry = qry.rstrip(', ')
        qry += " FROM " + table

        if conditions != {}:
            qry += self.create_condition_query(conditions)
        return self.execute_query(qry) 

    def query_range(self, columns, table, range_conditions, equality_conditions={}):
        '''
        columns - a list of columns to be retrieved
        table - from which ot be retrieved
        range_conditions - a two-leveled dictionary { col_name: {'min': #, 'max': #}, ...}
        conditions - other conditions (equality conditions)=
        '''
        qry = 'SELECT '
        for cname in columns:
            qry += cname + ', '
        qry = qry.rstrip(', ')
        qry += ' FROM {t} '.format(t=table)
        if equality_conditions != {}:
            qry += self.create_condition_query(equality_conditions)
            qry += ' AND '
        else:
            qry += 'WHERE '
        qry += self.create_range_condition_query(range_conditions) 
        qry = qry.rstrip('AND ')
        return self.execute_query(qry)

    def query_aggregate(self, column, table, fn, range_conditions={}, equality_conditions={}):
        '''
        fn - the code for the aggregate functino to perform
        if an unhandled code is given, it simply performs a select statement
        returns the result of the given aggregate fn on the database

        aggregate functions here are NOT exhaustive
        add codes for additional necessary aggregate functions later
        '''
        aggr_command = ""

        if fn == 0: #MAX
            aggr_command = "MAX" 
        elif fn == 1: #MIN
            aggr_command = "MIN"
        elif fn == 2: #COUNT
            aggr_command = "COUNT"
        elif fn == 3: #AVG
            aggr_command = "AVG"

        cond_qry = "" #conditions
        if equality_conditions != {} and range_conditions != {}:
            cond_qry = self.create_condition_query(equality_conditions)
            cond_qry += ' AND '
            cond_qry += self.create_range_condition_query(range_conditions)
        elif equality_conditions != {}:
            cond_qry += self.create_condition_query(equality_conditions)
        elif range_conditions != {}:
            cond_qry += ' WHERE '
            cond_qry += self.create_range_condition_query(range_conditions)

        qry = "SELECT " + aggr_command + "(" + column + ") " + "FROM " + table + cond_qry
        return self.execute_query(qry)
