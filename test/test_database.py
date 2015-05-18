#!/usr/bin/env python2

"""
To run:
[CISC475-4] $ /usr/bin/env python2 -m unittest test.test_database[.class.function]

Notice that the directory is the project directory, not testing/ or controller/

TODO: Make it possible to run these tests from main.py. It should be similar to 
importing unittest, telling it what to look at, and calling its main function.
"""

from controller import database
import unittest
import sqlite3  # Doesn't get imported when controller.database is imported
import logging

class TestDatabase(unittest.TestCase):
    """Test the functions in the DatabaseManager class."""

    # This is here so these dbs don't connect to the same or default db
    test_address = ''

#    def setUp(self):
#        """initializes data necessary to test database functionality"""
#	pass

    def test_connect(self):
        """ asserts that the changes made in connect() take effect """
	db = database.DatabaseManager(self.test_address)
	sql_conn_orig = db.sql_conn
	cursor_orig = db.cursor
	db.connect()

	self.assertFalse(sql_conn_orig == db.sql_conn)
	self.assertFalse(cursor_orig == db.cursor)
	self.assertEqual(db.sql_conn.text_factory, str)
	self.assertEqual(db.sql_conn.row_factory, sqlite3.Row)

    def test_disconnect(self):
        db = database.DatabaseManager(self.test_address)
	db.connect()
        db.disconnect()
        self.assertIsNone(db.cursor)
    
    def test_setup(self):
        db_setup = database.DatabaseManager(self.test_address)
	db_setup.connect()
	changes = db_setup.setup()
	
        # Table creations don't count as changes, so that can't be checked.
        # Instead, just make sure check_db_setup works as planned.
        self.assertTrue(db_setup.check_db_setup())

        # Database that tries to import a file that doesn't exist
	db_bad_fname = database.DatabaseManager(self.test_address)
	db_bad_fname.connect()
	self.assertRaises(IOError, db_bad_fname.setup, 'fileThatDoesntExist')
        self.assertFalse(db_bad_fname.check_db_setup())

    def test_check_db_setup(self):
        """ checks to see that (un)initialized dbs are recognized as such """
        # db_setup will check if a set-up db is accepted
        db_setup = database.DatabaseManager('tests/test.sql')
	db_setup.connect()
	db_setup.setup()
	self.assertTrue(db_setup.check_db_setup())
        db_setup.disconnect()

        # db_not_setup will test to see that uninitialized dbs aren't accepted
        # Different name so the dbs in this function are definitely different
	db_not_setup = database.DatabaseManager('')
        db_not_setup.connect()
        # don't call db_not_setup.setup()
	self.assertFalse(db_not_setup.check_db_setup()) 

    def test_import_file_to_database(self):
        db = database.DatabaseManager(self.test_address)
	self.assertRaises(IOError, db.import_file_to_database, 'fakeFileName')

        # Jamie's fixing this right now, so I'll do it later

    def test_execute_query(self):
        """ Note: This relies on other DatabaseManager functions 

        This does almost exactly what execute_query does, so I guess there's
        not much point to it.
        """

        test_Session = 'SELECT * FROM Session;'
        test_Chunk = 'SELECT * FROM Chunk;'
        test_GroupData = 'SELECT * FROM GroupData;'
        test_Session_Meta = 'SELECT * FROM Session_Meta;'
        
        # db will use the DatabaseManager functions
        db = database.DatabaseManager(self.test_address)
        db.connect()
        db.setup() # Set up schema/etc.
        db.setup('tests/test_data.sql') # Insert test data into db
        
        # db_test will perform all the steps manually
        db_test = database.DatabaseManager('')
        db_test.connect()
        db_test.setup()
        db_test.setup('tests/test_data.sql')
        db_test_cursor = db_test.sql_conn.cursor()

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

    def test_create_condition_query(self):
        """ Tests for string equivalence, not database functionality """

        # create_condition_query's parameter is a dictionary
        pass
