import psycopg2 as sql
from sql.manager import SQLManager

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
    
    def getTables(self) -> list:
        return self.__query_fetchAll__(self.queryShowTables(), 0)

    def getColumns(self, table:str = "tablename") -> list:
        return self.__query_fetchAll__(self.queryDescribeColumns(table))
    
    def queryShowTables(self):
        return "SELECT tablename FROM pg_catalog.pg_tables WHERE schemaname='public'"
    
    def queryDescribeColumns(self, table:str = "tablename"):
        return f"SELECT column_name FROM information_schema.columns WHERE table_name = '{table}'"

    def queryCreateTable(self, table:str = "tablename"):
        print("To create a table, it will be necessary to write each column")
        print("separated with commas, and specifying its attributes")
        print(" - example: id SERIAL PRIMARY KEY, name TEXT, age INTEGER")
        params = input(" -> ")
        return f"CREATE TABLE {table} ({params})"
    
    def queryViewUsers(self):
        return "SELECT usename FROM pg_user"
    
    def queryViewPrivilegesInTable(self, table:str = "tablename"):
        return f"SELECT grantee, privilege_type FROM information_schema.table_privileges WHERE table_name = '{table}'"
    
    def queryCreateUser(self, username:str|None = None, password:str|None = None):
        if username == None or len(username) == 0:
            print("Write the user name")
            username = input(" -> ")
        if password == None or len(password) == 0:
            print("Write the password for the user")
            password = input(" -> ")
        return f"CREATE USER {username} WITH PASSWORD '{password}'"
    
    def queryGrantPrivilegesToUser(self, table:str|None = None, username:str|None = None, permissions:list = []):
        if username == None or len(username) == 0: username = input("Write the user name\n -> ")
        def ask(permission, ask): 
            if len(permissions) == 0:
                permissions.append(permission) if input(ask) == 'yes' else None
        ask("SELECT", f"Can the user READ ROWS in the table '{table}'? (yes/no)\n -> ")
        ask("INSERT", f"Can the user INSERT ROWS in the table '{table}'? (yes/no)\n -> ")
        ask("UPDATE", f"Can the user EDIT ROWS in the table '{table}'? (yes/no)\n -> ")
        ask("DELETE", f"Can the user DELETE ROWS in the table '{table}'? (yes/no)\n -> ")
        permissions = ", ".join(permissions)
        if table == None or len(table) == 0: return f"GRANT {permissions} ON ALL TABLES IN SCHEMA public TO {username}"
        else: return f"GRANT {permissions} ON TABLE {table} TO {username}"
