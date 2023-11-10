from sys import argv as consoleParam

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
        
    def printDataBase(self):
        print("Host:", self.host)
        print("DataBase:", self.dbname)
        print("Port:", self.port)
        print("User:", self.user)
        print("Password:", self.password)
        print("DBType:", self.sqlType)
        if self.table != None: print("Table:", self.table)