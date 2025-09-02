# Python Generators – Database Seeding

## 📌 About the Exercise
This task introduces how to set up and seed a MySQL database in Python.  
We use Python’s `mysql-connector-python` library to connect to MySQL, create a database, define a table, and insert rows from a CSV file.

The project prepares the ground for using **generators** later to stream rows efficiently from the database.

---

## 🎯 Objectives
- Connect to a MySQL server using Python.
- Create the database `ALX_prodev` if it does not exist.
- Create a table `user_data` with the required schema.
- Insert data from `user_data.csv` into the table.
- Verify that data has been inserted successfully.

---

## 📂 Files
- **`seed.py`** → Contains all the functions to connect, create, and seed the database.  
- **`0-main.py`** → Driver script to test `seed.py`.  
- **`user_data.csv`** → Sample data file used to populate the table.  
- **`README.md`** → This documentation file.

