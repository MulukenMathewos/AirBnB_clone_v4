#!/usr/bin/python3

import pymysql
import os

# Get the values from environment variables
host = os.environ.get('HBNB_MYSQL_HOST')
user = os.environ.get('HBNB_MYSQL_USER')
password = os.environ.get('HBNB_MYSQL_PWD')
database = os.environ.get('HBNB_MYSQL_DB')

# Connect to the MySQL database
connection = pymysql.connect(host=host, user=user, password=password, database=database)
cursor = connection.cursor()

# Get the initial count of records in the table
cursor.execute("SELECT COUNT(*) FROM states")
initial_count = cursor.fetchone()[0]

# Execute the command to create a new state
cursor.execute("INSERT INTO states (name) VALUES ('California')")

# Get the updated count of records in the table
cursor.execute("SELECT COUNT(*) FROM states")
updated_count = cursor.fetchone()[0]

# Assert the difference is equal to 1
assert updated_count - initial_count == 1

# Close the database connection
cursor.close()
connection.close()
