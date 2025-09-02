#!/usr/bin/python3
"""
0-stream_users.py
Generator function to stream rows one by one from the user_data table.
"""

import mysql.connector


def stream_users():
    """
    Connects to the ALX_prodev database and streams rows one by one
    from the user_data table using a generator.
    Yields:
        dict: A dictionary containing user_id, name, email, and age.
    """
    # connect to the database
    connection = mysql.connector.connect(
        host="localhost",
        user="root",         # replace with your MySQL username
        password="password", # replace with your MySQL password
        database="ALX_prodev"
    )

    cursor = connection.cursor(dictionary=True)  # returns rows as dict
    cursor.execute("SELECT * FROM user_data;")

    for row in cursor:  # single loop requirement ✅
        yield row

    cursor.close()
    connection.close()
