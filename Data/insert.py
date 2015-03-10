import sqlite3

# so far test the dataviz.sql file

def setup(sql_file):
    con = sqlite3.connect(':memory:')
    cursor = con.cursor()
    with open(sql_file,'r') as schema:
        cursor.executescript(schema.read())  # catch 'em all
    con.commit()
    con.close()

setup('dataviz.sql')
