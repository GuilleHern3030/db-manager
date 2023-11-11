from sql.manager import SQLManager
from sys import version

class InvalidDB(SQLManager):
    def __init__(self, *err): 
        print("\033[91m")
        print(err)
        print("\033[95m", version, "\033[0m")

    def isConnected(self) -> bool: return False
    def close(self): pass

    # Abstract methods
    def queryGetTables(self): return None
    def queryCreateTable(self, table:str|None=None): return None
    def queryGetColumns(self, table:str|None=None): return None
    def queryGetUsers(self): return None
    def queryCreateUser(self, userName:str|None=None, password:str|None=None): return None
    def queryDeleteUser(self, userName:str|None=None): return None
    def queryGrantPrivilegesToUser(self, username:str|None = None, permissions:list = [], table:str|None = None): return None
    def queryGetPrivilegesInTable(self, table:str|None = None): return None