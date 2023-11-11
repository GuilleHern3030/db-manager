from . import inputIfNull, inputPrivileges, isParamStartsWith
from sql.manager import SQLManager
import psycopg2 as sql

class POSTGRE(SQLManager):
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
        return "SELECT tablename FROM pg_catalog.pg_tables WHERE schemaname='public'"
    
    def queryGetColumns(self, table:str|None=None):
        if isParamStartsWith(table, "SELECT "): return table
        table = inputIfNull(table, "Write the table name\n -> ")
        return f"SELECT column_name FROM information_schema.columns WHERE table_name = '{table}'"

    def queryCreateTable(self, table:str|None=None, columns:list = []):
        if isParamStartsWith(table, "CREATE TABLE "): return table
        table = inputIfNull(table, "Write the table name\n -> ")
        if len(columns) == 0:
            print("To create a table, it will be necessary to write each column specifying its attributes")
            print(" - example: id SERIAL PRIMARY KEY, name TEXT, age INTEGER")
            column = input(" -> ")
            while (len(column) > 0):
                columns.append(column)
                column = input(" -> ")
        if len(columns) == 0: raise Exception("Invalid input")
        columns = ", ".join(columns)
        return f"CREATE TABLE {table} ({columns})"
    
    def queryCreateUser(self, username:str|None = None, password:str|None = None):
        if isParamStartsWith(username, "CREATE USER "): return username
        username = inputIfNull(username, "Write the user name\n -> ")
        password = inputIfNull(username, "Write the password for the user\n -> ")
        return f"CREATE USER {username} WITH PASSWORD '{password}'"
    
    def queryDeleteUser(self, username:str|None = None):
        if isParamStartsWith(username, "DROP USER "): return username
        username = inputIfNull(username, "Write the user name\n -> ")
        return f"DROP USER IF EXISTS {username};"
    
    def queryGetUsers(self):
        return "SELECT usename FROM pg_user"
    
    def queryGetPrivilegesInTable(self, table:str|None = None):
        if isParamStartsWith(table, "SELECT "): return table
        table = inputIfNull(table, "Write the table name\n -> ")
        return f"SELECT grantee, privilege_type FROM information_schema.table_privileges WHERE table_name = '{table}'"
    
    def queryGrantPrivilegesToUser(self, username:str|None = None, privileges:list = [], table:str|None = None):
        if isParamStartsWith(username, "GRANT "): return username
        username = inputIfNull(username, "Write the user name\n -> ")
        if username in self.getUsers(0):
            if len(privileges) == 0: privileges = inputPrivileges(table)
            if len(privileges) == 0: raise Exception("Invalid input")
            privileges = ", ".join(privileges)
            if table == None or len(table) == 0: return f"GRANT {privileges} ON ALL TABLES IN SCHEMA public TO {username}"
            else: return f"GRANT {privileges} ON TABLE {table} TO {username}"
        else: raise Exception("Invalid user")
