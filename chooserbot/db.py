# db.py
from dotenv import load_dotenv
from abc import ABC, abstractmethod
import mysql.connector
import os

class Tables():
    NUM_OF_TABLES = 3
    Users, Items, Results = range(NUM_OF_TABLES)

    # placeholders
    Names = ['a'] * NUM_OF_TABLES
    CreateCommands = ['a'] * NUM_OF_TABLES

    Names[Users] = "Users"
    Names[Items] = "Items"
    Names[Results] = "Results"

class Database():
    def __init__(self, host, database, user, password):
        self.db = mysql.connector.connect(host=host, database=database, user=user, password=password)

    def create_table(self, command):
        # some input verification...? maybe not needed since commands come locally
        cursor = self.db.cursor()
        cursor.execute(command)
        self.db.commit()
        cursor.close()

    def print_table(self, table_name):
        cursor = self.db.cursor()
        command = "SELECT * FROM " + table_name
        cursor.execute(command)
        for entry in cursor:
            print(entry)

    def print_all_tables(self):
        cursor = self.db.cursor()
        cursor.execute("SHOW TABLES")
        for table in cursor:
            print(table)

    def drop_table(self, table_name):
        command = "DROP TABLE " + table_name
        cursor = self.db.cursor()
        cursor.execute(command)

def getDatabase():
    load_dotenv()
    host = os.getenv("DATABASE_HOST")
    database = os.getenv("DATABASE_NAME")
    user = os.getenv("DATABASE_USERNAME")
    password = os.getenv("DATABASE_PASSWORD")

    database = Database(host, database, user, password)
    return database

#database = getDatabase()

#for i in range(Tables.NUM_OF_TABLES):
#    database.print_table(Tables.Names[i])

#test = """INSERT INTO Users (UserID, Username)
#VALUES (0, 'Test')
#"""
#database.create_table(test)
