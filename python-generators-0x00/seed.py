# seed.py
import mysql.connector
from mysql.connector import Error
import csv
import uuid

def connect_db():
    """Connect to MySQL server (without selecting a DB)"""
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="audia",        # adapte avec ton user MySQL
            password="1234" # adapte avec ton mot de passe MySQL
        )
        return connection
    except Error as e:
        print(f"Error: {e}")
        return None

#---- Database creation
def create_database(connection):
    """Create database ALX_prodev if it does not exist"""
    cursor = connection.cursor()
    cursor.execute("CREATE DATABASE IF NOT EXISTS ALX_prodev;")
    cursor.close()

#--- Connexion to ALX_prodev
def connect_to_prodev():
    """Connect directly to ALX_prodev database"""
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="audia",
            password="1234",
            database="ALX_prodev"
        )
        return connection
    except Error as e:
        print(f"Error: {e}")
        return None


#---
def create_table(connection):
    """Create table user_data if it does not exist"""
    cursor = connection.cursor()
    query = """
    CREATE TABLE IF NOT EXISTS user_data (
        user_id VARCHAR(36) PRIMARY KEY,
        name VARCHAR(255) NOT NULL,
        email VARCHAR(255) NOT NULL,
        age DECIMAL NOT NULL,
        INDEX (user_id)
    );
    """
    cursor.execute(query)
    connection.commit()
    cursor.close()
    print("Table user_data created successfully")
