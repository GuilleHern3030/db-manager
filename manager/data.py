from sys import argv as consoleParam
from localdata.loader import loadLocalData
from routes.colors import COLOR_YELLOW, COLOR_DEFAULT

class Data():
    def __init__(self):
        self.sqlType = consoleParam[1] if len(consoleParam) > 1 else "mysql"
        self.host = consoleParam[2] if len(consoleParam) > 2 else "localhost"
        self.dbname = consoleParam[3] if len(consoleParam) > 3 else "test"
        self.port = consoleParam[4] if len(consoleParam) > 4 else "3306"
        self.user = consoleParam[5] if len(consoleParam) > 5 else "root"
        self.password = consoleParam[6] if len(consoleParam) > 6 else ""
        self.table = consoleParam[7] if len(consoleParam) > 7 else None

        self.autoConnect = len(consoleParam) > 6

        if len(consoleParam) <= 1:
            data = loadLocalData()
            if data != None and len(data) > 0:
                self.sqlType = data["sqlType"]
                self.host = data["host"]
                self.dbname = data["dbname"]
                self.port = data["port"]
                self.user = data["user"]
                self.password = data["password"]
        
    def printDataBase(self):
        print(f" Host:{COLOR_YELLOW}", self.host, COLOR_DEFAULT)
        print(f" DataBase:{COLOR_YELLOW}", self.dbname, COLOR_DEFAULT)
        print(f" Port:{COLOR_YELLOW}", self.port, COLOR_DEFAULT)
        print(f" User:{COLOR_YELLOW}", self.user, COLOR_DEFAULT)
        print(f" Password:{COLOR_YELLOW}", self.password, COLOR_DEFAULT)
        print(f" DBType:{COLOR_YELLOW}", self.sqlType, COLOR_DEFAULT)
        if self.table != None: print(f" Table:{COLOR_YELLOW}", self.table, COLOR_DEFAULT)