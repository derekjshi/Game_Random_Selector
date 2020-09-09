# tables.py
from typing import NamedTuple
from dotenv import load_dotenv
from abc import ABC, abstractmethod
import mysql.connector

class TableInterface(ABC):
    '''
        An abstract class which defines the required methods in our Table interface
        CRUD operations
    '''
    def __init__(self, name: str):
        self.name = name

    @abstractmethod
    def create_table(self):
        pass

    @abstractmethod
    def create_entity(self):
        pass    

    def retrieve_entity(self, db: mysql.connector.MySQLConnection, entity_id = None, entity_name = None):
        cmd = ""
        data_entity = ()

        if entity_id is not None:
            cmd = "SELECT * FROM " + self.name + " WHERE ID=%s"
            data_entity = (entity_id, )
        else:
            cmd = "SELECT * FROM " + self.name + " WHERE Name=%s"
            data_entity = (entity_name, )

        cursor = db.cursor()
        cursor.execute(cmd, data_entity)
        return cursor.fetchall()
        
    def retrieve_all(self, db: mysql.connector.MySQLConnection):
        cmd = "SELECT * FROM " + self.name
        cursor = db.cursor()
        cursor.execute(cmd)
        return cursor.fetchall()

    @abstractmethod
    def update_entity(self):
        pass

    def delete_entity(self, db: mysql.connector.MySQLConnection, entity_id = None, entity_name = None):
        cmd = ""
        data_entity = ()
        if entity_id is not None:
            cmd = "DELETE FROM " + self.name + "WHERE ID=%s"
            data_entity = (entity_id, )
        else:
            cmd = "DELETE FROM " + self.name + " WHERE Name=%s"
            data_entity = (entity_name, )

        cursor = db.cursor()
        cursor.execute(cmd, data_entity)
        db.commit()

class UsersTable(TableInterface):
    def create_table(self, db: mysql.connector.MySQLConnection):
        cursor = db.cursor()
        cmd = """CREATE TABLE Users (
            ID INT AUTO_INCREMENT,
            Name varchar(32) NOT NULL,
            PRIMARY KEY (ID)
        )
        """        
        cursor.execute(cmd)

    def create_entity(self, db: mysql.connector.MySQLConnection, username):
        cursor = db.cursor()
        cmd = """INSERT INTO Users 
            (ID, Name) 
            VALUES (%s, %s)
            """

        data_user = (0, username)
        cursor.execute(cmd, data_user)
        db.commit()

    def update_entity(self):
        # shouldn't allow updates on the user table...
        return

class ItemsTable(TableInterface):
    def create_table(self, db: mysql.connector.MySQLConnection):
        cursor = db.cursor()
        cmd = """CREATE TABLE Items (
            ID INT AUTO_INCREMENT,
            Name varchar(32) NOT NULL,
            UserID INT NOT NULL,
            PRIMARY KEY (ID),
            FOREIGN KEY (UserID) REFERENCES Users(ID)
        )
        """    
        cursor.execute(cmd)

    def create_entity(self, db: mysql.connector.MySQLConnection, item_name, user_id):
        cursor = db.cursor()
        cmd = """INSERT INTO Items 
            (ID, Name, UserID) 
            VALUES (%s, %s, %s)
        """

        data_item = (0, item_name, user_id)

        cursor.execute(cmd, data_item)
        db.commit()

    def update_entity(self):
        # shouldn't allow updates on the items table...
        return

class ResultsTable(TableInterface):
    def create_table(self, db: mysql.connector.MySQLConnection):
        cursor = db.cursor()
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

    def create_entity(self, db: mysql.connector.MySQLConnection, time_of_result, user_id, item_id):
        cursor = db.cursor()
        cmd = """INSERT INTO  
            (ID, TimeOfResult, UserID, ItemID), 
            VALUES (%s, %s, %s, %s)
        """
        data_results = (0, time_of_result, user_id, item_id)
        cursor.excute(cmd, data_results)
        db.commit()

    def update_entity(self):
        # shouldn't allow updates on the results table...
        return
