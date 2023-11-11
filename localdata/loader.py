from . import localDB, decrypt, TABLE_NAME

def loadLocalData() -> dict:
    dictionary = {}
    try:
        from manager.methods import connect
        sql = connect(localDB())
        data = sql.getRows(TABLE_NAME)[0]
        dictionary["host"] = decrypt(data[1])
        dictionary["dbname"] = decrypt(data[2])
        dictionary["port"] = decrypt(data[3])
        dictionary["user"] = decrypt(data[4])
        dictionary["password"] = decrypt(data[5])
        dictionary["sqlType"] = decrypt(data[6])
        sql.close()
    except: pass
    return dictionary