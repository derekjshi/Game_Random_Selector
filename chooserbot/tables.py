# tables.py
from typing import NamedTuple
from dotenv import load_dotenv
from abc import ABC, abstractmethod
import mysql.connector
from db import Database

class TableInterface(ABC):
    '''
        An abstract class which defines the required methods in our Table interface
        CRUD operations
    '''
    def __init__(self, name, database : Database):
        self.name = name
        self.db = database

    @abstractmethod
    def create_table(self):
        pass

    @abstractmethod
    def create_entity(self):
        pass    

    def retrieve_entity(self, entity_id):
        cmd = "SELECT * FROM " + self.name + " WHERE ID=" + entity_id
        cursor = self.db.cursor()
        cursor.execute(cmd)
        return cursor
        
    def retrieve_all(self):
        cmd = "SELECT * FROM " + self.name
        cursor = self.db.cursor()
        cursor.execute(cmd)
        return cursor

    @abstractmethod
    def update_entity(self):
        pass

    def delete_entity(self, entity_id):
        cmd = "DELETE FROM " + self.name + " WHERE ID=" + entity_id
        cursor = self.db.cursor()
        cursor.execute(cmd)
        self.db.commit()

class UsersTable(TableInterface):
    def create_table(self):
        cursor = self.db.cursor()
        cmd = """CREATE TABLE Users (
            ID INT AUTO_INCREMENT,
            Name varchar(32) NOT NULL,
            PRIMARY KEY (UserID)
        )
        """        
        
        cursor.execute(cmd)

    def create_entity(self, username):
        cursor = self.db.cursor()
        cmd = """INSERT INTO %s 
            (ID, Name) 
            VALUES (0, %s)
        """
        data_user = (self.name, username)
        cursor.execute(cmd, data_user)
        self.db.commit()

    def update_entity(self):
        # shouldn't allow updates on the user table...
        return

class ItemsTable(TableInterface):
    def create_table(self):
        cursor = self.db.cursor()
        cmd = """CREATE TABLE Items (
            ID INT AUTO_INCREMENT,
            Name varchar(32) NOT NULL,
            UserID INT NOT NULL,
            PRIMARY KEY (ID),
            FOREIGN KEY (UserID) REFERENCES Users(ID)
        )
        """    
        cursor.execute(cmd)

    def create_entity(self, item_name, user_id):
        cursor = self.db.cursor()
        cmd = """INSERT INTO %s 
            (ID, Name, UserID) 
            VALUES (0, %s, %d)
        """
        data_item = (self.name, item_name, user_id)
        cursor.execute(cmd, data_item)
        self.db.commit()

    def update_entity(self):
        # shouldn't allow updates on the items table...
        return

class ResultsTable(TableInterface):
    def create_table(self):
        cursor = self.db.cursor()
        cmd = """CREATE TABLE Results (
            ID INT AUTO_INCREMENT,
            TimeOfResult DATETIME NOT NULL,
            UserID INT NOT NULL,
            ItemID INT NOT NULL,
            PRIMARY KEY (ID),
            FOREIGN KEY (UserID) REFERENCES Users(ID),
            FOREIGN KEY (ItemID) REFERENCES Items(ID)
        )
        """
        cursor.execute(cmd)

    def create_entity(self, time_of_result, user_id, item_id):
        cursor = self.db.cursor()
        cmd = """INSERT INTO %s 
            (ID, TimeOfResult, UserID, ItemID), 
            VALUES (0, %s, %d, %d)
        """
        data_results = (self.name, time_of_result, user_id, item_id)
        cursor.excute(cmd, data_results)
        self.db.commit()

    def update_entity(self):
        # shouldn't allow updates on the results table...
        return
