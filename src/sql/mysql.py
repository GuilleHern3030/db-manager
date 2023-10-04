from src.sql.manager import SQLManager
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
    
    def getTables(self) -> list:
        return self.__query_fetchAll__(self.queryShowTables(), 0)

    def getColumns(self, table:str = "tablename") -> list:
        return self.__query_fetchAll__(self.queryDescribeColumns(table))
    
    def queryShowTables(self):
        return "SHOW TABLES"
    
    def queryDescribeColumns(self, table:str = "tablename"):
        return f"DESCRIBE {table}"

    def queryCreateTable(self, table:str = "tablename"):
        print("Para crear una tabla, será necesario escribir cada columna,")
        print("separada con comas y especificando algunos de sus atributos")
        print(" - ejemplo: id INT AUTO_INCREMENT, name VARCHAR(90) NOT NULL, age INT,  PRIMARY KEY(id)")
        print(" - registro de fecha: date DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP")
        params = input(" -> ")
        return f"CREATE TABLE {table} ({params})"