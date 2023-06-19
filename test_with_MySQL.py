#!/usr/bin/python3

import os

# Get the values from environment variables
host = os.environ.get('HBNB_MYSQL_HOST')
user = os.environ.get('HBNB_MYSQL_USER')
password = os.environ.get('HBNB_MYSQL_PWD')
database = os.environ.get('HBNB_MYSQL_DB')

# Get the initial count of records in the table
initial_count_command = "mysql -h {} -u {} -p{} -D {} -e 'SELECT COUNT(*) FROM states;'".format(host, user, password, database)
initial_count_output = os.popen(initial_count_command).read().strip()
initial_count = int(initial_count_output.split('\n')[1])

# Execute the command to create a new state
create_state_command = "mysql -h {} -u {} -p{} -D {} -e 'INSERT INTO states (name) VALUES (\"California\");'".format(host, user, password, database)
os.system(create_state_command)

# Get the updated count of records in the table
updated_count_command = "mysql -h {} -u {} -p{} -D {} -e 'SELECT COUNT(*) FROM states;'".format(host, user, password, database)
updated_count_output = os.popen(updated_count_command).read().strip()
updated_count = int(updated_count_output.split('\n')[1])

# Assert the difference is equal to 1
assert updated_count - initial_count == 1
