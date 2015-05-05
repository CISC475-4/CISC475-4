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

    def import_folder_to_database(self, dirpath):
        '''
        Given a path to a directly, imports all CSV and XLS[X] files with correct pathnames format to db
        '''
        #TODO: this function
        pass

    ## GENERAL DATABASE RELEVANT DATA
    def get_table_names(self):
        '''
        returns a list of all table names
        '''
        return self.db.retrieve_db_info()

    def get_columns_from_table(self, tablename):
        '''
        returns a list of all columns from a given table
        '''
        return [info[1] for info in self.db.retrieve_db_info(tablename)] #info[1] index of column name
    
    def get_all_child_ids(self):
        '''
        Calls teh database to retrieve all unique child_ids 
        returns a list of child_ids
        '''
        return self.db.retrieve_distinct_by_name("child_id", "Session")

    def get_all_sessions_for_child(self, child_id):
        '''
        Calls database to get all session_ids for a given child
        returns a list of session_ids
        '''
        condition = {"child_id" : child_id }
        return self.db.query_single("session_id", "Session", condition)

    ## DATA SPECIFIC TO GROUPDATA TABLE
    def get_all_combo_indexes(self, child_id, session_id):
        '''
        returns a list of all unique combo_index values from the GroupData table
        child_id and session_id must be provided (this is a unique triplet)
        '''
        column = 'combo_index'
        table = 'GroupData'
        conditions = {
            'child_id' : child_id,
            'session_id' : session_id
        }
        return self.db.query_single(column, table, conditions)

    def get_group_data_by_combo_index(self, columns, combo_index, child_id, session_id):
        '''
        columns - a list of columns to retrieve from GroupData tables 
        combo_index - the specific combo to retrieve the data from
        child_id - the child_id from which to retrieve the data
        session_id - the session from which to retrieve the data
        '''
        table = 'GroupData'
        conditions = {
            'child_id' : child_id,
            'session_id' : session_id,
            'combo_index' : combo_index
        }
        print str(columns) + '\n' + str(table) + '\n' + str(conditions)
        return self.db.query_multiple(columns, table, conditions)

    def get_num_chunks(self, combo_index, child_id, session_id):
        '''
        combo_index - the specific combo to retrieve the data from
        child_id - the child_id from which to retrieve the data
        session_id - the session from which to retrieve the data
        returns the number of chunks from a unique combo_index, child_id, and session_id triple
        '''
        column = 'num_chunks'
        table = 'GroupData'
        conditions = {
            'child_id' : child_id,
            'session_id' : session_id,
            'combo_index' : combo_index
        }
        return self.db.query_single(column, table, conditions)

    def get_chunk_max_duration(self, combo_index, child_id, session_id):
        '''
        combo_index - the specific combo to retrieve the data from
        child_id - the child_id from which to retrieve the data
        session_id - the session from which to retrieve the data
        returns the max chunk duration (chunk_max_dur) from a unique combo_index, child_id, session_id triple
        '''
        column = 'chunk_avg_dur' 
        table = 'GroupData'
        conditions = {
            'child_id' : child_id,
            'session_id' : session_id,
            'combo_index' : combo_index
        }
        return self.db.query_single(column, table, conditions)
        
    def get_chunk_avg_duration(self, combo_index, child_id, session_id):
        '''
        combo_index - the specific combo to retrieve the data from
        child_id - the child_id from which to retrieve the data
        session_id - the session from which to retrieve the data
        returns the avg chunk duration (chunk_avg_dur) from a unique combo_index, child_id, session_id triple
        '''
        column = 'chunk_avg_dur'
        table = 'GroupData'
        conditions = {
            'child_id' : child_id,
            'session_id' : session_id,
            'combo_index' : combo_index
        }
        return self.db.query_single(column, table, conditions)
         

    ## DATA SPECIFIC TO CHUNK TABLE
    def get_chunk_data_by_child_id(self, columns, child_id, session_id=None):
        '''
        columns: a list of column ids to get data from
        child_id: the child_id of which to retrieve data from
        session_id: (optional)
        '''
        #TODO: include session_id
        condition = {"child_id" : child_id}
        return self.db.query_multiple(self, columns, "Chunk", condition)

    def get_behaviors_for_child(self, behaviors, child_id, session_id=None, timestamps=False, time_start=None, time_end=None):
        '''
        behaviors - a list of behaviors (column names)
        child_id - the child_id 
        session_id - (optional) default retrieves all session
        timestamps - (optional) set to True if you want to retrieve timestamps with each data instance
        time_start - (optional) default retrieves all times, must include a time_end value 
        time_end - (optional) default retrieves all times, must include a time_start value
        '''
        #TODO: timestamps
        # build time constraints
        time_conditions = {}
        if time_start is not None:
            time_conditions['min'] = time_start
        if time_end is not None:
            time_conditions['max'] = time_end
        range_conditions = {'time': time_conditions}
        # build equality conditions
        equality_conditions = {'child_id': child_id}
        if session_id is not None:
            equality_conditions['session_id'] = session_id
        return self.db.query_range(behaviors, 'Chunk', range_conditions, equality_conditions)

    def get_max_behavior(self, behaviors, child_id, session_id=-1, timestamps=False, start_time=0, end_time=0):
        '''
        behaviors - a list of behaviors to get the max value of given the child_
        timestamps - (optional) set to True if you want to retrieve timestamps with each data instance
        optional parameters may be used for more specific queries
        returns a list of max values cooresponding to the list of behaviors
        '''
        #TODO: implement range querying, change defaults, session id
        aggr_code = 0 #cooresponding to the code for max iaggregate command
        max_behaviors = []
        conditions = {"child_id": child_id}
        #non-default session_id
        if session_id > -1:
            conditions['session_id'] = session_id

        #requesting the query from database object
        if type(behaviors) == type(list()):
            for behavior in behaviors: 
                max_val = self.db.query_aggregate(behavior, "Chunk", aggr_code, conditions) 
                max_behaviors += max_val
        else:
            #not handling behaviors that are not a list
           logging.error("Controller: Incorrect argument to query database")

        return max_behaviors
        

    def get_min_behavior(self, behaviors, child_id, session_id=None, timestamps=False, start_time=0, end_time=0):
        '''
        behaviors - a list of behaviors to get the max value of given the child_
        timestamps - (optional) set to True if you want to retrieve timestamps with each data instance
        optional parameters may be used for more specific queries
        returns a list of max values cooresponding to the list of behaviors
        '''
        #TODO: implement session id, range query, and timestamp
        aggr_code = 1 #cooresponding to the code for max aggregate command
        min_behaviors = []
        condition = {"child_id", child_id}
        if type(behaviors) == type(list()):
            for behavior in behaviors: 
                min_val = self.db.query_aggregate(behavior, "Chunk", aggr_code, condition) 
                min_behaviors += min_val
        else:
            #not handling behaviors that are not a list
           logging.error("Controller: Incorrect argument to query database")

        return min_behaviors

    def get_avg_behavior(self, behaviors, child_id, session_id=None, timestamps=False, start_time=0, end_time=0):
        '''
        behaviors - a list of behaviors to get the max value of given the child_
        timestamps - (optional) set to True if you want to retrieve timestamps with each data instance
        optional parameters may be used for more specific queries
        returns a list of avg values cooresponding to the list of behaviors
        '''
        #TODO: this whole function
        pass
        

    # TABLE SPECIFIC QUERIES
    def get_group_data(self, columns):
        '''
        calls db to query for specific columns in the GroupData table
        '''
        return self.db.query_multiple(columns, 'GroupData')

    def get_chunk_data(self, columns):
        '''
        calls db to query for specific columns in the Chunk table
        '''
        return self.db.query_multiple(columns, 'Chunk')

    def get_meta_data(self, columns):
        '''
        calls db to query for specific columns in the Session_Meta table
        '''
        return self.db.query_multiple(columns, 'Session_Meta')
