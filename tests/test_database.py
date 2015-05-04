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
#    def setUp(self):
#        """initializes data necessary to test database functionality"""
#	pass

    def test_connect(self):
	db = database.DatabaseManager()
	sql_conn_orig = db.sql_conn
	cursor_orig = db.cursor
	db.connect()

	self.assertFalse(sql_conn_orig == db.sql_conn)
	self.assertFalse(cursor_orig == db.cursor)
	self.assertEqual(db.sql_conn.text_factory, str)
	self.assertEqual(db.sql_conn.row_factory, sqlite3.Row)

    def test_disconnect(self):
        db = database.DatabaseManager()
	db.connect()
        db.disconnect()
        self.assertIsNone(db.cursor)
    
    def test_setup(self):
	"""I'm not sure if I understand what setup() is supposed to do"""
        db = database.DatabaseManager()
	db.connect()
	db.setup() # No input sql_filename
	
	# How to test logging messages?
	# There should be new data in the database if the setup was successful
	# Maybe table creations don't count as db changes?
	self.assertGreater(db.sql_conn.total_changes, 0)

	# No error messages for files that don't exist?
	db2 = database.DatabaseManager()
	db2.connect()
	self.assertRaises(IOError, db2.setup, 'fileThatDoesntExist')

    def test_check_db_setup(self):
        db_setup = database.DatabaseManager()
	db_setup.connect()
	db_setup.setup()
	db_not_setup = database.DatabaseManager()

	self.assertTrue(db_setup.check_db_setup())
	self.assertFalse(db_not_setup.check_db_setup())

    def test_import_file_to_database(self):
        db = database.DatabaseManager()
	self.assertRaises(IOError, db.import_file_to_database, 'fakeFileName')
        # @TODO: Finish this function
