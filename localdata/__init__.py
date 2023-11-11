def localDB():
    class LocalData:
        def __init__(self):
            self.host = ""
            self.dbname = "local"
            self.port = ""
            self.user = "root"
            self.password = ""
            self.sqlType = "sqlite"
    localdb = LocalData()
    return localdb

TABLE_NAME = "lastconnection"

TABLE_COLUMNS = [
    "id INTEGER PRIMARY KEY AUTOINCREMENT",
    "host TEXT",
    "dbname TEXT",
    "port TEXT",
    "user TEXT",
    "password TEXT",
    "sqlType TEXT"
]

def decrypt(data):
    from .Cryptography import Cryptography
    cpt = Cryptography()
    return cpt.decrypt(data)

class FileData:
    def __init__(self, data):
        self.host = data.host
        self.dbname = data.dbname
        self.port = data.port
        self.user = data.user
        self.password = data.password
        self.sqlType = data.sqlType
    
    def encrypt(self):
        from .Cryptography import Cryptography
        cpt = Cryptography(frequencyMin=1, frequencyMax=3)
        self.host = cpt.encrypt(self.host)
        self.dbname = cpt.encrypt(self.dbname)
        self.port = cpt.encrypt(self.port)
        self.user = cpt.encrypt(self.user)
        self.password = cpt.encrypt(self.password)
        self.sqlType = cpt.encrypt(self.sqlType)
    
    def dictionary(self):
        dictionary = {
            "host": f"'{self.host}'",
            "dbname": f"'{self.dbname}'",
            "port": f"'{self.port}'",
            "user": f"'{self.user}'",
            "password": f"'{self.password}'",
            "sqlType": f"'{self.sqlType}'",
            "sqlType": f"'{self.sqlType}'"
        }
        return dictionary