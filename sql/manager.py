from abc import ABC, abstractmethod
from . import inputIfNull, inputList, isParamStartsWith

class SQLManager(ABC):
    def __init__(self): self.conection = None

    def isConnected(self) -> bool: return self.conection != None
    
    @abstractmethod
    def queryGetTables(self): pass
    def getTables(self, index:int|None=None): return self.fetch(self.queryGetTables(), index)

    @abstractmethod # columns in format "id SERIAL PRIMARY KEY"
    def queryCreateTable(self, table:str|None=None, columns:list = []): pass
    def createTable(self, table:str|None=None, columns:list = []): return self.commit(self.queryCreateTable(table, columns))
    
    def queryDeleteTable(self, table:str|None = None): return f"DROP TABLE {inputIfNull(table, "Write the table name\n -> ")}"
    def deleteTable(self, table:str|None = None): return self.commit(self.queryDeleteTable(table))
    
    @abstractmethod
    def queryGetColumns(self, table:str|None=None): pass
    def getColumns(self, table:str|None=None): return self.fetch(self.queryGetColumns(table))
    
    def queryGetRows(self, table:str|None=None): return f"SELECT * FROM {inputIfNull(table, "Write the table name\n -> ")}"
    def getRows(self, table:str|None=None): return self.fetch(self.queryGetRows(table))
    
    def addRow(self, table:str|None = None, columns:dict = {}): return self.commit(self.queryAddRow(table, columns))

    def removeRow(self, table:str|None = None, where:dict = {}): return self.commit(self.queryRemoveRow(table, where))

    def editRow(self, table:str|None = None, columns:dict = {}, where:dict = {}): return self.commit(self.queryEditRow(table, columns, where))
    
    @abstractmethod
    def queryGetUsers(self): pass
    def getUsers(self, index:int|None=None): return self.fetch(self.queryGetUsers(), index)
    
    @abstractmethod
    def queryCreateUser(self, userName:str|None=None, password:str|None=None): pass
    def createUser(self, userName:str|None=None, password:str|None=None): return self.commit(self.queryCreateUser(userName, password))
    
    @abstractmethod
    def queryDeleteUser(self, userName:str|None=None): pass
    def deleteUser(self, userName:str|None=None): return self.commit(self.queryDeleteUser(userName))
    
    @abstractmethod
    def queryGrantPrivilegesToUser(self, username:str|None = None, permissions:list = [], table:str|None = None): pass
    def grantPrivilegesToUser(self, username:str|None = None, privileges:list = [], table:str|None = None): return self.commit(self.queryGrantPrivilegesToUser(username, privileges, table))
    
    @abstractmethod
    def queryGetPrivilegesInTable(self, table:str|None = None): pass
    def getPrivilegesInTable(self, table:str|None = None): return self.fetch(self.queryGetPrivilegesInTable(table))

    def close(self):
        try: self.conection.close()
        except: pass
        self.conection = None

    # Private methods

    def fetch(self, query:str, index:int|None=None) -> list:
        dataList = []
        try:
            cursor = self.conection.cursor()
            cursor.execute(query)
            data = cursor.fetchall()
            for content in data: 
                if index == None: dataList.append(content)
                else: dataList.append(content[index])
            cursor.close()
        except: pass
        return dataList

    def commit(self, query:str) -> bool|str:
        try:
            cursor = self.conection.cursor()
            cursor.execute(query)
            self.conection.commit()
            cursor.close()
            return True
        except Exception as err: return err

    # Console commands

    def printRows(self, rows):
        for row in rows: 
            result = "| "
            for col in row:
                if col == None: col = " "
                result = str(result) + str(col) + " | "
            print(result)
        
    def printColumns(self, columns):
        result = "| "
        for column in columns: 
            result = str(result) + str(column[0]) + " | "
        print(result)

    def queryAddRow(self, table:str|None = None, columns:dict = {}) -> str:
        if isParamStartsWith(table, "INSERT INTO "): return table
        table = inputIfNull(table, "Write the table name\n -> ")

        if len(columns) == 0:
            rowColumns = self.getColumns(table)
            if len(rowColumns) == 0: raise Exception("No data loaded (connection lost?)")
            print("Note: leaving blank is equivalent to autocomplete (id, datetime, ...)")
            print("Note: 'NULL' (whitout quotation marks)  is equivalent to NULL notation")
            (print("Columns: ", end=""), self.printColumns(self.getColumns(table)))
            columns = inputList(list(map(lambda columns: columns[0], rowColumns)))
            
        if len(columns) == 0: raise Exception("Invalid input")

        rowColumns = ", ".join(list(columns.keys()))
        values = ", ".join(list(columns.values()))
        query = f"INSERT INTO {table} ({rowColumns}) VALUES ({values})"
        return query

    def queryRemoveRow(self, table:str|None = None, where:dict = {}) -> str:
        if isParamStartsWith(table, "DELETE FROM "): return table
        table = inputIfNull(table, "Write the table name\n -> ")

        if len(where) == 0:
            rowColumns = self.getColumns(table)
            if len(rowColumns) == 0: raise Exception("No data loaded (connection lost?)")
            print("Write the WHERE clause")
            (print("Columns: ", end=""), self.printColumns(rowColumns))
            print("Note: leaving blank or 'NULL' is equivalent to omit")
            where = inputList(list(map(lambda columns: columns[0], rowColumns)), nullIsEqualsTo=None)

        if len(where) == 0: raise Exception("Invalid input")
        whereClause = []
        for key in list(where.keys()): whereClause.append(f"{key} = {where[key]}")
        whereClause = ", ".join(whereClause)
        return f"DELETE FROM {table} WHERE ({whereClause})"

    def queryEditRow(self, table:str|None = None, columns:dict = {}, where:dict = {}) -> str:
        if isParamStartsWith(table, "UPDATE "): return table
        table = inputIfNull(table, "Write the table name\n -> ")
        printColumns = lambda: (print("Columns: ", end=""), self.printColumns(self.getColumns(table)))
        
        if len(columns) == 0:
            print("\nWrite the new columns values")
            print("Note: leaving blank is equivalent to not modify the column")
            print("Note: 'NULL' (whitout quotation marks)  is equivalent to NULL notation")
            printColumns()
            columns = inputList(list(map(lambda columns: columns[0], self.getColumns(table))))

        if len(where) == 0:
            print("\n\nWrite the WHERE clause")
            printColumns()
            print("Note: leaving blank or 'NULL' is equivalent to omit")
            where = inputList(list(map(lambda columns: columns[0], self.getColumns(table))), nullIsEqualsTo=None)

        def parseData(dictionary:dict) -> str:
            if len(dictionary) == 0: raise Exception("Invalid input")
            data = []
            for key in list(dictionary.keys()): data.append(f"{key} = {dictionary[key]}")
            data = ", ".join(data)
            return data

        setters = parseData(columns)
        whereClause = parseData(where)
        return f"UPDATE {table} SET {setters} WHERE ({whereClause})"