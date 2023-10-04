import psycopg2 as sql
from src.sql.manager import SQLManager

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
        print("Para crear una tabla, será necesario escribir cada columna,")
        print("separada con comas y especificando algunos de sus atributos")
        print(" - ejemplo: id SERIAL PRIMARY KEY, name TEXT, age INTEGER")
        params = input(" -> ")
        return f"CREATE TABLE {table} ({params})"