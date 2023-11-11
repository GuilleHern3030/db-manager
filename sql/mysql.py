from . import inputIfNull, isParamStartsWith
from sql.manager import SQLManager
import MySQLdb as sql

class MYSQL(SQLManager):
    def __init__(self, dbHost, dbName, dbPort, dbUser, dbPassword):
        try:
            self.conection = sql.connect(
                host = dbHost,
                database = dbName,
                user = dbUser,
                password = dbPassword,
                port = int(dbPort)
            )
            print("\n\nCONNECTED\n\n")
        except Exception as err:
            print("Error:", err)
            self.conection = None
    
    def queryGetTables(self):
        return "SHOW TABLES"
    
    def queryGetColumns(self, table:str|None=None):
        if isParamStartsWith(table, "DESCRIBE "): return table
        table = inputIfNull(table, "Write the table name\n -> ")
        return f"DESCRIBE {table}"

    def queryCreateTable(self, table:str|None=None, columns:list = []):
        if isParamStartsWith(table, "CREATE TABLE "): return table
        if len(columns) == 0:
            print("To create a table, it will be necessary to write each column and specifying its attributes")
            print(" - example: id INT AUTO_INCREMENT, name VARCHAR(90) NOT NULL, age INT,  PRIMARY KEY(id)")
            print(" - timestamp format: date DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP")
            column = input(" -> ")
            while (len(column) > 0):
                columns.append(column)
                column = input(" -> ")
        if len(columns) == 0: raise Exception("Invalid input")
        columns = ", ".join(columns)
        return f"CREATE TABLE {table} ({columns})"
    
    def queryCreateUser(self, username:str|None = None, password:str|None = None):
        raise Exception("Not implemented")
    
    def queryDeleteUser(self, username:str|None = None):
        raise Exception("Not implemented")
    
    def queryGetUsers(self):
        raise Exception("Not implemented")
    
    def queryGrantPrivilegesToUser(self, username:str|None = None, privileges:list = [], table:str|None = None):
        raise Exception("Not implemented")
    
    def queryGetPrivilegesInTable(self, table:str|None = None):
        raise Exception("Not implemented")
    