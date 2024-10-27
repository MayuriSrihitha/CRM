# SQLite comes built into Python, so no additional installations needed!
import sqlite3

# Connect to SQLite database (this will create it if it doesn't exist)
connection = sqlite3.connect('db.sqlite3')

# prepare a cursor object
cursor = connection.cursor()

# Since SQLite doesn't have separate databases like MySQL,
# we don't need to create one. The database is the file itself.
# But we can create a test table to verify it works:
cursor.execute('''
    CREATE TABLE IF NOT EXISTS test_table (
        id INTEGER PRIMARY KEY,
        name TEXT
    )
''')

# Commit the changes and close the connection
connection.commit()
connection.close()

print("All Done! SQLite database created successfully.")
