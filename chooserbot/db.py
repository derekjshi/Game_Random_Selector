# db.py
from dotenv import load_dotenv
import mysql.connector
import os

class Database():
    def __init__(self, host, database, user, password):
        self.db = mysql.connector.connect(host=host, database=database, user=user, password=password)

    def create_tables(self):
        command = "CREATE TABLE Users (UserId INT AUTO_INCREMENT PRIMARY KEY, Username varchar(20))"
        cursor = self.db.cursor()
        cursor.execute(command)

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

    def drop_tables(self, table_name):
        command = "DROP TABLE " + table_name
        cursor = self.db.cursor()
        cursor.execute(command)

load_dotenv()
host = os.getenv("DATABASE_HOST")
database = os.getenv("DATABASE_NAME")
user = os.getenv("DATABASE_USERNAME")
password = os.getenv("DATABASE_PASSWORD")

database = Database(host, database, user, password)
#print(database.db)

