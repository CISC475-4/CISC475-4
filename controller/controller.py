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

    def get_data_by_child_id(self, columns, child_id):
        '''
        columns: a list of column ids to get data from
        child_id: the child_id of which to retrieve data from
        '''
        condition = {"child_id" : child_id}
        return self.db.query_multiple(self, columns, "Chunk", condition)

    def get_data_by_child_for_sessions(self, columns, child_id, session_ids):
        '''
        columns: a list of column ids to get data from
        child_id: the child_id of which to retrieve data from
        session_ids: a list of session ids to retrieve data from

        returns a dictionary of session_ids as key and a list of datapoints for each session
        '''
        #TODO:
        #for ID in session_ids:
        #    pass
        pass
        
        

    def get_behaviors_for_child(self, behaviors, child_id, session_id=None, time_start=None, time_end=None):
        '''
        behaviors - a list of behaviors (column names)
        child_id - the child_id 
        session_id - (optional) default retrieves all session
        time_start - (optional) default retrieves all times, must include a time_end value 
        time_end - (optional) default retrieves all times, must include a time_start value
        '''
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

    def get_max_behavior(self, behaviors, child_id, session_id=-1, start_time=0, end_time=0):
        '''
        behaviors - a list of behaviors to get the max value of given the child_
        optional parameters may be used for more specific queries
        returns a list of max values cooresponding to the list of behaviors
        '''
        #TODO: get min over a range
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
        

    def get_min_behavior(self, behaviors, child_id):
        '''
        behaviors - a list of behaviors to get the max value of given the child_
        optional parameters may be used for more specific queries
        returns a list of max values cooresponding to the list of behaviors
        '''
        #TODO: get min over a range
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
