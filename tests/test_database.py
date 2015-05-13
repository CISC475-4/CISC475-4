#!/usr/bin/env python2

"""
To run:
[CISC475-4] $ /usr/bin/env python2 -m unittest test.test_database[.class.function]

Notice that the directory is the project directory, not testing/ or controller/
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
        db_setup = database.DatabaseManager('test')
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
