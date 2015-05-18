#!/usr/bin/env python2

"""
To run:
[CISC475-4] $ /usr/bin/env python2 -m unittest test.test_database[.class.function]
or:
[CISC475-4] $ nosetests --exe

Notice that the directory is the project directory, not test/ or controller/

TODO: Make it possible to run these tests from main.py. It should be similar to 
importing unittest, telling it what to look at, and calling its main function.

The tests within this file are written using the unittest framework, but they
will be run using the nose library. nose is much more feature-rich than 
unittest. I'd like for it to be used in cooperation with the coverage library.

I think it should be noted that, in general, it's a bad idea to directly use
input in SQL queries/etc.. sqlite3 has a format for escaping parameters; I think
we should be using it. (Instead of `'DELETE FROM {n}'.format(n=table)`, we
should be using `'DELETE FROM ?'` and binding the needed parameter elsewhere in
a call to cursor.execute().
"""

from controller import database
import unittest
import sqlite3  # Doesn't get imported when controller.database is imported
import logging

class TestDatabase(unittest.TestCase):
    """Test the functions in the DatabaseManager class.
    With the exception of test___init__, all function names in this class will 
    be of the form test_F, where F is the name of a function from 
    controller/database.py to be tested.
    """

    # This is here so these dbs don't connect to the same or default db
    test_address = ''

#    def setUp(self):
#        """initializes data necessary to test database functionality"""
#	pass

    def test___init__(self):
        """asserts expected behavior of DatabaseManager initializations"""
        db = database.DatabaseManager(self.test_address)

        self.assertEqual(self.test_address, db.address)
        self.assertIsNone(db.sql_conn)
        self.assertIsNone(db.cursor)

    def test_connect(self):
        """ """
        # First case: see if having a set sql_conn variable returns None
        db_connected = database.DatabaseManager(self.test_address)
        db_connected.sql_conn = 'connection.sql' # It wouldn't be a str normally
        self.assertIsNone(db_connected.connect())

        # This shouldn't really be possible anyway, but if sql_conn is set up
        # properly, these non-default options still shouldn't have been set
        if type(db_connected.sql_conn) == sqlite3.Connection:
            # Some of the few things changed in connect()
            self.assertNotEqual(db_connected.sql_conn.row_factory, sqlite3.Row)
            self.assertNotEqual(db_connected.sql_conn.text_factory, str)

        # Second case: make sure all variables are updated properly
	db = database.DatabaseManager(self.test_address)
	sql_conn_orig = db.sql_conn
	cursor_orig = db.cursor
        # Without a valid sql_conn, db has no cursor, so this should fail
        # I think this should be caught in DatabaseManager. Just do an
        # `if self.cursor: ` before the execute line to make sure the cursor
        # exists.
        self.assertRaises(AttributeError, db.check_db_setup)
        # This should evaluate to False anyway. Setting it for now since I think
        # the above method should just return False or raise its own Exception
        was_setup_orig = False
	db.connect()

	self.assertNotEqual(sql_conn_orig, db.sql_conn)
	self.assertNotEqual(cursor_orig, db.cursor)
        self.assertNotEqual(was_setup_orig, db.check_db_setup())
	self.assertEqual(db.sql_conn.text_factory, str)
	self.assertEqual(db.sql_conn.row_factory, sqlite3.Row)

    def test_disconnect(self):
        db = database.DatabaseManager(self.test_address)
	db.connect()
        db.disconnect()

        self.assertIsNone(db.cursor)
        self.assertIsNone(db.sql_conn)
    
    def test_setup(self):
        db_setup = database.DatabaseManager(self.test_address)
	db_setup.connect()
	changes = db_setup.setup()
	
        # Table creations don't count as changes, so that can't be checked.
        # Instead, just make sure check_db_setup works as planned.
        self.assertTrue(db_setup.check_db_setup())

        # Database that tries to import a file that doesn't exist
        # There's actually no way to call setup() with a parameter in the
        # code at the moment, so maybe this isn't a problem.
	db_bad_fname = database.DatabaseManager(self.test_address)
        # Need to reproduct DatabaseManager.connect() here since it now calls
        # setup() itself                                              #
        db_bad_fname.sql_conn = sqlite3.connect(db_bad_fname.address, #
                                                db_bad_fname.timeout) #
        db_bad_fname.sql_conn.text_factory = sqlite3.Row              #
        db_bad_fname.sql_conn.text_factory = str                      #
        db_bad_fname.cursor = db_bad_fname.sql_conn.cursor()          #

        # Without setup() having been called, there will be nothing in the
        # database. Thus, both of the following assert statements should work
	self.assertRaises(IOError, db_bad_fname.setup, 'fileThatDoesntExist')
        # This will fail because connect() calls setup() now.
        self.assertFalse(db_bad_fname.check_db_setup())

    def test_check_db_setup(self):
        """ checks to see that (un)initialized dbs are recognized as such 
        There used to be more testing here, but with the addition of setup()
        in connect() many of the possible errors were avoided completely.
        """
        # db_setup will check if a set-up db is accepted
        db_setup = database.DatabaseManager('test/test.sql')
	db_setup.connect() # This will call db_setup.setup()
        
	self.assertTrue(db_setup.check_db_setup())
        
        db_setup.disconnect()

    def test_execute_query(self):
        """ 
        Note: This relies on other DatabaseManager functions. If those functions
        are also failing tests, check for errors there first.
        """

        test_Session = 'SELECT * FROM Session;'
        test_Chunk = 'SELECT * FROM Chunk;'
        test_GroupData = 'SELECT * FROM GroupData;'
        test_Session_Meta = 'SELECT * FROM Session_Meta;'
        
        # db will use the DatabaseManager functions
        db = database.DatabaseManager(self.test_address)
        db.connect()
        db.setup('test/test_data.sql') # Insert test data into db
        db.cursor = db.sql_conn.cursor()
        
        # db_test will perform the queries
        db_test = database.DatabaseManager('')
        db_test.connect()
        db_test.setup('test/test_data.sql')
        db_test_cursor = db_test.sql_conn.cursor()

        # DatabaseManager.execute_query() returns cursor.fetchall()
        db_test_cursor.execute(test_Session)
        self.assertListEqual(db_test_cursor.fetchall(), 
                             db.execute_query(test_Session))

        db_test_cursor.execute(test_Chunk)
        self.assertListEqual(db_test_cursor.fetchall(), 
                             db.execute_query(test_Chunk))

        db_test_cursor.execute(test_GroupData)
        self.assertListEqual(db_test_cursor.fetchall(), 
                             db.execute_query(test_GroupData))

        db_test_cursor.execute(test_Session_Meta)
        self.assertListEqual(db_test_cursor.fetchall(), 
                             db.execute_query(test_Session_Meta))

        db.disconnect()
        db_test.disconnect()

    def test_clear(self):
        """
        Note: I think clear's implementation could be better. Should tablenames
        be hardcoded into the function?
        """
	db = database.DatabaseManager(self.test_address)
        db.connect() 

        # Data will be entered into the database in this call.
        # There are 20 insertions in test_data.sql
        inserts = db.setup('test/test_data.sql')

        # The number of deletions should equal the number of insertions
        self.assertEqual(inserts, db.clear())

    def test_commit(self):
        """
        Note: This relies on other DatabaseManager functions. If this test
        fails, see if those functions are failing, too, as their failures 
        could be the cause of this test's failure.

        If this fails when you don't expect it to, replace the calls to
        db.execute_query() with manual insertions into the database.
        """

        # 4 insertions total.
        sql_insert = """
        INSERT INTO Session VALUES (1743, 64);
        INSERT INTO Session_Meta VALUES (1743, 64, 21.856, 11, 72);
        INSERT INTO GroupData VALUES (1743, 64, 3, 1.2, 3, 4.56, 7, 8.9, 10.01);
        INSERT INTO Chunk VALUES (123, 456, 789, 1011, "chunkfile.ext");
        """

        # db will use the DatabaseManager functions
        db = database.DatabaseManager(self.test_address)
        db.connect() # No changes counted for table creations/etc.
        # DatabaseManager.execute_query() works with non-query statements!
        db.execute_query('INSERT INTO Session VALUES (1743, 64);')
        db.execute_query('INSERT INTO Session_Meta VALUES ('
            '1743, 64, 21.856, 11, 72);')
        db.execute_query('INSERT INTO GroupData VALUES ('
            '1743, 64, 3, 1.23, 4, 5.67, 8, 9.0, 10.01);')
        db.execute_query('INSERT INTO Chunk VALUES ('
            '123, 456, 789, 1011, "chunkfile.ext");')
        db_commits = db.commit()

        # db_test will do everything itself
        # Note that this requires most of DatabaseManager.setup() to be
        # reproduced here, since we need to test at a lower level than that
        db_test = database.DatabaseManager(self.test_address)
        db_test.connect()
        # Should do the same as the execute_query() calls above
        db_test.cursor.executescript(sql_insert)
        db_test_commits = db_test.commit()

        self.assertEqual(db_commits, db_test_commits)
        
    def test_import_file_to_database(self):
        db = database.DatabaseManager(self.test_address)
	self.assertRaises(IOError, db.import_file_to_database, 'fakeFileName')

        # Jamie's fixing this right now, so I'll do it later

    def test_create_condition_query(self): # param is a dict
        """tests for string equivalence, not database functionality 

        Not for nothing, but the queries generated by create_condition_query
        will be very (comparatively) slow because they all contain subqueries.
        I don't know if there's an easy way to do it efficiently though, so 
        I'm not complaining.

        This just tests for basic functionality. There are plenty of testable
        errors that could occur that this test function doesn't cover.
        """

	db = database.DatabaseManager(self.test_address)

        # There's no way to add any part of the query before the WHERE [...]
        expected = ' WHERE child_id = 12345 AND time_modified = 88888 AND ('
        expected += 'session_id = 0 OR session_id = 1)'

        # The argument to be passed to create_condition_query--a dict
        conditions = {
            'child_id' : 12345,
            'session_id' : [00, 01],
            'time_modified' : 88888
        }

        self.assertEqual(expected, db.create_condition_query(conditions))

    def test_create_range_condition_query(self):
        """tests for string equality, not database functionality"""
	db = database.DatabaseManager(self.test_address)
        expected = ''

        self.fail('Not implemented. I don\'t understand this function!')

    def test_retrieve_db_info(self):
        # Based on what was output when I called this manually
        expected = [('Session',), ('Chunk',), ('GroupData',), ('Session_Meta',)]
        
	db = database.DatabaseManager(self.test_address)
        db.connect() # An exception is raised if this isn't called!
        
        # First test the function without parameters 
        self.assertListEqual(expected, db.retrieve_db_info())

        # Copied and pasted from test output...
        expected = [
            (0, 'child_id', 'numeric(5)', 1, None, 2), 
            (1, 'session_id', 'numeric(2)', 1, None, 3), 
            (2, 'time_loaded', 'numeric(10)', 1, None, 0), 
            (3, 'time_modified', 'numeric(10)', 1, None, 0), 
            (4, 'filename', 'varchar(255)', 1, None, 1)
        ]

        actual = db.retrieve_db_info('Session_Meta')

        # This doesn't work because the returned values are sqlite3.Row
        # objects, not tuples/strings/etc. ...
        #self.assertListEqual(expected, actual)

    def test_retrieve_distinct_by_name(self):
        pass

    def test_query_single(self):
        pass

    def test_query_multiple(self):
        pass

    def query_range(self):
        pass

    def test_query_aggregate(self):
        pass

    def test_import_csv_to_database(self):
        pass

    def test_import_excel_to_database(self):
        pass

    def test_import_file_to_database(self):
        pass
