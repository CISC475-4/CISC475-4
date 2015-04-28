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

    # ----------
    # Multiple session, one behavior analysis
    #-----------
    # TODO: implement method
    def get_behavior_types(self):
        '''
        Get a list of all possible behavior types
        return - list of strings (where the string represents the behavior)
        '''
        pass

    # TODO: implement method
    def get_behavior_types_specific_to_session(self, child_id, session_id):
        '''
        Get a list of behavior types that appear in a specific session (useful 
            if there are more behaviors available than appear in a specific session)
        child_id- a string representing a child id
        session_id - a string representing a session id
        return - list of strings (where the string represents the behavior)
        '''
        pass

    # TODO: implement method
    def get_behavior_data_from_session(self, behavior_id, child_id, session_id):
        '''
        Get data values for a behavior over the course of one session of a child
        behavior_id - a string representing the behavior being selected
        child_id- a string representing a child id
        session_id - a string representing a session id
        return - a list of values representing the behavior value over time
        TODO: we may need to return the total time as well to be able to
            figure out how long it is between behavior values
        '''
        # TODO: Get data from database
        pass 



    #-----------
    # Single session, multiple behavior analysis
    #-----------
    # TODO: implement method
    def get_all_child_ids(self):
        '''
        Get a list of child ids from the DB
        return - a list of strings (where each string represents a child id)
        '''
        # TODO: Get data from database
        pass

    # TODO: implement method
    def get_all_sessions_ids_for_child(self, child_id):
        '''
        Get a list of session ids from the DB given a child id
        child_id - a string representing a child id
        return - a list of strings (where each string represents a session id)
        '''
        # TODO: Get data from database
        pass


"""""
Behaviors needed for graphing:
x- Retreive a list of child ids and session ids
- After we have chosen a child/session, choose a behavior for each color bar graph.
- Load data for selected session(s)
    - One session multiple behaviors
    - Multiple sessions one behavior

Frontend???
- Specify two colors for graphing intensity -- for each behavior???
- Select range of values (time) to display

"""""