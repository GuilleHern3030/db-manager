from . import inputIfNull, isParamStartsWith
from sql.manager import SQLManager
import sqlite3 as sql

def dbPath(host:str="", dbName:str="", dbPort:str|int=""):
    if len(host) > 0: host = f"{host}-"
    if len(dbName) == 0: dbName = "local"
    if isinstance(dbPort, int) and dbPort == 0: dbPort = ""
    return f"{host}{dbName}{dbPort}.db"

class SQLITE(SQLManager):
    def __init__(self, dbHost, dbName, dbPort, dbUser, dbPassword):
        sqlite3 = dbPath(dbHost, dbName, dbPort)
        print(sqlite3)
        try:
            self.conection = sql.connect(sqlite3)
            print("\n\nCONNECTED\n\n")
        except Exception as err:
            print("Error:", err)
            self.conection = None
    
    def queryGetTables(self):
        return "SELECT name FROM sqlite_master WHERE type='table'"
    
    def queryGetColumns(self, table:str|None=None):
        if isParamStartsWith(table, "PRAGMA "): return table
        table = inputIfNull(table, "Write the table name\n -> ")
        return f"PRAGMA table_info({table})"

    def queryCreateTable(self, table:str|None=None, columns:list = []):
        if isParamStartsWith(table, "CREATE TABLE "): return table
        table = inputIfNull(table, "Write the table name\n -> ")
        if len(columns) == 0:
            print("To create a table, it will be necessary to write each column specifying its attributes")
            print(" - example: id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT, age INTEGER")
            column = input(" -> ")
            while (len(column) > 0):
                columns.append(column)
                column = input(" -> ")
        if len(columns) == 0: raise Exception("Invalid input")
        columns = ", ".join(columns)
        return f"CREATE TABLE {table} ({columns})"
    
    def queryCreateUser(self, username:str|None = None, password:str|None = None): raise Exception("No users in SQLITE")
    def queryDeleteUser(self, username:str|None = None): raise Exception("No users in SQLITE")
    def queryGetUsers(self): raise Exception("No users in SQLITE")
    def queryGetPrivilegesInTable(self, table:str|None = None): raise Exception("No users in SQLITE")
    def queryGrantPrivilegesToUser(self, username:str|None = None, privileges:list = [], table:str|None = None): raise Exception("No users in SQLITE")