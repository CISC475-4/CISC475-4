#!/usr/bin/env python2
import utility.file_utility
import database
import logging

from os import listdir


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
            logging.error(e.message)


    # TODO implement method
    def import_folder_to_database(self, path):
        """
        Given a path, imports all files in that path to the database where only the
        files that are in the required format will be loaded (other files are skipped).
        This is useful so we can load in multiple sessions all at once!

        input:
            path (string) path of the folder
        """
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
        return [info[1] for info in self.db.retrieve_db_info(tablename)] #info[1] is index of column name


    def get_behavior_types_specific_to_session(self, child_id, session_id):
        '''
        Get a list of behavior types that appear in a specific session (useful 
            if there are more behaviors available than appear in a specific session)
        child_id- a string representing a child id
        session_id - a string representing a session id
        return - list of strings (where the string represents the behavior)
        '''
        # TODO: priority 0; write this method
        pass

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
        column = 'chunk_max_dur' 
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

    def get_freq_occurence(self, combo_index, child_id, session_id):
        '''
        TODO: Requires a join with the chunk table (top 3 behaviors)
        Retrieves the top behaviors for each combo/code
        '''
        #TODO: this function
        pass

    ## DATA SPECIFIC TO CHUNK TABLE
    def get_behavior_types(self, child_id=None):
        '''
        returns the unique behavior_ids for all children
        given a child_id, will return all unique behavior_ids for that child
        '''
        #TODO: this function
        pass


    def get_behaviors_for_child(self, behaviors, child_id, session_id=None, time_start=None, time_end=None, timestamps=None):
        '''
        behaviors - a list of behaviors (column names)
        child_id - the child_id 
        session_id - (optional) default retrieves all session
        timestamps - (optional) set to True if you want to retrieve timestamps with each data instance
        time_start - (optional) default retrieves all times, must include a time_end value 
        time_end - (optional) default retrieves all times, must include a time_start value
        '''
        # build time constraints
        time_conditions = {}
        if time_start is not None:
            time_conditions['min'] = time_start
        if time_end is not None:
            time_conditions['max'] = time_end
        range_conditions = {}
        if time_conditions != {}:
            range_conditions = {'time': time_conditions}
        # build equality conditions
        equality_conditions = {'child_id': child_id}
        if session_id is not None:
            equality_conditions['session_id'] = session_id
        columns = []
        # retrieve behavior columns
        bh_amt = len(behaviors)
        if bh_amt > 0:
            columns.append('behavior_id')
            columns.append('behavior_lvl')
            #TODO: add the proper behaviors to condition 
            equality_conditions['behavior_id'] = [bh.lstrip('b') for bh in behaviors]

        # retrieve time column if requested
        if timestamps:
            columns.append('time')
            return self.db.query_range(columns, 'Chunk', range_conditions, equality_conditions)
        else:
            return self.db.query_multiple(columns, 'Chunk', equality_conditions)

    def get_max_behavior(self, behavior, child_id, session_id=None, time_start=None, time_end=None):
        '''
        behaviors - a single behavior to be gotten the max of
        optional parameters may be used for more specific queries
        returns a list of max values cooresponding to the list of behaviors
        '''
        aggr_code = 0 #cooresponding to the code for max iaggregate command
        equality_conditions = {"child_id": child_id}

        #build time constraints
        time_conditions = {}
        if time_start is not None:
            time_conditions['min'] = time_start
        if time_end is not None:
            time_conditions['max'] = time_end
        range_conditions = {}
        if time_conditions != {}:
            range_conditions = {'time': time_conditions}

        #non-default session_id
        if session_id != None:
            equality_conditions['session_id'] = session_id

        code = int(behavior.lstrip('b'))
        equality_conditions['behavior_id'] = code
        max_val = self.db.query_aggregate('behavior_lvl', "Chunk", aggr_code, range_conditions, equality_conditions) 

        return max_val[0][0] # surrounded in a 1-tuple with a 1-list
        

    def get_min_behavior(self, behavior, child_id, session_id=None, time_start=None, time_end=None):
        '''
        behaviors - a single behavior to be gotten the max of
        optional parameters may be used for more specific queries
        returns a list of max values cooresponding to the list of behaviors
        '''
        aggr_code = 1 #cooresponding to the code for min aggregate command
        equality_conditions = {"child_id": child_id}

        #build time constraints
        time_conditions = {}
        if time_start is not None:
            time_conditions['min'] = time_start
        if time_end is not None:
            time_conditions['max'] = time_end
        range_conditions = {}
        if time_conditions != {}:
            range_conditions = {'time': time_conditions}
        
        #non-default session_id
        if session_id != None:
           equality_conditions['session_id'] = session_id

        code = int(behavior.lstrip('b'))
        equality_conditions['behavior_id'] = code
        min_val = self.db.query_aggregate('behavior_lvl', "Chunk", aggr_code, range_conditions, equality_conditions) 

        return min_val[0][0]

    def get_avg_behavior(self, behavior, child_id, session_id=None, time_start=None, time_end=None):
        '''
        behaviors - a single behavior to be gotten the max of
        timestamps - (optional) set to True if you want to retrieve timestamps with each data instance
        optional parameters may be used for more specific queries
        returns a list of avg values cooresponding to the list of behaviors
        '''
        aggr_code = 3 #cooresponding to the code for max aggregate command
        equality_conditions = {"child_id": child_id}

        #build time constraints
        time_conditions = {}
        if time_start is not None:
            time_conditions['min'] = time_start
        if time_end is not None:
            time_conditions['max'] = time_end
        range_conditions = {}
        if time_conditions != {}:
            range_conditions = {'time': time_conditions}
        
        #non-default session_id
        if session_id != None:
           equality_conditions['session_id'] = session_id

        code = int(behavior.lstrip('b'))
        equality_conditions['behavior_id'] = code
        avg_val= self.db.query_aggregate('behavior_lvl', 'Chunk', aggr_code, range_conditions, equality_conditions)
        return avg_val[0][0]


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
