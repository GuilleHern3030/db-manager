from sql.manager import SQLManager
from sys import version

class InvalidDB(SQLManager):
    def __init__(self, err): 
        print(err)
        print(version)

    def isConnected(self) -> bool: return False
    def close(self): pass

    # Abstract methods
    def queryShowTables(self): return None
    def queryDescribeColumns(self, table:str): return None
    def queryCreateTable(self, table:str): return None
    def getTables(self): return None
    def getColumns(self, table:str): return None