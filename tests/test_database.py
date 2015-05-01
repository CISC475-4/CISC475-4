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

