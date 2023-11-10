from abc import ABC, abstractmethod

def SQL(dbHost, dbName, dbPort, dbUser, dbPassword, dbType):
    try:

        if dbType == 'mysql':
            from .mysql import MYSQL
            return MYSQL(dbHost, dbName, dbPort, dbUser, dbPassword)
        
        elif dbType == 'postgre':
            from .postgre import POSTGRE
            return POSTGRE(dbHost, dbName, dbPort, dbUser, dbPassword)
        
        else: raise Exception(f"{dbType} databases is not supported.")
    except Exception as err:
        from .invalid import InvalidDB
        return InvalidDB(err)

class SQLManager(ABC):
    def __init__(self):
        self.conection = None

    def isConnected(self) -> bool:
        return self.conection != None
    
    @abstractmethod
    def queryShowTables(self):
        pass
    
    @abstractmethod
    def queryDescribeColumns(self, table:str):
        pass
    
    @abstractmethod
    def queryCreateTable(self, table:str):
        pass
    
    def querySelectRows(self, table:str = "tablename"):
        return f"SELECT * FROM {table}"

    @abstractmethod
    def getTables(self):
        pass

    @abstractmethod
    def getColumns(self, table:str):
        pass
    
    @abstractmethod
    def queryViewUsers(self):
        pass
    
    @abstractmethod
    def queryCreateUser(self):
        pass
    
    @abstractmethod
    def queryGrantPrivilegesToUser(self, table:str|None = None, username:str|None = None, permissions:list = []):
        pass

    @abstractmethod
    def queryViewPrivilegesInTable(self, table:str|None):
        pass

    def getRows(self, table:str):
        return self.__query_fetchAll__(self.querySelectRows(table))

    def addRow(self, table:str, params:str = None):
        if table.find("INSERT INTO") != -1: return self.__query_commit__(table)
        elif params != None: return self.__query_commit__(f"INSERT INTO {table} {params}")
        else: return self.__query_commit__(self.queryAddRow(table))

    def removeRow(self, table:str, where:str = None):
        if table.find("DELETE FROM") != -1: return self.__query_commit__(table)
        elif where != None: return self.__query_commit__(f"DELETE FROM {table} WHERE {where}")
        else: return self.__query_commit__(self.queryRemoveRow(table))

    def editRow(self, table:str, params:str = None):
        if table.find("UPDATE ") != -1: return self.__query_commit__(table)
        elif params != None: return self.__query_commit__(f"UPDATE {table} {params}")
        else: return self.__query_commit__(self.queryEditRow(table))

    def createTable(self, table:str = "", params:str = None):
        if table.find("CREATE TABLE") != -1: return self.__query_commit__(table)
        elif params != None: return self.__query_commit__(f"CREATE TABLE {table} {params}")
        else: return self.__query_commit__(self.queryCreateTable(table))

    def deleteTable(self, table:str):
        return self.__query_commit__(f"DROP TABLE {table}")
    
    def getUsers(self):
        return self.__query_fetchAll__(self.queryViewUsers())
    
    def createUser(self, userName = None, password = None):
        return self.__query_commit__(self.queryCreateUser(userName, password))
    
    def grantPrivilegesToUser(self, table:str = "", userName:str = "", privileges:list = []):
        return self.__query_commit__(self.queryGrantPrivilegesToUser(table, userName, privileges))
    
    def getPrivilegesInTable(self, table:str = ""):
        return self.__query_fetchAll__(self.queryViewPrivilegesInTable(table))

    def close(self):
        try: self.conection.close()
        except: pass
        self.conection = None

    # Private methods

    def __query_fetchAll__(self, query:str, index:int|None=None) -> list:
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

    def __query_commit__(self, query:str) -> bool|str:
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

    def queryAddRow(self, table:str) -> str:
        columns = self.getColumns(table)
        if len(columns) == 0: raise("No data loaded (connection lost?)")
        print("Note: leaving blank is equivalent to NULL")
        print("Note: '-OMIT-' (whitout quotation marks)  is equivalent to autocomplete (id, datetime, ...)")

        values = []
        print("Columns: ", end="")
        self.printColumns(columns)
        columns = list(map(lambda columns: columns[0], columns))
        for i in range(len(columns)): 
            value = input(f"Write the '{columns[i]}' value: ")
            if len(value) == 0: values.append("NULL")
            elif value.isdigit(): values.append(value)
            elif value == '-OMIT-': 
                values.append(None)
                columns[i] = None
            else: values.append(f"'{value}'")

        for i in range(values.count(None)):
            values.remove(None)
            columns.remove(None)

        columnsString = ",".join(columns)
        valuesString = ",".join(values)
        return f"INSERT INTO {table} ({columnsString}) VALUES ({valuesString})"

    def queryRemoveRow(self, table:str) -> str:
        columns = self.getColumns(table)
        if len(columns) == 0: raise("No data loaded (connection lost?)")
        print("Columns: ", end="")
        self.printColumns(columns)
        print("Write the WHERE clause")
        print(" - format: COLUMN_NAME = VALUE_TO_FIND")
        print(" - note: different columns are separated with commas")
        print(" - example: id = 3, name = 'Guille'")
        whereClause = input(" -> ")
        return f"DELETE FROM {table} WHERE ({whereClause})"

    def queryEditRow(self, table:str) -> str:

        setters = []
        columns = self.getColumns(table)
        if len(columns) == 0: raise("No data loaded (connection lost?)")
        print("Note: leaving blank is equivalent to not modifying the value")
        for column in columns:
            value = input(f"Write the new value of '{column[0]}': ")
            if len(value) == 0: continue
            elif value.isdigit(): setters.append(f"{column[0]} = {value}")
            else: setters.append(f"{column[0]} = '{value}'")
        setters = ", ".join(setters)

        print("Columns: ", end="")
        self.printColumns(columns)
        print("Write the WHERE clause")
        print(" - format: COLUMN_NAME = VALUE_TO_FIND")
        print(" - note: different columns are separated with commas")
        print(" - example: id = 3, name = 'Guille'")
        whereClause = input(" -> ")
        return f"UPDATE {table} SET {setters} WHERE ({whereClause})"