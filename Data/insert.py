#!/usr/bin/env python2
import sqlite3

# so far test the dataviz.sql file

def setup(sql_file):
    con = sqlite3.connect('')

    # Makes the output from cursor.fetch*() into 'Row' objects (like dicts)
    con.row_factory = sqlite3.Row

    # Use bytestrings instead of Unicode in the results
    con.text_factory = str

    cursor = con.cursor()
    with open(sql_file,'r') as schema:
        cursor.executescript(schema.read())  # catch 'em all
    con.commit()

    # Make sure things actually made it into the database
    if con.total_changes == 0:
        raise Exception('Failed to update the database!')
    else:
        print 'Database creation successful.'

    con.close()

setup('dataviz.sql')
