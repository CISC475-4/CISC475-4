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
    # TODO: Delete later
    def retrieve_graph_data(self, x_label, y_label, z_label):
        '''
        retrieve_graph_data
        calls the database functions query the data
        '''
        #TODO: Still determining how the structure of this and related
        #return self.db.execute_query(x_label, y_label, z_label)
        return self.db.query_multiple([x_label, y_label, z_label], "Chunk") 

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
        return self.db.query_single_database("session_id", "Session", condition)

    def get_data_by_child_id(self, columns, child_id):
        '''
        columns: a list of column ids to get data from
        child_id: the child_id of which to retrieve data from
        '''
        condition = {"child_id" : child_id }
        return self.db.query_multiple(self, columns, "Chunk", condition)

    def get_behaviors_for_child(self, behaviors, child_id, session_id=0, time_start=0, time_end=0)
        '''
        behaviors - a list of behaviors (column names)
        child_id - the child_id 
        session_id - (optional) default retrieves all session
        time_start - (optional) default retrieves all times, must include a time_end value 
        time_end - (optional) default retrieves all times, must include a time_start value
        '''
        pass

    def get_max_behavior(self, behaviors, child_id, session_id=0, start_time=0, end_time=0):
        '''
        behaviors - a list of behaviors to get the max value of given the child_
        optional parameters may be used for more specific queries
        returns a list of max values cooresponding to the list of behaviors
        '''
        pass

    def get_min_behavior(self, behaviors, child_id):
        '''
        behaviors - a list of behaviors to get the max value of given the child_
        optional parameters may be used for more specific queries
        returns a list of max values cooresponding to the list of behaviors
        '''
        pass
        

    # TABLE SPECIFIC QUERIES
    def get_group_data(self, columns):
        '''
        calls db to query for specific columns in the GroupData table
        '''
        pass

    def get_chunk_data(self, columns):
        '''
        calls db to query for specific columns in the Chunk table
        '''
        pass

    def get_meta_data(self, columns):
        '''
        calls db to query for specific columns in the Session_Meta table
        '''
        pass


