# db.py
from dotenv import load_dotenv
from abc import ABC, abstractmethod
import mysql.connector
import os

from chooserbot.tables import UsersTable, ItemsTable, ResultsTable

class Database():
    def __init__(self, host, database, user, password):
        self.db = mysql.connector.connect(host=host, database=database, user=user, password=password)
        self.users_table = UsersTable("Users")
        self.items_table = ItemsTable("Items")
        self.results_table = ResultsTable("Results")

    def create_tables(self):
        table_list = ["Users", "Items", "Results"]
        cursor = self.db.cursor()
        cmd = "SHOW TABLES"
        cursor.execute(cmd)

        for table in cursor:
            if table[0] in table_list:
                table_list.remove(table[0])

        if "Users" in table_list:
            self.users_table.create_table(self.db)
            print("Users table created")
        else:
            print("Users table already exists. Not creating table")

        if "Items" in table_list:
            self.items_table.create_table(self.db)
            print("Items table created")
        else:
            print("Items table already exists. Not creating table")

        if "Results" in table_list:
            self.results_table.create_table(self.db)
            print("Results table created")
        else:
            print("Results table already exists. Not creating table")

def getDatabase():
    load_dotenv()
    host = os.getenv("DATABASE_HOST")
    database = os.getenv("DATABASE_NAME")
    user = os.getenv("DATABASE_USERNAME")
    password = os.getenv("DATABASE_PASSWORD")
    
    #database = mysql.connector.connect(host=host, database=database, user=user, password=password)
    database = Database(host, database, user, password)
    database.create_tables()

    return database
